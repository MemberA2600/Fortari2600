from tkinter import *

class SongInput:

    def __init__(self, loader, mother, w, h, text, input, font, focusIn, focusOut):

        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries
        self.__colors = self.__loader.colorPalettes

        self.__frame = Frame(mother,
                                   height=h,
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=TOP, fill=X)

        self.__labelFrame = Frame(self.__frame,
                                   height=h,
                                    width=round(w/8),
                                   bg=self.__colors.getColor("window"))
        self.__labelFrame.pack_propagate(False)
        self.__labelFrame.pack(side=LEFT, fill=Y)

        self.__label = Label(self.__labelFrame,
                             text = " "*2+self.__dictionaries.getWordFromCurrentLanguage(text),
                             bg=self.__colors.getColor("window"),
                             fg = self.__colors.getColor("font"),
                             font = font
                             )

        self.__label.pack_propagate(False)
        self.__label.pack(fill=BOTH, side=LEFT, anchor = W)

        self.__entryFrame = Frame(self.__frame,
                                   height=h,
                                    width=9999,
                                   bg=self.__colors.getColor("window"))
        self.__entryFrame.pack_propagate(False)
        self.__entryFrame.pack(side=LEFT, fill=BOTH)

        self.__entry = Entry (
            self.__entryFrame, width=9999,
            textvariable = input,
            bg=self.__colors.getColor("boxBackNormal"),
            fg=self.__colors.getColor("boxFontNormal"),
            font = font

        )
        self.__entry.pack_propagate(False)
        self.__entry.pack(fill=BOTH)

        self.__entry.bind("<FocusIn>", focusIn)
        self.__entry.bind("<FocusOut>", focusOut)