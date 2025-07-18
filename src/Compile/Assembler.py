from DataLine import DataLine
from threading import Thread
import os
import re
from copy import deepcopy

class Assembler():

    def __init__(self, __loader, projectPath, testIt, tv, deleteSrc):
        self.projectPath = projectPath
        self.__tv = tv
        self.__loader = __loader

        self.__testIt = testIt

        self.compile(projectPath+"source.asm")

        for num in self.freeBytes:
            if self.freeBytes[num] < 0:
                self.__testIt = False
                break

        if self.__testIt == True:
            path = "emulator/32-bit/Stella.exe"
            if __loader.config.getOSbits() == "64bit":
                path.replace("32", "64")

            s = Thread(target=self.runStella, args=[path])
            s.daemon = True
            s.start()

        if deleteSrc == True:
            os.remove(self.projectPath + "source.asm")

    def runStella(self, path):
        #self.__tv = "pal"
        command = os.getcwd() + os.sep+path + ' "' +  os.getcwd() + os.sep + self.executeName +  '"'
        #print(command)

        os.popen(command)

    def normalize(self, text):
        new = []

        text = text.split("\n")
        for line in text:
            if ";" in line:
                line = line.split(";", 2)[0]
            elif "!" in line:
                line = line.split("!", 2)[0]

            if ((len(re.findall(r"[a-zA-Z]", line)) == 0)
                or (line.startswith("#") or line.startswith("*"))
            ):
                continue
            line = re.sub(r"\s+", " ", line)
            line = re.sub(r"\t+", " ", line)

            new.append(line)

        return("\n".join(new))

    def collectVariables(self, text):
        variables = {}

        text = text.split("\n")
        for line in text:
            if line.startswith(" ") or ("=" not in line):
                continue
            line = line.replace(" ", "")
            variables[line.split("=")[0]] = line.split("=")[1]

        return(variables)

    def sleepToCode(self, text):
        new = []
        text = text.split("\n")
        for line in text:
            if "sleep" not in line:
                new.append(line)
                continue

            number = int(line.split("sleep", 1)[1].replace(" ", ""))
            if (number%2==0):
                new.append(" NOP\n"*int(number/2))
            else:
                #new.append(" NOP\n"*int((number/2)-1)+" JMP *+3\n")
                new.append(" NOP\n" * int((number / 2) - 1) + " BIT VBLANK\n")

        return("\n".join(new))


    def compactSleep(self, text):
        counter = 0

        template = (" LDA #XXX\n"+
                    "LoopFuck666\n"+
                    " SBC #1\n"+
                    " BCS LoopFuck666\n")

        new = []
        text = text.split("\n")

        for line in text:
            if "_sleep" not in line:
                new.append(line)
                continue



            number = int(line.split("_sleep", 1)[1].replace(" ", ""))

            if (number<14) or (number-2)%4 != 0:
                new.append("\tsleep\t"+str(number))
                #print(str(number))
                continue


            xxx = (number - 2)//4-1
            new.append(template.replace("666", str(counter)).replace("XXX", str(xxx)))
            #print(template.replace("666", str(counter)).replace("XXX", str(xxx)))
            counter+=1

        return ("\n".join(new))

    def setup(self, line, upper):

        if upper == True:
            copied = line.upper()
        else:
            copied = line
        if "," in copied:
            copied = copied.split(",")[0]
        copied = copied.replace("(", "").replace(")", "").replace(" ", "").replace("$", "")
        return(copied)

    def getSectionNames(self, code):
        sections = {}

        for line in code:
            if (len(re.findall(r"[a-zA-Z]", line)) == 0) or ("=" in line):
                continue
            elif ("#<" in line) or ("#>" in line):
                continue

            if line.startswith(" ") == False:
                sections[line.replace(" ", "")] = None

        return (sections)

    def changeOnesWithHashTag(self, variables, code):
        for key in variables:
            if variables[key][0] == "#":
               code = code.replace(key, variables[key])
               print(key)
        return code

    def createSquence(self, code, opcodes, variables, registers):

        code = code.split("\n")

        branchers = ["BCC", "BCS", "BEQ", "BNE", "BMI", "BPL", "BVC", "BVS"]

        sections = self.getSectionNames(code)
        codeLines = []
        freebytes = {}
        currentBank = 1
        errorMessageId = 0

        currentSEQNumber = 1
        currentAddress = 4096

        threeByters = []

        for r in registers:
            if len(r)>3:
                threeByters.append(registers[r])

        for v in variables:
            if len(variables[v])>3:
                threeByters.append(v)

        #print(threeByters)
        #print(variables)
        code = self.checkForTooDistant(code, branchers)

        for line in code:
            while line.endswith(" "):
                line = line[:-1]

            if (len(re.findall(r"[a-zA-Z]", line)) == 0) or ("=" in line):
                continue

            if line.startswith(" ") == False:
                sections[line.replace(" ", "")] = "$"+hex(currentAddress)[2:]
            else:

                line = line.split(" ")
                new = []
                for item in line:
                    if item != "":
                        new.append(item)

                line = new
                if line[0].upper()=="ALIGN":
                    try:
                        t = int(line[1])
                    except:
                        line[1] = "256"

                    while(currentAddress%int(line[1])>0):
                        codeLines.append(DataLine())
                        current = codeLines[-1]
                        current.address = currentAddress
                        currentAddress+=1
                        current.seq = currentSEQNumber
                        currentSEQNumber+=1
                        current.raw = deepcopy(line)
                        current.bytes.append(bytes([0]))

                elif line[0].upper()== "_ALIGN":
                    try:
                        t = int(line[1])
                    except:
                        line[1] = "256"

                    temp = hex(currentAddress).replace("0x", "")
                    while len(temp) < 4:
                        temp = "0" + temp

                    lastTwo = temp[-2:]

                    if int(lastTwo, 16) + int(line[1]) > 255:
                        while (currentAddress % 256 > 0):
                            codeLines.append(DataLine())
                            current = codeLines[-1]
                            current.address = currentAddress
                            currentAddress += 1
                            current.seq = currentSEQNumber
                            currentSEQNumber += 1
                            current.raw = deepcopy(line)
                            current.bytes.append(bytes([0]))

                elif line[0].upper()=="FILL":
                    counter = int(line[1])
                    while(counter>0):
                        codeLines.append(DataLine())
                        current = codeLines[-1]
                        current.address = currentAddress
                        currentAddress+=1
                        current.seq = currentSEQNumber
                        currentSEQNumber+=1
                        current.raw = deepcopy(line)
                        current.bytes.append(bytes([0]))
                        counter -= 1


                elif line[0].upper() == "REWIND":
                    border=int("0x"+line[1], 16)
                    while(currentAddress<border):
                        codeLines.append(DataLine())
                        current = codeLines[-1]
                        current.address = currentAddress
                        currentAddress += 1
                        current.seq = currentSEQNumber
                        currentSEQNumber += 1
                        current.raw = deepcopy(line)
                        current.bytes.append(bytes([0]))

                elif line[0].upper() == "saveFreeBytes".upper():
                    freebytes[currentBank] = 4096 - currentAddress%4096

                elif line[0].upper() == "BANK":

                    currentBank = int(line[1])
                    currentAddress = currentBank * 4096

                elif "BYTE" in line[0].upper():
                    codeLines.append(DataLine())
                    current = codeLines[-1]
                    current.address = currentAddress
                    currentAddress += 1
                    current.seq = currentSEQNumber
                    currentSEQNumber += 1
                    current.raw = deepcopy(line)

                else:
                    codeLines.append(DataLine())
                    current = codeLines[-1]
                    current.raw = deepcopy(line)
                    current.address = currentAddress

                    if len(line)==1:
                        currentAddress += 1
                    elif line[0].upper() in branchers:
                        currentAddress += 2
                        current.byteNum = 2
                    else:
                        line[1] = line[1].replace("*", str(currentAddress))
                        currentAddress += 2
                        current.byteNum = 2

                        thisIsAForcedConstant = False
                        try:
                            if variables[line[1]][0] == "#": thisIsAForcedConstant = True
                        except:
                            pass

                        if ("#" not in line[1]) and (line[1].split(",")[0].split("+")[0] in list(sections.keys()) or
                           (len(re.findall(r'[a-fA-F0-9]{4}', line[1])) > 0 and line[1] not in variables) or
                            line[1] in threeByters
                        ) and (thisIsAForcedConstant == False):
                            currentAddress += 1
                            current.byteNum = 3

                        if line[1].split(",")[0] in variables and thisIsAForcedConstant == False and current.byteNum == 2:
                           vName = line[1].split(",")[0]
                           if vName in variables:
                              if variables[vName].startswith("$"):
                                 if len(variables[vName][1:]) == 4:
                                    currentAddress += 1
                                    current.byteNum = 3

                        if "JMP" in line[0].upper() and "(" in line[1]:
                            currentAddress += 1
                            current.byteNum = 3

                    """
                    try:
                        print(line[1], current.byteNum)
                    except:
                        pass
                    """
                    current.seq = currentSEQNumber
                    currentSEQNumber += 1

        for line in codeLines:
            counter = 0
            second = ""

            if line.bytes != []:
                continue

            elif "BYTE" in line.raw[0].upper():

                try:
                    num = line.raw[1].replace("#", "")
                    if "%" in num:
                        num = int("0b" + num.replace("%", ""), 2)
                    elif "$" in num:
                        num = int("0x" + num.replace("$", ""), 16)
                    else:
                        num = int(num, 10)
                    line.bytes.append(bytes([num]))
                except Exception as e:
                    # print(line.raw[1])
                    second = self.checkIfSectionName(line.raw[1], sections)
                    second = self.starToAddress(currentAddress, second)
                    second = self.secondByteToNumeric(second, variables, registers, sections)
                    second = self.checkSARA(second)
                    second = self.doTheMath(second)
                    second = self.lowHighNibble(second)
                    if "#$" in second:
                        line.bytes.append(bytes([int(second.replace("#$", "0x"), 16)]))
                    elif "#%" in second:
                        line.bytes.append(bytes([int(second.replace("#%", "0b"), 2)]))
                    else:
                        line.bytes.append(bytes([int(second.replace("#", ""), 10)]))

                continue

            for c in opcodes.keys():
                counter += 1

                # Fix nullpage jump for Memory-based indirect jump
                if c == "$6C" and line.raw[0].upper() == "JMP" and "(" in line.raw[1] and \
                    len(re.findall(r"\$[0-9a-fA-F]{4}", line.raw[1])) == 0:

                   new = self.secondByteToNumeric(line.raw[1], variables, registers, sections)
                   line.raw[1]  = "("+"$00"+ new[2:4]+")"
                   self.createBytes(line, c, line.raw[1])
                   break


                if (line.byteNum == opcodes[c]["bytes"] and (opcodes[c]["opcode"] == line.raw[0].upper())):
                    #if len(line.raw) > 1:
                    #    if line.raw[1] == "PressedDelay": print(line.byteNum, opcodes[c]["opcode"])

                    if (line.byteNum == 1):
                        c = bytes([int(c.replace("$", "0x"), 16)])
                        line.bytes.append(c)
                        break

                    elif line.raw[0].upper() in branchers:
                        c = bytes([int(c.replace("$", "0x"), 16)])
                        line.bytes.append(c)
                        #print(line.raw)

                        second = self.checkIfSectionName(line.raw[1], sections)
                        second = self.starToAddress(line.address, second)
                        second = self.secondByteToNumeric(second, variables, registers, sections)
                        second = self.checkSARA(second)
                        second = self.doTheMath(second)
                        second = int(second.replace("$", "0x"), 16)

                        number = (second-line.address)-2
                        if (number<0):
                            number = 256 + number

                        line.bytes.append(bytes([number]))
                        break


                    else:
                        #print(line.raw)
                        second = self.checkIfSectionName(line.raw[1], sections)
                        second = self.starToAddress(line.address, second)
                        second = self.secondByteToNumeric(second, variables, registers, sections)
                        second = self.checkSARA(second)
                        second = self.doTheMath(second)
                        second = self.lowHighNibble(second)

                        if len(re.findall(r"\$[a-fA-F0-9]{4}", second))>0:
                            num = int("0x"+second[1], 16)
                            if num > 0 and num<9:
                                second = ("$"+hex(((num-1)*2)+1)+second[2:]).replace("0x", "")

                        if second.startswith("#") and opcodes[c]["format"] == "#aa":
                            self.createBytes(line, c, second)
                            break
                        else:

                            template = re.sub(r'[0-9a-fA-F]', "a", second.lower().replace("$", ""))

                            #if "ScreenJumpTable" in line.raw[1]:
                            #    print(line.raw, second, opcodes[c]["format"], line.byteNum)

                            if template.count("a")==1 or template.count("a")==3:
                                template = "a" + template

                            #print(second, template, template.upper(), opcodes[c]["format"].upper(), c)


                            if (line.raw[0].upper() == opcodes[c]["opcode"].upper() and template.upper() == opcodes[c]["format"].upper()):
                                self.createBytes(line, c, second)
                                break



        return(freebytes, codeLines, sections)

    def checkSARA(self, code):
        if ("LDA" not in code.upper()) and ("STA" not in code.upper()):
            return(code)
        elif "LDA" in code.upper():
            opcode = "LDA"
        else:
            opcode = "STA"

        number = re.findall(r"\$[a-fA-F0-9]{4}", code)[0].upper()
        number = int(number.replace("$", "0x"), 16)
        if number < 61440 or number > 61695:
            return (code)

        if opcode == "LDA" and number < 61568:
            number+=128
        elif opcode == "STA" and number > 61567:
            number-=128

        number = hex(number).replace("0x", "$")
        sendBack = "\t"+opcode+"\t"+number

        if "," in code:
            sendBack += ","+code.split(",")[1]

        return(sendBack)


    def checkForTooDistant(self, code, branchers):
        sections = {}

        num = 0
        for line in code:
            while line.endswith(" "):
                line = line[:-1]
            if line.startswith(" ") == False:
                sections[line] = num
            num += 1

        newCode = []
        num = 0
        for line in code:
            while line.endswith(" "):
                line = line[:-1]
            if line.startswith(" ") == True:
                splittedLine = line.split(" ")

                new = []
                for item in splittedLine:
                    if item != "":
                        new.append(item)

                splittedLine = new
                if splittedLine[0] in branchers:
                    try:
                        dif = (abs(num - sections[splittedLine[1]]))
                    except:
                        if "*" in splittedLine[1]:
                            dif = 1
                    if (dif > 40):
                        number = branchers.index(splittedLine[0])

                        if number % 2 == 0:
                            number += 1
                        else:
                            number -= 1


                        newCode.append(f" {branchers[number]} *+5")
                        newCode.append(f" JMP {splittedLine[1]}")
                        num += 1
                        for sec in sections:
                            if sections[sec]>num:
                                sections[sec]+=1

                    else:
                        newCode.append(line)
                else:
                    newCode.append(line)
            else:
                newCode.append(line)
            num += 1

        return(newCode)

    def starToAddress(self, address, second):
        return(second.replace("*", hex(address).replace("0x", "$")))

    def checkIfSectionName(self, name, sections):
        word = name.replace("#","").replace("<","").replace(">","").replace(" ", "")
        if word in sections:
            return(name.replace(word, sections[word]))
        else:
            return(name)


    def createBytes(self, line, c, second):
        c = bytes([int(c.replace("$", "0x"), 16)])
        line.bytes.append(c)

        if "," in second:
            second = second.split(",")[0]

        second = second.replace("#", "").replace("(", "").replace(")","")
        if second.startswith("%"):
            self.appendBytes(line, second.replace("%", "0b"))
        elif second.startswith("$"):
            second = second.replace("$", "")
            if len(second)==2:
                self.appendBytes(line, "0x"+second)
            else:
                self.appendBytes(line, "0x"+second[2:])
                self.appendBytes(line, "0x"+second[:2])

        else:
            self.appendBytes(line, second)

    def appendBytes(self, line, second):
        if second.startswith("0b"):
            line.bytes.append(bytes([int(second, 2)]))
        elif second.startswith("0x"):
            line.bytes.append(bytes([int(second, 16)]))
        else:
            #print(line, second)
            line.bytes.append(bytes([int(second, 10)]))

    def doTheMath(self, raw):
        if ("+" not in raw) and ("-" not in raw):
            return(raw)

        isItMath = False
        for charNum in range(0, len(raw)):
            if raw[charNum] == "+" or raw[charNum] == "-":
                try:
                    test = int(raw[charNum+1])
                    isItMath = True
                    break
                except:
                    continue

        if isItMath == False:
            return(raw)

        num = re.findall(r'[+|-]\d+', raw)[0]
        if "$" in raw:
            base = re.findall(r'\$[a-fA-f0-9]+', raw)[0]

            baseNumber = int(base.replace("$", "0x"), 16)

            newNum = hex(baseNumber+int(num)).replace("0x", "$")
            raw = raw.replace(base, newNum).replace(num, "")
        else:
            print(raw)
            base = re.findall(r'\d+[+|-]]', raw)[0]
            baseNumber = int(base[:-1])
            newNum = str(baseNumber+int(num))

            raw = raw.replace(base, newNum).replace(num, "")

        return (raw)


    def lowHighNibble(self, raw):
        #print(raw)

        if ("<" not in raw) and (">" not in raw):
            return(raw)

        try:
            numbers = re.findall(r'[<|>]\$[a-fA-F0-9]{4}', raw.replace("(",""))[0]
        except:
            #print(raw)
            changeTo = re.findall(r'[a-fA-F0-9]{3}', raw.replace("(",""))[0]
            raw = raw.replace(changeTo, "0"+changeTo)
            numbers = re.findall(r'[<|>]\$[a-fA-F0-9]{4}', raw.replace("(",""))[0]

        #print(numbers)
        if numbers[0]=="<":
            numbers=numbers[-2:]
        else:

            highNibbleChanger = {
                "0": "0",
                "1": "1",
                "2": "3",
                "3": "5",
                "4": "7",
                "5": "9",
                "6": "b",
                "7": "d",
                "8": "f"
            }

            numbers=numbers[-4:-2]
            #print(numbers)
            #numbers = hex(((int("0x"+numbers[0], 16)-1)*2)+1)[2:] + numbers[1]
            numbers = highNibbleChanger[numbers[0]] + numbers[1]
        #print(numbers)
        return ("#$"+numbers)

    def secondByteToNumeric(self, raw, variables, registers, sections):
        tempraw = re.findall(r'[a-zA-Z_0-9\-]+[a-zA-Z_0-9]', raw)
        #print(raw, tempraw)

        if tempraw==[]:
            return (raw)
        else:
            tempraw = tempraw[0]

        if ("-" in tempraw):
            test = tempraw.split("-")[-1]
            try:
                test = int(test)
                tempraw = "-".join(tempraw.split("-")[:-1])
            except:
                pass

        for item in sections:
            if (item == tempraw):
                return(raw.replace(item, sections[item]))
        for item in variables:
            if (item == tempraw):
                return(raw.replace(item, variables[item]))
        for item in registers:
            if (registers[item] == tempraw):
                return(raw.replace(registers[item], item))
        return(raw)


    def getNextName(self):
        base = self.projectPath.split("/")[-2]
        counter = 1

        name = self.generateName(base, counter)

        while os.path.exists(self.projectPath+"bin/"+name+".bin"):
            counter+=1
            name = self.generateName(base, counter)

        return(name)

    def generateName(self, base, counter):
        if (len(str(counter))) < 4:
            num = (4 - len(str(counter))) * "0" + str(counter)
        else:
            num = str(counter)

        return(base+"_"+self.__tv+"_"+num)

    def simplify(self, variables):
        simple_ones = {}
        for var in variables.keys():
            try:
                isItInt = False
                teszt   = int(variables[var].replace("#", ""))
                isItInt = True
            except:
                pass

            if variables[var].startswith("$") == True or isItInt == True or variables[var].startswith("%") == True:
               simple_ones[var] = variables[var]

        for var in variables:
            try:
                isItInt = False
                teszt   = int(variables[var].replace("#", ""))
                isItInt = True
            except:
                pass

            #print(var)
            if variables[var].startswith("$") == False             and\
               isItInt == False                                    and\
               variables[var].startswith("%")                      and\
               variables[var].startswith("#") == False:
               try:
                  variables[var] = simple_ones[variables[var]]
               except:
                  pass


        #for key in variables.keys():
        #    print(key, ": ", variables[key])

        return variables

    def compile(self, path):
        registers, opcodes =  self.__loader.io.loadRegOpCodes()
        file = open(path, "r")
        source = file.read()
        file.close()

        source = self.normalize(source)
        variables = self.simplify(self.collectVariables(source))


        source = self.compactSleep(source)
        source = self.sleepToCode(source)

        freeBytes, code, sections = self.createSquence(source, opcodes, variables, registers)

        name = self.getNextName()

        try:
           os.makedirs(self.projectPath + "/asm_log")
           os.makedirs(self.projectPath + "/bin")
        except:
            pass

        file = open(self.projectPath+"asm_log/"+name+".txt", "w")
        fileBin = open(self.projectPath+"bin/"+name+".bin", "wb")

        self.executeName = self.projectPath+"bin/"+name+".bin"

        toWrite = []
        lenOfNum = len(str(code[-1].address))

        for codeline in code:
            bytes_ = []
            for byte in codeline.bytes:
                bytes_.append(byte.hex())
                fileBin.write(byte)

            num = str(codeline.seq)
            while(len(num)<lenOfNum):
                num = "0" + num

            fos = str(num).ljust(lenOfNum+2) + str(codeline.getAddressInHex()).ljust(5)+" ".join(bytes_).ljust(40) + str(codeline.byteNum).ljust(2) + str(codeline.raw).ljust(35)
            if codeline.bytes == []:
                """
                self.errors.append(
                    self.__dictionaries.getWordFromCurrentLanguage("syntaxError")+
                    " ".join(codeline.raw)+" ("+str(codeline.getAddressInHex())
                )"""
                print(" ".join(codeline.raw))
                self.__testIt = False

            for section in sections:
                if sections[section][1:] == codeline.getAddressInHex():
                    toWrite.append(str(num).ljust(lenOfNum+2) + str(codeline.getAddressInHex()).ljust(5)+ ">>" + section)

            toWrite.append(fos)


        file.write(os.linesep.join(toWrite))
        file.close()
        fileBin.close()

        free = open("temp/free.txt", "w")
        txt = ""
        for data in freeBytes:
            txt += str(freeBytes[data]) + "\n"
        free.write(txt)
        free.close()

        self.freeBytes = freeBytes

