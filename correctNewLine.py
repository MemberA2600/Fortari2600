import os

def doIt(directroty):
    for root, dirs, files in os.walk(directroty):
        print(">> " + root)

        for dir in dirs:
            doIt(dir)

        for file in files:
            f = open(root + "/" + file, "r")
            try:
                txt = f.read()
                print("--- " + file)
                f.close()

                f = open(root + "/" + file, "w")
                f.write(txt)
            except (UnicodeDecodeError, PermissionError):
                pass
            f.close()

if __name__ == "__main__":
   doIt(os.getcwd())

