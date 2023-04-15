import re


class Command:

    def __init__(self, loader, name, string):
        self.__loader = loader
        self.name   = name

        data = string.split(",")
        if data[0]!= "[]":
            self.alias = data[0][1:-1].split(" ")
        else:
            self.alias = []

        if data[3].lower() == "end":
           self.endNeeded = True
           newName  = "end-"+name.split("-")[0]
           newAlias = []
           for a in self.alias:
               newAlias.append("end-"+a.split("-")[0])

           newString = "["+" ".join(newAlias) +"]"+"," + data[1] + "," + "end-command" + ",None,None,"+data[5]+",None,None,"+data[8]+",False"
           self.__loader.syntaxList[newName] = Command(loader, newName, newString)
        else:
            self.endNeeded = False

        if data[4].lower() == "brackets":
            self.bracketNeeded = True
        else:
            self.bracketNeeded = False

        if data[5] == "[]":
           self.sectionsAllowed = self.__loader.sections
        else:
           if data[5].startswith("[!") == False:
              self.sectionsAllowed = data[5][1:-1].split(" ")
           else:
             from copy import deepcopy
             nope = data[5][2:-1].split(" ")
             self.sectionsAllowed = deepcopy(self.__loader.sections)
             for item in nope:
                 self.sectionsAllowed.remove(item)

        if data[6] != "None":
           self.params = data[6][1:-1].split(" ")
           # print(self.params)
        else:
           self.params = []

        if data[7] != "None":
           self.does = data[7]
        else:
           self.does = None

        if data[8] != "None":
           self.levelAllowed = int(data[8])
        else:
           self.levelAllowed = None

        if data[9] == "True":
           self.flexSave = True
        else:
           self.flexSave = False

        for a in self.alias:
            newString = "[],[common],command,"+data[3].lower()+","+data[4].lower() + "," + data[5] +\
                         "," + data[6] + "," + data[7] + "," + data[8] + "," + data[9]
            self.__loader.syntaxList[a] = Command(loader, a, newString)

    def changeAliasToName(self, name, text):
        newText = []
        for line in text.split("\n"):
            if line.startswith("*") or line.startswith("#"):
                newText.append(line)
            else:
                for ali in self.alias:
                    line = re.sub(rf"\s+{ali}\s+", f" {name} ", text)
                    line = re.sub(rf"^{ali}\s+", f"{name} ", text)

                newText.append(line)
        return("\n".join(newText))