from tkinter import *
from threading import Thread
from PIL import Image, ImageTk
from SubMenu import SubMenu

class KernelChanger:

    def __init__(self, loader):
        self.dead = False
        self.__loader=loader
        self.OK = False

        self.__virtualMemory = self.__loader.virtualMemory
        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__smallFontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*11)

        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__smallFont = self.__loader.fontManager.getFont(round(self.__smallFontSize), False, False, False)


        self.__colors = self.__loader.colorPalettes
        self.__screenSize = self.__loader.screenSize

        self.__window = SubMenu(self.__loader, "changeKernel", self.__screenSize[0] / 5, self.__screenSize[1] / 3 - 15,
                           None, self.__addElements, 1)
        self.dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__frameChooser = Frame(self.__topLevelWindow)
        self.__frameChooser.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__frameChooser.pack(fill=BOTH)

        self.__title = Label(self.__frameChooser, text=self.__dictionaries.getWordFromCurrentLanguage("currentKernel"))
        self.__title.config(font =self.__font, bg=self.__loader.colorPalettes.getColor("window"),
                            fg=self.__loader.colorPalettes.getColor("font"))

        self.__static = StringVar()
        self.__static.set(self.__virtualMemory.kernel)
        self.__entry = Entry(self.__frameChooser, textvariable=self.__static)
        self.__entry.config(font =self.__font,
                            fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                            bg=self.__loader.colorPalettes.getColor("boxBackNormal"), state=DISABLED
                            )

        self.__title.pack(side=TOP, anchor=N, fill=X)
        self.__entry.pack(side=TOP, anchor=N, fill=X)

        self.__title2 = Label(self.__frameChooser, text=self.__dictionaries.getWordFromCurrentLanguage("availableKernels"))
        self.__title2.config(font =self.__font, bg=self.__loader.colorPalettes.getColor("window"),
                            fg=self.__loader.colorPalettes.getColor("font"))

        self.__title2.pack(side=TOP, anchor=N, fill=X)

        self.__listBoxFrame = Frame(self.__frameChooser)
        self.__listBoxFrame.config(bg=self.__loader.colorPalettes.getColor("window"),
                                   height=round(self.__topLevel.getTopLevelDimensions()[1]*0.6)
                                   )
        self.__listBoxFrame.pack_propagate(False)
        self.__listBoxFrame.pack(fill=X)

        self.__scrollBar = Scrollbar(self.__listBoxFrame)

        self.__listBox = Listbox(self.__listBoxFrame, selectmode=SINGLE,
                                 bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 fg=self.__loader.colorPalettes.getColor(
                                                                             "boxFontNormal"),
                                 height=999999,
                                 yscrollcommand=self.__scrollBar.set
                                 )
        self.__scrollBar.pack(side=RIGHT, anchor=SW, fill=Y)
        self.__listBox.config(font=self.__smallFont)
        self.__listBox.pack(fill=BOTH)

        selectables = []
        for item in self.__virtualMemory.kernel_types:
            self.__listBox.insert(END, item)
            selectables.append(item)

        self.__buttonsFrame = Frame(self.__frameChooser)
        self.__buttonsFrame.config(bg=self.__loader.colorPalettes.getColor("window"), height=round(self.__topLevel.getTopLevelDimensions()[1]*0.1))
        self.__buttonsFrame.pack_propagate(False)
        self.__buttonsFrame.pack(fill=X)

        self.__buttonsFrame1 = Frame(self.__buttonsFrame)
        self.__buttonsFrame1.config(bg=self.__loader.colorPalettes.getColor("window"), height=round(self.__topLevel.getTopLevelDimensions()[1]*0.1),
                                    width=round(self.__topLevel.getTopLevelDimensions()[0]/2))
        self.__buttonsFrame1.pack_propagate(False)


        self.__buttonsFrame2 = Frame(self.__buttonsFrame)
        self.__buttonsFrame2.config(bg=self.__loader.colorPalettes.getColor("window"), height=round(self.__topLevel.getTopLevelDimensions()[1]*0.1),
                                    width=round(self.__topLevel.getTopLevelDimensions()[0]/2))
        self.__buttonsFrame2.pack_propagate(False)

        #self.__buttonsFrame1.config(bg="red")
        #self.__buttonsFrame2.config(bg="blue")

        self.__buttonsFrame1.pack(side=LEFT, fill=Y)
        self.__buttonsFrame2.pack(side=LEFT, fill=Y)

        self.__buttonOK = Button(self.__buttonsFrame1,
                               width=round(self.__buttonsFrame.winfo_width()/2),
                               command=self.doThings,
                               state=DISABLED,
                               font=self.__font, fg=self.__colors.getColor("font"),
                               bg=self.__colors.getColor("window"))

        self.__buttonOK.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonOK.config(text="OK", font=self.__smallFont)
        self.__buttonOK.pack_propagate(False)
        self.__buttonOK.pack(fill=BOTH)

        self.__buttonCancel = Button(self.__buttonsFrame2,
                               width=round(self.__buttonsFrame.winfo_width()/2),
                               command=self.killMe,
                               font=self.__font, fg=self.__colors.getColor("font"),
                               bg=self.__colors.getColor("window"))

        self.__buttonCancel.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__buttonCancel.config(text=self.__dictionaries.getWordFromCurrentLanguage("cancel"), font=self.__smallFont)
        self.__buttonCancel.pack_propagate(False)
        self.__buttonCancel.pack(fill=BOTH)

        for number in range(0, self.__listBox.size()):
            if selectables[number] == self.__static.get():
                self.__listBox.select_set(number)


        e = Thread(target=self.enableDisable)
        e.daemon = True
        e.start()


    def killMe(self):
        self.__topLevelWindow.destroy()

    def enableDisable(self):
        from time import sleep

        while (self.dead==False and self.__loader.mainWindow.dead==False):
            try:
                if self.__listBox.get(ACTIVE)!=self.__static.get():
                    self.__buttonOK.config(state=NORMAL)
                else:
                    self.__buttonOK.config(state=DISABLED)
            except Exception as e:
                self.__loader.logger.errorLog(e)

            sleep(0.4)

    def doThings(self):
        self.__loader.soundPlayer.playSound("Ask")
        if (self.__fileDialogs.askYesOrNo("warning", "kernelChangeWarning") == "Yes"):
            self.__virtualMemory.changeKernelMemory(self.__static, self.__listBox.get(ACTIVE))

        self.killMe()


