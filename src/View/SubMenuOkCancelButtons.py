from tkinter import *
from threading import Thread

class SubMenuOkCancelButtons:

    def __init__(self, window, master, loader, font, function, enableDisableVar):
        self.__window = window
        self.__loader = loader
        self.__font = font
        self.__master = master
        try:
            self.__buttonFrame = Frame(master.getTopLevel(),
                                      width=master.getTopLevelDimensions()[0],
                                      height=self.__font.metrics('linespace'))
        except:
            self.__buttonFrame = Frame(master.getFrame(),
                                      width=master.getFrameSize()[0],
                                      height=self.__font.metrics('linespace'))

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__buttonFrame.place()
        self.__buttonFrame.pack(side=BOTTOM, anchor=S)
        self.__buttonFrame.pack_propagate(False)
        self.__function = function
        try:
            w = self.__loader.fontManager.getCharacterLenghtFromPixels(self.__font, round(master.getTopLevelDimensions()[0]/2))
        except:
            w = self.__loader.fontManager.getCharacterLenghtFromPixels(self.__font, round(master.getFrameSize()[0]/2))


        self.__OKButton=Button(self.__buttonFrame, text=self.__loader.dictionaries.getWordFromCurrentLanguage("ok"),
                               width=w,
                               command=self.__sendTrue, font=self.__font)
        self.__CancelButton=Button(self.__buttonFrame, text=self.__loader.dictionaries.getWordFromCurrentLanguage("cancel"),
                               width=w,
                               command=self.__sendFalse, font=self.__font)

        self.__OKButton.pack(side=LEFT, fill=Y, anchor=SE)
        self.__CancelButton.pack(side=RIGHT, fill=Y,anchor=SW)
        self.__OKButton.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__OKButton.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__CancelButton.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__CancelButton.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__buttonFrame.config(bg=self.__loader.colorPalettes.getColor("window"))

        if enableDisableVar != None:
            self.__var = enableDisableVar
            disableOK = Thread(target=self.__changeOK)
            disableOK.start()

    def __sendTrue(self):
        self.__function(True)

    def __sendFalse(self):
        self.__function(False)

    def __changeOK(self):
        while self.__loader.mainWindow.dead==False and self.__window.dead==False and self.stopThread==False:
            from time import sleep
            try:
                if self.__var() == True:
                    self.__OKButton.config(state=NORMAL)
                else:
                    self.__OKButton.config(state=DISABLED)
            except Exception as e:
                self.__loader.logger.errorLog(e)
            sleep(1)