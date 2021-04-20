from tkinter import *
from threading import Thread

class ListBoxInFrame:

    def __init__(self, name, loader, container, fontmanager, multi, data, function):

        self.__name = name
        self.__data = data
        self.__loader = loader
        self.__container = container
        self.__fontManager = fontmanager
        w = self.__loader.mainWindow.getWindowSize()
        self.__baseWidth=w[0]/10*multi
        self.__baseHeight=self.__container.getFrameSize()[1]

        self.__frame = Frame(self.__container.getFrame(), width=self.__baseWidth,
                             height=self.__container.getFrameSize()[1])
        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        #self.__frame.config(bg="red")
        self.__scrollBar = Scrollbar(self.__frame)
        self.__listBox = Listbox(   self.__frame, width=10,
                                    height=1000,
                                    yscrollcommand=self.__scrollBar.set,
                                    selectmode=BROWSE,
                                    )
        self.__listBox.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__scrollBar.pack(side=LEFT, anchor=W, fill=Y)
        self.__scrollBar.config(command=self.__listBox.yview)


        align = Thread(target=self.dinamicallyAlign)
        align.daemon = True
        align.start()
        self.__setFont()
        self.__listOfItems = []

        for d in data:
            self.__listBox.insert(END, d)
        self.__listBox.select_set(0)
        self.__frame.pack(side=LEFT, anchor=SE, fill=Y)
        self.sizeListBox()
        self.__loader.listBoxes[name] = self
        if function != None:
            self.__function = function
            f = Thread(target=self.__callCheckFunction)
            f.daemon = True
            f.start()

    def getSelectedName(self):
        return(self.__data[self.__listBox.curselection()[0]])

    def getSize(self):
        return(self.__frame.winfo_width(), self.__frame.winfo_height())

    def sizeListBox(self):
        self.__listBox.config(width=self.__fontManager.getCharacterLenghtFromPixels(
            self.__font, self.getSize()[0]-13
        ))

    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False:
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
            sleep(0.02)

    def __setFont(self):
        self.__font = self.__fontManager.getFont("small", False, False, False)
        self.__listBox.config(font=self.__font)


    def __callCheckFunction(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False:
            self.__function(self.__listBox)
            sleep(0.1)

