
def getTextFromKey(exe, key, command1, command2, command3):
    return         "\"" + exe + "\" /subkeyreg \"" + key + "\" " + command1 + "\n" + \
                   "\"" + exe + "\" /subkeyreg \"" + key + "\" " + command2 + "\n" + \
                   "\"" + exe + "\" /subkeyreg \"" + key + "\" " + command3 + "\n"



if __name__ == "__main__":
    path = "G:\Archieve-Copy\Programok\Intel_Fortran\\"
    exe  = "C:\Program Files (x86)\Windows Resource Kits\Tools\subinacl.exe"
    command1 = "/setowner=administrators"
    command2 = "/grant=administrators=f /grant=system=f /grant=Member=f"
    command3 = "/setowner=system"

    addToKey1 = "\shell\Open\Command"
    addToKey2 = "\shell\Open\ddeexec"
    addToKey3 = "\shell\DefaultIcon"
    addToKey4 = "\shell\shell"
    addToKey5 = "\CLSID"
    addToKey6 = "\CurVer"


    f = open(path + "keys.txt", "r")
    keys = f.read().replace("\r","").split("\n")
    f.close()

    toWrite = ""

    for key in keys:
        toWrite += getTextFromKey(exe, key, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey3, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey4, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey5, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey6, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey1, command1, command2, command3)
        toWrite += getTextFromKey(exe, key+addToKey2, command1, command2, command3)



    f = open(path + "updat.cmd", "w")
    f.write(toWrite)
    f.close()