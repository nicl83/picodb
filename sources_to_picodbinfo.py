# PicoDB main file
#
# this will eventually be a CGI script, but for now, let's just work on getting it
# to spit out valid HTML.
#
# early version, NJL 2020-JUN-14

import qrcode 
import requests
import sys
import json
import io
import os

import pDB_github

with open("config.json") as config_file, open("picodbInfo.json") as pdbInfoFile, open("sources.json") as sources_file:
    configData = json.load(config_file)
    picoDBInfo = json.load(pdbInfoFile)
    sources = json.load(sources_file)

qrcodeSaveLocation = configData["qrcodeSaveLocation"]

def genQRForCIA(version, url, name):
    saveto = f"{qrcodeSaveLocation}/{name}"
    fileName = f"{saveto}/{name}-{version}.png"
    
    if not os.path.exists(saveto):
        os.makedirs(saveto)
    
    if os.path.isfile(fileName):
        print(f"QR code for {name}-{version} already exists at {fileName}, skipping")
        return fileName
    else:
        CIAQR = qrcode.make(url)
        CIAQR.save(fileName)
        print(f"QR saved to {fileName}")
        return fileName

print("Generating picoDB information file, this may take some time")
currentSourceID = -1 # bloody zero indexing
for source in sources:

    currentSourceID += 1 # increment it by one
    currentSourceName = list(sources.keys())[currentSourceID] # please don't let me code tired again
    print(f"Generating info for source {currentSourceName}")
    picoDBInfo[currentSourceName] = {}

    if sources[source]["type"] == "github":
        currentSourceInfo = {}
        currentSourceReleases = pDB_github.getAllProjectCIAs(sources[source]["developer"], sources[source]["repository"])
        currentSourceDescription = pDB_github.getProjectDescription(sources[source]["developer"], sources[source]["repository"])
        currentSourceLatestRelease = currentSourceReleases[0]
        picoDBInfo[currentSourceName]["description"] = currentSourceDescription
        picoDBInfo[currentSourceName]["latestVersion"] = currentSourceLatestRelease["releaseTag"]
        picoDBInfo[currentSourceName]["latestURL"] = currentSourceLatestRelease["ciaURL"]
        currentSourceLatestQR = genQRForCIA(currentSourceLatestRelease["releaseTag"], currentSourceLatestRelease["ciaURL"], sources[source]["repository"])
        picoDBInfo[currentSourceName]["latestQR"] = currentSourceLatestQR
        
        oldVersions = {}
        for version in currentSourceReleases:
            currentVersion = version["releaseTag"]
            currentVersionInfo = {}
            currentVersionInfo["version"] = version["releaseTag"]
            currentVersionInfo["URL"] = version["ciaURL"]
            currentVersionQR = genQRForCIA(version["releaseTag"], version["ciaURL"], sources[source]["repository"])
            currentVersionInfo["QR"] = currentVersionQR
            oldVersions[currentVersion] = currentVersionInfo
        
        picoDBInfo[currentSourceName]["oldVersions"] = oldVersions #ugh, 6am code is the *worst*
        
    elif sources[source]["type"] == "other":
        currentVersionQR = genQRForCIA(sources[source]["version"], sources[source]["location"], sources[source]["name"])
        currentSourceInfo = {
            "latestVersion": sources[source]["version"],
            "description": sources[source]["description"],
            "latestURL": sources[source]["location"],
            "latestQR": currentVersionQR
            }
        picoDBInfo[currentSourceName] = currentSourceInfo
    
with open("picodbInfo.json", 'w', encoding="utf8") as pdbInfoFileOut:
    json.dump(picoDBInfo, pdbInfoFileOut, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)