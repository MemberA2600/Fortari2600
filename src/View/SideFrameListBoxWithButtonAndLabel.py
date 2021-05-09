from tkinter import *
from threading import Thread
from tkinter.font import Font

class SideFrameListBoxWithButtonAndLabel:

    def __init__(self, loader, frame, baseSize, name, percent,
                 fillFunction, buttonFunction, insertFunction, buttonText):

        self.__baseSize = baseSize
        self.__loader = loader
        self.__frame = frame
        self.__fillFunction = fillFunction
        self.__buttonFunction = buttonFunction
        self.__insertFunction = insertFunction
        self.__buttonText = buttonText

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__w = self.__frame.winfo_width()
        self.__h = round(self.__frame.winfo_height()*percent)

        self.__percent = percent

        self.__newFrame = Frame(self.__frame, width=self.__w, height=self.__h)
        self.__newFrame.config(bg=self.__loader.colorPalettes.getColor("window"))

        self.__newFrame.pack_propagate(False)
        self.__newFrame.pack(side=TOP, anchor=N)


        self.__fontManager = loader.fontManager

        self.__lastX = self.__loader.frames["rightFrame"].getScales()[0]
        self.__lastY = self.__loader.frames["rightFrame"].getScales()[1]

        self.setFonts()

        self.__label = Label(self.__newFrame, font=self.__fontNormal,
                                      text=self.__loader.dictionaries.getWordFromCurrentLanguage(name))

        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__label.pack(side=TOP, anchor=NW)

        self.__scrollBar = Scrollbar(self.__newFrame)

        self.__button = Button(self.__newFrame, text=self.__loader.dictionaries.getWordFromCurrentLanguage(buttonText),
                               font=self.__fontExtraSmall, command=self.command
                               )
        """ 
        if buttonText.startswith == "insert":
            command = self.__insertFunction
        else:
            command = self.__buttonFunction
        """
        self.__button.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__button.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__button.pack(side=BOTTOM, anchor=S, fill=X)

        self.__listBox = Listbox(self.__newFrame,
                                 yscrollcommand=self.__scrollBar.set,
                                 selectmode=BROWSE,
                                 exportselection=False
                                 )
        self.__scrollBar.pack(side=RIGHT, anchor=SW, fill=Y)
        self.__listBox.pack(side=LEFT, anchor=SW)
        self.__listBox.pack_propagate(False)
        self.setSizes()
        self.__loader.listBoxes[name] = self.__listBox

        self.__scrollBar.config(command=self.__listBox.yview)

        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.config(font=self.__fontExtraSmall)

        t = Thread(target=self.scaler)
        t.daemon = True
        t.start()

        self.__loader.destroyable.append(self.__listBox)
#        self.__loader.destroyable.append(self.__scrollBar)

        self.__loader.destroyable.append(self.__button)
        self.data=[]
        self.refiller()
        self.__loader.destroyable.append(self.__listBox)
        #self.__listBox.select_clear()

    def command(self):
        if self.__buttonText.startswith("select"):
            self.__buttonFunction(self.__listBox, self.data)
        else:
            self.__insertFunction(self.__listBox, self.data)

    def getSelectedName(self):
        return(self.data[self.__listBox.curselection()[0]])

    def getListBoxAndScrollBar(self):
        return(self.__listBox, self.__scrollBar)

    def refiller(self):
        self.__fillFunction(self.__listBox, self)

    def setSizes(self):
        if self.__frame!=None and self.__newFrame!=None:
            try:
                if self.__listBox!=None:
                    self.__listBox.config(width=round(self.__w * self.__lastX ),
                                      height=round(self.__newFrame.winfo_height() * self.__lastY - self.__fontNormal.metrics(
                                          'linespace') - 10)
                                      )
            except Exception as e:
                self.__loader.logger.errorLog(e)

    def setFonts(self):
        self.__fontNormalSize = ((self.__frame.winfo_width() / 200) *
                                 (self.__frame.winfo_height()  / 600) * self.__baseSize
                                 )

        self.__fontSmallSize = ((self.__frame.winfo_width()  / 200) *
                                (self.__frame.winfo_height()/ 600) * self.__baseSize * 0.75
                                )

        self.__fontExtraSmallSize = ((self.__frame.winfo_width()  / 200) *
                                     (self.__frame.winfo_height() / 600) * self.__baseSize * 0.65
                                     )


        self.__fontNormal = self.__loader.fontManager.getFont(
            round(self.__fontNormalSize),
            False, False, False)
        self.__fontSmall = self.__loader.fontManager.getFont(round(self.__fontSmallSize),
                                                             False, False, False)
        self.__fontExtraSmall = self.__loader.fontManager.getFont(round(self.__fontExtraSmallSize),
                                                             False, False, False)

    def scaler(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.__frame!=None and self.__newFrame!=None and self.stopThread==False:
            if self.__button != None:
                try:
                    self.getSelectedName()
                    self.__button.config(state=NORMAL)
                except:
                    try:
                        self.__button.config(state=DISABLED)
                    except Exception as e:
                        self.__button.destroy()
                        #self.__loader.logger.errorLog(e)

            if (self.__lastX != self.__loader.frames["rightFrame"].getScales()[0] or
                    self.__lastY != self.__loader.frames["rightFrame"].getScales()[1]
            ):
                self.__lastX = self.__loader.frames["rightFrame"].getScales()[0]
                self.__lastY = self.__loader.frames["rightFrame"].getScales()[1]

                try:
                    self.__newFrame.config(height=self.__h*self.__lastY,
                                       width=self.__w*self.__lastX)
                except Exception as e:
                    self.__loader.logger.errorLog(e)



                self.setFonts()
                self.setSizes()

                try:
                    self.__label.config(font=self.__fontNormal)
                    self.__listBox.config(font=self.__fontExtraSmall)
                    self.__button.config(font=self.__fontSmall)


                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)
