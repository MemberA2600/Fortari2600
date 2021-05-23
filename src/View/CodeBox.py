from tkinter import scrolledtext
from tkinter import *
from threading import Thread

class CodeBox:

    def __init__(self, loader, editor, frame):

        self.__loader = loader
        self.keyPress = False
        self.ctrlPressed = False

        self.__bank = self.__loader.BFG9000.getSelected()[0]
        self.__section = self.__loader.BFG9000.getSelected()[1]
        self.__editor = editor
        self.__frame = frame
        self.__config = self.__loader.config

        self.__lastScaleX = self.__editor.getScales()[0]
        self.__lastScaleY = self.__editor.getScales()[1]

        self.box = scrolledtext.ScrolledText(self.__frame, width=999999, height=9999999, wrap=WORD)
        self.box.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.also = False
        self.getFont()
        self.tintingThreads=[]
        self.highOriginal = ""

        self.box.pack(side=BOTTOM, anchor=S, fill=BOTH)
        self.loadCode()
        self.__loader.currentEditor = self.box
        self.addTinting()

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        t = Thread(target=self.checker)
        t.daemon = True
        t.start()

        self.box.bind("<Key>", self.keyPressed)
        self.box.bind("<KeyRelease>", self.keyReleased)
        self.box.bind("<MouseWheel>", self.mouseWheel)
        self.box.bind("<FocusIn>", self.__loader.mainWindow.focusIn)
        self.box.bind("<FocusOut>", self.__loader.mainWindow.focusOut)

    def getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__editor.getWindowSize()[0] / 955
        h = self.__editor.getWindowSize()[1] / 686

        self.__fontSize = (baseSize * w * h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.box.config(font=self.__font)

    def loadCode(self):
        self.box.delete(1.0, END)
        self.box.insert(1.0, self.__loader.virtualMemory.codes[self.__bank][self.__section].code)
        self.lastLen=len(self.__loader.virtualMemory.codes[self.__bank][self.__section].code)

    def checker(self):
        from time import sleep
        while (self.__loader.mainWindow.dead == False and self.stopThread==False):
            if (self.keyPress==True):
                sleep(0.75)
                if (self.keyPress == False):
                    self.__loader.BFG9000.saveAllCode()
                    self.addTinting()

            if "replacerFrame" in self.__loader.frames.keys():
                if (self.__loader.frames["replacerFrame"].originalText.get() != self.highOriginal or
                    self.__loader.frames["replacerFrame"].alsoComments.get() != self.also):
                        self.highOriginal = self.__loader.frames["replacerFrame"].originalText.get()
                        self.also = self.__loader.frames["replacerFrame"].alsoComments.get()
                        self.addTinting()


            if self.__loader.frames["CodeEditor"].forceCheck==True:
                self.__loader.frames["CodeEditor"].forceCheck=False
                self.loadCode()
                self.addTinting()
                for bank in self.__loader.virtualMemory.codes.keys():
                    for section in self.__loader.virtualMemory.codes[bank].keys():
                        if section not in ["subroutines", "vblank", "enter", "leave", "overscan", "screen_bottom"]:
                            continue
                        if self.__loader.frames["CodeEditor"].forceValue == None:
                            self.__loader.virtualMemory.codes[bank][section].changed = True
                        else:
                            if self.__loader.frames["CodeEditor"].forceValue in self.__loader.virtualMemory.codes[bank][section].code:
                                self.__loader.virtualMemory.codes[bank][section].changed = True
                self.__loader.virtualMemory.archieve()

            sleep(0.05)

    def keyPressed(self, event):
        self.keyPress = True
        try:
            test = ord(event.keysym)
            self.__editor.changed = True
        except:
            if len(self.__loader.virtualMemory.codes[self.__bank][self.__section].code)!=self.lastLen:
                self.__editor.changed = True
                self.lastLen = len(self.__loader.virtualMemory.codes[self.__bank][self.__section].code)

        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.ctrlPressed = True

    def keyReleased(self, event):
        self.keyPress = False
        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.ctrlPressed = False

    def mouseWheel(self, event):
        if self.ctrlPressed == True:
            if event.delta > 0 and int(self.__config.getValueByKey("codeBoxFont"))<36:
                self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont"))+1))
                self.getFont()

            if event.delta < 0 and int(self.__config.getValueByKey("codeBoxFont"))>12:
                self.__config.setKey("codeBoxFont", str(int(self.__config.getValueByKey("codeBoxFont"))-1))
                self.getFont()

    def addTinting(self):
        text = self.box.get(0.0, END).split("\n")
        for tag in self.box.tag_names():
            self.box.tag_remove(tag, "0.0", END)
        self.addCommentTinting(text)
        self.waitForEndAll()
        if "replacerFrame" in self.__loader.frames.keys():
            if len(self.__loader.frames["replacerFrame"].originalText.get()) > 0:
                self.addHighLight(text, self.__loader.frames["replacerFrame"].originalText.get())
        self.waitForEndAll()

    def waitForEndAll(self):
        while len(self.tintingThreads)>0:
            for t in self.tintingThreads:
                if t.is_alive() == False:
                    self.tintingThreads.remove(t)


    def addCommentTinting(self, text):
        self.box.tag_config("comment", foreground=self.__loader.colorPalettes.getColor("comment"),
                                  font=self.__loader.fontManager.getFont(round(self.__fontSize), False, True, False))
        lineNum = 0
        for line in text:
            lineNum+=1
            q = Thread(target=self.commentTintingThread, args=[line, lineNum])
            q.daemon = True
            self.tintingThreads.append(q)
            q.start()

    def commentTintingThread(self, line, lineNum):
        if line.startswith("#") or line.startswith("*"):
            self.box.tag_add("comment", f"{str(lineNum)}.0", f"{str(lineNum)}.{str(len(line))}")
        else:
            poz = self.getPositionOfFirstDeliminator(line)
            if poz != None:
                self.box.tag_add("comment", f"{str(lineNum)}.{str(poz)}", f"{str(lineNum)}.{str(len(line))}")

    def addHighLight(self, text, word):
        self.box.tag_config("highLight", background=self.__loader.colorPalettes.getColor("highLight"))
        lineNum = 0
        for line in text:
            lineNum+=1
            q = Thread(target=self.highLightTintingThread, args=[line, lineNum, word])
            q.daemon = True
            self.tintingThreads.append(q)
            q.start()

    def highLightTintingThread(self, line, lineNum, word):
        if self.__loader.frames["replacerFrame"].alsoComments.get() == 0:
            if line.startswith("#") or line.startswith("*"):
                return
            elif word in line:
                theLen = len(line)
                if self.getPositionOfFirstDeliminator(line) != None:
                    theLen = self.getPositionOfFirstDeliminator(line)

                for poz in range(0, theLen):
                    if line[poz:poz+len(word)] == word:
                        self.box.tag_add("highLight", f"{str(lineNum)}.{str(poz)}", f"{str(lineNum)}.{str(poz+len(word))}")

        else:
            for poz in range(0, len(line)):
                if line[poz:poz + len(word)] == word:
                    self.box.tag_add("highLight", f"{str(lineNum)}.{str(poz)}", f"{str(lineNum)}.{str(poz+len(word))}")


    def getPositionOfFirstDeliminator(self, line):
        deliminator = self.__config.getValueByKey("deliminator")
        valid = 0
        for position in range(0, len(line) - len(deliminator)+1):
            if line[position] == "(":
                valid += 1
            elif line[position] == ")":
                valid -= 1
            elif valid == 0:
                if line[position:position + len(deliminator)] == deliminator:
                    return(position)
        return(None)

    def replaceTextInThisSection(self, bank, section, original, new):
        if self.__loader.frames["replacerFrame"].alsoComments.get() == 1:
            self.__loader.virtualMemory.codes[bank][section].code = self.__loader.virtualMemory.codes[bank][section].code.replace(original, new)
        else:
            text = self.__loader.virtualMemory.codes[bank][section].code.split("\n")
            newText = []
            for line in text:
                if line.startswith("#") or line.startswith("*"):
                    newText.append(line)
                elif self.getPositionOfFirstDeliminator(line) == None:
                    newText.append(line.replace(original, new))
                else:
                    poz = self.getPositionOfFirstDeliminator(line)
                    newText.append(
                            line[:poz].replace(original, new) + line[poz:]
                    )
            self.__loader.virtualMemory.codes[bank][section].code = "\n".join(newText)
        if new in (self.__loader.virtualMemory.codes[bank][section].code):
            self.__loader.virtualMemory.codes[bank][section].changed = True

        if bank==self.__bank and section==self.__section:
            self.loadCode()