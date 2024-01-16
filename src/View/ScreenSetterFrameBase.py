from tkinter import *
from threading import Thread
from copy import deepcopy
from time import sleep

class ScreenSetterFrameBase:

    def __init__(self, loader, baseFrame, data, name, changeName, dead, names):

        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data
        self.__changeName = changeName
        self.__dead = dead
        self.__names = names
        self.__countBack = 0

        if type(data) == str: self.__data = self.__data.split(" ")

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize*1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize*1.5), False, False, False)
        self.__name = name
        if self.__name.get() == "": self.__name.set(self.__data[0])

        self.__errors = {}
        self.__originalName = self.__name.get()

        self.__titleLabel = Label(  self.__baseFrame,
                                    text = self.__data[1],
                                    bg = self.__colors.getColor("font"),
                                    fg = self.__colors.getColor("window"),
                                    justify = LEFT, font = self.__normalFont
                                  )
        self.__titleLabel.pack_propagate(False)
        self.__titleLabel.pack(side = TOP, anchor = N, fill = X)


        self.__errorText = StringVar()
        self.__errorText.set("")
        self.__errorLabel = Label(  self.__baseFrame,
                                    textvariable = self.__errorText,
                                    bg = self.__colors.getColor("window"),
                                    fg = self.__colors.getColor("font"),
                                    justify = LEFT, font = self.__smallFont
                                  )
        self.__errorLabel.pack_propagate(False)
        self.__errorLabel.pack(side = TOP, anchor = N, fill = X)

        self.__nameFrame = Frame(   self.__baseFrame, width = self.__baseFrame.winfo_width(),
                                    bg = self.__loader.colorPalettes.getColor("window"),
                                    height = self.__baseFrame.winfo_height() // 16)
        self.__nameFrame.pack_propagate(False)
        self.__nameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__nameLabel = Label(  self.__nameFrame,
                                    text = self.__dictionaries.getWordFromCurrentLanguage("name")+" ",
                                    bg = self.__colors.getColor("window"),
                                    fg = self.__colors.getColor("font"),
                                    justify = LEFT, font = self.__normalFont
                                  )
        self.__nameLabel.pack_propagate(False)
        self.__nameLabel.pack(side = LEFT, anchor = E, fill = Y)

        self.__nameEntry = Entry(self.__nameFrame,
                                        bg=self.__colors.getColor("boxBackNormal"),
                                        fg=self.__colors.getColor("boxFontNormal"),
                                        width=9999,
                                        textvariable=self.__name,
                                        font=self.__normalFont
                                        )

        self.__nameEntry.pack_propagate(False)
        self.__nameEntry.pack(fill=BOTH, side = LEFT, anchor = E)

        self.registerError("segmentName")
        self.registerError("nameAlready")
        self.registerError("delimiterInName")

        self.__nameEntry.bind("<KeyRelease>", self.checkNameEntry)
        self.__nameEntry.bind("<FocusOut>", self.checkNameEntry)

        self.__loader.threadLooper.addToThreading(self, self.loop, [])
        #t = Thread(target=self.loop)
        #t.daemon = True
        #t.start()

    def loop(self):
        try:
            foundError = False

            for errorKey in self.__errors:
                if self.__errors[errorKey] == True:
                    foundError = True
                    self.setErrorText(errorKey)
                    break

            if foundError == False:
                self.clearErrorText()

            if self.__countBack > 0: self.__countBack -= 1
            if self.__countBack == 1: self.__checkIfNewName()

        except Exception as e:
            pass


    def checkNameEntry(self, event):
        import re
        noError = True

        if len(re.findall(r'^[a-zA-Z][0-9a-zA-Z_]*$', self.__name.get())) == 0:
           self.__errors["segmentName"] = True
           noError = False
           self.__nameEntry.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved"))

        delimiters1 = self.__loader.config.getValueByKey("validObjDelimiters")
        delimiters2 = self.__loader.config.getValueByKey("validLineDelimiters")

        for d in delimiters1:
           if d in self.__name.get():
               self.__errors["delimiterInName"] = True
               noError = False
               self.__nameEntry.config(
                    bg=self.__colors.getColor("boxBackUnSaved"),
                    fg=self.__colors.getColor("boxFontUnSaved"))

        for d in delimiters2:
           if d in self.__name.get():
               self.__errors["delimiterInName"] = True
               noError = False
               self.__nameEntry.config(
                    bg=self.__colors.getColor("boxBackUnSaved"),
                    fg=self.__colors.getColor("boxFontUnSaved"))

        if noError == True:
            self.__errors["segmentName"] = False
            self.__errors["delimiterInName"] = False

            self.__nameEntry.config(
                bg = self.__colors.getColor("boxBackNormal"),
                fg=self.__colors.getColor("boxFontNormal")
            )

        eventType = str(event).split(" ")[0][1:]
        if eventType == "FocusOut":
            self.__checkIfNewName()
        else:
            self.__countBack = 100

    def __checkIfNewName(self):
        newName = self.__name.get()
        oldName = self.__data[0]

        counter = 0
        while (newName in self.__names) and (newName != oldName):
            newName =  self.__name.get() + "_" + str(counter)
            counter += 1
            self.__name.set(newName)

        if newName == oldName: return

        for error in self.__errors.keys():
            if self.__errors[error] == True:
               return

        self.__data[0] = newName
        self.__changeName(oldName, newName)


    def registerError(self, text):
        self.__errors[text] = False

    def changeErrorState(self, text, state):
        self.__errors[text] = state

    def setErrorText(self, text):
        if text != "":
            self.__errorText.set(
                self.__dictionaries.getWordFromCurrentLanguage(text)
            )
            self.__errorLabel.config(
                bg=self.__colors.getColor("boxBackUnSaved"),
                fg=self.__colors.getColor("boxFontUnSaved")
            )
        else:
            self.__errorText.set("")
            self.__errorLabel.config(
                bg=self.__colors.getColor("window"),
                fg=self.__colors.getColor("font")
            )

    def clearErrorText(self):
        self.setErrorText("")

    def hasError(self):
        return self.__errorText.get() != ""