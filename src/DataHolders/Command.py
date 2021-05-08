import re

class Command:

    def __init__(self, loader, string):
        self.__loader = loader
        data = string.split(",")
        self.alias = data[0][1:-1].split(" ")

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