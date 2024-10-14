from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from time import sleep
from copy import deepcopy
from tkinter import scrolledtext
from PIL import ImageTk, Image as IMAGE

class Oven:

    def __init__(self, loader, blocks, code):
        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow

        self.__blocks = blocks
        self.__code   = code

        self.dead = False
        self.__changed = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__running  = 0
        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__picIndex = 0

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__miniFont2 = self.__fontManager.getFont(int(self.__fontSize*0.55), False, False, False)
        self.__miniFont3 = self.__fontManager.getFont(int(self.__fontSize*0.35), False, False, False)

        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)

        self.__sizes = [self.__screenSize[0] / 1.05, self.__screenSize[1] / 1.05 - 40]
        self.__window = SubMenu(self.__loader, "rawData", self.__sizes[0], self.__sizes[1], None, self.__addElements, 2)

        self.dead = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__narrowFtame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 6, height = self.__sizes[1] )

        self.__narrowFtame.pack_propagate(False)
        self.__narrowFtame.pack(side=LEFT, anchor=W, fill=Y)

        self.__mostFrame = Frame(self.__topLevelWindow,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 6 * 5, height = self.__sizes[1] )

        self.__mostFrame.pack_propagate(False)
        self.__mostFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        t1 = Thread(target = self.__loadNarrow)
        t1.daemon = True
        t1.start()

        t2 = Thread(target = self.__allTheOthers)
        t2.daemon = True
        t2.start()

        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)

    def loop(self):
        if self.__running == 0:
           self.__picIndex += 1
           if self.__picIndex > 15: self.__picIndex = 0

           self.__thatPic = self.__canvas.create_image(
               0, 0, image=self.__buffer[self.__picIndex // 4], anchor=NW
           )


    def __allTheOthers(self):
        self.__running += 1

        while self.__mostFrame.winfo_width() < 2: sleep(0.00000001)

        self.__theBigCancasFrame = Frame(self.__mostFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__mostFrame.winfo_width(), height = self.__sizes[1] // 12 * 5 )

        self.__theBigCancasFrame.pack_propagate(False)
        self.__theBigCancasFrame.pack(side=TOP, anchor=N, fill=X)

        self.__bigCanvas = Canvas(self.__theBigCancasFrame, bg = "black",
                               height=self.__sizes[1] // 12 * 7, width=self.__mostFrame.winfo_width())
        self.__bigCanvas.pack_propagate(False)
        self.__bigCanvas.pack(side=TOP, fill=BOTH, anchor=CENTER)

        """
        self.__globalSwitchesFrame = Frame(self.__mostFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__mostFrame.winfo_width(), height = self.__sizes[1] // 12)

        self.__globalSwitchesFrame.pack_propagate(False)
        self.__globalSwitchesFrame.pack(side=TOP, anchor=N, fill=X)
        """

        self.__disableOnAuto = []

        h = self.__sizes[1] // 24 * 7

        self.__columnsFrame1 = Frame(self.__mostFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__mostFrame.winfo_width(), height = h)

        self.__columnsFrame1.pack_propagate(False)
        self.__columnsFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__columnsFrame2 = Frame(self.__mostFrame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__mostFrame.winfo_width(), height = h)

        self.__columnsFrame2.pack_propagate(False)
        self.__columnsFrame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__columnThings = []

        m      = 15
        border = 7

        self.__max = m

        self.__blank        = self.__dictionaries.getWordFromCurrentLanguage("blank")

        self.__dataItems    = [self.__blank]
        self.__dataItems_1  = []
        self.__colorItems   = []

        #self.__lastSelecteds = []

        for b in self.__blocks:
            blockPlace = {
                True: [self.__colorItems], False: [self.__dataItems, self.__dataItems_1]
            }

            listOfThem = blockPlace[b["color"]]

            #last = len(b["bytes"])
            for item in listOfThem:
                for label in b["labels"]:
                    item.append(label)

        for num in range(0, m):
            self.__columnThings.append({
                "frames"     : [],
                "listbox"    : None,
                "scrollbar"  : None,
                "mirrorVal"  : IntVar(),
                "cutBits"    : IntVar(),
                "mirrorRadio": None,
                "cutRadio"   : None,
                "label"      : None,
                "items"      : None,
                "last"       : None,
                "radios"     : [0, 0]
            })

            smallSize = h // 16

            if num < border:
               w = self.__mostFrame.winfo_width() // border
               thatFrame = self.__columnsFrame1
            else:
               w = self.__mostFrame.winfo_width() // (m - border)
               thatFrame = self.__columnsFrame2

            f = Frame(thatFrame,
                      bg    = self.__loader.colorPalettes.getColor("window"),
                      width = w, height = h)

            f.pack_propagate(False)
            f.pack(side=LEFT, anchor=W, fill=Y)

            f1 = Frame(f,
                      bg    = self.__loader.colorPalettes.getColor("window"),
                      width = w, height = smallSize)

            f1.pack_propagate(False)
            f1.pack(side=TOP, anchor=N, fill=X)

            f2 = Frame(f,
                      bg    = self.__loader.colorPalettes.getColor("window"),
                      width = w, height = smallSize)

            f2.pack_propagate(False)
            f2.pack(side=TOP, anchor=N, fill=X)

            f3 = Frame(f,
                      bg    = self.__loader.colorPalettes.getColor("window"),
                      width = w, height = smallSize)

            f3.pack_propagate(False)
            f3.pack(side=TOP, anchor=N, fill=X)

            f4 = Frame(f,
                      bg    = self.__loader.colorPalettes.getColor("window"),
                      width = w, height = h - (smallSize * 3))

            f4.pack_propagate(False)
            f4.pack(side=TOP, anchor=N, fill=X)

            if num == m - 1: self.__globalSwitchesFrame = f4

            self.__columnThings[-1]["frames"] = [f, f1, f2, f3, f4]

            while f1.winfo_width() < 2 or f2.winfo_width() < 2 or f3.winfo_width() < 2 or f4.winfo_width() < 2: sleep(0.000001)

            n = str(num + 1)
            if len(n) == 1: n = "0" + n

            txt = self.__loader.dictionaries.getWordFromCurrentLanguage("pixelData") + n
            c   = False
            if   num == 12:
                 txt = self.__loader.dictionaries.getWordFromCurrentLanguage("colorData")
                 c   = True
            elif num == 13:
                 txt = self.__loader.dictionaries.getWordFromCurrentLanguage("backColor")
                 c   = True
            elif num == m - 1:
                 txt = self.__loader.dictionaries.getWordFromCurrentLanguage("globalSwitches")

            l = Label(f1, text=txt,
                          font=self.__miniFont, fg=self.__colors.getColor("font"),
                          bg=self.__colors.getColor("window")
                          )

            l.pack_propagate(False)
            l.pack(side=TOP, anchor=N, fill=BOTH)

            self.__columnThings[-1]["label"] = l

            if num == m - 1:
               break

            if num < 12:

               rb1 = Checkbutton(f2, width=f2.winfo_width(),
                                 bg=self.__colors.getColor("window"),
                                 name="cutBits_" + str(num + 1),
                                 justify=LEFT, state = DISABLED,
                                 variable=self.__columnThings[-1]["cutBits"],
                                 activebackground=self.__colors.getColor("highLight"),
                                 command=None, font = self.__miniFont2,
                                 text = self.__loader.dictionaries.getWordFromCurrentLanguage("cutLower")
                                 )

               rb1.pack_propagate(False)
               rb1.pack(fill=Y, side=LEFT, anchor=E)

               rb2 = Checkbutton(f3, width=f3.winfo_width(),
                                 bg=self.__colors.getColor("window"),
                                 name="mirror_" + str(num + 1),
                                 justify=LEFT, state = DISABLED,
                                 variable=self.__columnThings[-1]["mirrorVal"],
                                 activebackground=self.__colors.getColor("highLight"),
                                 command=None, font = self.__miniFont2,
                                 text = self.__loader.dictionaries.getWordFromCurrentLanguage("mirrorHorizontally")
                                 )

               rb2.pack_propagate(False)
               rb2.pack(fill=Y, side=LEFT, anchor=E)

               self.__columnThings[-1]["cutRadio"]    = rb1
               self.__columnThings[-1]["mirrorRadio"] = rb2

               self.__loader.threadLooper.bindingMaster.addBinding(self, rb1, "<Button-1>", self.__changeThings, 2)
               self.__loader.threadLooper.bindingMaster.addBinding(self, rb2, "<Button-1>", self.__changeThings, 2)

               self.__disableOnAuto.append(rb1)
               self.__disableOnAuto.append(rb2)

            sBar = Scrollbar(f4)
            lBox = Listbox(f4, width=f4.winfo_width(),
                           height=f4.winfo_height(),
                           name = "lbox_" + str(num + 1),
                           yscrollcommand=sBar.set,
                           selectmode=BROWSE,
                           exportselection=False,
                           font=self.__miniFont,
                           justify=LEFT
                           )

            lBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
            lBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
            lBox.pack_propagate(False)

            sBar.pack(side=RIGHT, anchor=W, fill=Y)
            lBox.pack(side=LEFT, anchor=W, fill=BOTH)

            sBar.config(command=lBox.yview)

            self.__loader.threadLooper.bindingMaster.addBinding(self, lBox, "<ButtonRelease-1>", self.__changeThings,  2)
            self.__loader.threadLooper.bindingMaster.addBinding(self, lBox, "<KeyRelease-Up>"  , self.__changeThings,  2)
            self.__loader.threadLooper.bindingMaster.addBinding(self, lBox, "<KeyRelease-Down>", self.__changeThings,  2)

            self.__columnThings[-1]["listbox"]   = lBox
            self.__columnThings[-1]["scrollbar"] = sBar

            if   num == 0:
                 listOfThem = self.__dataItems_1
            elif c:
                 listOfThem = self.__colorItems
            else:
                 listOfThem = self.__dataItems

            for item in listOfThem:
                lBox.insert(END, item)

            lBox.select_set(0)
            if num > 1: lBox.config(state = DISABLED)

            self.__columnThings[-1]["last"]  = listOfThem[0]
            self.__columnThings[-1]["items"] = listOfThem

        self.__autoDetect = IntVar()
        self.__auto       = 1
        self.__autoDetect.set(self.__auto)

        while self.__globalSwitchesFrame.winfo_width() < 2: sleep(0.0000001)

        pieces = 10

        self.__autoDetectFrame = Frame(self.__globalSwitchesFrame,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 width = self.__globalSwitchesFrame.winfo_width(), height = self.__globalSwitchesFrame.winfo_height() // pieces)

        self.__autoDetectFrame.pack_propagate(False)
        self.__autoDetectFrame.pack(side=TOP, anchor=N, fill=X)

        self.__autoDetectButton = Checkbutton(self.__autoDetectFrame, width=f2.winfo_width(),
                          bg=self.__colors.getColor("window"),
                          name="autoDetect",
                          justify=LEFT,
                          variable=self.__autoDetect,
                          activebackground=self.__colors.getColor("highLight"),
                          command=None, font=self.__miniFont2,
                          text=self.__loader.dictionaries.getWordFromCurrentLanguage("autoDetect")
                          )

        self.__autoDetectButton.pack_propagate(False)
        self.__autoDetectButton.pack(fill=Y, side=LEFT, anchor=E)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__autoDetectButton, "<Button-1>", self.__changeThings, 2)

        self.__thatLabelFrame = Frame(self.__globalSwitchesFrame,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 width = self.__globalSwitchesFrame.winfo_width(), height = self.__globalSwitchesFrame.winfo_height() // pieces)

        self.__thatLabelFrame.pack_propagate(False)
        self.__thatLabelFrame.pack(side=TOP, anchor=N, fill=X)

        self.__thatLabel = Label(self.__thatLabelFrame,
                                 text=self.__loader.dictionaries.getWordFromCurrentLanguage("pixelSize"),
                                 font=self.__miniFont, fg=self.__colors.getColor("font"),
                                 bg=self.__colors.getColor("window")
                                 )

        self.__thatLabel.pack_propagate(False)
        self.__thatLabel.pack(side=TOP, anchor=N, fill=BOTH)

        numbers = ["1x", "2x", "4x"]

        self.__radios = []
        schema        = {"frame": None, "radioButton": None}
        self.__size = IntVar()
        self.__sizeVal = 1
        self.__size.set(self.__sizeVal)

        self.__noBullshit = []

        for n in range(0, 3):
            self.__radios.append(deepcopy(schema))
            f = Frame(self.__globalSwitchesFrame,
                      bg = self.__loader.colorPalettes.getColor("window"),
                      width = self.__globalSwitchesFrame.winfo_width(),
                      height = self.__globalSwitchesFrame.winfo_height() // pieces)

            f.pack_propagate(False)
            f.pack(side=TOP, anchor=N, fill=X)

            self.__radios[-1]["frame"] = f

            rb = Radiobutton(f, width=f2.winfo_width(),
                              bg=self.__colors.getColor("window"),
                              name="size_" + str(n + 1),
                              justify=LEFT, state = DISABLED,
                              variable=self.__size,
                              activebackground=self.__colors.getColor("highLight"),
                              command=None, font=self.__miniFont, value = n + 1,
                              text=numbers[n]
                              )

            rb.pack_propagate(False)
            rb.pack(fill=Y, side=LEFT, anchor=E)

            self.__disableOnAuto.append(rb)
            self.__noBullshit   .append(rb)

            self.__loader.threadLooper.bindingMaster.addBinding(self, rb, "<Button-1>", self.__changeThings, 2)

            self.__radios[-1]["radioButton"] = rb

        self.__thatLabelFrame2 = Frame(self.__globalSwitchesFrame,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 width = self.__globalSwitchesFrame.winfo_width(), height = self.__globalSwitchesFrame.winfo_height() // pieces)

        self.__thatLabelFrame2.pack_propagate(False)
        self.__thatLabelFrame2.pack(side=TOP, anchor=N, fill=X)

        self.__thatLabel2 = Label(self.__thatLabelFrame2,
                                 text=self.__loader.dictionaries.getWordFromCurrentLanguage("playfield"),
                                 font=self.__miniFont, fg=self.__colors.getColor("font"),
                                 bg=self.__colors.getColor("window")
                                 )

        self.__thatLabel2.pack_propagate(False)
        self.__thatLabel2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__doubledFrame = Frame(self.__globalSwitchesFrame,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 width = self.__globalSwitchesFrame.winfo_width(), height = self.__globalSwitchesFrame.winfo_height() // pieces)

        self.__doubledFrame.pack_propagate(False)
        self.__doubledFrame.pack(side=TOP, anchor=N, fill=X)

        self.__doubled       = IntVar()
        self.__d             = 0
        self.__doubled.set(self.__d)

        self.__doubledButton = Checkbutton(self.__doubledFrame, width=f2.winfo_width(),
                          bg=self.__colors.getColor("window"),
                          name="doubled_0",
                          justify=LEFT, state = DISABLED,
                          variable=self.__doubled,
                          activebackground=self.__colors.getColor("highLight"),
                          command=None, font=self.__miniFont2,
                          text=self.__loader.dictionaries.getWordFromCurrentLanguage("doubled")
                          )

        self.__doubledButton.pack_propagate(False)
        self.__doubledButton.pack(fill=Y, side=LEFT, anchor=E)

        self.__mirroredFrame = Frame(self.__globalSwitchesFrame,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 width = self.__globalSwitchesFrame.winfo_width(), height = self.__globalSwitchesFrame.winfo_height() // pieces)

        self.__mirroredFrame.pack_propagate(False)
        self.__mirroredFrame.pack(side=TOP, anchor=N, fill=X)

        self.__mirrored       = IntVar()
        self.__m             = 0
        self.__mirrored.set(self.__m)

        self.__mirroredButton = Checkbutton(self.__mirroredFrame, width=f2.winfo_width(),
                          bg=self.__colors.getColor("window"),
                          name="mirrored_0",
                          justify=LEFT, state = DISABLED,
                          variable=self.__mirrored,
                          activebackground=self.__colors.getColor("highLight"),
                          command=None, font=self.__miniFont2,
                          text=self.__loader.dictionaries.getWordFromCurrentLanguage("mirrored")
                          )

        self.__mirroredButton.pack_propagate(False)
        self.__mirroredButton.pack(fill=Y, side=LEFT, anchor=E)

        self.__disableOnAuto.append(self.__doubledButton)
        self.__disableOnAuto.append(self.__mirroredButton)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__mirroredButton, "<Button-1>", self.__changeThings, 2)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__doubledButton , "<Button-1>", self.__changeThings, 2)

        self.__running -= 1

    def __changeThings(self, event):
        thing = event.widget
        name  = str(thing).split(".")[-1]

        if thing.cget("state") == DISABLED: return

        autoDetectCheck = False
        redrawn         = False

        num   = 0
        value = 0
        try:
            num   = int(name.split("_")[-1])
            value = num
            name  = name.split("_")[0]
        except:
            pass
        num -= 1

        if   name == "autoDetect":
             self.__auto     = 1 - self.__auto
             autoDetectCheck = self.__auto
             if autoDetectCheck: redrawn = True

             s = {True: DISABLED, False: NORMAL}

             for item in self.__disableOnAuto:
                 name = str(item).split(".")[-1]
                 num  = int(name.split("_")[-1]) - 1

                 nonBlank = False

                 if num == 0 or item in self.__noBullshit:
                    nonBlank = True
                 else:
                    #print(num)
                    selected = self.__columnThings[num - 1]["listbox"].curselection()[0]
                    if self.__columnThings[num - 1]["items"][selected] != self.__blank:
                       nonBlank = True

                 if s[self.__auto] == DISABLED or nonBlank:
                    item.config(state = s[self.__auto])

        elif name == "size":
             if self.__sizeVal != value: redrawn = True
             self.__sizeVal = value

        elif name == "doubled":
             redrawn  = True
             self.__d = 1 - self.__d

        elif name == "mirrored":
             redrawn  = True
             self.__m = 1 - self.__m

        elif name == "lbox":
             selected = self.__columnThings[num]["listbox"].curselection()[0]
             if self.__columnThings[num]["last"] != self.__columnThings[num]["items"][selected]:
                redrawn = True
                self.__columnThings[num]["last"] = self.__columnThings[num]["items"][selected]

                #  "frames", "listbox", "scrollbar", "mirrorVal", "cutBits"
                #  "mirrorRadio", "cutRadio", "label",  "items", "last"

                for n in range(num + 1, self.__max):
                    if self.__columnThings[num]["last"] == self.__blank:
                       for key in ["listbox", "mirrorRadio", "cutRadio"]:
                           if self.__columnThings[n][key] != None:
                              self.__columnThings[n][key].config(state = DISABLED)
                    else:
                        if    self.__columnThings[n-1]["last"]  != self.__blank:
                           if self.__columnThings[n]["listbox"] != None:
                              self.__columnThings[n]["listbox"].config(state=NORMAL)

                           if self.__auto == False and self.__columnThings[n]["mirrorRadio"] != None:
                              self.__columnThings[n]["mirrorRadio"].config(state=NORMAL)
                              self.__columnThings[n]["cutRadio"]   .config(state=NORMAL)

        elif name == "cutBits":
             self.__columnThings[num]["radios"][0] = 1 - self.__columnThings[num]["radios"][0]
             redrawn = True

        elif name == "mirrorVal":
             self.__columnThings[num]["radios"][1] = 1 - self.__columnThings[num]["radios"][1]
             redrawn = True

        elif thing in self.__noBullshit:
             self.__sizeVal = value
             redrawn = True

        if autoDetectCheck:
           typ = "sprite"

           firstThree = [self.__columnThings[0]["last"], self.__columnThings[1] ["last"], self.__columnThings[2] ["last"]]
           nextThree  = [self.__columnThings[3]["last"], self.__columnThings[4] ["last"], self.__columnThings[5] ["last"]]
           others     = [self.__columnThings[6]["last"], self.__columnThings[7] ["last"], self.__columnThings[8] ["last"],
                         self.__columnThings[9]["last"], self.__columnThings[10]["last"], self.__columnThings[11]["last"]]

           pfMirroring = True
           pfDoubling  = True

           if firstThree.count(self.__blank) == 0:
              if   nextThree.count(self.__blank) == 3                                    :
                   typ        = "playfield"
                   pfDoubling = True
              elif nextThree.count(self.__blank) == 0 and others.count(self.__blank) == 6:
                   typ        = "playfield"
                   pfDoubling = False

           for n in range(0, 13):
               self.__columnThings[n]["radios"]    = [0,0]
               self.__columnThings[n]["mirrorVal"].set(0)
               self.__columnThings[n]["cutBits"]  .set(0)

           self.__autoDetect.set(0)
           self.__auto = 0

           if typ == "playfield":
               if   pfDoubling:
                    PF3 = self.__columnThings[0]["last"]
               else:
                    PF3 = self.__columnThings[3]["last"]

              # Normal   PF: mirrored PF0, simple PF1, mirrored P2, mirrored PF0, simple PF1,   mirrored PF2
              # Mirrored PF: mirrored PF0, simple PF1, mirrored P2, simple PF2,   mirrored PF1, simple PF0

               block1      = self.getBlockByLabel(PF3)
               block1IsPF0 = True

               for b in block1:
                   if b != self.cutLowerNibble(b):
                      block1IsPF0 = False
                      break

               pfMirroring = 1 - block1IsPF0

               self.__m = pfMirroring
               self.__d = pfDoubling

               self.__mirrored.set(self.__m)
               self.__doubled .set(self.__d)

               mirroring = {
                   False: [True, False, True, True, False, True],
                   True : [True, False, True, False, True, False]
               }

               cutting = {
                   False: [True, False, False, True, False, False],
                   True : [True, False, False, False, False, True],
               }

               for NN in range(0, 6):
                   if pfDoubling and NN > 2: break
                   m = mirroring[pfMirroring][NN]
                   c = cutting  [pfMirroring][NN]

                   self.__columnThings[NN]["radios"]   = [c, m]
                   self.__columnThings[NN]["cutBits"]  .set(c)
                   self.__columnThings[NN]["mirrorVal"].set(m)

    def cutLowerNibble(self, b):
        value , mode  = self.convertEntryToNum(b)
        binary        = self.formatNum(value, "bin")[:5] + "0000"
        value2, dummy = self.convertEntryToNum(binary)
        return self.formatNum(value2, mode)

    def convertEntryToNum(self, num):
        if num.startswith("%"):
            mode = "bin"
            value = int(num.replace("%", "0b"), 2)
        elif num.startswith("$"):
            mode = "hex"
            value = int(num.replace("$", "0x"), 16)
        else:
            mode = "dec"
            value = int(num)

        return value, mode

    def formatNum(self, theNumber, mode):
        if   mode == "bin":
             theNumber = bin(theNumber).replace("0b", "")
             return "%" + ((8 - len(theNumber)) * "0") + theNumber
        elif mode == "hex":
             theNumber = hex(theNumber).replace("0x", "")
             return ("$" + ((2 - len(theNumber)) * "0") + theNumber).upper()
        else:
             return str(theNumber)


    def getBlockByLabel(self, label):
        for block in self.__blocks:
            if label in block["labels"]:
               return block

        return False

    def __loadNarrow(self):
        self.__running += 1

        while self.__narrowFtame.winfo_width() < 2: sleep(0.00000001)

        # 325 x 115

        w = round(self.__narrowFtame.winfo_width())
        h = round(115 * (self.__narrowFtame.winfo_width() / 325))


        self.__narrowFtameUpper = Frame(self.__narrowFtame,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   width = self.__sizes[0] // 10, height = h )

        self.__narrowFtameUpper.pack_propagate(False)
        self.__narrowFtameUpper.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__narrowFtameUpper, bg = self.__loader.colorPalettes.getColor("window"),
                               height=h, width=w)
        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, fill=BOTH, anchor=CENTER)

        self.__buffer = []

        for num in range(0, 4):
            #self.__buffer.append(IMAGE.open(str("others/img/cooker/0" + str(num) + ".png")).resize(w, h, IMAGE.ANTIALIAS))

            self.__buffer.append(
                ImageTk.PhotoImage(IMAGE.open("others/img/cooker/0" + str(num) + ".png").resize((w, h), IMAGE.ANTIALIAS)))

        self.__thatPic = self.__canvas.create_image(
            0, 0, image=self.__buffer[0], anchor=NW
        )

        self.__asmBox    = scrolledtext.ScrolledText(self.__narrowFtame, width=999999, height=self.__sizes[1]//2, wrap=WORD)
        self.__asmBox.pack(fill=BOTH, side=BOTTOM, anchor=S)

        self.__asmBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                fg=self.__loader.colorPalettes.getColor("boxFontNormal"))


        self.__getFont()

        self.__asmBox.insert(END, self.__code)
        self.__formatting()

        self.__asmBox.bind("<Key>", lambda e: "break")
        self.__running -= 1

    def __formatting(self):
        y = 0
        for line in self.__code.split("\n"):
            y = y + 1
            if len(line) == 0: continue

            if line[0] in (" ", "\t"):
               wasNonSpace = False
               for poz in range(0, len(line)):
                   if line[poz] in (" ", "\t"):
                      if wasNonSpace: break
                   else:
                      wasNonSpace = True

               self.addTag(y, 0  , poz      , "command")

               if ";" in line:
                  self.addTag(y, poz, line.index(";")      , "number")
                  self.addTag(y, line.index(";"), len(line), "comment")
               else:
                  self.addTag(y, poz, len(line), "number" )

            else:
               if line[0] in ["#", "*"] and line[1:5] not in ("NAME", "BANK"):
                  self.addTag(y, 0, len(line), "comment")
               else:
                  self.addTag(y, 0, len(line), "label")


    def addTag(self, Y, X1, X2, tag):
        self.__asmBox.tag_add(tag, str(Y) + "." + str(X1) , str(Y) + "." + str(X2))

    def __getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__loader.mainWindow.getWindowSize()[0] / 1600
        h = self.__loader.mainWindow.getWindowSize()[1] / 1200

        self.__fontSize = (baseSize * w * h)
        self.__normalFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__boldFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, False)
        self.__italicFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False)
        self.__undelinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, True)
        self.__boldItalicFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, False)
        self.__boldUnderlinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, False, True)
        self.__boldItalicUnderLinedFont = self.__loader.fontManager.getFont(round(self.__fontSize), True, True, True)

        self.__tagSettings = {
            "comment": {
                "foreground": self.__loader.colorPalettes.getColor("comment"),
                "font": self.__italicFont
            },
            "number": {
                "foreground": self.__loader.colorPalettes.getColor("number"),
                "font": self.__normalFont
            },
            "command": {
                "foreground": self.__loader.colorPalettes.getColor("command"),
                "font": self.__boldFont
            },
            "label": {
                "foreground": self.__loader.colorPalettes.getColor("portState"),
                "font": self.__boldUnderlinedFont
            }
        }

        for key in self.__tagSettings:
            if "background" not in self.__tagSettings[key]:
                self.__asmBox.tag_config(key,
                                            foreground=self.__tagSettings[key]["foreground"],
                                            font=self.__tagSettings[key]["font"])
            elif "foreground" not in self.__tagSettings[key]:
                self.__asmBox.tag_config(key,
                                            background=self.__tagSettings[key]["background"],
                                            font=self.__tagSettings[key]["font"])
            else:
                self.__asmBox.tag_config(key,
                                            foreground=self.__tagSettings[key]["foreground"],
                                            background=self.__tagSettings[key]["background"],
                                            font=self.__tagSettings[key]["font"])

        self.__asmBox.config(font=self.__normalFont)
        self.__asmBox.tag_raise("sel")

