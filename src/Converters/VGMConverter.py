#Using VMG modules of https://github.com/cdodd/vgmparse

class VGMConverter:

    def __init__(self, loader, path, removePercuss, maxChannels, removeOutside, cutOut):

        self.__loader = loader
        from threading import Thread
        import os

        txt  = ".".join(path.split(".")[:-1])+".txt"
        txt2 = "/".join(txt.split("/")[:-1])+"/renamed.txt"
        try:
            os.remove(txt)
        except:
            pass

        t = Thread(target=self.vgm2textThread, args=[path])
        t.daemon = True
        t.start()

        from time import sleep
        counter = 0

        while True:
            if counter == 500:
                break

            if os.path.exists(txt):
                try:
                    os.rename(txt, txt2)
                    break
                except:
                    pass
            else:
                counter+=1
            sleep(0.01)

        self.__loader.executor.killByForce("vgm2txt")

        file = open(txt2, "r")
        data = file.read().replace("\r","").split("VGMData:")
        file.close()

        os.remove(txt2)

        from VGMDataItem import VGMDataItem

        data[0] = data[0].replace("NES APU", "NES_APU").replace("GB DMG", "GB_DMG")

        headerData = data[0].split("\n")[1:]
        processData = data[1].split("\n")

        self.__vgmHeader = {}
        self.__vgmData = []

        self.__unused = []
        self.__used = []

        for line in headerData:
            line = line.replace("\t", " ").split(" ")
            newLine = []
            for item in line:
                if item != "":
                    newLine.append(item)

            line = newLine
            if line!=[]:
                if "Version:" in line:
                    self.__vgmHeader["version"] = float(line[-1][1:-1])
                if line[0] in self.__unused:
                    continue

                if line[-1] == "unused":
                    self.__unused.append(line[0])
                    continue

                if "Rate:" in line:
                    self.__vgmHeader["rate"] = float(line[-2])

                if line[1] == "Clock:":
                    self.__vgmHeader[line[0]] = {}
                    self.__vgmHeader[line[0]]["clock"] = int(line[2])
                    self.__used.append(line[0])

                if line[0] in self.__used and line[1] != "Clock:":
                    if line[2] == "Flags:":
                        self.__vgmHeader[line[0]][line[1].lower()+"_flags"] = int(line[3], 16)
                    else:
                        self.__vgmHeader[line[0]][line[1].lower().replace(":","")] = int(line[2],16)

                if line[0] == "Volume":
                    self.__vgmHeader["volume"] = float(line[-1])

        self.__noteNum = 0

        for line in processData:
            if line != "":
                self.__vgmData.append(VGMDataItem(line))
                if "Key On" in line:
                    self.__noteNum+=1

        #print(self.__vgmHeader)
        #for item in self.__vgmData:
        #    print(item.command, item.dataBytes, item.dataByteStrings, item.extraData)

        # OPL2 is fully compatible with OPL, OPL3 is handled as OPL2

        if (("YM3812" in self.__used) or ("YM3526" in self.__used) or
            ("YMF262" in self.__used) or ("YMF262A" in self.__used)
            or ("YMF262B" in self.__used)):
            self.__oplData = self.callVGMExtractor("YM3812", ["OPL2"], ("5A", "5B", "5E", "5F"))

        file = open("temp/shit.txt", "w")
        file.write(data[0])
        file.close()

    def callVGMExtractor(self, program, extraData, codeBytes):
        bytes = ""
        for item in self.__vgmData:
            if item.dataByteStrings[0] in codeBytes or item.dataByteStrings[0] == "61":
                bytes += " ".join(item.dataByteStrings) + "\n"

        data = self.__loader.executor.callFortran("VGMConverter",
                                                program, bytes,
                                                str(self.__vgmHeader["volume"]) + " " + str(
                                                self.__vgmHeader["rate"]) + " " + str(self.__noteNum) + " "+"|".join(extraData),
                                                True, True)
        return(data)


    def vgm2textThread(self, path):
        self.__loader.executor.execute("vgm2txt", ['"'+path+'"', '"'+"0"+'"', '"'+"0"+'"'], True)


