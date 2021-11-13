class VGMByteDict:

    def __init__(self, loader):
        self.__loader = loader

        self.__headerDict = {}
        self.__commandDict = {}

        for item in open("config/VGMHeaderDict.txt", "r").read().replace("\r","").split("\n"):
            item = item.split("=")
            longNum = int(item[0])
            parts = item[1].split(",")
            self.__headerDict[longNum] = []
            for part in parts:
                FFF = part.split("-")
                if FFF[1] == "#":
                    continue
                bits = FFF[0].split(":")
                self.__headerDict[longNum].append({
                    "name": FFF[1],
                    "starting": int(bits[0]),
                    "ending": int(bits[1])
                })

        for item in open("config/VGMCommandDict.txt", "r").read().replace("\r","").split("\n"):
            item = item.split("=")

    def testPrintingHeaderStuff(self):
        for num in range(0,32,2):
            names = []
            if num in self.__headerDict.keys():
                for item in self.__headerDict[num]:
                    names.append(item["name"])
            if num+1 in self.__headerDict.keys():
                for item in self.__headerDict[num+1]:
                    names.append(str.ljust(item["name"], item["ending"]-item["starting"]+2))

            print(str(num//2)+": "+" | ".join(names))


    def headerData(self, long):
        try:
            return(self.__headerDict[long])
        except:
            return None

    def headerKeys(self):
        return(self.__headerDict.keys())