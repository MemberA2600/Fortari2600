import os

wordToFind = '!!!MAINVARS!!!'

for root, dirs, files in os.walk(os.getcwd()+"/src", False):
    for file in files:
        if ".py" in file and ".pyc" not in file:
            f = open(root + "/" + file, "r")
            try:
                r = f.read()
                if wordToFind in r: print("Found in: " + root + "/" + file)
            except:
                print("Unable to open: " + root + "/" + file)

            f.close()


