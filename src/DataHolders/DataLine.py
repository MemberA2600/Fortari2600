class DataLine:

    def __init__(self):
        self.raw = []
        self.seq = None
        self.address = None
        self.bytes = []
        self.byteNum = 1

    def getAddressInHex(self):
        return(hex(self.address)[2:])