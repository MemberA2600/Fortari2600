from tkinter import *
from threading import Thread

class LeftFrameEditor:

    def __init__(self, loader, frame, validity, view):
        self.__loader = loader
        self.__frame = frame

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
                                self.applyDeliminatorChange, self.delimiterChangerValid)


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
                self.__loader.frames["CodeEditor"].forceCheck = True
