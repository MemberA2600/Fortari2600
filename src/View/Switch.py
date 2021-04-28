from tkinter import *
from PIL import Image as IMAGE, ImageTk

class Switch:

    def __init__(self, loader, master, window, bankNum, banks):

        self.__loader = loader
        self.__master = master
        self.__window = window
        self.__bankNum = bankNum
        self.__banks = banks

        #self.__fontSize = int(self.__loader.screenSize[0]/1300 * self.__loader.screenSize[1]/1050*14)
        self.__normalFont = self.__loader.fontManager.getFont("normal", False, False, False)
        self.__smallFont = self.__loader.fontManager.getFont("small", False, False, False)


        self.__frame = Frame(self.__window, width=self.__window.winfo_width()/7)
        self.__frame.config(bg="black")
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=LEFT, anchor=NW, fill=Y)

        self.__bankLabel = Label(self.__frame,
                                 bg = "black",
                                 fg = "darkred",
                                 font = self.__normalFont,
                                 text = "Bank"+str(self.__bankNum)
                                 )
        self.__bankLabel.pack(side=TOP, anchor=N)

        self.lockLabel = Label(self.__frame,
                                 bg = "black",
                                 fg = "orangered",
                                 font = self.__smallFont,
                                 text = self.__loader.virtualMemory.locks["bank"+str(self.__bankNum)]
                                 )
        self.lockLabel.pack(side=TOP, anchor=N)

        self.__w = round(self.__frame.winfo_width()/2)
        self.__h = round(self.__w*1.72)

        while True:
            try:
                self.__imgLocked = ImageTk.PhotoImage(IMAGE.open("others/img/switchOn.png").resize((self.__w, self.__h), IMAGE.ANTIALIAS))
                self.__imgUnLocked = ImageTk.PhotoImage(IMAGE.open("others/img/switchOff.png").resize((self.__w, self.__h), IMAGE.ANTIALIAS))
                break
            except Exception as e:

                self.__loader.logger.errorLog(e)


        self.createSwitch()

        if bankNum == 5:
            self.__endButton = Button(self.__frame, bg="black", fg="orangered", font=self.__normalFont,
                                      text=self.__loader.dictionaries.getWordFromCurrentLanguage("exit"),
                                      command=self.killFrame, activebackground="darkred", relief=FLAT)
            self.__endButton.pack(side=BOTTOM, anchor=CENTER, fill=X)


    def createSwitch(self):
        try:
            self.__switch.destroy()
        except Exception as e:
            self.__loader.logger.errorLog(e)

        if self.__loader.virtualMemory.locks["bank"+str(self.__bankNum)]!="":
            self.__switch = Button(self.__frame, relief=FLAT, bg="black", image=self.__imgLocked,
                                   activebackground="darkred", command=self.removeLock)
            self.__switch.pack(side=TOP, anchor=N)
        else:
            self.__switch = Label(self.__frame, bg="black", image=self.__imgUnLocked)
            self.__switch.pack(side=TOP, anchor=N)

    def removeLock(self):
        text = self.__loader.virtualMemory.locks["bank"+str(self.__bankNum)]
        self.__loader.soundPlayer.playSound("switchOff")
        for num in range(2,9):
            bank = "bank"+str(num)
            if self.__loader.virtualMemory.locks[bank] == text:
                self.__loader.virtualMemory.locks[bank] = ""
                self.__banks[num-2].createSwitch()
                self.__banks[num-2].lockLabel.config(text = "")

    def killFrame(self):
        self.__loader.virtualMemory.createTheBankConfigFromMemory()
        self.__window.destroy()