# picoDB library for handling github projects
#
# tl;dr: get a GitHub project, and pull data from it, such as the icon, the download
# link for the CIA/3DSX, older version info, etc etc
#
# early version, NJL 2020-JUN-14

import requests
import json
import io

with open("config.json") as config_file:
    configData = json.load(config_file)
    
githubTokenHeader = 'token {0}'.format(configData["githubAuthorizationToken"])

githubAPILocation = "https://api.github.com"
githubAPIVersionHeader = {'Accept': 'application/vnd.github.v3+json', 'Authorization': githubTokenHeader}

class unknownGithubError(Exception):
    pass
    
class GithubNotFoundError(Exception):
    pass

def getProjectDescription(projectAuthor, projectName):
    githubRequestURL = "{0}/repos/{1}/{2}".format(githubAPILocation, projectAuthor, projectName)
    githubResponse = requests.get(githubRequestURL, headers=githubAPIVersionHeader) # get the data from Github
    
    if githubResponse.status_code == 200: # the request completed successfully
        projectData = json.loads(githubResponse.content) # decode JSON data from Github
        projectDescription = projectData["description"] # get description from GH data
        return projectDescription # return description to caller
    elif githubResponse.status_code == 404: # project not found
        raise GithubNotFoundError("The project for which you have requested the description of could not be found.")
    else: # oopsie woopsie uwu
        raise unknownGithubError("An unknown error occured while trying to obtain the project description.") # something went wrong, let the owner handle it
        
def getLatestProjectCIA(projectAuthor, projectName):
    githubRequestURL = "{0}/repos/{1}/{2}/releases/latest".format(githubAPILocation, projectAuthor, projectName)
    githubResponse = requests.get(githubRequestURL, headers=githubAPIVersionHeader) # get the data from Github
    
    if githubResponse.status_code == 200: # the request completed successfully
        releaseData = json.loads(githubResponse.content) # decode JSON data from Github
        releaseAssets = releaseData["assets"] # get all assets from GH data
        releaseTag = releaseData["tag_name"]
        for releaseFile in releaseAssets:
            releaseDownloadLink = releaseFile['browser_download_url']
            if releaseDownloadLink.endswith(".cia"):
                releaseInfo = {"ciaURL": releaseDownloadLink, "releaseTag": releaseTag}
                return releaseInfo
        raise GithubNotFoundError("A CIA file for the project you requested could not be found.")
    elif githubResponse.status_code == 404: # project not found
        raise GithubNotFoundError("The project for which you have requested the latest CIA could not be found.")
    else: # oopsie woopsie uwu
        raise unknownGithubError("An unknown error occured while trying to obtain the latest CIA.") # something went wrong, let the owner handle it

def getAllProjectCIAs(projectAuthor, projectName):
    githubRequestURL = "{0}/repos/{1}/{2}/releases".format(githubAPILocation, projectAuthor, projectName)
    githubResponse = requests.get(githubRequestURL, headers=githubAPIVersionHeader) # get the data from Github
    
    if githubResponse.status_code == 200: # the request completed successfully
        releases = []
        releaseData = json.loads(githubResponse.content) # decode JSON data from Github
        for release in releaseData: # iterate through all releases
            releaseInfo = {} # initialise an empty dict for release info
            
            releaseInfo["releaseTag"] = release["tag_name"]
            
            releaseAssets = release["assets"] # hey it's obvious but it helps
            releaseInfo["ciaURL"] = "none" # sanity check to ensure a valid CIA has been found
            for releaseFile in releaseAssets:
                possibleDownloadLink = releaseFile['browser_download_url']
                if possibleDownloadLink.endswith(".cia"):
                    releaseInfo["ciaURL"] = possibleDownloadLink # a valid download link was found
            
            if releaseInfo["ciaURL"] != "none":
                releases.append(releaseInfo)
        
        if len(releases) == 0:
            raise GithubNotFoundError("No valid releases were found for the requested project.")
        else:
            return releases
            
    elif githubResponse.status_code == 404: # project not found
        raise GithubNotFoundError("The project for which you have requested the latest CIA could not be found.")
    else: # oopsie woopsie uwu
        raise unknownGithubError("An unknown error occured while trying to obtain the latest CIA.") # something went wrong, let the owner handle it

if __name__ == '__main__':
    print("This is a library file, silly!")