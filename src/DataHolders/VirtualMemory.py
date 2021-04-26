from DataItem import DataItem
import os
from MemoryItem import MemoryItem


class VirtualMemory:

    def __init__(self, loader):

        self.__loader = loader
        self.codes = {}
        self.locks = {}

        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.locks[bankNum] = ""
            self.codes[bankNum] = {}
            if (num == 1):
                self.codes[bankNum]["bank_configurations"] = DataItem()
                self.codes[bankNum]["global_variables"] = DataItem()
            else:
                for section in self.__loader.sections:
                    self.codes[bankNum][section] = DataItem()

        self.types = {
            "bit": 1,
            "doubleBit": 2,
            "nibble": 4,
            "byte": 8
        }

        self.resetMemory()
        self.addSystemMemory()

        """
        self.addVariable("pacal", "nibble", "global")
        self.addVariable("sajt", "doubleBit", "bank2")
        self.addVariable("marha", "nibble", "global")
        self.removeVariable("sajt", "bank2")
        self.addVariable("velő", "nibble", "bank3")


        for address in self.memory.keys():
            if len(self.memory[address].variables.keys())>0:
                print(address)
                for valiable in self.memory[address].variables.keys():
                    print(valiable)
                    print(self.memory[address].variables[valiable].usedBits)
                print(self.memory[address].freeBits)

        """
    def addSystemMemory(self):
        pass

    def addArray(self, name):
        self.arrays[name] = []

    def removeArray(self, name):
        self.array.pop(name)


    def checkIfExists(self, name, validity):
        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                if name == variable:
                    if validity == "global":
                        return(True)
                    else:
                        if validity == self.memory[address].variables[variable].validity:
                            return(True)
        return(False)

    def removeVariable(self, name, validity):
        for address in self.memory.keys():
            if name in self.memory[address].variables.keys():
                if validity == "global":
                    self.memory[address].addBitsToGlobalAddress(self.memory[address].variables[name].usedBits)
                    self.memory[address].variables.pop(name)
                    return(True)
                else:
                    if self.memory[address].variables[name].validity == validity:
                        self.memory[address].addBitsToBankAddress(self.memory[address].variables[name].usedBits, validity)
                        self.memory[address].variables.pop(name)
                        return(True)
        return(False)


    def addVariable(self, name, type, validity):
        neededBits = self.types[type]
        success = False

        for memoryAddress in self.memory.keys():
            if len(self.memory[memoryAddress].freeBits[validity])>=neededBits:
                bits = self.getIfThereAreAvaiableBitNearAndInARow(self.memory[memoryAddress].freeBits[validity], neededBits)
                if bits == False:
                    continue
                else:
                    if validity == "global":
                        self.memory[memoryAddress].removeBitsFromGlobalAddress(bits)
                    else:
                        self.memory[memoryAddress].removeBitsFromBankAddress(bits, validity)
                    self.memory[memoryAddress].addVariable(name, type, bits, validity)
                    success = True
                    break


        return(success)
            #print(memoryAddress)

    def getIfThereAreAvaiableBitNearAndInARow(self, data, needed):
        startNum = 0
        while ((startNum+needed-1)<8):
            canIHazACheezBurger = []
            for num in range(startNum, startNum+needed):
                canIHazACheezBurger.append(num)
            check = True
            for num in canIHazACheezBurger:
                if (num in data) == False:
                    check = False
                    break

            if check == True:
                #print(canIHazACheezBurger)
                return(canIHazACheezBurger)
            else:
                startNum+=1
        return(False)

    def resetMemory(self):
        self.memory={}
        self.arrays={}

        for i in range(128, 256):
            self.memory["$"+self.getHex(i)] = MemoryItem()
        for i in range(0,128):
            I = self.getHex(i)
            if len(I)==1:
                I = "0"+I

            self.memory["$10"+I] = MemoryItem()


    def getHex(self, i):
        return(hex(i)[2:])

    def getSARAReadAddressFromWriteAddress(self, num):
        num = "$10"+hex(int(num[3:], 16)+128)[2:]

        return(num)

    def getSARAWriteAddressFromReadAddress(self, num):
        num = "$10"+hex(int(num[3:], 16)+128)[2:]

        return(num)

    def setLocksAfterLoading(self):
        lines = self.codes["bank1"]["bank_configurations"].code.split("\n")
        for line in lines:
            if line.startswith("*"):
                continue
            else:
                self.locks[line.split("=")[0]] = line.split("=")[1].replace("\n","").replace("\r","")

    def createTheBankConfigFromMemory(self):
        text = []
        text.append("*** This is where you set the details of banks such as name, role, and so on.")
        for bank in self.locks.keys():
            if self.locks[bank]!="":
                text.append(bank+"="+self.locks[bank])

        self.codes["bank1"]["bank_configurations"].code = os.linesep.join(text)
        #print(self.__loader.virtualMemory.codes["bank1"]["bank_configurations"].code)

    def setglobalVariablesFromMemory(self):
        lines = self.codes["bank1"]["global_variables"].code.split("\n")
