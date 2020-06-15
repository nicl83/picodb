import json, io

with open("sources.json") as sources_file:
    sources = json.load(sources_file)

command = "null"

print("""Welcome to picoDB's sources manager,
             for people who are scared of touching
             JSON files by hand, which is totally
             cool by me
             """)
             
while command != "exit":
    
    command = input("Enter a source type (github, other) or type exit to exit: ")
    
    if command == "github": # oh boy
        developer = input("Enter the name of the repository developer: ")
        repository = input("Enter the repository name: ")
        sourceInfo = {"developer": developer, "repository": repository, "type": "github"}
        if repository in sources:
            overwriteConfirmation = input("A repository with this name has already been added, would you like to replace it [y/n]: ")
            if overwriteConfirmation == 'y':
                print("Overwriting repository {0}.".format(repository))
                sources[repository] = sourceInfo
            else:
                print("The repository was not overwritten.")
        else:
            print("Adding repository {0}.".format(repository))
            sources[repository] = sourceInfo
    
    elif command == "other":
        name = input("Enter the name of the application: ")
        developer = input("Enter the name of the application developer: ")
        location = input("Enter the URL to the CIA for this application: ")
        description = input("Enter a short description for this application: ")
        version = input("Enter the applications current version: ")
        sourceInfo = {"name": name, "developer": developer, "location": location, "description": description, "version": version, "type": "other"}
        if name in sources:
            overwriteConfirmation = input("A source with this name has already been added, would you like to replace it [y/n]: ")
            if overwriteConfirmation == 'y':
                print("Overwriting source {0}.".format(name))
                sources[name] = sourceInfo
            else:
                print("The source was not overwritten.")
        else:
            print("Adding source {0}.".format(name))
            sources[name] = sourceInfo
            
with io.open('sources.json', 'w', encoding="utf8") as sources_file_out:
    str_ = json.dumps(sources,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    
    sources_file_out.write(str_)