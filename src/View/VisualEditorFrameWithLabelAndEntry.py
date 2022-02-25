from tkinter import *


class VisualEditorFrameWithLabelAndEntry:

    def __init__(self, loader, default, masterFrame, h, text, font, releaseBind, focusBind):
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries


        self.__value = StringVar()

        if default != None:
            self.__value.set(default)

        self.__frame = Frame(masterFrame, height = h, bg=self.__loader.colorPalettes.getColor("window"))
        while self.__frame.winfo_width() < 2:
            self.__frame.config(width = masterFrame.winfo_width())
            self.__frame.pack_propagate(False)
            self.__frame.pack(side=TOP, anchor=N, fill=X)

        self.__f1 = Frame(self.__frame, height = h, bg=self.__loader.colorPalettes.getColor("window"),
                          width = self.__frame.winfo_width()//4 * 3)

        while (self.__f1.winfo_width() < self.__frame.winfo_width()//2):
            self.__f1.config(width = self.__frame.winfo_width()//4 * 3)
            self.__f1.pack_propagate(False)
            self.__f1.pack(side=LEFT, anchor=E, fill=Y)

        self.__f2 = Frame(self.__frame, height = h, bg=self.__loader.colorPalettes.getColor("window"),
                          width = self.__frame.winfo_width()//4)
        self.__f2.pack_propagate(False)
        self.__f2.pack(side=LEFT, anchor=E, fill=BOTH)


        self.__label = Label(self.__f1, text=self.__dictionaries.getWordFromCurrentLanguage(text),
                                   font=font,
                                   bg = self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__label.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__entry = Entry(self.__f2, textvariable=self.__value, name="nope")
        self.__entry.config(width=99999, bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = CENTER,
                                  font=font
                                  )

        if releaseBind!=None:
            self.__entry.bind("<KeyRelease>", releaseBind)

        if focusBind!=None:
            self.__entry.bind("<FocusOut>", focusBind)
        self.__entry.pack(side=LEFT, anchor=E, fill=BOTH)

    def getEntry(self):
        return(self.__entry)

    def getValue(self):
        return(self.__value.get())

    def setValue(self, value):
        self.__value.set(value)