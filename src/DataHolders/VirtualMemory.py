from DataItem import DataItem
import os
from MemoryItem import MemoryItem
from threading import Thread
from tkinter import END
from copy import deepcopy

class VirtualMemory:

    def __init__(self, loader):

        self.__loader = loader
        self.codes = {}
        self.locks = {}
        self.subs = {}
        self.bankLinks = {}
        self.kernel_types = []
        self.kernel = "common"

        for root, dirs, files in os.walk("templates/skeletons/"):
            for file in files:
                if "main_kernel" in file:
                    self.kernel_types.append(file.replace("_main_kernel.asm", ""))


        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.locks[bankNum] = None
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
        self.emptyArchieved()

        t = Thread(target=self.testPrintMemory)
        t.daemon = True
        t.start()

    def archieve(self):
        self.archieved = self.archieved[:self.cursor+1]

        self.archieved.append(
            {
             "viewed": [
                 self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].curselection()[0],
                 self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].curselection()[0]
             ],
             "codes": deepcopy(self.codes),
             "locks": deepcopy(self.locks),
             "memory": deepcopy(self.memory),
             "subs": deepcopy(self.subs),
             "bankLinks": deepcopy(self.bankLinks),
            }
        )

        if len(self.archieved)>int(self.__loader.config.getValueByKey("maxUndo")):
            self.archieved.pop(0)

        self.cursor = len(self.archieved)-1

    def changeKernelMemory(self, old, new):
        from copy import deepcopy
        oldVirtualMemory = deepcopy(self.memory)

        newVirtualMemory = {}
        tempItems = []
        names = []

        #self.memory[address].variables[name]
        self.kernel = new

        for address in self.memory.keys():
            for name in self.memory[address].variables:
                if self.memory[address].variables[name].system == False:
                    names.append(name)
                    tempItems.append(deepcopy(self.memory[address].variables[name]))

        self.resetMemory()
        self.addSystemMemory()

        self.success = False
        """
        for item in tempItems:
            for name in memoryItem.variables.keys():
                item = memoryItem.variables[item]
                self.success = self.addVariable(self, name, item.type, item.validity)
                if self.success == False:
                    break
        """

        for num in range(0, len(tempItems)):
            name = names[num]
            item = tempItems[num]

            self.success = self.addVariable(name, item.type, item.validity)
            if self.success == False:
                break

        if self.success == True:
            self.emptyArchieved()
            for array in self.arrays:
                for var in self.arrays[array]:
                    exists = False
                    for num in range(1,9):
                        bank = "bank" + str(num)
                        exists = self.getVariableByName(var, bank)
                        if exists != False:
                            break
                    if exists == False:
                        self.removeItemFromArray(array,var)
            self.__loader.soundPlayer.playSound("Success")

        else:
            self.kernel = old
            self.memory = deepcopy(oldVirtualMemory)
            data = {}
            data["#kernel#"] = new

            self.__loader.filedialogs.displayError(self.__loader.dictionaries.getWordFromCurrentLanguage("notEnoughMemory"),
                                                   self.__loader.dictionaries.getWordFromCurrentLanguage(
                                                       "kernelChangeFail"),
                                                   data, None
                                                   )

    def getArcPrev(self):
        self.cursor-=1
        self.__goToState()

    def getArcNext(self):
        self.cursor+=1
        self.__goToState()

    def __goToState(self):
        self.codes = deepcopy(self.archieved[self.cursor]["codes"])
        self.locks = deepcopy(self.archieved[self.cursor]["locks"])
        self.memory = deepcopy(self.archieved[self.cursor]["memory"])
        self.subs = deepcopy(self.archieved[self.cursor]["subs"])
        self.bankLinks = deepcopy(self.archieved[self.cursor]["bankLinks"])

        self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].select_clear(0, END)
        self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].select_clear(0, END)

        self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].select_set(self.archieved[self.cursor]["viewed"][0])
        self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].select_set(self.archieved[self.cursor]["viewed"][1])

        self.__loader.BFG9000.first = True

    def emptyArchieved(self):
        self.cursor = 0
        self.archieved = []

    def testPrintMemory(self):
        from time import sleep

        while self.__loader.mainWindow == None or self.__loader.mainWindow.dead==False:
            sleep(10)
            string=""
            for address in self.memory.keys():
                if len(self.memory[address].variables.keys())>0:
                    string+=address+os.linesep
                    for valiable in self.memory[address].variables.keys():
                        string+=valiable+os.linesep
                        string+=self.memory[address].variables[valiable].type+os.linesep
                        string+=self.memory[address].variables[valiable].validity+os.linesep
                        string+=str(self.memory[address].variables[valiable].usedBits)+os.linesep

                        #for XXX in self.memory[address].freeBits:
                        #    string += XXX + ":" + str(self.memory[address].freeBits[XXX]) +  os.linesep
                    string +="------------------------------"+os.linesep
            for array in self.arrays.keys():
                string += array + ": " +self.getArrayValidity(array)+", "+ str(list(self.arrays[array].keys()))+os.linesep
            if len(self.arrays.keys())>0:
                string += "------------------------------" + os.linesep

            self.__loader.logger.addToLog(string)


    def addSystemMemory(self):
        d = self.__loader.dataReader.readDataFile("templates"+os.sep+self.kernel+"_system_variables.a26")
        for key in d:
            self.addVariable(key, d[key].split(",")[0], "global")
            self.getVariableByName(key, "bank1").system=True
            if d[key].split(",")[1].replace(" ","").replace("\t", "") == "non-iter":
                self.getVariableByName(key, "bank1").iterable = False

    def addArray(self, name):
        self.arrays[name] = {}

    def removeArray(self, name):
        self.arrays.pop(name)

    def addItemsToArray(self, name, itemname, var):
        self.arrays[name][itemname] = var

    def removeItemFromArray(self, name, item):
        self.arrays[name].pop(item)

    def checkForDeadReferences(self, name):
        for array in self.arrays.keys():
            if name in self.arrays[array]:
                self.arrays[array].pop(name)
        if self.__loader.frames["ArrayFrame"].arrName.getEntry()!="":
            self.__loader.frames["ArrayFrame"].fillListBoxes()

    def getAddressOnVariableIsStored(self, name, bank):
        section="local_variables"
        if bank == "bank1":
            section = "global_variables"

        for address in self.memory.keys():
            for id in self.memory[address].variables.keys():
                #print(id, name)
                if name == id:
                    return(address)
        return(False)

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
                    self.checkForDeadReferences(name)
                    return(True)
                else:
                    if self.memory[address].variables[name].validity == validity:
                        self.memory[address].addBitsToBankAddress(self.memory[address].variables[name].usedBits, validity)
                        self.memory[address].variables.pop(name)
                        self.checkForDeadReferences(name)
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

        for i in range(128, 248):
            self.memory["$"+self.getHex(i)] = MemoryItem()
        for i in range(0,128):
            I = self.getHex(i)
            if len(I)==1:
                I = "0"+I

            self.memory["$F0"+I] = MemoryItem()
        self.addSystemMemory()


    def getHex(self, i):
        return(hex(i)[2:])

    def getSARAReadAddressFromWriteAddress(self, num):
        num = "$F0"+hex(int(num[3:], 16)+128)[2:]

        return(num)

    def getSARAWriteAddressFromReadAddress(self, num):
        num = "$F0"+hex(int(num[3:], 16)+128)[2:]

        return(num)

    def setLocksAfterLoading(self):
        lines = self.codes["bank1"]["bank_configurations"].code.split("\n")
        for line in lines:
            if line.startswith("*"):
                continue
            else:
                if line.split("=")[0] == "bank1":
                    self.kernel = line.split("=")[1].replace("\n","").replace("\r","")
                else:
                    from Lock import Lock
                    self.locks[line.split("=")[0]] = Lock(line.split("=")[1].replace("\n","").replace("\r",""))

    def createTheBankConfigFromMemory(self):
        text = []
        text.append("*** This is where you set the details of banks such as name, role, and so on.")
        text.append(str("bank1="+self.kernel))
        for bank in self.locks.keys():
            if self.locks[bank]!=None:
                text.append(bank+f"={self.locks[bank].name},{self.locks[bank].type},{str(self.locks[bank].number)}")

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
        validate = "global"
        if bank != "bank1":
            validate = bank

        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                if self.memory[address].variables[variable].validity != validate:
                    continue
                string += variable + "=" + self.memory[address].variables[variable].type + os.linesep

        for array in self.arrays.keys():
            if self.getArrayValidity(array) == validate:
                string+=array + "=array(" + ",".join(list(self.arrays[array].keys()))+")"+os.linesep
        #print(string)
        self.codes[bank][section].code = string

    def getArrayValidity(self,arrayname):
        try:
            arrayKeyList = list(self.arrays[arrayname].keys())

            for num in range(0, len(arrayKeyList)):
                name = list(self.arrays[arrayname].keys())[num]
                for address in self.memory.keys():
                    for variable in self.memory[address].variables.keys():
                        #print(variable, name)
                        if variable == name and self.memory[address].variables[variable].validity!="global":
                            return(self.memory[address].variables[variable].validity)
        except:
            pass
        return("global")

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

    def getBanksAvailableForLocking(self):
        this = []
        for num in range(3, 9):
            bankNum = "bank" + str(num)
            if self.locks[bankNum] == None:
                this.append(num)

        return(this)

    def registerNewLock(self, bankNum, name, type, number, last):
        from Lock import Lock

        bankNum = "bank" + str(bankNum)

        if self.locks[bankNum] == None:
            if last == "LAST":
                self.locks[bankNum] = Lock(name+","+type+","+str(number)+",LAST")
            else:
                self.locks[bankNum] = Lock(name+","+type+","+str(number))
            return(True)
        else:
            return(False)