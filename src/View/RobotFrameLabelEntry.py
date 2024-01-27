from tkinter import *

class RobotFrameLabelEntry:

    def __init__(self, loader, motherFrame, w, h, font, checker, default, name):
        
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.baseFrame = Frame(motherFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  w,
                                height= h)
        self.baseFrame.pack_propagate(False)
        self.baseFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.labelFrame = Frame(self.baseFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  round(w*0.66),
                                height= h)
        self.labelFrame.pack_propagate(False)
        self.labelFrame.pack(side=LEFT, anchor=E, fill=Y)

        self.label = Label(self.labelFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                font = font, justify = LEFT,
                                text = self.__dictionaries.getWordFromCurrentLanguage(name))
        self.label.pack_propagate(False)
        self.label.pack(side=LEFT, anchor=E, fill=Y)

        self.var = StringVar()
        self.var.set(default)
        self.entryFrame = Frame(self.baseFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                       width=round(w * 0.33),
                                       height=h)
        self.entryFrame.pack_propagate(False)
        self.entryFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.entry = Entry(self.entryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=3,
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 textvariable=self.var, name=name,
                                 font=font, justify=CENTER,
                                 command=None)
        self.entry.pack_propagate()
        self.entry.pack(side=TOP, anchor=N, fill=BOTH)

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.entry, "<KeyRelease>", checker, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.entry, "<FocusOut>"  , checker, 1)

        #elf.entry.bind("<KeyRelease>", checker)
        #self.entry.bind("<FocusOut>", checker)
