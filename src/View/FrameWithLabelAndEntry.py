from tkinter import *
from threading import Thread

class FrameWithLabelAndEntry:

    def __init__(self, frame, loader, text, baseSize):

        self.__container = frame
        self.__loader = loader

        self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
        self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()

        self.__w = self.__container.winfo_width()
        self.__h = round(self.__container.winfo_height()/5)

        self.__frame = Frame(self.__container, width=self.__w,
                             height=self.__h)

        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.__frame.config(bg="blue")

        self.__loader.destroyable.append(self.__frame)

        self.__frame.pack_propagate(False)
        self.__frame.pack(side=TOP, anchor=NW)

        self.__loader = loader

        self.__fontSize = ((self.__loader.screenSize[0] / 1350) *
                           (self.__loader.screenSize[1] / 1100) * baseSize
                           )

        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__fontU = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__fontI = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)

        try:
            self.__label = Label(self.__frame,
                                 text=loader.dictionaries.getWordFromCurrentLanguage(text),
                                 font=self.__fontI)
        except:
            self.__label = Label(self.__frame,
                                 text=text,
                                 font=self.__fontI)

        self.__stringVar=StringVar()
        self.__entry = Entry(self.__frame, font = self.__font, textvariable=self.__stringVar)
        self.__entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__entry.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.__entry.config(width=40)
        self.__label.pack(side=LEFT, anchor = SE)
        self.__entry.pack(side=LEFT, anchor = SE)

        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

    def setEntry(self, text):
        self.__stringVar.set(text)

    def getEntry(self):
        return(self.__stringVar.get())

    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.__container!=None:
            if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastScaleY != self.__loader.mainWindow.getScales()[1]):
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]


                if self.__frame!=None:
                    try:
                        self.__frame.config(width=self.__w * self.__lastScaleX,
                                             height=self.__h * self.__lastScaleY)
                        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize*self.__lastScaleX*self.__lastScaleY), False, False, False)
                        self.__fontU = self.__loader.fontManager.getFont(round(self.__fontSize*self.__lastScaleX*self.__lastScaleY), False, False, True)
                        self.__fontI = self.__loader.fontManager.getFont(round(self.__fontSize*self.__lastScaleX*self.__lastScaleY), False, True, False)
                    except Exception as e:
                        self.__loader.logger.errorLog(e)

                try:
                    self.__label.config(font=self.__fontI)
                    self.__entry.config(font=self.__font)

                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)