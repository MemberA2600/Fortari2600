#Using VMG modules of https://github.com/cdodd/vgmparse

from VGMBytes import VGMBytes
from VGMByteDict import VGMByteDict
import gzip
from io import BytesIO as ByteBuffer

class VGMConverter:

    def __init__(self, loader, path, removePercuss, maxChannels, removeOutside, cutOut):

        self.__loader = loader
        self.__loader.collector.manuallyRegisterPackage("vgmparse")

        ext = path.split(".")[-1]

        #file = ByteBuffer(open(path, "rb").read())
        f = open(path, "rb")
        file=ByteBuffer(f.read())
        f.close()

        if ext == "vgz":
            file = gzip.GzipFile(fileobj=file, mode='rb')

        self.__vgmBytes = VGMBytes(self.__loader, file)

        #print(vgmDataByteString)

        self.__byteDict = VGMByteDict(self.__loader)
        self.header = self.__constructHeader()
        #self.__byteDict.testPrintingHeaderStuff()

        self.__validateHeader()

    def __constructHeader(self):
        header = {}

        index = 0
        for lineNum in self.__byteDict.headerKeys():
            items = self.__byteDict.headerData(lineNum)
            bytes8 = self.__vgmBytes.byteString[index:(index+16)]
            index+=16

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
               self.header["hex"]["valid"] = self.header["VGM"]["hex"] == "56676d20"
               if self.header["hex"]["valid"] == False:
                    return(None)

