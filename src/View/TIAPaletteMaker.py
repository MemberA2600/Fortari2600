from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from SubMenuFrame import SubMenuFrame
from tkinter import *
import re
from time import sleep


class TIAPaletteMaker:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.dead = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*18)

        self.__focused = None

        self.__screenSize = self.__loader.screenSize

        self.__colorLines = []
        import random
        base = random.randint(0,23)*10

        for num in range(0, 20):
            i = (num*2)+base
            if i>254:
                i-=256
            x = hex(i)[2:]
            if len(x)==1:
                x="0"+x
            self.__colorLines.append("$"+x)

        self.__window = SubMenu(self.__loader, "colorPalette", self.__screenSize[0] / 1.80, self.__screenSize[1] / 2 - 45,
                           None, self.__addElements)
        self.dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.75), False, False, False)

        self.__frame1 = SubMenuFrame(self.__loader, self.__topLevel, self.__topLevelWindow,
                                     self.__topLevel.getTopLevelDimensions()[0]*0.5)

        self.__title = SubMenuLabel(self.__frame1.getFrame(),
                                       self.__loader,
                                       "preview",
                                       self.__smallFont)

        self.__forDraw = Frame(self.__frame1.getFrame(), bg="black", width=9999999, height=999999)
        self.__forDraw.pack_propagate(False)
        self.__forDraw.pack(side=BOTTOM, fill=BOTH, anchor=S)
        self.__rows = []


        for num in range(0, 20):
            self.__rows.append({})
            temp = 0
            while(temp < 1):
                temp=int(self.__forDraw.winfo_height() / 20)
            frame = Frame(self.__forDraw, width=999999, height=temp)
            frame.pack_propagate(False)
            frame.place(x=0, y=temp*num)

            sv = StringVar()
            sv.set(self.__colorLines[num])
            entry = Entry(self.__forDraw, width=3, font=self.__smallFont, textvariable=sv,
                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                          bg = self.__loader.colorPalettes.getColor("boxBackNormal")
            )
            #entry.pack_propagate(False)
            entry.place(x=0, y=int(self.__forDraw.winfo_height()/20)*num)
            entry.bind("<KeyRelease>", self.keyReleased)
            entry.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
            entry.bind("<FocusOut>", self.__loader.mainWindow.focusOut)
            entry.bind("<FocusIn>", self.focusIn)
            entry.bind("<FocusOut>", self.focusOut)

            self.__rows[num]["frame"] = frame
            self.__rows[num]["sv"] = sv
            self.__rows[num]["entry"] = entry

        self.__setColors()
        self.__frame2 = SubMenuFrame(self.__loader, self.__topLevel, self.__topLevelWindow,
                                     self.__topLevel.getTopLevelDimensions()[0]*0.5)

        self.__title2 = SubMenuLabel(self.__frame2.getFrame(),
                                       self.__loader,
                                       "colorPicker",
                                       self.__smallFont)

        self.__colors = Frame(self.__frame2.getFrame(), width=999999999, height=round(self.__frame2.getFrame().winfo_height()*0.40))
        self.__colors.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__colors.pack_propagate(False)
        self.__colors.pack(side=TOP, fill=X, anchor=S)

        baseX = 0
        while (baseX == 0) :
            baseX = round(self.__colors.winfo_width()/16)
            baseY = baseX

        self.__pickerButtons = []
        counter = 0
        for color in self.__loader.colorDict.TIAColors.keys():


            button = Button(self.__colors, width=baseX, height=1)
            button.config(bg=self.__loader.colorDict.getHEXValueFromTIA(color), fg=self.__loader.colorDict.getHEXValueFromTIA(color))
            button.config(font=self.__smallFont)
            button.config(text=color)
            button.config(activebackground=self.__loader.colorDict.getHEXValueFromTIA(color))

            button.pack_propagate(False)
            button.place(x=counter//8*baseX, y=counter%8*baseY)
            button.bind("<Button-1>", self.copyColor)

            counter+=1

        self.__otherFrame = Frame(self.__frame2.getFrame(), width=999999999, height=round(self.__frame2.getFrame().winfo_height()*0.60))
        self.__otherFrame.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__otherFrame.pack_propagate(False)
        self.__otherFrame.pack(side=BOTTOM, fill=X, anchor=S)


    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None

    def copyColor(self, event):
        try:
            self.focused.delete(0, END)
            self.focused.insert(INSERT, event.widget.cget("text"))
            for num in range(0,20):
                if self.focused == self.__rows[num]["entry"]:
                    self.__colorLines[num] = self.__rows[num]["sv"].get().lower()

                    self.__rows[num]["frame"].config(
                        bg=self.__loader.colorDict.getHEXValueFromTIA(self.__colorLines[num]))
        except:
            pass

    def keyReleased(self, event):
        for num in range(0,20):
            if event.widget == self.__rows[num]["entry"]:
                error = True
                if re.findall(r"^\$[0-9a-eA-E][02468aceACE]$", self.__rows[num]["sv"].get()):

                    error = False
                    self.__colorLines[num] = self.__rows[num]["sv"].get().lower()

                    self.__rows[num]["frame"].config(
                        bg=self.__loader.colorDict.getHEXValueFromTIA(self.__colorLines[num]))
                elif len(self.__rows[num]["sv"].get())>3:

                    self.__rows[num]["sv"].set(self.__rows[num]["sv"].get()[:3])

                if error:
                    self.__rows[num]["entry"].config(
                        fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                        bg=self.__loader.colorPalettes.getColor("boxBackUnSaved")
                    )
                else:
                    self.__rows[num]["entry"].config(
                        fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                        bg=self.__loader.colorPalettes.getColor("boxBackNormal")
                    )

    def __setColors(self):
        for num in range(0, 20):
            #print(self.__colorLines[num],
            #      self.__loader.colorDict.TIAColors[self.__colorLines[num]].red,
            #      self.__loader.colorDict.TIAColors[self.__colorLines[num]].blue,
            #      self.__loader.colorDict.TIAColors[self.__colorLines[num]].green,
            #      self.__loader.colorDict.getHEXValueFromTIA(self.__colorLines[num]))
            self.__rows[num]["frame"].config(bg=self.__loader.colorDict.getHEXValueFromTIA(self.__colorLines[num]))
