from tkinter import *
from threading import Thread

class NewListBoxInFrame():

    def __init__(self, name, loader, container, data, function, side):
        self.__name = name
        self.__loader = loader

        self.__loader.listBoxes[name] = self

        self.__container = container

        self.stopThread = False

        if function!=None:
            self.__function = function

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        try:
            self.__originalW = self.__container.getFrameSize()[0]
            self.__originalH = self.__container.getFrameSize()[1]
            self.__frame = Frame(self.__container.getFrame())
        except:
            try:
                self.__originalW = self.__container.getTopLevelDimensions()[0]
                self.__originalH = self.__container.getTopLevelDimensions()[1]
                self.__frame = Frame(self.__container.getTopLevel())
            except:
                self.__originalW = self.__container.winfo_width()
                self.__originalH = self.__container.winfo_height()
                self.__frame = Frame(self.__container)

        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frame.config(width=100000, height=100000)

        self.__frame.pack_propagate(False)
        self.__frame.pack(side=side, fill=BOTH)
        self.__first = True

        self.__scrollBar = Scrollbar(self.__frame)
        self.__listBox = Listbox(   self.__frame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__scrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection = False
                                    )
        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.pack_propagate(False)


        self.__scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__listBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__scrollBar.config(command=self.__listBox.yview)

        align = Thread(target=self.dinamicallyAlign)
        align.daemon = True
        align.start()
        self.__setFont()
        self.__listOfItems = []

        self.filler(data)

        if name !="bankBox" and name != "sectionBox":
            #self.__loader.destroyable.append(self)
            self.__loader.destroyable.append(self.__listBox)
            self.__loader.destroyable.append(self.__scrollBar)
        if function != None:
            self.__function = function
            f = Thread(target=self.__callCheckFunction)
            f.daemon = True
            f.start()

    def getScales(self):
        try:
            self.__newW = self.__container.getFrameSize()[0]
            self.__newH = self.__container.getFrameSize()[1]
        except:
            try:
                self.__newW = self.__container.getTopLevelDimensions()[0]
                self.__newH = self.__container.getTopLevelDimensions()[1]
            except:
                self.__newW = self.__container.winfo_width()
                self.__newH = self.__container.winfo_height()



        return (
            self.__newW / self.__originalW,
            self.__newH / self.__originalH
        )

    def getListBoxAndScrollBar(self):
        return(self.__listBox, self.__scrollBar)

    def getSize(self):
        return(self.__frame.winfo_width(), self.__frame.winfo_height())

    def filler(self, data):
        try:
            self.data = data
            self.__listBox.delete(0, END)
            for d in data:
                self.__listBox.insert(END, d)
            self.__frame.pack(side=LEFT, anchor=SE, fill=Y)
            if len(data)>0:
                self.__listBox.select_set(0)
        except Exception as e:
            self.__loader.logger.errorLog(e)

    def __setFont(self):
        self.__fontSize = 18*(self.__originalW*self.getScales()[0]/320)*(self.__originalH*self.getScales()[1]/210)
        if self.__fontSize<8:
            self.__fontSize=8
        self.__font = self.__loader.fontManager.getFont(self.__fontSize, False, False, False)
        self.__listBox.config(font=self.__font)


    def __callCheckFunction(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.stopThread==False:
            self.__function(self.__listBox)
            sleep(0.1)

    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False or self.__first == True and self.stopThread==False:
            try:
                if (self.__lastScaleX == self.__loader.mainWindow.getScales()[0]
                        and self.__lastScaleY == self.__loader.mainWindow.getScales()[1]):

                    sleep(0.05)
                    continue
                self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                self.__setFont()
                self.__first = False
            except Exception as e:
                self.__loader.logger.errorLog(e)

            sleep(0.02)

    def getSelectedName(self):
        from time import sleep
        trial = 6
        while trial>0:
            try:
                return (self.data[self.__listBox.curselection()[0]])
            except:
                sleep(0.1)
                trial-=1