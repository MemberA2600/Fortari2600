from tkinter import *
from SubMenu import SubMenu

class KernelTester:

    def __init__(self, loader, clicked):

        self.dead = False

        import os


        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        if clicked > 4:
            self.__loader.soundPlayer.playSound("ClickW2")


        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs

        from FontManager import FontManager
        self.__fontManager = FontManager(self.__loader)

        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__smallerFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)

        w = round(self.__screenSize[0] / 3)
        h = round(self.__screenSize[1]/2.6  - 40)

        self.__topLevelWindow  = Toplevel()
        self.__topLevelWindow.title(self.__dictionaries.getWordFromCurrentLanguage("kernelTester"))
        self.__topLevelWindow.geometry("%dx%d+%d+%d" % (w, h, (self.__screenSize[0]/2-w/2), (self.__screenSize[1]/2-h/2-50)))
        self.__topLevelWindow.resizable(False, False)

        self.__topLevelWindow.config(bg=self.__loader.colorPalettes.getColor("window"))
        try:
            self.__topLevelWindow.iconbitmap("others/img/"+name+".ico")
        except:
            self.__topLevelWindow.iconbitmap("others/img/icon.ico")

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

        self.__addElements(self)

        try:
            from os import mkdir
            mkdir("temp/")
        except:
            pass

        self.__topLevelWindow.mainloop()
        self.dead = True

        try:
            from shutil import rmtree
            rmtree('temp/')
        except:
            pass

    def getTopLevelDimensions(self):
        return(round(self.__screenSize[0] / 3),
               round(self.__screenSize[1]/3  - 40))

    def __addElements(self, top):
        self.__topLevel = top

        self.__title = Label(self.__topLevelWindow, text = self.__dictionaries.getWordFromCurrentLanguage("kernelTester"),
                             bg = self.__loader.colorPalettes.getColor("window"),
                             fg = self.__loader.colorPalettes.getColor("font"),
                             font =  self.__normalFont, justify=CENTER)
        self.__title.pack(side=TOP, anchor = N, fill=X)

        self.__smallTitle = Label(self.__topLevelWindow, text = self.__dictionaries.getWordFromCurrentLanguage("foundOut"),
                             bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                             fg = self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                             font =  self.__smallerFont, justify=CENTER)
        self.__smallTitle.pack(side=TOP, anchor = N, fill=X)

        from KernelTesterLoaderFrame import KernelTesterLoaderFrame

        self.__openKernelFrame = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/6), self.__smallFont,
                                                         "kernelFile", round(self.__topLevel.getTopLevelDimensions()[0]), self)

        self.__openKernelFrame.setValue("E:/PyCharm/P/Fortari2600/templates/skeletons/common_main_kernel.asm")

        self.__openEnter = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/6), self.__smallFont,
                                                         "enterBank2", round(self.__topLevel.getTopLevelDimensions()[0]), self)

        self.__openOverscan = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/6), self.__smallFont,
                                                         "overscanBank2", round(self.__topLevel.getTopLevelDimensions()[0]), self)

        self.__openScreenTopData = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/6), self.__smallFont,
                                                         "screenTopData", round(self.__topLevel.getTopLevelDimensions()[0]), self)

        self.__openKernelData = KernelTesterLoaderFrame(self.__loader, self.__topLevelWindow,
                                                         round(self.__topLevel.getTopLevelDimensions()[1]/6), self.__smallFont,
                                                         "kernelData", round(self.__topLevel.getTopLevelDimensions()[0]), self)


        self.__testButton = Button(self.__topLevelWindow, stat=DISABLED,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font"),
                                   text=self.__dictionaries.getWordFromCurrentLanguage("testWithEmulator")[:-1],
                                   font=self.__normalFont, width=9999, command=self.__startTesting)

        self.__testButton.pack_propagate(False)
        self.__testButton.pack(side=TOP, anchor=S, fill=BOTH)

        from threading import Thread
        e = Thread(target=self.checkIfAllValid)
        e.daemon = True
        e.start()

    def checkIfAllValid(self):
        from time import sleep

        while self.dead == False:

            try:
                if (self.__openKernelFrame.valid == True
                        and self.__openEnter.valid == True
                        and self.__openOverscan.valid == True
                        and self.__openKernelData.valid == True
                        and self.__openScreenTopData.valid == True

                ) :
                    self.__testButton.config(state=NORMAL)
                else:
                    self.__testButton.config(state=DISABLED)

                sleep(0.1)
            except:
                pass

    def __startTesting(self):
        from threading import Thread

        t = Thread(target=self.__testing)
        t.daemon = True
        t.start()

    def __testing(self):
        from Compiler import Compiler

        c = Compiler(self.__loader, None, "kernelTest", [
            self.__loader.io.loadWholeText(self.__openKernelFrame.getValue()),
            self.__loader.io.loadWholeText(self.__openEnter.getValue()),
            self.__loader.io.loadWholeText(self.__openOverscan.getValue()),
            self.__loader.io.loadWholeText(self.__openScreenTopData.getValue()),
            self.__loader.io.loadWholeText(self.__openKernelData.getValue())
            ])
