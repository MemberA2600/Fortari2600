from tkinter import *

class FortariMB:

    def __init__(self, loader, frame, state, font, defaultText, items, multiSelect, translate, command, defaultSelected):
        self.__loader          = loader
        self.__frame           = frame
        self.__items           = items
        self.multiSelect     = multiSelect
        self.__command         = command
        self.__defaultSelected = defaultSelected

        if translate:
           for num in range(0, len(items)):
              try:
                 items[num] = self.__loader.dictionaries.getWordFromCurrentLanguage(items[num])
              except:
                 pass

        self.__default = defaultText
        menuButton = {}
        mName = StringVar()
        mName.set(defaultText)
        m = Menubutton(frame, textvariable=mName, relief=RAISED,
                       bg=self.__loader.colorPalettes.getColor("window"),
                       width=9999,
                       fg=self.__loader.colorPalettes.getColor("font"),
                       state=state, font=font, justify=CENTER,
                       command=None)
        m.pack_propagate(False)
        m.pack(side=TOP, anchor=CENTER, fill=BOTH)

        menuButton["button"] = m
        menuButton["text"] = mName

        self.__selectVars = []
        self.__selected = StringVar()

        menu = Menu(m, tearoff=0,
                    bg=self.__loader.colorPalettes.getColor("window"),
                    fg=self.__loader.colorPalettes.getColor("font"),
                    font=font
                    )
        m["menu"] = menu

        for num in range(0, len(items)):
            if multiSelect:
               self.__selectVars.append(IntVar())
               menu.add_checkbutton(label = items[num], variable = self.__selectVars[num], command = self.__clicked)
            else:
               menu.add_radiobutton(label = items[num], variable = self.__selected, command = self.__clicked)

        self.__menuButtonName = mName
        self.__menuButton = m

        for item in self.__defaultSelected:
            self.select(item, True)

    def __clicked(self):
        if self.multiSelect == False:
           self.__menuButtonName.set(self.__selected.get())

        self.__command()

    def getSelected(self):
        if self.multiSelect:
           selectedOnes = []
           index = -1
           for var in self.__selectVars:
               index = index + 1
               if var.get() == 1:
                  selectedOnes.append(self.__items[index])
           return(selectedOnes)
        else:
           return self.__selected.get()

    def isSelected(self, one):
        if self.multiSelect:
           selectedOnes = []
           index = -1
           for var in self.__selectVars:
               index = index + 1
               if self.__items[index] == one:
                  return var.get()
        else:
           return self.__selected.get() == one

    def select(self, one, state):
        if one in ("[", "]"): raise ValueError

        if type(one) == int:
           one = self.__items[one]

        if self.multiSelect:
           listOfThem = one
           if type(one) == str:
               listOfThem = one[1:-1].split(",")

           for item in listOfThem:
               if item in self.__items:
                  self.__selectVars[self.__items.index(item)].set(state)
        else:
           if state:
              self.__selected.set(one)
              self.__menuButtonName.set(one)
           else:
              self.__selected.set("")
              self.__menuButtonName.set(self.__default)

    def deSelect(self):
        if self.multiSelect == False:
           self.__selected.set("")
           self.__menuButtonName.set(self.__default)
        else:
           for var in self.__selectVars:
               var.set(0)

    def changeState(self, state):
        self.__menuButton.config(state = state)

    def selectDefault(self):
        self.deSelect()
        self.select(self.__defaultSelected, True)