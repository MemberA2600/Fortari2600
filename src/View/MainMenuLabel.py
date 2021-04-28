from tkinter import Label, TOP, NW, NORMAL, DISABLED
from threading import Thread

class MainMenuLabel:

    def __init__(self, master, loader, text, baseSize):
        self.__loader = loader

        self.__fontSize = ((self.__loader.screenSize[0]/1350) *
                            (self.__loader.screenSize[1]/1100) * baseSize
                           )

        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        try:
            self.__label = Label(master,
                                 text = loader.dictionaries.getWordFromCurrentLanguage(text),
                                 font=self.__font)
        except:
            self.__label = Label(master,
                                 text = text,
                                 font=self.__font)
        self.__label.pack(side=TOP, anchor = NW)
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()



    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False:
            if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastScaleY != self.__loader.mainWindow.getScales()[1]):
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                self.__font = self.__loader.fontManager.getFont(round(self.__fontSize*self.__lastScaleX*self.__lastScaleY), False, False, False)
                try:
                    self.__label.config(font=self.__font)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)