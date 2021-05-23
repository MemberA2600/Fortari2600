from tkinter import *
from threading import Thread

class LeftFrameEditor:

    def __init__(self, loader, frame, validity, view):
        self.__loader = loader
        self.__frame = frame

        self.__bank = self.__loader.BFG9000.getSelected()[0]
        self.__section = self.__loader.BFG9000.getSelected()[1]

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__originalW = self.__frame.winfo_width()
        self.__originalH = self.__frame.winfo_height()
        self.__loader.frames["leftFrame"] = self

        from LeftFrameSetterFrame import LeftFrameSetterFrame
        self.__delimiterSetter = LeftFrameSetterFrame(self.__loader, "deliminatorFrame",
                                 self.__frame, "deliminatorSetter", self, 0.15, 20,
                                validity, view, self.addItemsToDelimiterSetter,
                                self.applyDeliminatorChange, self.delimiterChangerValid, None)

        self.__replacerSetter = LeftFrameSetterFrame(self.__loader, "replacerFrame",
                                 self.__frame, "replacer", self, 0.50, 20,
                                validity, view, self.addItemsToReplacer,
                                self.applyReplace, self.replaceChangerValid, None)

        self.__screenItems = LeftFrameSetterFrame(self.__loader, "screenItems",
                                 self.__frame, "screenItems", self, 0.35, 20,
                                validity, view, self.addScreenItemsItems,
                                self.addScreenItem, self.screenItemsValid, "insertItem")

        t = Thread(target=self.sizing)
        t.daemon = True
        t.start()

    def sizing(self):
        from time import sleep
        while self.__loader.mainWindow.dead == False and self.stopThread==False:

            sleep(0.04)


    def getScales(self):
        return(
            self.__frame.winfo_width()/self.__originalW,
            self.__frame.winfo_height() / self.__originalH,
        )

    def getSizes(self):
        return(
            self.__frame.winfo_width(), self.__frame.winfo_height()
        )

    def addScreenItemsItems(self, father, frame, items):
        pass

    def addScreenItem(self):
        pass

    def screenItemsValid(self):
        pass

    def delimiterChangerValid(self, father, entryVar):
        problem = False

        if len(entryVar.get()) == 0:
            problem = True
        elif " " in entryVar.get():
            problem = True
        elif "\t" in entryVar.get():
            problem = True
        else:
            if len(re.findall(r"^[a-zA-Z0-9]+$", entryVar.get()))>0:
                problem = True
            elif len(re.findall(r"^([0-9]+[\+\-\=\*\/]{1,2}[0-9]*)+$", entryVar.get()))>0:
                problem = True
            elif len(re.findall(r"^[a-zA-Z][a-zA-Z-0-9\-\_]+$", entryVar.get()))>0:
                problem = True


        if problem == False:
            father.enableButton()
        else:
            father.disableButton()


    def addItemsToDelimiterSetter(self, father, frame, items):
        father.entryVar = StringVar()
        father.entryVar.set(self.__loader.config.getValueByKey("deliminator"))

        father.__entry = Entry(frame, width=9999999, textvariable = father.entryVar)
        father.__entry.pack(side=BOTTOM, anchor=SW)
        father.__entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        father.__entry.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        father.__entry.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        father.__entry.bind("<FocusOut>", self.__loader.mainWindow.focusOut)

        items.append(father.__entry)

    def applyDeliminatorChange(self):
        old = self.__loader.config.getValueByKey("deliminator")
        new = self.__loader.frames["deliminatorFrame"].entryVar.get()

        for bank in self.__loader.virtualMemory.codes.keys():
            for section in self.__loader.virtualMemory.codes[bank].keys():
                if section not in ["subroutines", "vblank", "enter", "leave", "overscan", "screen_bottom"]:
                    continue
                lines = self.__loader.virtualMemory.codes[bank][section].code.split("\n")
                newText = []
                for line in lines:
                    if line.startswith("*") or line.startswith("#"):
                        newText.append(line)
                        continue
                    for num in range(0, len(line)-len(old)+1):
                        valid = 0
                        if line[num] == "(":
                            valid+=1
                        elif line[num] == ")":
                            valid-=1
                        elif valid == 0 and line[num:num+len(old)] == old:
                            line = line[:num] + new + line[num+len(old):]
                    newText.append(line)
                self.__loader.config.setKey("deliminator", new)
                self.__loader.virtualMemory.codes[bank][section].code = "\n".join(newText)
                self.__loader.frames["CodeEditor"].forceValue = new
                self.__loader.frames["CodeEditor"].forceCheck = True
                self.__loader.config.saveConfig()


    def addItemsToReplacer(self, father, frame, items):
        father.originalText = StringVar()
        father.newText = StringVar()

        father.alsoComments = IntVar()
        father.__commentSelect = Checkbutton(frame, variable=father.alsoComments,
                                             text=self.__loader.dictionaries.getWordFromCurrentLanguage("alsoComments"))

        father.__commentSelect.pack(side=BOTTOM, anchor=SW)
        father.selectedOption = IntVar()
        father.__optionSection = Radiobutton(frame, variable=father.selectedOption, value=0,
                                             text=self.__loader.dictionaries.getWordFromCurrentLanguage("thisText"))

        father.__optionBank = Radiobutton(frame, variable=father.selectedOption, value=1,
                                          text=self.__loader.dictionaries.getWordFromCurrentLanguage("thisBank"))

        father.__optionFull = Radiobutton(frame, variable=father.selectedOption, value=2,
                                          text=self.__loader.dictionaries.getWordFromCurrentLanguage("fullCode"))


        father.__optionFull.pack(side=BOTTOM, anchor=SW)
        father.__optionBank.pack(side=BOTTOM, anchor=SW)
        father.__optionSection.pack(side=BOTTOM, anchor=SW)

        father.replaceLabel = Label(frame, text=self.__loader.dictionaries.getWordFromCurrentLanguage("newText"))

        father.__replaceEntry = Entry(frame, width=9999999, textvariable=father.newText)
        father.__replaceEntry.pack(side=BOTTOM, anchor=SW)
        father.__replaceEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        father.__replaceEntry.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        father.replaceLabel.pack(side=BOTTOM, anchor=SW)

        father.originalLabel = Label(frame, text = self.__loader.dictionaries.getWordFromCurrentLanguage("originalText"))

        father.__originalEntry = Entry(frame, width=9999999, textvariable = father.originalText)
        father.__originalEntry.pack(side=BOTTOM, anchor=SW)
        father.__originalEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        father.__originalEntry.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        father.originalLabel.pack(side=BOTTOM, anchor=SW)

        items.append(father.__originalEntry)
        items.append(father.originalLabel)
        items.append(father.__replaceEntry)
        items.append(father.replaceLabel)
        items.append(father.__optionSection)
        items.append(father.__optionBank)
        items.append(father.__optionFull)
        items.append(father.__commentSelect)

        father.__originalEntry.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        father.__originalEntry.bind("<FocusOut>", self.__loader.mainWindow.focusOut)
        father.__replaceEntry.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        father.__replaceEntry.bind("<FocusOut>", self.__loader.mainWindow.focusOut)

    def applyReplace(self):
        if self.__replacerSetter.selectedOption.get() == 0:
            self.__loader.frames["CodeEditor"].codeBox.replaceTextInThisSection(
                self.__bank, self.__section, self.__replacerSetter.originalText.get(), self.__replacerSetter.newText.get())

        elif self.__replacerSetter.selectedOption.get() == 1:
            for section in self.__loader.virtualMemory.codes[self.__bank].keys():
                if section not in ["subroutines", "vblank", "enter", "leave", "overscan", "screen_bottom"]:
                    continue
                self.__loader.frames["CodeEditor"].codeBox.replaceTextInThisSection(
                    self.__bank, section, self.__replacerSetter.originalText.get(), self.__replacerSetter.newText.get())
        else:
            for bank in self.__loader.virtualMemory.codes.keys():
                for section in self.__loader.virtualMemory.codes[bank].keys():
                    if section not in ["subroutines", "vblank", "enter", "leave", "overscan", "screen_bottom"]:
                        continue
                    self.__loader.frames["CodeEditor"].codeBox.replaceTextInThisSection(
                        bank, section, self.__replacerSetter.originalText.get(),
                        self.__replacerSetter.newText.get())

        self.__loader.frames["CodeEditor"].forceValue = self.__replacerSetter.newText.get()
        self.__loader.frames["CodeEditor"].forceCheck = True


    def replaceChangerValid(self, father, entryVar):
        if len(entryVar.get()) == 0:
            father.disableButton()
        else:
            father.enableButton()

