import re


class Command:

    def __init__(self, loader, name, string):
        self.__loader = loader
        self.__name   = name
        data = string.split(",")
        self.alias = data[0][1:-1].split(" ")
        if data[3].lower() == "end":
           newName  = "end-"+name
           newAlias = []
           for a in self.alias:
               newAlias.append("end-"+a)

           newString = "["+" ".join(newAlias) +"]"+"," + data[1] + "," + "end-command" + ",None,None"
           self.__loader.syntaxList[newName] = Command(loader, newName, newString)

        if data[4] == "brackets":
            self.bracketNeeded = True
        else:
            self.bracketNeeded = False


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