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

        self.getFont()
        self.tintingThreads=[]

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
                sleep(0.35)
                if (self.keyPress == False):
                    self.__loader.BFG9000.saveAllCode()
                    self.addTinting()

            for t in self.tintingThreads:
                if t.is_alive() == False:
                    self.tintingThreads.remove(t)

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

    def getPositionOfFirstDeliminator(self, line):
        deliminator = self.__config.getValueByKey("deliminator")
        valid = 0
        for position in range(0, len(line) - len(deliminator)):
            if line[position] == "(":
                valid += 1
            elif line[position] == ")":
                valid -= 1
            elif valid == 0:
                if line[position:position + len(deliminator)] == deliminator:
                    return(position)
        return(None)