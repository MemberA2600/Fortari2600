class WaveConverter:

    def __init__(self, loader, path):
        #Accepts 8000 Hz, mono, 16 pit PCM

        self.__loader = loader

        file = open(path, "rb")
        bytes = file.read()
        file.close()

        byteStrings = []

        for byte in bytes:
            byteStrings.append(hex(byte).replace("0x", ""))

        self.result = None

        header = {}

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

        if header["valid"] == False:
           self.result = None
        else:
            uncompressed = self.__convertTo4Bits(byteStrings[44:])


            shit = open("fuck.txt", "w")
            pee = ""
            for byte in uncompressed:
                pee += "\tbyte\t#%"+byte+"\n"
            shit.write(pee)
            shit.close()


    def __convertTo4Bits(self, data):

        newData = []
        length = len(data) // 2 * 2

        for num in range(0, length, 2):


            newByte = bin(int("0x"+data[num+1][0]+data[num][0], 16)).replace("0b", "")
            while len(newByte) < 8:
                newByte = "0" + newByte

            newData.append(newByte)

        return(newData)



if __name__ == "__main__":
    WaveConverter(None, "F:\PyCharm\P\\toDelete\\forTest17\Test.wav")