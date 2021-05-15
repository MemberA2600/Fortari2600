from tkinter import *
from MemorySetter import MemorySetter
from CodeEditor import CodeEditor

class BFG9000:

    def __init__(self, loader, editor, editorHandler, minus):
        self.__loader = loader
        self.__editor = editor
        self.__editorHandler = editorHandler
        self.__loader.BFG9000 = self
        self.actual = None
        self.__w = self.__editorHandler.getWindowSize()[0]*0.66
        self.__h = self.__editorHandler.getWindowSize()[1]-minus-25

        self.__bankBox = self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0]
        self.__sectionBox = self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0]

        self.__lastScaleX = self.__editorHandler.getScales()[0]
        self.__lastScaleY = self.__editorHandler.getScales()[1]


        self.frame = Frame(self.__editor, width=self.__editorHandler.getWindowSize()[0],
                                 height=self.__h,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 #fg=self.__loader.colorPalettes.getColor("font"),
                                 )

        self.frame.pack_propagate(False)
        self.frame.pack(side=BOTTOM, anchor=S, fill=BOTH)
        self.__classicEditorTypes = ["enter", "leave", "overscan", "vblank"]

        self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
        self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()

        self.__mainFrame = Frame(self.frame, width=self.__w, height=self.__h,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 #fg=self.__loader.colorPalettes.getColor("font"),
                                 )

        self.__mainFrame.pack_propagate(False)
        self.first = True

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
        self.__mainFrame.pack(side=LEFT, anchor=S, fill=BOTH)
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
            self.actual = MemorySetter(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame, bank, "MemorySetter")
        elif section in self.__classicEditorTypes:
            self.actual = CodeEditor(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame, bank, "CodeEditor")


    def saveAllCode(self):
        if self.__selectedBank!="bank1" and self.__loader.frames["CodeEditor"].changed == True:
            self.__loader.virtualMemory.codes[self.__selectedBank][self.__selectedSection].code = self.__loader.currentEditor.get(0.0, END)
            self.__loader.virtualMemory.codes[self.__selectedBank][self.__selectedSection].changed = True
            self.__loader.virtualMemory.archieve()

    def clearFrames(self, color):
        #if self.__selectedSection in self.__classicEditorTypes:
        #    self.saveAllCode()

        for item in self.__loader.destroyable:
            item.destroy()

        self.__loader.mainWindow.stopThreads()
        #del self.actual
        self.__loader.currentEditor = None

        self.destroyAll(self.__mainFrame.place_slaves())
        self.destroyAll(self.__mainFrame.pack_slaves())
        self.destroyAll(self.__leftFrame.pack_slaves())
        self.destroyAll(self.__leftFrame.place_slaves())
        self.destroyAll(self.__rightFrame.pack_slaves())
        self.destroyAll(self.__rightFrame.place_slaves())


        self.__mainFrame.config(bg=color)
        self.__leftFrame.config(bg=color)
        self.__rightFrame.config(bg=color)
        self.__loader.BFG9000.frame.config(bg=color)

    def destroyAll(self, list):
        for item in list:
            try:
                item.destroy()
            except:
                pass



    def getSelected(self):
        return(self.__selectedBank, self.__selectedSection)

    def checker(self):
        from time import sleep
        while self.__editorHandler.dead==False:
            if self.first == True or (
                    self.__selectedBank != self.__loader.listBoxes["bankBox"].getSelectedName() or
                    (self.__selectedSection != self.__loader.listBoxes["sectionBox"].getSelectedName() and
                    self.__selectedBank != "bank1"
                    )) or self.__lastPath !=self.__loader.mainWindow.projectPath:

                self.__lastPath = self.__loader.mainWindow.projectPath
                self.first = False
                self.actual = None


                if self.__lastPath ==None:
                    from AtariLogo import AtariLogo
                    self.clearFrames("black")
                    self.actual = AtariLogo(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame)

                else:
                    self.clearFrames(self.__loader.colorPalettes.getColor("window"))
                    self.saveFrameToMemory(self.__selectedBank, self.__selectedSection)

                    self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
                    if self.__loader.virtualMemory.locks[self.__selectedBank] != None:
                        self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()

                        from LockNChase import LockNChase
                        self.clearFrames("black")
                        self.actual = LockNChase(self.__loader, self.__mainFrame, self.__leftFrame, self.__rightFrame)

                    else:
                        if self.__selectedBank == "bank1":
                            self.__selectedSection = "global_variables"

                        else:
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

    def selectOnBoxes(self, num):
        self.__bankBox.select_clear(0,END)
        self.__bankBox.select_set(num - 1)
        if num > 1:
            from threading import Thread
            t = Thread(target=self.selectSecond, args=[num])
            t.daemon
            t.start()

    def selectSecond(self, num):
        from time import sleep
        while self.__sectionBox.curselection()[0]!=2:
            self.__sectionBox.select_clear(0, END)
            self.__sectionBox.select_set(2)