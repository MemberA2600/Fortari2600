from tkinter import *

class LockFrame:

    def __init__(self, loader, window, masterFrame):
        self.__loader = loader
        self.__window = window
        self.__masterFrame = masterFrame

        self.__frame = Frame(self.__masterFrame.getFrame(), width=99999, height=99999)

        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.__frame.config(bg="red") # testing only

        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.pack(side=BOTTOM, anchor=SE, fill=BOTH)


        self.createLabels()

        self.__scaleLastX = self.__window.getScales()[0]
        self.__scaleLastY = self.__window.getScales()[1]

        from threading import Thread
        t = Thread(target=self.resize)
        t.daemon = True
        t.start()

    def createLabels(self):
        self.getImgs()
        self.__labels = []
        for num in range(1, 9):
            self.createLabel(num)

    def getImgs(self):
        self.__lockOn = self.__loader.io.getImg("lockClosed", round(self.__frame.winfo_width()/4)-5)
        self.__lockOff = self.__loader.io.getImg("lockOpened", round(self.__frame.winfo_width()/4)-5)

    def setImg(self, label, labelNum):
        if self.__loader.virtualMemory.locks["bank"+str(labelNum)] == "":
            label.config(image = self.__lockOff)
        else:
            label.config(image = self.__lockOn)



    def createLabel(self, num):
        self.__labels.append(Label(self.__frame, image = self.__lockOn))
        self.__labels[num-1].config(bg=self.__loader.colorPalettes.getColor("window"))
        self.setImg(self.__labels[num-1], num)
        self.__labels[num - 1].place(
            x= ((num-1)%4) * self.__frame.winfo_width()/4,
            y= ((num-1)//4) * self.__frame.winfo_width()/4
        )

    def resize(self):
        from time import sleep
        while self.__window.dead==False:
            if (self.__scaleLastX != self.__window.getScales()[0] or
                    self.__scaleLastY != self.__window.getScales()[1]
                ):
                self.__scaleLastX = self.__window.getScales()[0]
                self.__scaleLastY = self.__window.getScales()[1]
                self.createLabels()
                sleep(0.002)
                continue

            sleep(0.04)