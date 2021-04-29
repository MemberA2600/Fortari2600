from tkinter import *
from threading import Thread
from tkinter.font import Font

class SideFrameListBoxWithButtonAndLabel:

    def __init__(self, loader, frame, baseSize, name, percent,
                 fillFunction, buttonFunction):

        self.__loader = loader
        self.__frame = frame
        self.__fillFunction = fillFunction
        self.__buttonFunction = buttonFunction

        self.__w = self.__frame.winfo_width()
        self.__h = round(self.__frame.winfo_height()*percent)

        self.__percent = percent

        self.__newFrame = Frame(self.__frame, width=self.__w, height=self.__h)
        self.__newFrame.config(bg=self.__loader.colorPalettes.getColor("window"))

        self.__newFrame.pack_propagate(False)
        self.__newFrame.pack(side=TOP, anchor=N)


        self.__fontManager = loader.fontManager

        self.__fontNormalSize = ((self.__loader.screenSize[0] / 1350) *
                                 (self.__loader.screenSize[1] / 1100) * baseSize
                                 )

        self.__fontSmallSize = ((self.__loader.screenSize[0] / 1350) *
                                (self.__loader.screenSize[1] / 1100) * baseSize * 0.75
                                )

        self.__fontExtraSmallSize = ((self.__loader.screenSize[0] / 1350) *
                                (self.__loader.screenSize[1] / 1100) * baseSize * 0.65
                                )


        self.__lastX = self.__loader.mainWindow.getScales()[0]
        self.__lastY = self.__loader.mainWindow.getScales()[1]

        self.setFonts()

        self.__label = Label(self.__newFrame, font=self.__fontNormal,
                                      text=self.__loader.dictionaries.getWordFromCurrentLanguage(name))

        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__label.pack(side=TOP, anchor=NW)

        self.__scrollBar = Scrollbar(self.__newFrame)

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

        self.data=[]
        self.refiller()
        self.__loader.destroyable.append(self.__listBox)
        self.__listBox.select_clear

    def getSelectedName(self):
        return(self.data[self.__listBox.curselection()[0]])

    def getListBoxAndScrollBar(self):
        return(self.__listBox, self.__scrollBar)

    def refiller(self):
        self.__fillFunction(self.__listBox, self.data)

    def setSizes(self):
        self.__listBox.config(width=round(self.__w * self.__lastX ),
                              height=round(self.__newFrame.winfo_height() * self.__lastY - self.__fontNormal.metrics(
                                  'linespace') - 10)
                              )

    def setFonts(self):
        self.__fontNormal = self.__loader.fontManager.getFont(
            round(self.__fontNormalSize * self.__lastX * self.__lastY),
            False, False, False)
        self.__fontSmall = self.__loader.fontManager.getFont(round(self.__fontSmallSize * self.__lastX * self.__lastY),
                                                             False, False, False)
        self.__fontExtraSmall = self.__loader.fontManager.getFont(round(self.__fontExtraSmallSize * self.__lastX * self.__lastY),
                                                             False, False, False)

    def scaler(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False:
            if (self.__lastX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastY != self.__loader.mainWindow.getScales()[1]
            ):
                self.__lastX = self.__loader.mainWindow.getScales()[0]
                self.__lastY = self.__loader.mainWindow.getScales()[1]

                self.__newFrame.config(height=self.__h*self.__lastY,
                                       width=self.__w*self.__lastX)


                self.setFonts()
                self.setSizes()

                try:
                    self.__label.config(font=self.__fontNormal)
                    self.__listBox.config(font=self.__fontExtraSmall)

                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(0.04)
