from tkinter import *

class FrameLabelEntryUpDown:

    def __init__(self, loader, parent, w, h, text, mini, maxi, font, function, default, font2, key, errors, focusIn, focusOut):

        self.focusIn = focusIn
        self.focusOut = focusOut

        self.__loader = loader
        self.__colors = self.__loader.colorPalettes
        self.__dictionaries = self.__loader.dictionaries

        self.__errorCounters = errors
        self.__key = key

        self.__frame = Frame(parent, width=w,
                                   bg=self.__colors.getColor("window"))
        self.__frame.pack_propagate(False)
        self.__frame.pack(side=LEFT, anchor = W, fill=Y)

        self.__frame3 = Frame(self.__frame, width=w, height=h//2,
                                   bg=self.__colors.getColor("window"))
        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=TOP, anchor = N, fill=X)

        self.__label = Label(self.__frame3,
                             width=w,
                             bg=self.__colors.getColor("window"),
                             fg=self.__colors.getColor("font"),
                             font=font,
                             text = self.__dictionaries.getWordFromCurrentLanguage(text)
                             )
        self.__label.pack_propagate(False)
        self.__label.pack(side=TOP, anchor=N, fill=X)

        self.__variable = StringVar()
        self.__variable.set(str(default))

        self.__frame2 = Frame(self.__frame, width=w, height=h//2,
                                   bg=self.__colors.getColor("window"))
        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=TOP, anchor = N, fill=BOTH)

        self.__function = function

        self.__entry = Entry(
                        self.__frame2,
                        width=9999,
                        bg=self.__colors.getColor("boxBackNormal"),
                        fg=self.__colors.getColor("boxFontNormal"),
                        font=font2, justify = CENTER,
                        textvariable = self.__variable,
                        state = DISABLED
        )
        self.__entry.pack(side=TOP, anchor = N, fill = BOTH)

        self.__entry.bind("<FocusIn>", self.focusIn)
        self.__entry.bind("<FocusOut>", self.__checkEntry)
        self.__entry.bind("<KeyRelease>", self.__checkEntry)
        self.__min = mini
        self.__max = maxi

    def enable(self):
        self.__entry.config(state=NORMAL)

    def __checkEntry(self, event):
        if "FocusOut" in str(event):
            self.focusOut(event)
        try:
            number = int(self.__variable.get())
            self.__entry.config(bg=self.__colors.getColor("boxBackNormal"),
                                fg=self.__colors.getColor("boxFontNormal"))
        except:
            self.__entry.config(bg=self.__colors.getColor("boxBackUnSaved"),
                                fg=self.__colors.getColor("boxFontUnSaved"))

            self.__errorCounters[self.__key] = 1
            return

        self.__errorCounters[self.__key] = 0
        if number < self.__min:
            number = self.__min
        elif number > self.__max:
            number = self.__max

        self.__variable.set(str(number))

        if self.__function!=None:
            self.__function(number)


    def setValue(self, val):
        self.__variable.set(str(val))