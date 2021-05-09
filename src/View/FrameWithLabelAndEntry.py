from tkinter import *
from threading import Thread

class FrameWithLabelAndEntry:

    def __init__(self, frame, loader, text, baseSize, ewidth, side):

        self.__container = frame
        self.__loader = loader
        self.__ewidth=ewidth

        self.stopThread = False
        self.__loader.stopThreads.append(self)

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

        self.__setFontSize()

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

        self.__entry.config(width=ewidth)
        self.__label.pack(side=LEFT, anchor = SE)
        self.__entry.pack(side=side, anchor = SW)

        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
        self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

        self.__entry.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        self.__entry.bind("<FocusOut>", self.__loader.mainWindow.focusOut)

    def __setFontSize(self):
        baseSize=14
        w = self.__loader.frames["MemorySetter"].getWindowSize()[0]/955
        h = self.__loader.frames["MemorySetter"].getWindowSize()[1]/686

        self.__fontSize = (baseSize*w*h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__fontU = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__fontI = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)

    def setEntry(self, text):
        self.__stringVar.set(text)

    def disable(self):
        self.__entry.config(state=DISABLED)

    def getEntry(self):
        try:
            return(self.__stringVar.get())
        except Exception as e:
            self.__loader.logger.errorLog(e)

    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.__container!=None and self.stopThread==False:
            if (self.__lastScaleX != self.__loader.frames["MemorySetter"].getScales()[0] or
                    self.__lastScaleY != self.__loader.frames["MemorySetter"].getScales()[1]):
                self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
                self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]


                if self.__frame!=None:
                    try:
                        self.__frame.config(width=self.__w * self.__lastScaleX,
                                             height=self.__h * self.__lastScaleY)
                        self.__setFontSize()

                    except Exception as e:
                        self.__loader.logger.errorLog(e)

                try:
                    self.__label.config(font=self.__fontI)
                    self.__entry.config(font=self.__font)

                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)