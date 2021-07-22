from PIL import Image as IMG, ImageTk
from copy import deepcopy
from tkinter import *
from SubMenu import SubMenu

class PictureToCode:

    def __init__(self, loader, kernel, mode, w, changed):
        if mode == "playfield":
            self.__w = 40
            if kernel=="common":
                self.__mirroring = [0,1,1]

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.doThings = False


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

        self.__screenSize = self.__loader.screenSize

        formats = [
            "bmp", "dds", "eps", "gif", "dib", "ico", "jpg", "jpeg", "pcx", "png", "tga", "tiff", "pdf"
        ]

        self.answer = self.__fileDialogs.askForFileName("loadPicture",
                                                   False, [formats, "*"], self.__mainWindow.projectPath)

        if self.answer !="":
            image = IMG.open(self.answer, "r")

            self.__func = None
            self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
            self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)


            self.__window = SubMenu(self.__loader, "loadPicture", self.__screenSize[0] / 1.5,
                                    self.__screenSize[1]/4  - 45, None, self.__addElements, 2)

            self.dead = True


            #Window is dead.

            if self.doThings == True:

                width, height = image.size

                multi = self.__w/width
                h = round(image.height*multi)

                w = self.__w
                imageSized = image.resize((w, h), IMG.ANTIALIAS)
                imgColorData = imageSized.load()

                imageClone = deepcopy(imageSized)

                if self.__invert.get():
                    from PIL import ImageOps
                    imageClone = ImageOps.invert(imageClone)

                fn = lambda x: 255 if x > int(self.__tres.get()) else 0
                altImage = deepcopy(imageClone).convert('L').point(fn, mode='1')

                #GetColors
                imgPixelData = altImage.load()


                self.__picture = []
                for Y in range(0, h):
                    row = []
                    for X in range(0, w):
                        row.append(imgColorData[X,Y])

                    self.__picture.append(self.calculateRow(row))

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__imageFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame.pack_propagate(False)
        self.__imageFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__tres=StringVar()
        self.__tres.set("128")

        self.__controllerFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__controllerFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__titleLabel = Label(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__titleLabel.pack(side=TOP, anchor=N, fill=X)

        self.__number = Entry(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__tres, width=999999999,
                                  font=self.__normalFont
                              )

        self.__number.bind("<KeyRelease>", self.__checkNumber)

        self.__number.pack(side=TOP, anchor=N, fill=X)
        self.__minus = self.__loader.io.getImg("negative", None)
        self.__plus = self.__loader.io.getImg("positive", None)

        self.__invert = IntVar()
        self.__invert.set(0)

        self.__check = Checkbutton(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("invert"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"),
                                  font=self.__smallFont,
                                   variable = self.__invert, command = self.updateBlackAndWhite
                                  )



        self.__buttonFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2), height=round(self.__topLevel.getTopLevelDimensions()[1] / 4))
        self.__buttonFrame.pack_propagate(False)
        self.__buttonFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__minusButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__minus, command=self.__neg
                                    )
        self.__minusButton.pack_propagate(False)
        self.__minusButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__positiveButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__plus, command=self.__pos
                                    )
        self.__positiveButton.pack_propagate(False)
        self.__positiveButton.pack(side=LEFT, anchor=E, fill=Y)

        self.__check.pack(side=TOP, anchor=N, fill=X)

        self.__buttonFrame2 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height = round(self.__topLevel.getTopLevelDimensions()[1] / 3))
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__okButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                    font=self.__smallFont, command=self.setAndKill
                                    )
        self.__okButton.pack_propagate(False)
        self.__okButton.pack(side=TOP, anchor=E, fill=X)

        self.__cancelButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                    font=self.__smallFont, command=self.killMe
                                    )
        self.__cancelButton.pack_propagate(False)
        self.__cancelButton.pack(side=TOP, anchor=E, fill=X)

        self.__imageFrame2 = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame2.pack_propagate(False)
        self.__imageFrame2.pack(side=LEFT, anchor=W, fill=Y)

        self.__photo = self.blackAndWhite()

    def killMe(self):
        self.__topLevelWindow.destroy()
        self.dead=True

    def setAndKill(self):
        self.doThings = True
        self.killMe()

    def __checkNumber(self, event):
        num = 0
        try:
            num = int(self.__tres.get())
        except:
            self.__number.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontSaved")
            )
        self.__number.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

        if num<0:
            num = self.__tres.set("0")
        elif num>255:
            num = self.__tres.set("255")

        self.updateBlackAndWhite()

    def __pos(self):
        num = int(self.__tres.get())

        if num<245:
            self.__tres.set(str(num+10))

        self.updateBlackAndWhite()


    def __neg(self):
        num = int(self.__tres.get())

        if num>10:
            self.__tres.set(str(num-10))

        self.updateBlackAndWhite()

    def calculateRow(self, row):
        pass

    def blackAndWhite(self):

        from copy import deepcopy

        #for slave in self.__imageFrame.pack_slaves():
        #    slave.destroy()

        h = round(self.__topLevel.getTopLevelDimensions()[1])
        image = IMG.open(self.answer, "r")
        width, height = image.size

        multi = h / height
        w = round(image.width * multi)

        imageSized = image.resize((w, h), IMG.ANTIALIAS)

        self.img1 = ImageTk.PhotoImage(imageSized)

        self.label1 = Label(self.__imageFrame,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image = self.img1
            )
        self.label1.pack(side=LEFT, fill=BOTH)

        self.label2 = Label(self.__imageFrame2,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image=self.img1
            )
        self.label2.pack(side=RIGHT, fill=BOTH)
        self.updateBlackAndWhite()

    def updateBlackAndWhite(self):
        image = IMG.open(self.answer, "r")

        if self.__invert.get():
            from PIL import ImageOps
            image = ImageOps.invert(image)

        width, height = image.size
        h = round(self.__topLevel.getTopLevelDimensions()[1])


        multi = h / height
        w = round(image.width * multi)
        imageSized = image.resize((w, h), IMG.ANTIALIAS)

        fn = lambda x: 255 if x > int(self.__tres.get()) else 0
        altImage = deepcopy(imageSized).convert('L').point(fn, mode='1')


        self.img2 = ImageTk.PhotoImage(altImage)

        self.label2.config(image = self.img2)

if __name__ == "__main__":
    code = PictureToCode("C:\cat.jpg", "common", "playfield", None)
