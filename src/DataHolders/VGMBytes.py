class VGMBytes:

    def __init__(self, loader, file):
        self.__loader = loader

        try:
            file = file.read()
        except:
            pass

        self.byteString = ""
        self.bytes = []
        for byte in file:
            B = hex(byte).replace("0x","")
            self.bytes.append(B)
            self.byteString += B
