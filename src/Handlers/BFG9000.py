from tkinter import *
from MemorySetter import MemorySetter

class BFG9000:

    def __init__(self, loader, editor, editorHandler, minus):
        self.__loader = loader
        self.__editor = editor
        self.__editorHandler = editorHandler
        self.__loader.BFG9000 = self

        self.__w = self.__editorHandler.getWindowSize()[0]*0.66
        self.__h = self.__editorHandler.getWindowSize()[1]-minus-25

        self.__lastScaleX = self.__editorHandler.getScales()[0]
        self.__lastScaleY = self.__editorHandler.getScales()[1]


        self.frame = Frame(self.__editor, width=self.__editorHandler.getWindowSize()[0],
                                 height=self.__h,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 #fg=self.__loader.colorPalettes.getColor("font"),
                                 )

        self.frame.pack_propagate(False)
        self.frame.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
        self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()

        self.__mainFrame = Frame(self.frame, width=self.__w, height=self.__h,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 #fg=self.__loader.colorPalettes.getColor("font"),
                                 )

        self.__mainFrame.pack_propagate(False)
        self.__first = True

        self.__w2 = self.__editorHandler.getWindowSize()[0]*0.18
        self.__leftFrame = Frame(self.frame, width=self.__w2, height=self.__h,
                                 bg=self.__loader.colorPalettes.getColor("window"))
        self.__rightFrame = Frame(self.frame, width=self.__w2, height=self.__h,
                                 bg=self.__loader.colorPalettes.getColor("window"))

       # self.__mainFrame.config(bg="red")
       # self.__leftFrame.config(bg="blue")
       # self.__rightFrame.config(bg="blue")

        self.__leftFrame.pack_propagate(False)
        self.__rightFrame.pack_propagate(False)

        self.__leftFrame.pack(side=LEFT, anchor=SW, fill=Y)
        self.__mainFrame.pack(side=LEFT, anchor=S, fill=Y)
        self.__rightFrame.pack(side=RIGHT, anchor=SE, fill=Y)
        self.__lastPath = None

        from threading import Thread
        t = Thread(target=self.checker)
        t.daemon = True
        t.start()

        r = Thread(target=self.resizer)
        r.daemon = True
        r.start()

    def saveFrameToMemory(self, bank, section):
        if bank == "bank1" or section == "local_variables":
            self.__loader.virtualMemory.writeVariablesToMemory(bank)


    def loadFromMemoryToFrame(self, bank, section):

        if bank == "bank1" or section == "local_variables":
            self.__loader.virtualMemory.setVariablesFromMemory(bank)
        if bank == "bank1":
            main = MemorySetter(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame, "global")


    def clearFrames(self, color):
        self.destroyAll(self.__mainFrame.pack_slaves())
        self.destroyAll(self.__leftFrame.pack_slaves())
        self.destroyAll(self.__rightFrame.pack_slaves())

        self.__mainFrame.config(bg=color)
        self.__leftFrame.config(bg=color)
        self.__rightFrame.config(bg=color)
        self.__loader.BFG9000.frame.config(bg=color)

    def destroyAll(self, list):
        for item in list:
            item.destroy()

    def getSelected(self):
        return(self.__selectedBank, self.__selectedSection)

    def checker(self):
        from time import sleep
        while self.__editorHandler.dead==False:
            if self.__first == True or (
                    self.__selectedBank != self.__loader.listBoxes["bankBox"].getSelectedName() or
                    self.__selectedSection != self.__loader.listBoxes["sectionBox"].getSelectedName()
            ) or self.__lastPath !=self.__loader.mainWindow.projectPath:

                self.__lastPath = self.__loader.mainWindow.projectPath
                self.__first = False

                if self.__lastPath ==None:
                    from AtariLogo import AtariLogo
                    self.clearFrames("black")
                    atariLogo = AtariLogo(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame)
                else:
                    self.clearFrames(self.__loader.colorPalettes.getColor("window"))
                    self.saveFrameToMemory(self.__selectedBank, self.__selectedSection)

                    self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
                    self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()
                    #print(self.__selectedBank, self.__selectedSection)

                    self.loadFromMemoryToFrame(self.__selectedBank, self.__selectedSection)
                sleep(0.4)
            sleep(0.4)

    def resizer(self):
        from time import sleep
        while self.__editorHandler.dead == False:
            if (self.__lastScaleX != self.__editorHandler.getScales()[0] or
                self.__lastScaleY != self.__editorHandler.getScales()[1]):
                    self.__lastScaleX = self.__editorHandler.getScales()[0]
                    self.__lastScaleY = self.__editorHandler.getScales()[1]

                    self.frame.config(
                        width=self.__editorHandler.getWindowSize()[0] * self.__lastScaleX,
                        height=self.__h * self.__lastScaleY
                    )

                    self.__leftFrame.config(
                        width=self.__w2 * self.__lastScaleX,
                        height=self.__h * self.__lastScaleY
                    )

                    self.__mainFrame.config(
                        width=self.__w * self.__lastScaleX,
                        height=self.__h * self.__lastScaleY
                    )

                    self.__rightFrame.config(
                        width=self.__w2 * self.__lastScaleX,
                        height=self.__h * self.__lastScaleY
                    )

                    sleep(0.02)
                    continue

            sleep(0.05)