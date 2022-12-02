import re


class Command:

    def __init__(self, loader, name, string):
        self.__loader = loader
        self.__name   = name
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

           newString = "["+" ".join(newAlias) +"]"+"," + data[1] + "," + "end-command" + ",None,None"
           self.__loader.syntaxList[newName] = Command(loader, newName, newString)
        else:
            self.endNeeded = False

        if data[4].lower() == "brackets":
            self.bracketNeeded = True
        else:
            self.bracketNeeded = False

        for a in self.alias:
            newString = "[],[common],command,"+data[3].lower()+","+data[4].lower()
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