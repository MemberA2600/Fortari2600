from tkinter import *

class VisualLoaderFrame:

    def __init__(self, loader, masterFrame, ten, fontNormal, fontSmall, labelText, default, entryName, bindedFunc,
                 w, openCommand, saveCommand):

        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.__frame = Frame(masterFrame, height=ten * 3,
                                       bg=self.__loader.colorPalettes.getColor("window"))
        self.__frame.pack_propagate(False)

        self.__frame.pack(side=TOP, anchor=N, fill=X)

        if labelText!=None:
            self.__title = Label(self.__frame, text=self.__dictionaries.getWordFromCurrentLanguage(labelText),
                                       font=fontNormal,
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font")
                                       )
            self.__title.pack(side=TOP, anchor=W, fill=X)

        self.__subFrame = Frame(self.__frame, height=ten * 2,
                                       bg=self.__loader.colorPalettes.getColor("window"))
        self.__subFrame.pack_propagate(False)
        self.__subFrame.pack(side=TOP, anchor=N, fill=X)

        self.__NameFrame = Frame(self.__subFrame, height=ten,
                                  bg=self.__loader.colorPalettes.getColor("window"))
        self.__NameFrame.pack_propagate(False)
        self.__NameFrame.pack(side=TOP, anchor=N, fill=X)

        self.__NameLabel = Label(self.__NameFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  font=fontSmall,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  fg=self.__loader.colorPalettes.getColor("font")
                                  )
        self.__NameLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__Value = StringVar()
        self.__Value.set(default)

        self.__NameEntry = Entry(self.__NameFrame, textvariable=self.__Value, name=entryName)
        self.__NameEntry.config(width=99999, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 font=fontSmall
                                 )

        self.__NameEntry.pack(side=LEFT, anchor=E, fill=BOTH)
        self.__NameEntry.bind("<KeyRelease>", bindedFunc)

        self.__buttons = Frame(self.__subFrame, height=ten,
                                             bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttons.pack_propagate(False)
        self.__buttons.pack(side=TOP, anchor=N, fill=X)

        self.__openPic = self.__loader.io.getImg("open", None)
        self.__savePic = self.__loader.io.getImg("save", None)

        self.__openButton = Button(self.__buttons, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__openPic, width=w,
                                   command = openCommand)

        self.__openButton.pack(side = LEFT, anchor = W, fill=Y)

        self.__saveButton = Button(self.__buttons, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__savePic, width=w,
                                   state=DISABLED, command=saveCommand)

        self.__saveButton.pack(side = LEFT, anchor = W, fill=Y)

    def getEntry(self):
        return(self.__NameEntry)

    def getValue(self):
        return(self.__Value.get())

    def setValue(self, value):
        self.__Value.set(value)

    def enableSave(self):
        self.__saveButton.config(state=NORMAL)

    def disableSave(self):
        self.__saveButton.config(state=DISABLED)