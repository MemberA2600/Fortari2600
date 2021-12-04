#Using VMG modules of https://github.com/cdodd/vgmparse

from VGMBytes import VGMBytes
from VGMByteDict import VGMByteDict
import gzip
from io import BytesIO as ByteBuffer

class VGMConverter:

    def __init__(self, loader, path, removePercuss, maxChannels, removeOutside, cutOut):

        self.__loader = loader
      # self.__loader.collector.manuallyRegisterPackage("vgmparse")

        ext = path.split(".")[-1]

        #file = ByteBuffer(open(path, "rb").read())
        f = open(path, "rb")
        file=ByteBuffer(f.read())
        f.close()

        if ext == "vgz":
            file = gzip.GzipFile(fileobj=file, mode='rb')

        #f = open("temp/temp.vgm", mode="wb")
        #f.write(file.read())
        #f.close

        byteData = ""

        for byte in file.read():
            byteData+=hex(byte).replace("0x","")+"\n"

        self.__loader.executor.callFortran("VGMConverter", "LoadHeader", byteData, None, True, True)

        """
        self.__vgmBytes = VGMBytes(self.__loader, file)

        #print(vgmDataByteString)

        self.__byteDict = VGMByteDict(self.__loader)
        self.header = self.__constructHeader()
        #self.__byteDict.testPrintingHeaderStuff()

        self.__validateHeader()
        """

    def __constructHeader(self):
        header = {}

        index = 0
        for lineNum in self.__byteDict.headerKeys():
            items = self.__byteDict.headerData(lineNum)
            bytes8 = self.__vgmBytes.byteString[index:(index+16)]
            index+=16

            #print(lineNum, bytes8)

            temp = []
            for n in range(0,16,2):
                temp.append(bytes8[n:n+2])

            if items != None:
                for subitem in items:
                    header[subitem["name"]] = {}
                    header[subitem["name"]]["hex"] = "".join(temp[subitem["starting"]:(subitem["ending"]+1)])

        return header

    def __validateHeader(self):
        for item in self.header.keys():
            if item == "VGM":
               self.header["VGM"]["valid"] = self.header["VGM"]["hex"] == "56676d20"
               if self.header["VGM"]["valid"] == False:
                    return(None)

            elif item == "EOF_Offset":
                num = int("0x"+self.header["EOF_Offset"]["hex"], 16)
                self.header["EOF_Offset"]["value"] = num
                self.header["EOF_Offset"]["fileLen"] = num+4
                self.header["EOF_Offset"]["fileLenWithoutHeader"] = num-252

            elif "_Clock" in item:
                self.header[item]["clock"] = int("0x"+self.header[item]["hex"], 16)
                print(self.header[item]["clock"])
