class Variable:

    def __init__(self, type, bits, validity, color, bcd, allocType, allocAddress):
        self.type         = type
        self.usedBits     = bits
        self.validity     = validity
        self.system       = False
        self.iterable     = True
        self.linkable     = True
            #"global", bank{2-8}
        self.bcd          = bcd
        self.color        = color
        self.register     = False

        self.fixedAlloc   = allocType
        if self.fixedAlloc:
           self.fixedAddress = allocAddress
        else:
           self.fixedAddress = False