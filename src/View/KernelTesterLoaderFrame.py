from tkinter import *

class KernelTesterLoaderFrame:

    def __init__(self, loader, parent, h, font, title, w, boss):
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries
        self.__fileDialogs = self.__loader.fileDialogs
        self.__topLevelW = parent
        self.__boss = boss


        self.__frame = Frame(parent, height=h, width=w,
                             bg=self.__loader.colorPalettes.getColor("window")
                             )

        self.__frame.pack_propagate(False)
        self.__frame.pack(side = TOP, anchor = N, fill=X)

        self.__title = Label(self.__frame, text = self.__dictionaries.getWordFromCurrentLanguage(title),
                             bg = self.__loader.colorPalettes.getColor("window"),
                             fg = self.__loader.colorPalettes.getColor("font"),
                             font =  font, justify=LEFT)
        self.__title.pack(side=TOP, anchor = N, fill=X)

        self.__FFF = Frame(self.__frame, width=w,
                             height = round(h/2),
                             bg=self.__loader.colorPalettes.getColor("window"),
                             )
        self.__FFF.pack_propagate(False)
        self.__FFF.pack(side = TOP, anchor = N, fill=BOTH)

        """
        while self.__FFF.winfo_width() == 1 or self.__FFF.winfo_height() == 1:
            self.__FFF.config(width=self.__frame.winfo_width(),
                             height = round(self.__frame.winfo_height()/2))
            self.__FFF.pack(side=TOP, anchor=N, fill=BOTH)
            print(self.__FFF.winfo_width(), self.__FFF.winfo_height())
        """

        self.__entryFrame = Frame(self.__FFF, width=round(w/4*3),
                             bg=self.__loader.colorPalettes.getColor("window"),
                             )


        self.__entryVal = StringVar()

        self.__entryFrame.pack_propagate(False)
        self.__entryFrame.pack(side = LEFT, anchor = W, fill=Y)

        self.__entry = Entry(self.__entryFrame, textvariable = self.__entryVal,
                             bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                             fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                             width=99999, font=font
                             )
        self.__entry.pack_propagate(False)
        self.__entry.pack(side=TOP, anchor=N, fill=BOTH)
        self.__entry.bind("<KeyRelease>", self.checkIfValidFileName)

        """
        while self.__entryFrame.winfo_width() == 1 or self.__entryFrame.winfo_height() == 1:
            self.__entryFrame.config(width=99999, height=99999)
            self.__entryFrame.pack(side=TOP, anchor=N, fill=BOTH)
            print(self.__entryFrame.winfo_width(), self.__entryFrame.winfo_height())

        """
        #print(self.__FFF.winfo_width(), self.__FFF.winfo_height(), self.__entryFrame.winfo_width(), self.__entryFrame.winfo_height())

        self.__openPic = self.__loader.io.getImg("open", round(h*0.33))

        self.__button = Button(self.__FFF, image = self.__openPic, width=round(w/4),
                               height = h,
                               command = self.openFileName,
                               bg=self.__loader.colorPalettes.getColor("window")
                              )

        self.__button.pack_propagate(False)
        self.__button.pack(side=RIGHT, anchor=E, fill=BOTH)

        self.valid = False

        from threading import Thread
        e = Thread(target=self.checkIfExists)
        e.daemon = True
        e.start()

    def checkIfExists(self):
        from time import sleep
        import os

        while self.__boss.dead == False:
            if os.path.exists(self.__entryVal.get()):
                self.valid = True
            else:
                self.valid = False
            sleep(0.1)

    def getValue(self):
        return self.__entryVal.get()

    def setValue(self, val):
        self.__entryVal.set(val)

    def checkIfValidFileName(self, event):
        widget = self.__entry
        value = self.__entryVal.get()

        if self.__loader.io.checkIfValidFileName(value):
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                          )

        else:
            widget.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                          fg=self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                          )

    def openFileName(self):

        self.__entryVal.set(self.__fileDialogs.askForFileName("openFile", False, ["asm", "*"],
                                                  "templates/"))

        self.__topLevelW.deiconify()
        self.__topLevelW.focus()