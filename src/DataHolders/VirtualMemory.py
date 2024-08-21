from DataItem import DataItem
import os
from MemoryItem import MemoryItem
from copy import deepcopy
from ObjectMaster import ObjectMaster

class VirtualMemory:

    def __init__(self, loader):

        self.__loader = loader
        self.codes = {}
        self.locks = {}
        self.subs = {}
        self.bankLinks = {}
        self.kernel_types = []
        self.kernel = "common"
        self.changedCodes = {}
        self.objectMaster = ObjectMaster(loader)
        self.excludeForBank1Routines = ["temp18", "temp19"]
        self.includeJukeBox    = True
        self.includeKernelData = True
        self.includeCollisions = True
        self.firstAddress = 0x96
        self.lastAddress  = self.firstAddress
        self.stactStart   = 0xf8

        self.__kernelOnlyVars = {}

        self.registers = {}
        txt = self.__loader.io.loadWholeText("templates/6507Registers_Editor.a26").split("\n")
        for line in txt:
            key                 = line.split("=")[0]
            self.registers[key] = {}
            valueList           = line.split("=")[1].split(",")

            self.registers[key]["allowedIO"]       = valueList[0]
            if valueList[0] == "-":
               self.registers[key]["allowedSections"] = []
            else:
               if valueList[1] == "[]":
                  self.registers[key]["allowedSections"] = self.__loader.sections
               else:
                  self.registers[key]["allowedSections"] = []
                  datas = valueList[1][1:-1]
                  if datas[0] == "!":
                     datas[1:] = datas.split(" ")
                     for s in self.__loader.sections:
                         if s not in datas:
                            self.registers[key]["allowedSections"].append(s)
                  else:
                     datas     = datas.split(" ")
                     for d in datas:
                         self.registers[key]["allowedSections"].append(d)

            self.registers[key]["bitMask"]       = valueList[2]
            if valueList[3] == "True":
               self.registers[key]["colorVar"]   = True
            else:
               self.registers[key]["colorVar"]   = False

        for root, dirs, files in os.walk("templates/skeletons/"):
            for file in files:
                if "main_kernel" in file:
                    self.kernel_types.append(file.replace("_main_kernel.asm", ""))

        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.locks[bankNum] = None
            self.codes[bankNum] = {}
            self.changedCodes[bankNum] = {}
            if (num == 1):
                #self.codes[bankNum]["bank_configurations"] = DataItem()
                #self.codes[bankNum]["global_variables"] = DataItem()

                #self.changedCodes[bankNum]["bank_configurations"] = False
                #self.changedCodes[bankNum]["global_variables"] = False

                for section in self.__loader.bank1Sections:
                    self.codes[bankNum][section] = DataItem()
                    self.changedCodes[bankNum][section] = False

            else:
                for section in self.__loader.sections:
                    self.codes[bankNum][section] = DataItem()
                    self.changedCodes[bankNum][section] = False

        self.types = {
            "bit": 1,
            "doubleBit": 2,
            "tripleBit": 3,
            "nibble": 4,
            "byte": 8
        }

        self.__portStates = {}
        txt = self.__loader.io.loadWholeText("templates/portStates.csv")

        for line in txt.split("\n")[1:]:
            if line == "": continue
            line = line.split(";")
            self.__portStates[line[0]]          = {}
            self.__portStates[line[0]]["alias"] = line[1][1:-1].split(" ")
            self.__portStates[line[0]]["code"]  = line[2]
            self.__portStates[line[0]]["code"]  = self.__portStates[line[0]]["code"].replace(r"\n", "\n").replace(r"\t", "\t")


        #for key in self.__portStates:
            #print(">>"+key+"<<", "\n", self.__portStates[key]["code"])
            #if "col " in key or "col " in self.__portStates[key]["alias"] or "collision " in key or "collision " in self.__portStates[key]["alias"]: print("fucked " + key)

        self.resetMemory()
        self.emptyArchieved()

    def returnAllPortStatesAsList(self):
        listToReturn = []

        for key in self.__portStates.keys():
            listToReturn.append(key)
            #if key == "" or key == " " : print("1", key)
            for k in self.__portStates[key]["alias"]:
                #if "k" == " " or k == "": print("2", key)
                listToReturn.append(k)

        return listToReturn

    def returnCodeOfPortState(self, nameOrAlias):
        name = ""

        if nameOrAlias in self.__portStates.keys():
           name = nameOrAlias
        else:
           for key in self.__portStates.keys():
               if nameOrAlias in self.__portStates[key]["alias"]:
                  name = key
                  break

        if name == "":
           return False
        else:
           return self.__portStates[name]["code"]

    def archieve(self):
        self.archieved = self.archieved[:self.cursor+1]

        self.archieved.append(
            {
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

    def generateMemoryAllocationForAssembler(self, validity):
        text = ""
        already = self.getKernelsPreSetVars()

        for address in self.memory.keys():
            for name in self.memory[address].variables:
                if self.memory[address].variables[name].validity == validity and\
                 ( self.memory[address].variables[name].system   == False or name not in already ):
                   text += name + " = " + address + "\n"
        return(text)

    def getMemoryPartOfKernelOnly(self, kernel, element):
        txt   = ""
        first = self.firstAddress
        for item in [[self.includeKernelData, "sysVars"], [self.includeJukeBox, "musicVars"], [self.includeCollisions, "collVars"]]:
           if item[0]:
              subTXT = open("templates/skeletons/"+kernel+"_"+element+"_" + item[1] + ".asm", "r").read()
              first, subTXT  = self.replaceMemoryAddressesAndSetFirst(first, subTXT)
              txt += subTXT

        return txt

    def replaceMemoryAddressesAndSetFirst(self, first, txt):
        txt     = txt.split("\n")
        lastOne = ""

        for lineNum in range(0, len(txt)):
            line = txt[lineNum]

            if   "#L#" in line:
                  line    = line.replace("#L#", lastOne)
            elif "#1#" in line or "#2#" in line:
                  lastOne = hex(first).replace("0x", "")

                  if "#2#" in line:
                      first += 2
                      line    = line.replace("#2#", lastOne)
                  else:
                      first += 1
                      line    = line.replace("#1#", lastOne)

            txt[lineNum] = line

        #print("\n".join(txt))
        self.lastAddress = first

        return first, "\n".join(txt)

    def getKernelsPreSetVars(self):
        import re

        txt = self.getMemoryPartOfKernelOnly(self.kernel, "main_kernel")
        vars = re.findall(r'.+\s\=\s\$[0-9a-fA-F]{2}', txt)

        forReturn = []
        for item in vars:
            forReturn.append(item.split(" ")[0])

        return(forReturn)

    """
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

    """
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

        self.__loader.bigFrame.loadCurrentFromMemory()

    def isSara(self, name):
        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                if variable == name:
                   if len(address) > 3:
                       return True
                   else:
                       return False
        return False

    def emptyArchieved(self):
        self.cursor = 0
        self.archieved = []

        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.changedCodes[bankNum] = {}
            if (num == 1):
                #self.changedCodes[bankNum]["bank_configurations"] = False
                #self.changedCodes[bankNum]["global_variables"] = False
                for section in self.__loader.bank1Sections:
                    self.changedCodes["bank1"][section] = False
            else:
                for section in self.__loader.sections:
                    self.changedCodes[bankNum][section] = False

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


                    string +="------------------------------"+os.linesep
            for array in self.arrays.keys():
                string += array + ": " +self.getArrayValidity(array)+", "+ str(list(self.arrays[array].keys()))+os.linesep
            if len(self.arrays.keys())>0:
                string += "------------------------------" + os.linesep

            self.__loader.logger.addToLog(string)


    def addSystemMemory(self):
        datas = []
        if self.includeKernelData:
           datas.append(self.__loader.dataReader.readDataFile("templates"+os.sep+self.kernel+"_system_variables.a26"))
        else:
           datas.append(self.__loader.dataReader.readDataFile("templates" + os.sep + "empty_system_variables.a26"))

        if self.includeJukeBox:
           datas.append(self.__loader.dataReader.readDataFile("templates" + os.sep + "jukeBox_system_variables.a26"))

        if self.includeCollisions:
           datas.append(self.__loader.dataReader.readDataFile("templates" + os.sep + "collisions_system_variables.a26"))

        for d in datas:
            for key in d:
                #print(key, d[key])
                self.addVariable(key, d[key].split(",")[0], "global", False, False, False, False, False)
                self.getVariableByName(key, "bank1").system=True
                if d[key].split(",")[1].replace(" ","").replace("\t", "") == "non-iter":
                    self.getVariableByName(key, "bank1").iterable = False
                if d[key].split(",")[2].replace(" ","").replace("\t", "") == "non-link":
                    self.getVariableByName(key, "bank1").linkable = False
                if d[key].split(",")[3].replace(" ","").replace("\t", "") == "BCD":
                    self.getVariableByName(key, "bank1").bcd = True
                if d[key].split(",")[4].replace(" ","").replace("\t", "") == "colorVar":
                    self.getVariableByName(key, "bank1").colorVar = True

        self.__kernelOnlyVars = {}
        kernelCode = self.getMemoryPartOfKernelOnly(self.kernel, "main_kernel").split('\n')

        for line in kernelCode:
            line = line.split(";")[0].strip().split(" = ")
            if len(line) > 1:
                var = line[0]
                val = line[1]
                if "$" in val:
                    found = False
                    for d in datas:
                        if var in d.keys():
                           found = True
                           break

                    if found == False:
                       self.__kernelOnlyVars[var] = val.upper()
                       #print(var, val.upper())

    def addArray(self, name):
        #self.archieve()
        self.arrays[name] = {}

    def removeArray(self, name):
        #self.archieve()
        self.arrays.pop(name)

    def addItemsToArray(self, name, itemname, var):
        #self.archieve()
        self.arrays[name][itemname] = var

    def removeItemFromArray(self, name, item):
        #self.archieve()
        self.arrays[name].pop(item)

    def checkForDeadReferences(self, name):
        for array in self.arrays.keys():
            if name in self.arrays[array]:
                self.arrays[array].pop(name)



    def getAddressOnVariableIsStored(self, name, bank):
        section="local_variables"
        if bank == "bank1":
            section = "global_variables"

        for address in self.memory.keys():
            for id in self.memory[address].variables.keys():
                #print(id, name)
                if name == id:
                    return(address)

        for var in self.__kernelOnlyVars:
            if var == name:
               return self.__kernelOnlyVars[var]

        return(False)

    def getVariableByName(self, name, bank):
        if name in self.registers:
           return self.convertRegisterToVariable(name)

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


    def addVariable(self, name, type, validity, color, bcd, allocType, allocAddress, allocBits):
        neededBits = self.types[type]
        success = False

        if allocType == False:
           for memoryAddress in self.memory.keys():
                if len(self.memory[memoryAddress].freeBits[validity]) >= neededBits:
                    #bits = self.getIfThereAreAvaiableBitNearAndInARow(self.memory[memoryAddress].freeBits[validity], neededBits)
                    bits = self.getTheFirstFreeBitsOnAddessAndBank(validity, neededBits, memoryAddress)
                    if bits == False:
                        continue
                    else:
                        if validity == "global":
                            self.memory[memoryAddress].removeBitsFromGlobalAddress(bits)
                        else:
                            self.memory[memoryAddress].removeBitsFromBankAddress(bits, validity)
                        self.memory[memoryAddress].addVariable(name, type, bits, validity, color, bcd, False, False)
                        #print(name, memoryAddress, type, validity)

                        success = True
                        break
        else:
            self.memory[allocAddress].addVariable(name, type, allocBits, validity, color, bcd, True, allocAddress)
            success = True

        return(success)
            #print(memoryAddress)

    def getTheFirstFreeBitsOnAddessAndBank(self, validity, numOfBits, address):
        if type(numOfBits) != int: numOfBits = self.types[numOfBits]

        listOfBits = []

        availableBits = deepcopy(self.memory[address].freeBits[validity])

        if len(availableBits) < numOfBits:
           #if address.upper() == "$DE":
           #   for varName in self.memory[address].variables.keys():
           #       print(address, varName, validity)

           return False

        for bitNum in availableBits:
            if len(listOfBits) == 0:
                listOfBits.append(bitNum)
            else:
                if bitNum - listOfBits[-1] == 1:
                    listOfBits.append(bitNum)
                else:
                    listOfBits = [bitNum]

            if len(listOfBits) == numOfBits:
               #for varName in self.memory[address].variables.keys():
               #    print(address, varName, validity)

               #print(address, validity)

               return (listOfBits)

        return False


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

        for i in range(128, self.stactStart):
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
        num = "$F0"+hex(int(num[3:], 16)-128)[2:]

        return(num)

    def getVariableByName2(self, name):
        if name in self.registers:
           return self.convertRegisterToVariable(name)

        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                if variable == name:
                    return self.memory[address].variables[variable]
        return False

    def convertRegisterToVariable(self, name):
        from Variable import Variable

        register = self.registers[name]

        if  register["allowedIO"] in ["r", "-"]:
            iter = False
        else:
            iter = True

        if  register["allowedIO"] == "-":
            link = False
        else:
            link = True

        mask     = register["bitMask"]
        firstOne = -1
        lastOne  = -1

        bits = []

        reversed = mask[::-1]
        for num in range(0, 8):
            if reversed[num] == "1":
               if firstOne == -1:
                  firstOne = num
               lastOne = num
               bits.append(num)

        length = lastOne - firstOne + 1
        typ = "other"

        for t in self.types.keys():
            if length == self.types[t]:
               typ = t
               break

        var = Variable(typ, bits, "global", register["colorVar"], False)

        var.system   = True
        var.iterable = iter
        var.linkable = link
        var.register = True

        return var

    def setLocksAfterLoading(self):
        lines = self.codes["bank1"]["bank_configurations"].code.split("\n")
        for line in lines:
            if line.startswith("*"):
                continue
            else:
                if line.split("=")[0] == "bank1":
                    self.kernel = line.split("=")[1].replace("\n","").replace("\r","").split(",")[0]
                else:
                    from Lock import Lock
                    self.locks[line.split("=")[0]] = Lock(line.split("=")[1].replace("\n","").replace("\r",""))

    def createTheBankConfigFromMemory(self):
        text = []
        text.append("*** This is where you set the details of banks such as name, role, and so on.")
        text.append(str("bank1=" + self.kernel + "," + str(self.includeKernelData), + "," + str(self.includeJukeBox) + "," + str(self.includeCollisions)))
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

                if data[1].upper().startswith("ARRAY") == False:
                    if self.checkIfExists(name, validity):
                        continue

                    subData = data[1].replace("\n","").replace("\r","").split(",")
                    TYPE    = subData[0]
                    color   = subData[1]
                    bcd     = subData[2]

                    if color == "color":
                       color = True
                    else:
                       color = False

                    if bcd == "BCD":
                       bcd = True
                    else:
                       bcd = False

                    allocType    = subData[3]
                    allocAddress = subData[4]
                    allocBits    = subData[5]

                    if allocType == "static":
                       allocType = True
                       allocBits = allocBits.split("|")
                    else:
                       allocType    = False
                       allocAddress = False
                       allocBits    = []

                    if (TYPE in self.types.keys()):
                        self.addVariable(name, TYPE, validity, color, bcd, allocType, allocAddress, allocBits)
                    else:
                        self.addArray(name)
                        data = TYPE[6:-1].split(",")
                        for item in data:
                            self.addItemsToArray(name, item, self.getVariableByName(item, bank))
                else:
                    self.addArray(name)
                    data = data[1][6:-1].split(",")
                    for item in data:
                        self.addItemsToArray(name, item, self.getVariableByName(item, bank))

            except Exception as e:
                #print(str(e))
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

                color      = "non-Color"
                bcd        = "binary"
                fixedAlloc = ["dynamic", "False", "False"]

                if self.memory[address].variables[variable].color      == True: color = "Color"
                if self.memory[address].variables[variable].bcd        == True: bcd   = "BCD"
                if self.memory[address].variables[variable].fixedAlloc == True:
                   fixedAlloc = ["static", address, "|".join(self.memory[address].variables[variable].usedBits)]

                string += variable + "=" + self.memory[address].variables[variable].type + "," +\
                          color    + "," + bcd + "," + ",".join(fixedAlloc) + os.linesep

        for array in self.arrays.keys():
            if self.getArrayValidity(array) == validate:
                string+=array + "=array(" + ",".join(list(self.arrays[array].keys()))+")"+os.linesep
        print(string)
        self.codes[bank][section].code = string
        self.changedCodes[bank][section] = True

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

    def returnBankLocks(self):
        this = {}
        for num in range(3, 9):
            bankNum = "bank" + str(num)
            if self.locks[bankNum] != None:
                this[bankNum] = self.locks[bankNum]

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

    def returnVariablesForBank(self, bankNum):
        readOnly  = []
        writatble = []
        all       = []
        nonSystem = []

        if type(bankNum) == int:
           bankNum = "bank" + str(bankNum)

        for address in self.memory.keys():
            for variable in self.memory[address].variables.keys():
                var = self.memory[address].variables[variable]

                if  (var.validity == "global" or
                     var.validity == bankNum):
                     all.append(variable)
                     if var.system == False and (bankNum != "bank1" or (variable not in self.excludeForBank1Routines)):
                        nonSystem.append(variable)
                        writatble.append(variable)
                     elif var.iterable == True and (bankNum != "bank1" or (variable not in self.excludeForBank1Routines)):
                        writatble.append(variable)
                     elif var.linkable == True:
                        readOnly.append(variable)


        for var in self.__kernelOnlyVars.keys():
            if var not in all:
               all.append(var)
               readOnly.append(var)

        return writatble, readOnly, all, nonSystem

    def returnArraysOnValidity(self, bank):
        all = []
        writable = []
        readonly = []

        if type(bank) == int: bank = "bank" + str(bank)

        for array in self.arrays.keys():
            if self.getArrayValidity(array) in (bank, "global"):
                all.append(array)
                if self.hasArrayReadOnly(array) == True:
                   readonly.append(array)
                else:
                   writable.append(array)


                """
                readonlyTempVar = []
                writableTempVar = []

                for variable in self.arrays[array]:
                    for address in self.memory.keys():
                        if variable in self.memory[address].variables.keys():
                            var = self.memory[address].variables[variable]
                            if var.system == False or var.iterable == True:
                                all.append(variable)
                                writableTempVar.append(variable)
                            elif var.linkable == True:
                                all.append(variable)
                                readonlyTempVar.append(variable)
                if len(readonlyTempVar) > 0:
                   readonly.append(array)
                else:
                    writable.append(array)
                """

        return writable, readonly, all

    def hasArrayReadOnly(self, array):
        for variable in self.arrays[array]:
            for address in self.memory.keys():
                if variable in self.memory[address].variables.keys():
                    var = self.memory[address].variables[variable]
                    if var.iterable == False:
                       return True
        return False