from tkinter import *

class HexEntry:

    def __init__(self, loader, frame, colors, colorDict, font, colorConstans, num, focusIn, focusOut):

        self.__textVar = StringVar()

        if colorConstans != None:
            self.__textVar.set(colorConstans[num])
        else:
            self.__textVar.set("$00")

        self.__num = num

        self.__loader = loader
        self.__colors = colors
        self.__colorConstans = colorConstans
        self.__colorDict = colorDict

        self.__entry = Entry(frame,
                            bg=self.__colors.getColor("boxBackNormal"),
                            fg=self.__colors.getColor("boxFontNormal"),
                            width=9999999,
                            textvariable=self.__textVar,
                            justify=CENTER,
                            font=font
                            )

        self.__entry.pack_propagate(False)
        self.__entry.pack(fill=BOTH)

        self.__entry.bind("<FocusOut>", self.__checkColorEntry)
        self.__entry.bind("<KeyRelease>", self.__checkColorEntry)

        self.__secondaryOut = None

        if focusIn != None:
            self.__entry.bind("<FocusIn>", focusIn)
        if focusOut != None:
            self.__secondaryOut = focusOut

        self.setColorOfEntry()

    def changeState(self, state):
        self.__entry.config(state = state)

    def getEntry(self):
        return self.__entry

    def setColorOfEntry(self):

        color1 = self.__colorDict.getHEXValueFromTIA(self.__textVar.get())

        num = int("0x"+self.__textVar.get()[2], 16)
        if num>8:
            num = self.__textVar.get()[:2]+hex(num-6).replace("0x","")
        else:
            num = self.__textVar.get()[:2]+hex(num+6).replace("0x","")

        color2 = self.__colorDict.getHEXValueFromTIA(num)
        self.__entry.config(bg=color1, fg=color2)

    def __checkColorEntry(self, event):

        if (len(self.__textVar.get()))<3:
            self.setInValid()
            return
        elif (len(self.__textVar.get()))>3:
            self.__textVar.set(self.__textVar.get()[:3])

        if self.__textVar.get()[0]!="$":
            self.setInValid()
            return

        try:
            num = int(self.__textVar.get().replace("$", "0x"), 16)
        except:
            self.setInValid()
            return

        self.setColorOfEntry()
        if  self.__colorConstans!=None:
            self.__colorConstans[self.__num] = self.__textVar.get()
        if self.__secondaryOut != None:
            self.__secondaryOut(event)

    def setInValid(self):
        self.__entry.config(
            bg = self.__loader.colorPalettes.getColor("boxBackUnSaved"),
            fg = self.__loader.colorPalettes.getColor("boxFontUnSaved")
        )

    def setValue(self, val):
        self.__textVar.set(val)
        self.setColorOfEntry()

    def getValue(self):
        return(self.__textVar.get())