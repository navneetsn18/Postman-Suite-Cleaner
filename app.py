import sys
import json
import re

def suiteCleanUp(folders):
    for folder in folders:
        for responses in folder['item']:
            if len(responses["response"]) > 0:
                responses["response"] = []
    print("INFO: Data Cleaned Successfully!!")

def updateUrl(url,version):

    envRegex = "(\w+.ocp)"
    versionRegex = "(\d+-){1,}\w+"

    newEnv = "dev.ocp" if ("dev" in version.split("-")[-1] or "int" in version.split("-")[-1]) else "qa.ocp"
    
    url = re.sub(versionRegex,version,url) #Changes the version ie: 11-24-2-4-dev
    url = re.sub(envRegex,newEnv,url) #Changes env like qa to dev

    return url

def fixUrls(folders):
    urls = set()
    for folder in folders:
        for request in folder['item']:
            urls.add(request['request']['url']['raw'].split("/")[2])
    
    print("\nNo. Url")

    for i,j in enumerate(urls):
        print("{}. {}".format(i+1,j))
    
    choice = "1"
    choices = [str(i+1) for i in range(len(urls))]

    while choice in choices:
        choice = input("Enter the Url Number that you want to fix: ")
        if choice in choices:
            change = input("1. Change Version \n2. Change Complete Url")
            if change == "1":
                version = input("Enter the new version (Eg: 11-22-1-0-dev)")
                for folder in folders:
                    for request in folder['item']:
                        if request['request']['url']['raw'].split("/")[2] == urls[int(choice)-1]:
                            updatedUrl = updateUrl(request['request']['url']['raw'],version)
                            request['request']['url']['raw'] = updatedUrl
                            request['request']['url']['host'][0] = updatedUrl.split("/")[2].split(".")[0]
            elif change == "2":
                updatedUrl = input("Enter the complete Url")
                for folder in folders:
                    for request in folder['item']:
                        if request['request']['url']['raw'].split("/")[2] == urls[int(choice)-1]:
                            request['request']['url']['host'][0] = updatedUrl.split("/")[2].split(".")[0]
            else:
                print("Incorrect Input")
            
    print("INFO: Urls Fixed Successfully!!")

def save(data,fileName):
    with open("New_"+fileName, 'w') as outfile:
        json.dump(data, outfile)
    print("INFO: Data Saved Successfully!!")

if __name__ == "__main__":

    jsonFile = open(sys.argv[1]) #Open the file
    suiteData = json.load(jsonFile) #Load the data from json file

    choices = ["1","2","3"]
    choice = "1"

    while choice in choices:
        print("Choose from the menu below:")
        print("1. Cleanup the Suite")
        print("2. Fix the Urls")
        print("3. Save the Changes")
        print("Press any other key to exit ")
        choice = input()

        if choice == "1":
            suiteCleanUp(suiteData['item']) #Clean up the suite
        elif choice == "2":
            fixUrls(suiteData['item']) #Fix Urls
        elif choice == "3":
            save(suiteData,sys.argv[1]) #Save Data
