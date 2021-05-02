class Variable:

    def __init__(self, type, bits, validity):
        self.type = type
        self.usedBits = bits
        self.validity = validity
        self.system = False
        self.iterable=True
            #"global", bank{2-8}

