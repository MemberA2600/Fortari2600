from tkinter import *
from threading import Thread

class MainMenuLabel:

    def __init__(self, master, loader, text, baseSize, bossname):
        self.__loader = loader
        self.__master = master

        self.stopThread = False
        self.__loader.stopThreads.append(self)


        self.__bossName =  bossname

        w = self.__loader.frames[bossname].getWindowSize()[0]/955
        h = self.__loader.frames[bossname].getWindowSize()[1]/686

        self.__fontSize = (baseSize*w*h)

        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        try:
            self.__label = Label(master,
                                 text = loader.dictionaries.getWordFromCurrentLanguage(text),
                                 font=self.__font)
        except:
            self.__label = Label(master,
                                 text = text,
                                 font=self.__font)
        self.__label.pack(side=TOP, anchor = W)
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__lastScaleX = self.__loader.frames[bossname].getScales()[0]
        self.__lastScaleY = self.__loader.frames[bossname].getScales()[1]

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

    def changeColor(self, color, bgcolor):
        self.__label.config(fg=color, bg=bgcolor)

    def changePack(self, side, anchor):
        self.__label.pack(side=side, anchor=anchor)

    def getH(self):
        return(self.__label.winfo_height())

    def changeText(self, text):
        if text == "":
            try:
                self.__label.config(text="",
                                    font=self.__font)
            except Exception as e:
                self.__loader.logger.errorLog(e)
        else:
            try:
                self.__label.config(text = self.__loader.dictionaries.getWordFromCurrentLanguage(text),
                                     font=self.__font)
            except:
                self.__label.config(text = text,
                                     font=self.__font)

    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastScaleX != self.__loader.frames[self.__bossName].getScales()[0] or
                    self.__lastScaleY != self.__loader.frames[self.__bossName].getScales()[1]):
                self.__lastScaleX = self.__loader.frames[self.__bossName].getScales()[0]
                self.__lastScaleY = self.__loader.frames[self.__bossName].getScales()[1]

                self.__font = self.__loader.fontManager.getFont(round(self.__fontSize*self.__lastScaleX*self.__lastScaleY), False, False, False)
                try:
                    self.__label.config(font=self.__font)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)