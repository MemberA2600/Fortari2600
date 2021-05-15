from tkinter import *
from threading import Thread
from MainMenuLabel import MainMenuLabel
from FrameWithLabelAndEntry import FrameWithLabelAndEntry
from NewListBoxInFrame import NewListBoxInFrame
from CreateAndDeleteButtons import CreateAndDeleteButtons

class ArrayFrame:

    def __init__(self, frame, loader):
        self.__container = frame
        self.__loader = loader
        #self.__modify = False

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__w = self.__container.winfo_width()
        self.__h = round(self.__container.winfo_height()/2.5)
        self.__first = True
        self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
        self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

        self.__thisFrame = Frame(self.__container, width=self.__w, height=self.__h)
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__thisFrame.pack_propagate(False)
        #self.__thisFrame.place(x=5, y=self.__loader.frames["VariableFrame"].getH() + 15+self.__loader.frames["SwitchFrame"].getH()+ self.__loader.frames["MemorySetter"].title.getH())
        self.__thisFrame.pack(side=BOTTOM, fill=X, anchor=NE)

        #self.__thisFrame.config(bg="red")
        self.__loader.destroyable.append(self.__thisFrame)

        self.__arrayLabel = MainMenuLabel(self.__thisFrame, self.__loader, "manageArray", 22, "MemorySetter")
        self.arrName = FrameWithLabelAndEntry(self.__thisFrame, loader, "arrName", 14, 40, LEFT)
        self.__errorLabel = MainMenuLabel(self.__thisFrame, self.__loader, "", 10, "MemorySetter")

        self.__frameVariables = Frame(self.__thisFrame, width=round(self.__thisFrame.winfo_width() / 5),
                                      height=self.__thisFrame.winfo_height())
        self.__frameVariables.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frameVariables.pack_propagate(False)
        self.__frameVariables.pack(side=LEFT, anchor=W, fill=Y)

        self.__frameAvailable = Frame(self.__thisFrame, width=round(self.__thisFrame.winfo_width() / 5),
                                      height=self.__thisFrame.winfo_height())
        self.__frameAvailable.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frameAvailable.pack_propagate(False)
        self.__frameAvailable.pack(side=LEFT, anchor=W, fill=Y)

        self.__containedLabel = MainMenuLabel(self.__frameVariables, self.__loader, "arrVariables", 14, "MemorySetter")
        self.__varListBox = NewListBoxInFrame("includedVariables", self.__loader, self.__frameVariables,
                            [], None, LEFT)

        self.__availableLabel = MainMenuLabel(self.__frameAvailable, self.__loader, "arrAvailable", 14, "MemorySetter")
        self.__avListBox = NewListBoxInFrame("availableVariables", self.__loader, self.__frameAvailable,
                            [], None, LEFT)

        self.__arrayButtons = CreateAndDeleteButtons(self.__loader, self.__thisFrame,
                                                        "array",
                                                        self.__checkThings,
                                                        self.__createArr,
                                                        self.__deleteArr,
                                                        )

        self.__loader.frames["ArrayFrame"] = self

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()


    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.__container!=None and self.stopThread == False:
            if (self.__lastScaleX != self.__loader.frames["MemorySetter"].getScales()[0] or
                    self.__lastScaleY != self.__loader.frames["MemorySetter"].getScales()[1])\
                    or self.__first==True:

                self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
                self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]
                self.__first = False
                if self.__thisFrame!=None:
                    try:
                        self.__thisFrame.config(width=self.__w * self.__lastScaleX,
                                     height=self.__h * self.__lastScaleY)
                        self.__frameVariables.config(width=round(self.__thisFrame.winfo_width()/5),
                                      height=self.__thisFrame.winfo_height())
                        self.__frameAvailable.config(width=round(self.__thisFrame.winfo_width()/5),
                                      height=self.__thisFrame.winfo_height())


                    except Exception as e:
                        self.__loader.logger.errorLog(e)
                #self.__thisFrame.place(x=5, y=self.__loader.frames["VariableFrame"].getH() + 15+self.__loader.frames["SwitchFrame"].getH()+ self.__loader.frames["MemorySetter"].title.getH())
            sleep(0.04)

    def __checkIfNameIsValid(self, text):
        if len(text)==0:
            self.__errorLabel.changeText("")
            return(False)
        elif len(text)<4:
            self.__errorLabel.changeText("arrNameTooShort")
            return(False)

        import re
        if len(re.findall(r'^[a-zA-Z][a-zA-Z0-9_-]+$', text))==0:
            self.__errorLabel.changeText("arrNameNotValid")
            return(False)

        for address in self.__loader.virtualMemory.memory.keys():
            if self.__lastText in self.__loader.virtualMemory.memory[address].variables.keys():
                if self.__loader.virtualMemory.memory[address].variables[self.__lastText].system == True:
                    self.__errorLabel.changeText("systemVar")
                else:
                    self.__errorLabel.changeText("alreadyVar")
                return (False)

        for command in self.__loader.syntaxList.keys():
            if command == self.__lastText:
                self.__errorLabel.changeText("commandName")
                return (False)
            else:
                for alias in self.__loader.syntaxList[command].alias:
                    if alias == self.__lastText:
                        self.__errorLabel.changeText("commandName")
                        return (False)

        return(True)

    def __checkThings(self, buttonCreate, buttonDelete, others):
        self.__buttonCreate = buttonCreate
        self.__buttonDelete = buttonDelete
        self.__mod = False

        self.__loader.destroyable.append(self.__buttonCreate)
        self.__loader.destroyable.append(self.__buttonDelete)

        self.__buttonVarAdd = others[0]
        self.__buttonVarDel = others[1]

        self.__loader.destroyable.append(self.__buttonVarAdd)
        self.__loader.destroyable.append(self.__buttonVarDel)

        self.__buttonVarAdd.config(command=self.__moveLeft)
        self.__buttonVarDel.config(command=self.__moveRight)

        self.__lastText = ""
        self.__lastSelectedType = ""

        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__container != None and self.stopThread == False:
            try:
                self.__varListBox.getSelectedName()
                self.__buttonVarDel.config(state=NORMAL)
            except:
                try:
                    self.__buttonVarDel.config(state=DISABLED)
                except Exception as e:
                    self.__loader.logger.errorLog(e)
            try:
                self.__avListBox.getSelectedName()
                self.__buttonVarAdd.config(state=NORMAL)
            except:
                try:
                    self.__buttonVarAdd.config(state=DISABLED)
                except Exception as e:
                    self.__loader.logger.errorLog(e)
            if (self.__lastText!=self.arrName.getEntry()):
                self.__lastText = self.arrName.getEntry()

                self.__varListBox.filler([])
                self.__avListBox.filler([])

                #print(self.__lastText)
                #print(self.__lastSelectedType)
                if self.__checkIfNameIsValid(self.__lastText) == False:
                    self.__buttonCreate.config(state=DISABLED)
                    self.__buttonDelete.config(state=DISABLED)

                    sleep(0.1)
                    continue

                self.__buttonCreate.config(state=NORMAL)
                self.__selectedValidity = self.__loader.listBoxes["bankBox"].getSelectedName()
                if self.__selectedValidity == "bank1":
                    self.__selectedValidity = "global"

                #print(self.__selectedValidity)

                if self.__lastText in self.__loader.virtualMemory.arrays.keys():
                    if (self.__loader.virtualMemory.getArrayValidity(self.__lastText)!="global" and
                            self.__selectedValidity != self.__loader.virtualMemory.getArrayValidity(self.__lastText)):
                        self.__buttonCreate.config(state=DISABLED)
                        self.__buttonDelete.config(state=DISABLED)
                        self.__buttonVarDel.config(state=DISABLED)
                        self.__buttonVarAdd.config(state=DISABLED)
                        self.__errorLabel.changeText("arrLocated")

                    else:
                        self.__buttonCreate.config(text =
                                            self.__loader.dictionaries.getWordFromCurrentLanguage("modify"))
                        self.__mod = True

                        self.fillListBoxes()
                        self.__buttonDelete.config(state=NORMAL)

                else:
                    self.__buttonCreate.config(text =
                                        self.__loader.dictionaries.getWordFromCurrentLanguage("create"))
                    self.__mod = False
                    self.fillListBoxes()

                    self.__buttonDelete.config(state=DISABLED)

                sleep(0.1)
                continue

            sleep(0.4)

    def fillListBoxes(self):
        temp = []
        if self.__mod==True:
            for address in self.__loader.virtualMemory.memory.keys():
                for variable in self.__loader.virtualMemory.memory[address].variables.keys():
                    if (self.__loader.virtualMemory.memory[address].variables[variable].iterable == True and
                            variable in list(self.__loader.virtualMemory.arrays[
                                                 self.__lastText
                                             ].keys())):
                        temp.append(variable + " (" + self.__loader.virtualMemory.memory[address].variables[
                            variable].validity + ")")

            temp.sort()
        self.__varListBox.filler(temp)
        """
        self.__varListBox.filler(list(self.__loader.virtualMemory.arrays[
                        self.__lastText
                                 ].keys()))
        """
        temp2 = []
        for address in self.__loader.virtualMemory.memory.keys():
            for variable in self.__loader.virtualMemory.memory[address].variables.keys():

                if ((variable + " (" + self.__loader.virtualMemory.memory[address].variables[
                    variable].validity + ")" not in temp) and
                        self.__loader.virtualMemory.memory[address].variables[variable].iterable == True and
                        (self.__loader.virtualMemory.memory[address].variables[variable].validity == "global" or
                         self.__loader.virtualMemory.memory[address].variables[
                             variable].validity == self.__selectedValidity)):
                    temp2.append(variable + " (" + self.__loader.virtualMemory.memory[address].variables[
                        variable].validity + ")")

        temp2.sort()
        self.__avListBox.filler(temp2)


    def __createArr(self):
        #self.__loader.virtualMemory.archieve()
        self.__original = self.__loader.virtualMemory.getArrayValidity(self.__lastText)
        if self.__mod == True:
            #self.__modify = True
            self.__deleteArr()
        self.__loader.virtualMemory.addArray(self.__lastText)
        for variable in self.__varListBox.data:
            varName = variable.split(" ")[0]
            self.__loader.virtualMemory.addItemsToArray(
                self.__lastText,
                varName,
                self.__loader.virtualMemory.getVariableByName(varName, None)
            )
        self.__loader.frames["rightFrame"].arrays.refiller()
        self.arrName.setEntry(self.__lastText)
        bank = self.__loader.virtualMemory.getArrayValidity(self.__lastText)
        self.__finish(True, bank)

    def __deleteArr(self):
        #if self.__modify == False:
        #    self.__loader.virtualMemory.archieve()

        bank = self.__loader.virtualMemory.getArrayValidity(self.__lastText)
        self.__loader.virtualMemory.removeArray(self.__lastText)
        self.__loader.frames["rightFrame"].arrays.refiller()
        self.__finish(False,bank)

    def __finish(self, create, bank):

        section = "local_variables"
        if bank == "global":
            bank = "bank1"
            section = "global_variables"
        self.__loader.virtualMemory.codes[bank][section].changed = True
        self.__loader.virtualMemory.moveVariablesToMemory(bank)
        self.__loader.virtualMemory.archieve()
        self.__modify = False


        if create == False:
            self.arrName.setEntry("")
        else:
            bank = self.__original
            bank = self.__loader.virtualMemory.getArrayValidity(self.__lastText)
            section = "local_variables"
            if bank == "global":
                bank = "bank1"
                section = "global_variables"
            self.__loader.virtualMemory.codes[bank][section].changed = True
            self.__loader.virtualMemory.moveVariablesToMemory(bank)

            self.__lastText = ""

    def __moveLeft(self):
        self.__changeLists(self.__avListBox, self.__varListBox)

    def __moveRight(self):
        self.__changeLists(self.__varListBox, self.__avListBox)

    def __changeLists(self, list1, list2):
        selected = list1.getSelectedName()
        fromList = []
        toList = []

        for item in list1.data:
            fromList.append(item)
        for item in list2.data:
            toList.append(item)

        toList.append(selected)
        fromList.remove(selected)

        list1.filler(fromList)
        list2.filler(toList)



