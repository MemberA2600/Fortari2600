from tkinter import *
from threading import *

class CreateAndDeleteButtons:

    def __init__(self, loader, container, name, function, buttonPressedFunction1, buttonPressedFunction2):

        self.__loader = loader
        self.__container = container
        self.__name = name
        self.__buttonPressedFunction1 = buttonPressedFunction1
        self.__buttonPressedFunction2 = buttonPressedFunction2

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
        self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

        self.__w = self.__container.winfo_width()/4
        self.__h = self.__container.winfo_height()

        self.__setFont()

        self.__frame = Frame(self.__container, width=self.__w)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=LEFT, anchor=SW, fill=Y)

        self.__buttonCreate= Button(self.__frame, width=round(self.__frame.winfo_width()/2),
                            font=self.__font, text=self.__setText("create"),
                                    state=DISABLED)
        self.__buttonCreate.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonCreate.config(fg=self.__loader.colorPalettes.getColor("font"))
        if self.__buttonPressedFunction1 != None:
            self.__buttonCreate.config(command=self.__buttonPressedFunction1)

        self.__buttonDelete= Button(self.__frame, width=round(self.__frame.winfo_width()/2),
                            font=self.__font, text=self.__setText("delete"),
                                    state=DISABLED)
        self.__buttonDelete.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonDelete.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__buttonDelete.pack(side=BOTTOM, anchor=S, fill=X)
        self.__buttonCreate.pack(side=BOTTOM, anchor=S, fill=X)
        if self.__buttonPressedFunction2 != None:
            self.__buttonDelete.config(command=self.__buttonPressedFunction2)

        self.__others = []

        self.__loader.destroyable.append(self.__buttonCreate)
        self.__loader.destroyable.append(self.__buttonDelete)

        if self.__name == "variable":
            self.__addressLabel = Label(self.__frame, font=self.__smallFont,
                                        text = self.__loader.dictionaries.getWordFromCurrentLanguage("varAddress"))
            self.__addressLabel.config(bg = self.__loader.colorPalettes.getColor("window"))
            self.__addressLabel.config(fg = self.__loader.colorPalettes.getColor("font"))
            self.__addressLabel.pack(side=TOP, anchor=NW)

            self.__addressVar = StringVar()
            self.__addressEntry = Entry(self.__frame, font=self.__smallFont,
                                        textvariable=self.__addressVar, state=DISABLED)
            self.__addressEntry.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"))
            self.__addressEntry.config(fg = self.__loader.colorPalettes.getColor("boxFontNormal"))
            self.__addressEntry.pack(side=TOP, anchor=NW, fill=X)

            self.__others.append(self.__addressEntry)
            self.__others.append(self.__addressVar)

            self.__bitsLabel = Label(self.__frame, font=self.__smallFont,
                                        text = self.__loader.dictionaries.getWordFromCurrentLanguage("usedBits"))
            self.__bitsLabel.config(bg = self.__loader.colorPalettes.getColor("window"))
            self.__bitsLabel.config(fg = self.__loader.colorPalettes.getColor("font"))
            self.__bitsLabel.pack(side=TOP, anchor=NW)

            self.__bitsVar = StringVar()
            self.__bitsEntry = Entry(self.__frame, font=self.__smallFont,
                                        textvariable=self.__bitsVar, state=DISABLED)
            self.__bitsEntry.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"))
            self.__bitsEntry.config(fg = self.__loader.colorPalettes.getColor("boxFontNormal"))
            self.__bitsEntry.pack(side=TOP, anchor=NW, fill=X)

            self.__others.append(self.__bitsEntry)
            self.__others.append(self.__bitsVar)
        elif self.__name == "array":
            self.__anotherFrame = Frame(self.__frame, width=self.__w, height=round(self.__h/5))
            self.__anotherFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
            self.__anotherFrame.pack_propagate(False)

            self.__anotherFrame.pack(side=BOTTOM, anchor=CENTER, fill=BOTH)

            self.__buttonAddVar = Button(self.__anotherFrame,
                                         font=self.__bigFont, text="<<",
                                         state=DISABLED)
            self.__buttonAddVar.config(bg=self.__loader.colorPalettes.getColor("window"))
            self.__buttonAddVar.config(fg=self.__loader.colorPalettes.getColor("font"))

            self.__buttonAddVar.config(command=self.__buttonPressedFunction1)


            self.__buttonDelVar = Button(self.__anotherFrame,
                                         font=self.__bigFont, text=">>",
                                         state=DISABLED)
            self.__buttonDelVar.config(bg=self.__loader.colorPalettes.getColor("window"))
            self.__buttonDelVar.config(fg=self.__loader.colorPalettes.getColor("font"))

            self.__buttonDelVar.config(command=self.__buttonPressedFunction1)

            self.__buttonAddVar.pack(side=LEFT, anchor=NW, fill=X)
            self.__buttonDelVar.pack(side=LEFT, anchor=NE, fill=X)

            self.__loader.destroyable.append(self.__buttonAddVar)
            self.__loader.destroyable.append(self.__buttonDelVar)

            self.__others.extend([self.__buttonAddVar, self.__buttonDelVar])

        t = Thread(target=self.resize)
        t.daemon=True
        t.start()

        if function!=None:
            self.__function = function
            c = Thread(target=self.__function, args=[self.__buttonCreate, self.__buttonDelete, self.__others])
            c.daemon=True
            c.start()

    def __setFont(self):
        baseSize=12
        w = self.__loader.frames["MemorySetter"].getWindowSize()[0]/955
        h = self.__loader.frames["MemorySetter"].getWindowSize()[1]/686

        self.__fontSize = (baseSize*w*h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize*0.9), False, False, False)
        self.__bigFont = self.__loader.fontManager.getFont(round(self.__fontSize*1.25), False, False, False)

        self.__smallFont = self.__loader.fontManager.getFont(round(self.__fontSize*0.75), False, False, False)

    def __setText(self, txt):
        return(self.__loader.dictionaries.getWordFromCurrentLanguage(txt))

    def resize(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__container != None and self.stopThread==False:
            if (self.__lastScaleX != self.__loader.frames["MemorySetter"].getScales()[0] or
                    self.__lastScaleY != self.__loader.frames["MemorySetter"].getScales()[1]):
                self.__lastScaleX = self.__loader.frames["MemorySetter"].getScales()[0]
                self.__lastScaleY = self.__loader.frames["MemorySetter"].getScales()[1]

                self.__setFont()
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
                        if self.__name == "variable":
                            self.__addressLabel.config(font=self.__smallFont)
                            self.__addressEntry.config(font=self.__smallFont)

                            self.__bitsLabel.config(font=self.__smallFont)
                            self.__bitsEntry.config(font=self.__smallFont)
                        elif self.__name == "array":
                            self.__anotherFrame.config(
                                width=self.__w*self.__lastScaleX,
                                height=round(self.__h / 5)*self.__lastScaleY)


                    except Exception as e:
                        self.__loader.logger.errorLog(e)

            sleep(0.04)