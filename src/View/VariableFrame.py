from tkinter import *
from threading import Thread
from MainMenuLabel import MainMenuLabel
from FrameWithLabelAndEntry import FrameWithLabelAndEntry
from ListBoxInFrame import ListBoxInFrame
from CreateAndDeleteButtons import CreateAndDeleteButtons

class VariableFrame:

    def __init__(self, frame, loader):
        self.__container = frame
        self.__loader = loader

        self.__w = self.__container.winfo_width()
        self.__h = round(self.__container.winfo_height()/2.5)

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        self.__thisFrame = Frame(self.__container, width=self.__w, height=self.__h)
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__thisFrame.pack_propagate(False)
        self.__thisFrame.pack(side=TOP, anchor=E)

        #self.__thisFrame.config(bg="red")
        self.__loader.destroyable.append(self.__thisFrame)

        self.__variableLabel = MainMenuLabel(self.__thisFrame, self.__loader, "manageVariable", 16)
        self.varName = FrameWithLabelAndEntry(self.__thisFrame, loader, "varName", 14)
        self.__errorLabel = MainMenuLabel(self.__thisFrame, self.__loader, "", 10)

        self.__varListBox = ListBoxInFrame("typeSelector", self.__loader, self.__thisFrame,
                            self.__loader.fontManager, 0.15, ["bit", "doubleBit", "nibble", "byte"], None)

        self.__variableButtons = CreateAndDeleteButtons(self.__loader, self.__thisFrame,
                                                        "variable",
                                                        self.__checkThings,
                                                        self.__createVar,
                                                        self.__deleteVar
                                                        )

        self.__loader.frames["VariableFrame"] = self

        from StatusFrame import StatusFrame
        self.__statusFrame = StatusFrame(self.__thisFrame, self.__loader)

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.__container!=None:
            if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastScaleY != self.__loader.mainWindow.getScales()[1]):
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                if self.__thisFrame!=None:
                    try:
                        self.__thisFrame.config(width=self.__w * self.__lastScaleX,
                                     height=self.__h * self.__lastScaleY)
                    except Exception as e:
                        self.__loader.logger.errorLog(e)

            sleep(0.04)

    def __checkThings(self, buttonCreate, buttonDelete, others):
        self.__buttonCreate = buttonCreate
        self.__buttonDelete = buttonDelete

        self.__loader.destroyable.append(self.__buttonCreate)
        self.__loader.destroyable.append(self.__buttonDelete)


        self.__variableEntry = others[0]
        self.__variableEntryText = others[1]
        self.__bitEntry = others[2]
        self.__bitEntryText = others[3]
        self.__variableListBox = self.__varListBox.getListBoxAndScrollBar()[0]
        self.__mod = False

        self.__lastText = ""
        self.__lastSelectedType = ""

        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__container != None:
            if (self.__lastText!=self.varName.getEntry() or
                self.__lastSelectedType!=self.__varListBox.getSelectedName()):
                self.__lastText = self.varName.getEntry()
                self.__lastSelectedType = self.__varListBox.getSelectedName()

                #print(self.__lastText)
                #print(self.__lastSelectedType)
                if self.__checkIfNameIsValid(self.__lastText) == False:
                    try:
                        self.__buttonCreate.config(state=DISABLED)
                        self.__buttonDelete.config(state=DISABLED)
                    except Exception as e:
                        self.__loader.logger.errorLog(e)

                    sleep(0.1)
                    continue


                self.__buttonCreate.config(state=NORMAL)
                self.__selectedValidity = self.__loader.listBoxes["bankBox"].getSelectedName()
                if self.__selectedValidity == "bank1":
                    self.__selectedValidity = "global"

                #print(self.__selectedValidity)

                if self.__loader.virtualMemory.checkIfExists(self.__lastText, self.__selectedValidity):
                    self.__buttonCreate.config(text =
                                        self.__loader.dictionaries.getWordFromCurrentLanguage("modify"))
                    self.__mod = True
                    self.__buttonDelete.config(state=NORMAL)
                    self.__variableEntryText.set(
                        self.__loader.virtualMemory.getAddressOnVariableIsStored(self.__lastText, self.__selectedValidity))

                    self.__variableListBox.select_clear(0, END)
                    selector = {
                        "bit": 0, "doubleBit": 1, "nibble": 2, "byte": 3
                                }
                    self.__variableListBox.select_set(selector[self.__loader.virtualMemory.
                                                      getVariableByName(self.__lastText, self.__selectedValidity).type])


                    text = ""
                    for num in (self.__loader.virtualMemory.
                                getVariableByName(self.__lastText, self.__selectedValidity).usedBits):

                        text += str(num)+", "
                    self.__bitEntryText.set(text[:-2])


                else:
                    self.__buttonCreate.config(text =
                                        self.__loader.dictionaries.getWordFromCurrentLanguage("create"))
                    self.__mod = False
                    self.__buttonDelete.config(state=DISABLED)
                    self.__variableEntryText.set("")
                    self.__bitEntryText.set("")


                sleep(0.1)
                continue

            sleep(0.4)

    def __createVar(self):
        if self.__mod == True:
            self.__deleteVar()
        self.__loader.virtualMemory.addVariable(self.__lastText,
                                                   self.__varListBox.getSelectedName(),
                                                   self.__selectedValidity
                                                   )
        self.__saveThings()
        self.__modifyFields(True)
        self.__loader.frames["rightFrame"].variables.refiller()

    def __deleteVar(self):
        self.__loader.virtualMemory.removeVariable(self.__lastText,
                                                   self.__selectedValidity
                                                   )
        self.__saveThings()
        self.__modifyFields(False)
        self.__loader.frames["rightFrame"].variables.refiller()

    def __saveThings(self):
        bank = self.__selectedValidity
        section = "local_variables"
        if bank == "global":
            bank = "bank1"
            section = "global_variables"

        self.__loader.virtualMemory.moveVariablesToMemory(bank)
        self.__loader.virtualMemory.codes[bank][section].changed = True


    def __modifyFields(self, bool):
        if bool == False:
            self.varName.setEntry("")
            self.__variableEntryText.set("")
            self.__bitEntryText.set("")
            self.__buttonCreate.config(text=
                                       self.__loader.dictionaries.getWordFromCurrentLanguage("create"))
        self.__lastText = ""
        self.__loader.frames["statusFrame"].calculateFreeRAM()

    def __checkIfNameIsValid(self, text):
        if len(text)==0:
            self.__errorLabel.changeText("")
            return(False)
        elif len(text)<4:
            self.__errorLabel.changeText("varNameTooShort")
            return(False)

        import re
        if len(re.findall(r'^[a-zA-Z][a-zA-Z0-9_-]+$', text))==0:
            self.__errorLabel.changeText("varNameNotValid")
            return(False)

        for address in self.__loader.virtualMemory.memory.keys():
            if self.__lastText in self.__loader.virtualMemory.memory[address].variables.keys():
                if self.__loader.virtualMemory.memory[address].variables[self.__lastText].system == True:
                    self.__errorLabel.changeText("systemVar")
                    return (False)

        if self.__lastText in self.__loader.virtualMemory.arrays.keys():
            self.__errorLabel.changeText("alreadyArr")
            return (False)

        self.__errorLabel.changeText("")
        return(True)