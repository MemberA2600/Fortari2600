from Variable import Variable

class MemoryItem:

    def __init__(self):

        self.freeBits = {}
        self.freeBits["global"] = [0, 1, 2, 3, 4, 5, 6, 7]
        for num in range(2,9):
            self.freeBits["bank"+str(num)] = [0, 1, 2, 3, 4, 5, 6, 7]


        self.variables = {}

    def addVariable(self, name, type, bits, validity):
        self.variables[name] = Variable(type, bits, validity)

    def addBitsToGlobalAddress(self, bits):
        self.freeBits["global"].extend(bits)
        self.freeBits["global"] = self.sortedSet(self.freeBits["global"])
        for num in range(2,9):
            self.freeBits["bank"+str(num)].extend(bits)
            self.freeBits["bank" + str(num)] = self.sortedSet(self.freeBits["bank" + str(num)])

    def addBitsToBankAddress(self, bits, bankNum):
        self.freeBits["global"].extend(bits)
        self.freeBits["global"] = self.sortedSet(self.freeBits["global"])
        self.freeBits[bankNum].extend(bits)
        self.freeBits[bankNum] = self.sortedSet(self.freeBits[bankNum])

    def sortedSet(self, L):
        __list = list(set(L))
        __list.sort()
        return(__list)

    def removeBitsFromGlobalAddress(self, bits):
        self.freeBits["global"] = self.makeSetRemoveSortGiveBack(self.freeBits["global"], bits)
        for num in range(2, 9):
            self.freeBits["bank"+str(num)] = self.makeSetRemoveSortGiveBack(self.freeBits["bank"+str(num)], bits)

    def removeBitsFromBankAddress(self, bits, num):
        self.freeBits["global"] = self.makeSetRemoveSortGiveBack(self.freeBits["global"], bits)
        self.freeBits[num] = self.makeSetRemoveSortGiveBack(self.freeBits[num], bits)


    def makeSetRemoveSortGiveBack(self, A, B):
        setA = set(A)
        setB = set(B)

        A = list(setA.difference(setB))
        A.sort()
        return(A)