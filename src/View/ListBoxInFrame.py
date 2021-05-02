from tkinter import *
from threading import Thread

class ListBoxInFrame:

    def __init__(self, name, loader, container, fontmanager, multi, data, function):

        self.__name = name
        self.__loader = loader
        self.__container = container
        self.__fontManager = fontmanager
        w = self.__loader.mainWindow.getWindowSize()
        self.__baseWidth=w[0]/10*multi
        self.__baseSize=round(w[0]/1350*w[1]/1100*10)

        try:
            self.__baseHeight=self.__container.getFrameSize()[1]
            self.__frame = Frame(self.__container.getFrame(), width=self.__baseWidth,
                                 height=self.__container.getFrameSize()[1])
        except:
            try:
                self.__baseHeight=self.__container.getTopLevelDimensions()[1]
                self.__frame = Frame(self.__container.getTopLevel(), width=self.__baseWidth,
                                     height=self.__container.getTopLevelDimensions()[1])
            except:

                self.__baseWidth = self.__container.winfo_width()  * multi
                self.__baseHeight=self.__container.winfo_height()
                self.__frame = Frame(self.__container, width=self.__baseWidth,
                                     height=self.__baseHeight)

        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))


        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        #self.__frame.config(bg="red")
        self.__scrollBar = Scrollbar(self.__frame)
        self.__listBox = Listbox(   self.__frame, width=10,
                                    height=1000,
                                    yscrollcommand=self.__scrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection = False
                                    )

        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))


        align = Thread(target=self.dinamicallyAlign)
        align.daemon = True
        align.start()
        self.__setFont()
        self.__listOfItems = []

        self.filler(data)
        self.__loader.listBoxes[name] = self

        if function != None:
            self.__function = function
            f = Thread(target=self.__callCheckFunction)
            f.daemon = True
            f.start()
        self.__listBox.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__scrollBar.pack(side=LEFT, anchor=W, fill=Y)
        self.__scrollBar.config(command=self.__listBox.yview)

        if name !="bankBox" and name != "sectionBox":
            self.__loader.destroyable.append(self.__listBox)
            self.__loader.destroyable.append(self.__scrollBar)

        self.__listBox.after(100, self.tryAgain)

    def tryAgain(self):
        self.__listBox.pack(side=LEFT, anchor=E, fill=BOTH)


    def filler(self, data):
        self.data = data
        self.__listBox.delete(0, END)
        for d in data:
            self.__listBox.insert(END, d)
        self.__frame.pack(side=LEFT, anchor=SE, fill=Y)
        self.sizeListBox()
        if len(data)>0:
            self.__listBox.select_set(0)

    def getSelectedName(self):
        from time import sleep
        trial = 6
        while trial>0:
            try:
                return (self.data[self.__listBox.curselection()[0]])
            except:
                sleep(0.1)
                trial-=1

    def getListBoxAndScrollBar(self):
        return(self.__listBox, self.__scrollBar)

    def getSize(self):
        return(self.__frame.winfo_width(), self.__frame.winfo_height())

    def sizeListBox(self):
        self.__listBox.config(width=self.__fontManager.getCharacterLenghtFromPixels(
            self.__font, self.getSize()[0]-13
        ))



    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False:
            try:
                if (self.__lastScaleX == self.__loader.mainWindow.getScales()[0]
                        and self.__lastScaleY == self.__loader.mainWindow.getScales()[1]):

                    sleep(0.05)
                    continue
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                self.__frame.config(width=round(self.__baseWidth*self.__lastScaleX))
                self.__frame.config(height=round(self.__baseHeight*self.__lastScaleY))

                self.__setFont()
                self.sizeListBox()
            except Exception as e:
                self.__loader.logger.errorLog(e)

            sleep(0.02)

    def __setFont(self):
        self.__font = self.__fontManager.getFont(self.__baseSize, False, False, False)
        self.__listBox.config(font=self.__font)


    def __callCheckFunction(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False:
            self.__function(self.__listBox)
            sleep(0.1)

