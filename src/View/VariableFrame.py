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

        self.__thisFrame.config(bg="red")
        self.__loader.destroyable.append(self.__thisFrame)

        self.__variableLabel = MainMenuLabel(self.__thisFrame, self.__loader, "manageVariable", 16)
        self.__varName = FrameWithLabelAndEntry(self.__thisFrame, loader, "varName", 14)

        self.__varListBox = ListBoxInFrame("typeSelector", self.__loader, self.__thisFrame,
                            self.__loader.fontManager, 0.15, ["bit", "doubleBit", "nibble", "byte"], None)

        self.__variableButtons = CreateAndDeleteButtons(self.__loader, self.__thisFrame,
                                                        self.__checkThings
                                                        )
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

    def __checkThings(self, buttonCreate, buttonDelete):
        self.__buttonCreate = buttonCreate
        self.__buttonDelete = buttonDelete
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__container != None:
            self.__text = self.__varName.getEntry()
            self.__selectedType = self.__varListBox.getSelectedName()

            sleep(0.1)