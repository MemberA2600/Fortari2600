import os

def checkModules(module, number, fileNames, listTwo):

    number[0] += 1

    f = open(fileNames[module], "r")
    text = f.readlines()
    f.close()

    for line in text:
        if "#" in line: continue
        if "(" not in line: continue

        for item in listOfModules:
            if item not in listTwo:
                continue

            if item+"(" in line:
                try:
                    listTwo.remove(item)
                except:
                    pass

                checkModules(item, number, fileNames, listTwo)

    number[0] -= 1


# Get List of Items

listOfModules = []

for root, dirs, files in os.walk(os.getcwd()+"/src", False):
    for file in files:
        if ".py" in file and "__pycache__" not in root:
            listOfModules.append(file.replace(".py", "").split(".")[0])

listOfModules = list(set(listOfModules))
listOfModules.sort()

#check if they are mentioned

from copy import deepcopy

listTwo = deepcopy(listOfModules)
fileNames = {
            "main": os.getcwd()+"/main.py"
            }

for root, dirs, files in os.walk(os.getcwd()+"/src", False):
    for file in files:
        if ".py" in file and "__pycache__" not in root:
            filename = root + "/" + file.replace(".py", "").split(".")[0] + ".py"
            filename = filename.replace("\\", "/")
            fileNames[file.replace(".py", "").split(".")[0]] = filename

#delete If Not Mentioned

number = [0]

checkModules("main", number, fileNames, listTwo)

projectName = os.getcwd().replace("\\", "/").split("/")[-1]
archievedPath = os.getcwd().replace(projectName, projectName + "ArchievedSrc")

try:
    os.mkdir(archievedPath)
except Exception as e:
    #print(str(e))
    pass

import shutil

for file in listTwo:
    print("Archieved "+file)
    shutil.move(fileNames[file], archievedPath)

for root, dirs, files in os.walk(os.getcwd()+"/src", False):
    for dir in dirs:
        if "__pycache__" in dir:
            shutil.rmtree(root+"/"+dir)
            print("Deleted: "+root+"\\"+dir)
