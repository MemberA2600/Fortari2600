class WaveConverter:

    def __init__(self, loader, path, tv_type):
        #Accepts 8000 Hz, mono, 16 pit PCM

        self.__loader = loader

        file = open(path, "rb")
        bytes = file.read()
        file.close()

        byteStrings = []

        for byte in bytes:
            byteStrings.append(hex(byte).replace("0x", ""))
            if len(byteStrings[-1]) == 1: byteStrings[-1] = "0" + byteStrings[-1]
        self.result = None

        header = {}

        self.__tv = tv_type.upper()

        if "".join(byteStrings[0:4]) == "52494646".lower():
           header["valid"] = True
        else:
           header["valid"] = False

        header["chuckSize"] = int("0x"+byteStrings[7] +
                                       byteStrings[6] +
                                       byteStrings[5] +
                                       byteStrings[4], 16)

        if "".join(byteStrings[8:15]) != "57415645666D74".lower():
           header["valid"] = False


        header["bits"] = int("0x"+byteStrings[19] +
                                  byteStrings[18] +
                                  byteStrings[17] +
                                  byteStrings[16], 16)

        if header["bits"] != 16:
           header["valid"] = False

        header["format"] = int("0x" + byteStrings[21] +
                                      byteStrings[20], 16)

        if header["format"] != 1:
           header["valid"] = False

        header["numberOfChannel"] = int("0x" + byteStrings[23] +
                                               byteStrings[22], 16)

        if header["numberOfChannel"] != 1:
           header["valid"] = False


        header["sampleRate"] = int("0x"+byteStrings[27] +
                                        byteStrings[26] +
                                        byteStrings[25] +
                                        byteStrings[24], 16)

        if header["sampleRate"] != 8000:
           header["valid"] = False

        header["byteRate"] = int("0x"+byteStrings[31] +
                                      byteStrings[30] +
                                      byteStrings[29] +
                                      byteStrings[28], 16)

        header["bitsPerSample"] = int("0x" + byteStrings[35] +
                                             byteStrings[34], 16)

        if float(header["byteRate"]) != header["sampleRate"] * header["numberOfChannel"] * header["bitsPerSample"] / 8:
           header["valid"] = False

        header["blockAlign"] = int("0x" + byteStrings[33] +
                                          byteStrings[32], 16)

        if float(header["blockAlign"]) != header["numberOfChannel"] * header["bitsPerSample"] / 8:
           header["valid"] = False

        if "".join(byteStrings[36:40]) != "64617461".lower():
           header["valid"] = False

        header["dataSize"] = int("0x"+byteStrings[43] +
                                      byteStrings[42] +
                                      byteStrings[41] +
                                      byteStrings[40], 16)

        self.mode = ""
        link = None

        if header["valid"] == False:
           self.result = None
           self.mode = "failed"
        else:
            self.result = {}

            uncompressed = self.__convertTo4Bits(byteStrings[44:])

            keys = self.__loader.executor.callFortran("WaveConverter","GetKeys", "\n".join(uncompressed), None, True, True).split("\n")

            keyDict = {}
            keyDict["EOF"] = keys[0]

            comp = True
            for num in (0, 16):
                num = bin(num).replace("0b","")
                while len(num) < 8: num = "0"+num
                if num not in keys:
                   comp = False
                   break


            if comp == False:
                self.result["SoundBytes"] = ""
                for byte in uncompressed:
                    if ("0" in byte) or ("1" in byte):
                        self.result["SoundBytes"] += "\tBYTE\t#%" + byte + "\n"

                self.result["SoundBytes"] += "\tBYTE\t#%" + keyDict["EOF"] + "\n"
                self.result["EOF"] = keyDict["EOF"]
                self.mode = "uncompressed"

            else:
                self.result["SoundBytes"] = ""

                compressed = self.__loader.executor.callFortran("WaveConverter", "Compress", "\n".join(uncompressed), None,
                                                          True, True).split("\n")
                for byte in compressed:
                    if ("0" in byte) or ("1" in byte):
                        self.result["SoundBytes"] += "\tBYTE\t#%" + byte + "\n"

                link = compressed
                self.result["SoundBytes"] += "\tBYTE\t#%" + keyDict["EOF"] + "\n"
                self.result["EOF"] = keyDict["EOF"]
                self.mode = "compressed"


            if self.mode != "failed":
                bytes = self.result["SoundBytes"].split("\n")
                b = 0
                for line in bytes:
                    if "BYTE" in line.upper():
                        b+=1

                if b > 3650:
                    self.mode += "3bit"
                    raw = []
                    try:
                        for num in range(0, len(uncompressed), 3):
                            byte1 = uncompressed[num]
                            byte2 = uncompressed[num + 1]
                            byte3 = uncompressed[num + 2]

                            raw.append(byte1)

                            raw.append(
                                byte3[0:4] + byte2[0:4]
                            )

                            # raw.append(
                            #    byte2[0:2] + byte2[4:6] + byte1[0:2] + byte1[4:6]
                            # )
                    except:
                        pass

                    self.result["SoundBytes"] = ""
                    newKeys = {}

                    if self.mode == "compressed3bit":
                        newKeys["00000000"] = False
                        for num in range(0, 16):
                            num = bin(num).replace("0b", "") + "0000"
                            while len(num) < 8:
                                num = "0" + num
                            newKeys[num] = False

                        raw = self.__loader.executor.callFortran("WaveConverter", "Compress",
                                                                 "\n".join(raw), None,
                                                                 True, True).split("\n")

                    else:
                        for num in range(0, 255):
                            num = bin(num).replace("0b", "")
                            while len(num) < 8:
                                num = "0" + num
                            newKeys[num] = False

                    n = 0
                    for byte in raw:
                        if ("0" in byte) or ("1" in byte):
                            self.result["SoundBytes"] += "\tBYTE\t#%" + byte + "\n"
                            newKeys[byte] = True
                            n = n + 1
                        if n > 3800: break

                    for key in newKeys:
                        if newKeys[key] == False:
                            self.result["EOF"] = key
                            break

                    self.result["SoundBytes"] += "\tBYTE\t#%" + self.result["EOF"] + "\n"



            if self.mode != "failed":
                bytes = self.result["SoundBytes"].split("\n")
                b = 0
                for line in bytes:
                    if "BYTE" in line.upper():
                        b+=1

                if b > 3650:

                   if "uncompressed" in self.mode:
                       self.mode = "uncompressed"

                   else:
                       self.mode = "compressed"

                   self.mode += "2bit"

                   raw = []
                   try:
                        for num in range(0, len(uncompressed), 2):
                            byte1 = uncompressed[num]
                            byte2 = uncompressed[num+1]

                            raw.append(
                                byte2[0:4] + byte1[0:4]
                            )

                            #raw.append(
                            #    byte2[0:2] + byte2[4:6] + byte1[0:2] + byte1[4:6]
                            #)
                   except:
                       pass

                   self.result["SoundBytes"] = ""
                   newKeys = {}

                   if self.mode == "compressed2bit":
                       newKeys["00000000"] = False
                       for num in range(0, 16):
                           num = bin(num).replace("0b", "")+"0000"
                           while len(num) < 8:
                               num = "0" + num
                           newKeys[num] = False

                       raw = self.__loader.executor.callFortran("WaveConverter", "Compress",
                                                                       "\n".join(raw), None,
                                                                       True, True).split("\n")

                   else:
                      for num in range(0, 255):
                          num = bin(num).replace("0b","")
                          while len(num) < 8:
                              num = "0"+num
                          newKeys[num] = False

                   n = 0
                   for byte in raw:
                       if ("0" in byte) or ("1" in byte):
                           self.result["SoundBytes"] += "\tBYTE\t#%" + byte + "\n"
                           newKeys[byte] = True
                           n = n + 1
                       if n > 3800 : break

                   for key in newKeys:
                       if newKeys[key] == False:
                           self.result["EOF"] = key
                           break

                   self.result["SoundBytes"] += "\tBYTE\t#%" + self.result["EOF"] + "\n"


            if self.mode != "failed":
                bytes = self.result["SoundBytes"].split("\n")
                b = 0
                for line in bytes:
                    if "BYTE" in line.upper():
                        b+=1

                if b > 3650:

                   if "uncompressed" in self.mode:
                       self.mode = "uncompressed"

                   else:
                       self.mode = "compressed"

                   self.mode += "1bit"

                   raw = []
                   try:
                        for num in range(0, len(uncompressed), 4):
                            byte1 = uncompressed[num]
                            byte2 = uncompressed[num+1]
                            byte3 = uncompressed[num+2]
                            byte4 = uncompressed[num+3]

                            raw.append(
                                byte3[0:4] + byte1[0:4]
                                #byte4[0:2] + byte3[0:2] + byte2[0:2] + byte1[0:2]
                            )

                            #raw.append(
                            #    byte2[0:2] + byte2[4:6] + byte1[0:2] + byte1[4:6]
                            #)
                   except:
                       pass

                   self.result["SoundBytes"] = ""
                   newKeys = {}

                   if self.mode == "compressed1bit":
                       newKeys["00000000"] = False
                       for num in range(0, 16):
                           num = bin(num).replace("0b", "")+"0000"
                           while len(num) < 8:
                               num = "0" + num
                           newKeys[num] = False

                       raw = self.__loader.executor.callFortran("WaveConverter", "Compress",
                                                                       "\n".join(raw), None,
                                                                       True, True).split("\n")

                   else:
                      for num in range(0, 255):
                          num = bin(num).replace("0b","")
                          while len(num) < 8:
                              num = "0"+num
                          newKeys[num] = False

                   n = 0
                   for byte in raw:
                       if ("0" in byte) or ("1" in byte):
                           self.result["SoundBytes"] += "\tBYTE\t#%" + byte + "\n"
                           newKeys[byte] = True
                           n = n + 1
                       if n > 3800 : break

                   for key in newKeys:
                       if newKeys[key] == False:
                           self.result["EOF"] = key
                           break

                   self.result["SoundBytes"] += "\tBYTE\t#%" + self.result["EOF"] + "\n"

    def __convertTo4Bits(self, data):

        newData = []
        length = len(data) // 2 * 2

        for num in range(0, length, 2):

            newByte = bin(int("0x"+data[num+1][0]+data[num][0], 16)).replace("0b", "")
            while len(newByte) < 8:
                newByte = "0" + newByte

            newData.append(newByte)

        return(newData)

"""

if __name__ == "__main__":
    WaveConverter(None, "F:\PyCharm\P\\toDelete\\forTest17\Test.wav", "NTSC")

"""