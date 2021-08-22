from tkinter import *

class LockFrame:

    def __init__(self, loader, window, masterFrame, fontManager, ):
        self.__loader = loader
        self.__window = window
        self.__masterFrame = masterFrame
        self.__fontManager = fontManager

        self.stopThread = False
        #self.__loader.stopThreads.append(self)

        self.__frame = Frame(self.__masterFrame.getFrame(), width=99999, height=99999)

        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.__frame.config(bg="red") # testing only

        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.pack(side=BOTTOM, anchor=SE, fill=BOTH)

        self.createLabels()

        self.__scaleLastX = self.__window.getScales()[0]
        self.__scaleLastY = self.__window.getScales()[1]

        self.__button = Button(self.__frame, width=99999, bg=self.__loader.colorPalettes.getColor("window"),
                               text=self.__loader.dictionaries.getWordFromCurrentLanguage("lockButton"),
                               command = self.openWindow)

        if len(self.__loader.virtualMemory.kernel_types)>1:
            self.__button2 = Button(self.__frame, width=99999, bg=self.__loader.colorPalettes.getColor("window"),
                               text=self.__loader.dictionaries.getWordFromCurrentLanguage("changeKernel"),
                               command = self.openWindow2)
            self.__button2.pack(side=BOTTOM, fill=X, anchor=SW)

        self.setButtonFont()

        self.__button.pack(side=BOTTOM, fill=X, anchor=SW)


        self.__locks = []
        self.saveLocks()

        from threading import Thread
        t = Thread(target=self.resize)
        t.daemon = True
        t.start()

        l = Thread(target=self.locker)
        l.daemon = True
        l.start()

    def getFrame(self):
        return(self.__frame)

    def saveLocks(self):
        for item in self.__loader.virtualMemory.locks:
            self.__locks.append(item)


    def setButtonFont(self):
        self.__fontSize = int(self.__loader.screenSize[0]/1300 * self.__loader.screenSize[1]/1050*10
                              *self.__scaleLastX*self.__scaleLastY)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.9), False, False, False)
        self.__button.config(font=self.__smallFont)
        if len(self.__loader.virtualMemory.kernel_types)>1:
            self.__button2.config(font=self.__smallFont)


    def createLabels(self):
        self.getImgs()
        self.__labels = []
        for num in range(1, 7):
            self.createLabel(num)

    def getImgs(self):
        while True:
            try:
                self.__lockOn = self.__loader.io.getImg("lockClosed", round(self.__frame.winfo_width()/4)-5)
                self.__lockOff = self.__loader.io.getImg("lockOpened", round(self.__frame.winfo_width()/4)-5)
                break
            except Exception as e:
                self.__loader.logger.errorLog(e)
                continue

    def setImg(self, label, labelNum):
        if self.__loader.virtualMemory.locks["bank"+str(labelNum)] == "":
            label.config(image = self.__lockOff)
        else:
            label.config(image = self.__lockOn)

    def openWindow(self):
        from LockManagerWindow import LockManagerWindow
        w = LockManagerWindow(self.__loader)

    def openWindow2(self):
        from KernelChanger import KernelChanger
        w = KernelChanger(self.__loader)


    def createLabel(self, num):
        self.__labels.append(Label(self.__frame, image = self.__lockOn))
        self.__labels[num-1].config(bg=self.__loader.colorPalettes.getColor("window"))
        self.setImg(self.__labels[num-1], num+2)
        self.__labels[num - 1].place(
            x= ((num-1)%3) * self.__frame.winfo_width()/3,
            y= ((num-1)//3) * self.__frame.winfo_width()/3+5
        )

    def resize(self):
        from time import sleep
        while self.__window.dead==False and self.stopThread==False:
            if (self.__scaleLastX != self.__window.getScales()[0] or
                    self.__scaleLastY != self.__window.getScales()[1]
                ):
                self.__scaleLastX = self.__window.getScales()[0]
                self.__scaleLastY = self.__window.getScales()[1]
                self.createLabels()
                self.setButtonFont()
                for num in range(1, 7):
                    self.__locks[num - 1] = "LOL"
                sleep(0.01)
                continue

            sleep(0.04)

    def locker(self):
        from time import sleep
        while self.__window.dead==False and self.stopThread==False:

            state=NORMAL
            if self.__window.projectPath == None:
                state=DISABLED
            if len(self.__loader.virtualMemory.kernel_types) > 1:
                self.__button2.config(state=state)
            self.__button.config(state=state)
            for item in self.__labels:
                try:
                    item.config(state=state)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            for num in range(1,7):
                if self.__locks[num-1] != self.__loader.virtualMemory.locks["bank"+str(num+2)]:
                    self.__locks[num-1] = self.__loader.virtualMemory.locks["bank"+str(num+2)]
                    if self.__locks[num-1] == None:
                        self.__labels[num-1].config(image = self.__lockOff)
                    else:
                        self.__labels[num-1].config(image=self.__lockOn)

            #import random
            #num = random.randint(2,8)
            #self.__loader.virtualMemory.locks["bank" + str(num)] = "meh"

            sleep(0.5)