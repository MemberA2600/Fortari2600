from tkinter import *

class MusicBankFrameEntry:

    def __init__(self, loader, frame, topLevel, banks,
                 num, focusIn, focusOut, font, errorCounters,
                 bankEntries, artistData):
        self.__loader = loader
        self.__colors = self.__loader.colorPalettes
        self.__banks = banks
        self.__bankNum = num
        self.__virtualMemory = self.__loader.virtualMemory
        self.__errorCounters = errorCounters
        self.__bankEntries = bankEntries

        self.__artistName = artistData[0]
        self.__songTitle = artistData[1]

        self.__bankEntries["bank"+str(num+1)] = self

        self.focusIn = focusIn
        self.focusOut = focusOut

        self.__container = Frame(frame, width=round(topLevel.getTopLevelDimensions()[0]*0.5*0.15),
                                    height=round(topLevel.getTopLevelDimensions()[1]*0.03),
                                   bg=self.__colors.getColor("window"))
        self.__container.pack_propagate(False)
        self.__container.pack(side=LEFT, fill=Y)

        self.__value = StringVar()
        self.__value.set(str(self.__banks[self.__bankNum]))

        self.__entry = Entry(self.__container, name="bank"+str(num+1),
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999999,
                                        textvariable=self.__value,
                                        justify=CENTER,
                                        font=font
                                        )

        self.__entry.pack_propagate(False)
        self.__entry.pack(fill=BOTH)

        self.__entry.bind("<FocusIn>", self.focusIn)
        self.__entry.bind("<FocusOut>", self.__checkBank)
        self.__entry.bind("<KeyRelease>", self.__checkBank)

    def getValue(self):
        return(int(self.__value.get()))

    def setValue(self, val):
        self.__value.set(str(val))

    def __checkBank(self, event):
        if "FocusOut" in str(event):
            self.focusOut(event)
        name = str(event.widget).split(".")[-1]
        num = 0

        freeBanks = self.__virtualMemory.getBanksAvailableForLocking()

        entries = self.__bankEntries

        try:
            num = int(entries[name].getValue())
        except:
            event.widget.config(
                bg = self.__colors.getColor("boxBackUnSaved"),
                fg = self.__colors.getColor("boxFontUnSaved")
            )

            self.__errorCounters[name] = 1
            return

        self.__errorCounters[name] = 0
        if (    num<3 or num>8
                or self.bankEQ(entries) == True
                or (int(entries[name].getValue()) not in freeBanks)):
            for changeNum in range(3,8):
                if changeNum in freeBanks:
                    entries[name].setValue(str(changeNum))
                    return

                title = (self.__artistName.get() + "_-_" + self.__songTitle.get()).replace(" ", "_")
                if self.__loader.virtualMemory.locks["bank"+str(changeNum)].name == title:
                    entries[name].setValue(str(changeNum))
                    return

        self.__loader.fileDialogs.displayError("bankLockError", "bankLockErrorMessage", None, None)

    def bankEQ(self, entries):
        for b1 in range(1,5):
            for b2 in range(1, 5):
                if (int(entries["bank"+str(b1)].getValue()) == int(entries["bank"+str(b2)].getValue())):
                    return (True)

        return(False)