from DataItem import DataItem
import os
from MemoryItem import MemoryItem
from threading import Thread

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


        t = Thread(target=self.testPrintMemory)
        t.daemon = True
        t.start()

    def testPrintMemory(self):
        from time import sleep

        while self.__loader.mainWindow == None or self.__loader.mainWindow.dead==False:
            for address in self.memory.keys():
                if len(self.memory[address].variables.keys())>0:
                    string=address+os.linesep
                    for valiable in self.memory[address].variables.keys():
                        string+=valiable+os.linesep
                        string+=str(self.memory[address].variables[valiable].usedBits)+os.linesep
                        string+=self.memory[address].variables[valiable].type+os.linesep
                        string+=self.memory[address].variables[valiable].validity+os.linesep

                        for XXX in self.memory[address].freeBits:
                            string += XXX + ":" + str(self.memory[address].freeBits[XXX]) +  os.linesep
                    string ="------------------------------"+os.linesep
                    self.__loader.logger.addToLog(string)
            sleep(10)

    def addSystemMemory(self):
        pass

    def addArray(self, name):
        self.arrays[name] = {}

    def removeArray(self, name):
        self.array.pop(name)

    def addItemsToArray(self, name, itemname, var):
        self.arrays[name][itemname] = var

    def removeItemFromArray(self, name, item):
        self.arrays[name].pop(item)

    def getVariableByName(self, name, bank):
        section="local_variables"
        if bank == "bank1":
            section = "global_variables"


        for address in self.memory.keys():
            for id in self.memory[address].variables.keys():
                #print(id, name)
                if name == id:
                    return(self.memory[address].variables[id])
        return(False)

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

    def moveMemorytoVariables(self, bank):
        section="local_variables"
        validity = bank
        if bank == "bank1":
            section = "global_variables"
            validity = "global"

        lines = self.codes[bank][section].code.split("\n")
        for line in lines:
            try:
                if line.startswith("*"):
                    continue
                data = line.split("=")
                name=data[0]
                if self.checkIfExists(name, validity):
                    continue
                TYPE = data[1].replace("\n","").replace("\r","")
                if (TYPE in self.types.keys()):
                    self.addVariable(name, TYPE, validity)
                else:
                    self.addArray(name)
                    data = TYPE[6:-1].split(",")
                    for item in data:
                        self.addItemsToArray(name, item, self.getVariableByName(item, bank))
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def moveVariablesToMemory(self, bank):
        section="local_variables"
        string="*** Here you can find variables those are only aviable for this screen."+os.linesep
        if bank == "bank1":
            section = "global_variables"
            string="*** This is where you set the variables for the whole project, so the ones shouldn't"+os.linesep+\
               "*** be overwritten anywhere."+os.linesep

        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                string += variable + "=" + self.memory[address].variables[variable].type + os.linesep
        for array in self.arrays.keys():
            string+=array + "=(" + ",".join(list(self.arrays[array].keys()))+")"+os.linesep

        self.codes[bank][section].code = string



    def setVariablesFromMemory(self, mode):
        #print("faszom", mode)

        if mode=="all":
            for num in range(1,9):

                self.moveMemorytoVariables("bank"+str(num))
        else:
            self.moveMemorytoVariables(mode)


    def writeVariablesToMemory(self, mode):
        if mode=="all":
            for num in range(1,9):
                self.moveVariablesToMemory("bank"+str(num))
        else:
            self.moveVariablesToMemory(mode)


        #self.moveMemorytoVariables("bank1")
