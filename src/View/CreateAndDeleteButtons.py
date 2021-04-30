from tkinter import *
from threading import *

class CreateAndDeleteButtons:

    def __init__(self, loader, container, function):

        self.__loader = loader
        self.__container = container

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        self.__w = self.__container.winfo_width()/4

        baseSize=14
        self.__fontSize = ((self.__loader.screenSize[0]/1350) *
                            (self.__loader.screenSize[1]/1100) * baseSize
                           )

        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)

        self.__frame = Frame(self.__container, width=self.__w)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=LEFT, anchor=SW, fill=Y)

        self.__buttonCreate= Button(self.__frame, width=round(self.__frame.winfo_width()/2),
                            font=self.__font, text=self.__setText("create"),
                                    state=DISABLED)
        self.__buttonCreate.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonCreate.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__buttonDelete= Button(self.__frame, width=round(self.__frame.winfo_width()/2),
                            font=self.__font, text=self.__setText("delete"),
                                    state=DISABLED)
        self.__buttonDelete.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonDelete.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__buttonDelete.pack(side=BOTTOM, anchor=S)
        self.__buttonCreate.pack(side=BOTTOM, anchor=S)

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

        if function!=None:
            self.__function = function
            c = Thread(target=self.__function, args=[self.__buttonCreate, self.__buttonDelete])
            c.daemon=True
            c.start()

    def __setText(self, txt):
        return(self.__loader.dictionaries.getWordFromCurrentLanguage(txt))



    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__container != None:
            if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastScaleY != self.__loader.mainWindow.getScales()[1]):
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                self.__font = self.__loader.fontManager.getFont(round(self.__fontSize*
                                                                      self.__lastScaleY*
                                                                      self.__lastScaleX
                                                                      ), False, False, False)

                if self.__frame != None:
                    try:
                        self.__frame.config(width=self.__w * self.__lastScaleX)
                        self.__buttonCreate.config(font=self.__font,
                                                   width=round(self.__frame.winfo_width()/2*
                                                   self.__lastScaleX*
                                                    self.__lastScaleY)
                                                   )
                        self.__buttonDelete.config(font=self.__font,
                                                   width=round(self.__frame.winfo_width()/2*
                                                   self.__lastScaleX*
                                                    self.__lastScaleY)
                                                   )
                    except Exception as e:
                        self.__loader.logger.errorLog(e)

            sleep(0.04)