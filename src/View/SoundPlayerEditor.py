from SubMenu import SubMenu
from tkinter import *
from threading import Thread

class SoundPlayerEditor:

    def __init__(self, loader, mainWindow):
        self.__loader = loader
        self.__mainWindow = mainWindow

        self.firstLoad = True
        self.dead = False
        self.changed = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__focused = None
        self.__screenSize = self.__loader.screenSize
        self.__opened = False
        self.__mode = None

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)


        self.__sizes = {
            "common": [self.__screenSize[0] / 6, self.__screenSize[1]/4  - 25]
        }


        self.__window = SubMenu(self.__loader, "soundPlayer", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.dead = True

    def __closeWindow(self):
        self.dead = True
        self.__topLevelWindow.destroy()
        self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__labelText = StringVar()

        hei = self.__topLevel.getTopLevelDimensions()[1]//6

        self.__topLabel = Label(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("font"),
                                fg=self.__loader.colorPalettes.getColor("window"), font = self.__smallFont,
                                width = 9999999,
                                textvariable = self.__labelText)
        self.__topLabel.pack_propagate(False)
        self.__topLabel.pack(side=TOP, anchor=N, fill=X)

        self.__topFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= hei)
        self.__topFrame.pack_propagate(False)
        self.__topFrame.pack(side=TOP, anchor=N, fill=X)

        self.__buttonFrame1 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame1.pack_propagate(False)
        self.__buttonFrame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame2 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame3 = Frame(self.__topFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame3.pack_propagate(False)
        self.__buttonFrame3.pack(side=LEFT, anchor=E, fill=Y)

        self.__openImage = self.__loader.io.getImg("open", None)
        self.__recordImage = self.__loader.io.getImg("record", None)
        self.__robotImage = self.__loader.io.getImg("robot", None)
        self.__playImage = self.__loader.io.getImg("play", None)
        self.__saveImage = self.__loader.io.getImg("save", None)
        self.__emulatorButton = self.__loader.io.getImg("stella", None)


        self.__openButton = Button(self.__buttonFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   name="openSound",
                                   image=self.__openImage, width=999999999, command=self.__plainOpen)
        self.__openButton.pack_propagate(False)
        self.__openButton.pack(fill=BOTH)

        self.__recordButton = Button(self.__buttonFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                     name="recordSound",
                                   image=self.__recordImage, width=999999999, command=self.__createMiddleRecording)
        self.__recordButton.pack_propagate(False)
        self.__recordButton.pack(fill=BOTH)

        self.__robotButton = Button(self.__buttonFrame3, bg=self.__loader.colorPalettes.getColor("window"),
                                    name="generateSpeech",
                                   image=self.__robotImage, width=999999999, command=self.__robotMenu)
        self.__robotButton.pack_propagate(False)
        self.__robotButton.pack(fill=BOTH)

        self.__mouseHover     = False
        self.__mouseHoverSave = False

        self.__openButton.bind("<Enter>", self.__mouseEnter)
        self.__recordButton.bind("<Enter>", self.__mouseEnter)
        self.__robotButton.bind("<Enter>", self.__mouseEnter)

        self.__openButton.bind("<Leave>", self.__mouseLeave)
        self.__recordButton.bind("<Leave>", self.__mouseLeave)
        self.__robotButton.bind("<Leave>", self.__mouseLeave)

        self.__middleFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= round(hei * 3 ))
        self.__middleFrame.pack_propagate(False)
        self.__middleFrame.pack(side=TOP, anchor=N, fill=X)

        self.__fileFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= hei//2)
        self.__fileFrame.pack_propagate(False)
        self.__fileFrame.pack(side=TOP, anchor=N, fill=X)

        self.__textFrame = Frame(self.__fileFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=round(self.__topLevel.getTopLevelDimensions()[0]*0.80),
                                 height= hei//2)
        self.__textFrame.pack_propagate(False)
        self.__textFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__lockFrame = Frame(self.__fileFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=round(self.__topLevel.getTopLevelDimensions()[0]*0.2),
                                 height= hei//2)
        self.__lockFrame.pack_propagate(False)
        self.__lockFrame.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__lock = self.__loader.io.getImg("lockClosed", (hei//2, hei//2))
        self.__lockLabel = Label(self.__lockFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=round(self.__topLevel.getTopLevelDimensions()[0]*0.2*0.55),
                                 image = self.__lock,
                                 height= hei//2)
        self.__lockLabel.pack_propagate(False)
        self.__lockLabel.pack(side=LEFT, fill=Y, anchor=W)

        self.__lockNum = StringVar()

        self.__lockEntry = Entry(
                        self.__lockFrame,
                        width=1,
                        bg=self.__colors.getColor("boxBackNormal"),
                        fg=self.__colors.getColor("boxFontNormal"),
                        font=self.__miniFont, justify = CENTER,
                        textvariable = self.__lockNum
        )

        self.__lockEntry.pack_propagate(False)
        self.__lockEntry.pack(side= LEFT, fill=BOTH, anchor = W)

        self.__lockEntry.bind("<FocusOut>", self.__checkLock)
        self.__lockEntry.bind("<KeyRelease>", self.__checkLock)

        self.__checkLock(None)

        self.__title = StringVar()
        self.__title.set("Hamster_Eating_Pickles")

        self.__titleEntry = Entry(
                        self.__textFrame,
                        width=9999,
                        bg=self.__colors.getColor("boxBackNormal"),
                        fg=self.__colors.getColor("boxFontNormal"),
                        font=self.__miniFont,
                        textvariable = self.__title
        )

        self.__titleEntry.pack_propagate(False)
        self.__titleEntry.pack(fill=BOTH)

        self.__titleEntry.bind("<FocusOut>", self.__checkFileName)
        self.__titleEntry.bind("<KeyRelease>", self.__checkFileName)


        self.__bottomFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= hei)
        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__buttonFrame4 = Frame(self.__bottomFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame4.pack_propagate(False)
        self.__buttonFrame4.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame5 = Frame(self.__bottomFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=  self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame5.pack_propagate(False)
        self.__buttonFrame5.pack(side=LEFT, anchor=E, fill=Y)

        self.__buttonFrame6 = Frame(self.__bottomFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width= self.__topLevel.getTopLevelDimensions()[0]//3,
                                 height= hei)
        self.__buttonFrame6.pack_propagate(False)
        self.__buttonFrame6.pack(side=LEFT, anchor=E, fill=Y)

        self.__saveButton = Button(self.__buttonFrame4, bg=self.__loader.colorPalettes.getColor("window"),
                                   state = DISABLED, name="ok", image=self.__saveImage, width=999999999, command=self.__save)
        self.__saveButton.pack_propagate(False)
        self.__saveButton.pack(fill=BOTH)

        self.__playButton = Button(self.__buttonFrame5, bg=self.__loader.colorPalettes.getColor("window"),
                                   state = DISABLED, name="play", image=self.__playImage, width=999999999, command=self.__justPlay)
        self.__playButton.pack_propagate(False)
        self.__playButton.pack(fill=BOTH)

        self.__previewButton = Button(self.__buttonFrame6, bg=self.__loader.colorPalettes.getColor("window"),
                                      state = DISABLED, name="testWithEmulator", image=self.__emulatorButton, width=999999999, command=self.__testThread)
        self.__previewButton.pack_propagate(False)
        self.__previewButton.pack(fill=BOTH)

        self.__playButton.bind("<Enter>", self.__mouseEnter)
        self.__playButton.bind("<Leave>", self.__mouseLeave)
        self.__saveButton.bind("<Enter>", self.__mouseEnter)
        self.__saveButton.bind("<Leave>", self.__mouseLeave)
        self.__previewButton.bind("<Enter>", self.__mouseEnter)
        self.__previewButton.bind("<Leave>", self.__mouseLeave)

        self.__createRainbow()

        self.__loader.threadLopper(self, self.checker, [])

    def __checkLock(self, event):
        teszt = 0
        try:
            self.__lockNum.set(self.__lockNum.get()[0])
            teszt = int(self.__lockNum.get())
        except:
            self.__lockNum.set("")

        banks = self.__loader.virtualMemory.getBanksAvailableForLocking()
        if self.__lockNum.get() == "":
            try:
                self.__lockNum.set(str(banks[0]))
            except:
                self.__lockNum.set("3")
        else:
            if teszt not in banks:
                try:
                    self.__lockNum.set(str(banks[0]))
                except:
                    self.__lockNum.set("3")


    def __checkFileName(self, event):
        OK = self.__loader.io.checkIfValidFileName(self.__title.get())

        if OK == False:
           self.__titleEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                    fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                                    )
           self.__saveButton.config(state = DISABLED)
        else:
            self.__titleEntry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                     fg=self.__loader.colorPalettes.getColor("boxFontNormal")
                                     )
            if self.__mode != None: self.__saveButton.config(state = NORMAL)


    def checker(self):
            if self.__mouseHover != self.__mouseHoverSave:
               self.__mouseHoverSave = self.__mouseHover


    def __convertToASM(self):
        from WaveConverter import WaveConverter

        wc = WaveConverter(self.__loader, "temp/temp.wav", "NTSC")

        if wc.mode == "failed":
            return wc.mode, None, None
        else:
            initText = "\nPlaySoundXX_EOF_byte = %"+wc.result["EOF"]+"\n"
            dataText = "\nPlaySoundXX_Table\n" + wc.result["SoundBytes"]

            temp = wc.result["SoundBytes"].split("\n")
            b = 0
            for line in temp:
                if ("0" in line) or ("1" in line):
                    b+=1

            limits = {
                "uncompressed": 3600,
                "compressed": 3575,
                "uncompressed3bit": 3500,
                "compressed3bit": 3475,
                "uncompressed2bit": 3600,
                "compressed2bit": 3575,
                "uncompressed1bit": 3600,
                "compressed1bit": 3575
            }

            if b>limits[wc.mode.lower()]:
               new = []
               b = 0
               for line in temp:
                  if ("0" in line) or ("1" in line):
                    b+=1
                    new.append(line)
                  if b == limits[wc.mode.lower()] - 1:
                    new.append("\tBYTE\t#%"+wc.result["EOF"]+"\n")
                    break



               dataText = "\nPlaySoundXX_Table\n" + "\n".join(new)

            #print(b, wc.mode)
            return wc.mode, initText, dataText

    def __formToData(self, mode, initText, dataText):
        moduleName = "wavePlayer" + mode[0].upper() + mode[1:]
        toSave = self.__loader.io.loadSubModule(moduleName)
        toSave = (toSave.replace("!!!Init_Stuff!!!", initText).replace("!!!Data_Stuff!!!", dataText)
                  .replace("PlaySoundXX", self.__title.get()))

        return toSave

    def __save(self):
        mode, initText, dataText = self.__convertToASM()
        if mode == "failed":
            self.__loader.fileDialogs.displayError("waveError", "waveErrorMessage", None, None)
        else:
            toSave = "* Lock="+ self.__lockNum.get()+"\n" + self.__formToData(mode, initText, dataText)

            file = open(self.__loader.mainWindow.projectPath+"waveforms/"+self.__title.get()+".asm", "w")
            file.write(toSave)
            file.close()

            #self.__loader.virtualMemory.registerNewLock(self.__lockNum.get(), self.__title.get(), "waveform", 0, "LAST")
            self.__soundPlayer.playSound("Success")

    def __testThread(self):
        t = Thread(target=self.__test)
        t.daemon = True
        t.start()

    def __test(self):
        mode, initText, dataText = self.__convertToASM()
        if mode == "failed":
            self.__loader.fileDialogs.displayError("waveError", "waveErrorMessage", None, None)
        else:
            toTest = self.__formToData(mode, initText, dataText)
            from Compiler import Compiler
            Compiler(self.__loader, "common", "testWav", [toTest, self.__lockNum.get(), self.__title.get()])

    def __mouseLeave(self, event):
        self.__labelText.set("")

    def __mouseEnter(self, event):
        name = str(event.widget).split(".")[-1]
        self.__labelText.set(self.__dictionaries.getWordFromCurrentLanguage(name))
        if self.__labelText.get()[-1] == ":":
            self.__labelText.set(self.__labelText.get()[:-1])

    def __plainOpen(self):
        self.__deleteMiddle()
        self.__openWavAndConvertToLO(None)
        self.__mode = "open"

        if self.__opened == True:
            self.__createRainbow()

    def __justPlay(self):
        from datetime import datetime
        from shutil   import copyfile

        name = ("temp/temp"+str(datetime.now()) + ".wav").replace(" ", "-").replace(":", "-")
        copyfile("temp/temp.wav", name)

        self.__soundPlayer.play(name)

    def __deleteMiddle(self):
        try:
            self.__rainbow.dead = True
        except:
            pass
        self.__rainbow = None
        shits = self.__middleFrame.pack_slaves()
        for shit in shits:
            shit.destroy()

        self.__opened = False

    def __openWavAndConvertToLO(self, path):
        try:
            if path == None:
                path = self.__fileDialogs.askForFileName("openWav", False, ["wav", "*"], self.__loader.mainWindow.projectPath)

            self.openWavAndConvertDown(path)

            self.__soundPlayer.playSound("Success")

            self.__playButton.config(state = NORMAL)
            self.__previewButton.config(state = NORMAL)
            if self.__loader.io.checkIfValidFileName(self.__title.get()) == True:
                self.__saveButton.config(state = NORMAL)
            self.__opened = True

        except Exception as e:
            self.__playButton.config(state=DISABLED)
            self.__previewButton.config(state=DISABLED)
            self.__saveButton.config(state=DISABLED)
            self.__opened = False
            self.__mode   = None

            #self.__createRainbow()

            self.__fileDialogs.displayError('importError', 'importErrorMessage', None, str(e))
            self.__createRainbow()

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def openWavAndConvertDown(self, path):
        import wave
        import audioop

        try:
            waveInput = wave.open(path, "rb")
        except:
            import soundfile

            data, samplerate = soundfile.read('temp/temp.wav')
            soundfile.write('temp/temp.wav', data, samplerate, subtype='PCM_16')
            waveInput = wave.open(path, "rb")

        converted = waveInput.readframes(waveInput.getnframes())

        if waveInput.getframerate() != 8000:
            converted = audioop.ratecv(converted, waveInput.getsampwidth(), waveInput.getnchannels(),
                                       waveInput.getframerate(), 8000, None)
            converted = converted[0]

        if waveInput.getnchannels() == 2:
            converted = audioop.tomono(converted, waveInput.getsampwidth(), 0.5, 0.5)

        if waveInput.getsampwidth() > 1:
            converted = audioop.lin2lin(converted, waveInput.getsampwidth(), 1)
            converted = audioop.bias(converted, 1, 128)

        waveInput.close()

        waveOutput = wave.open("temp/temp.wav", "wb")
        waveOutput.setnchannels(1)
        waveOutput.setsampwidth(1)
        waveOutput.setframerate(8000)
        waveOutput.writeframes(converted)
        waveOutput.close()

    def __createRainbow(self):
        self.__deleteMiddle()
        from Rainbow import Rainbow

        self.__rainbow = Rainbow(self.__loader,
                                 (self.__topLevel.getTopLevelDimensions()[0],
                                 round(self.__topLevel.getTopLevelDimensions()[1] / 5 * 2.5)),
                                 self.__middleFrame
                                 )

    def __createMiddleRecording(self):
        self.__deleteMiddle()
        self.__mode = "record"

        self.__middleF1 = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  self.__topLevel.getTopLevelDimensions()[0],
                                height= (self.__topLevel.getTopLevelDimensions()[1]//5) // 2)
        self.__middleF1.pack_propagate(False)
        self.__middleF1.pack(side=TOP, anchor=E, fill=X)

        self.__middleF1_1 = Frame(self.__middleF1, bg=self.__loader.colorPalettes.getColor("window"),
                                width=  (self.__topLevel.getTopLevelDimensions()[0]//3) * 2,
                                height= (self.__topLevel.getTopLevelDimensions()[1]//5) // 2)
        self.__middleF1_1.pack_propagate(False)
        self.__middleF1_1.pack(side=LEFT, anchor=E, fill=Y)

        self.__timeLabel = Label(self.__middleF1_1, bg=self.__loader.colorPalettes.getColor("window"),
                                text = self.__dictionaries.getWordFromCurrentLanguage("recordTime"),
                                 fg=self.__loader.colorPalettes.getColor("font"), font = self.__miniFont)
        self.__timeLabel.pack_propagate(False)
        self.__timeLabel.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__timeEntryFrame = Frame(self.__middleF1, bg=self.__loader.colorPalettes.getColor("window"),
                                width=  (self.__topLevel.getTopLevelDimensions()[0]//3),
                                height= (self.__topLevel.getTopLevelDimensions()[1]//5) // 2)
        self.__timeEntryFrame.pack_propagate(False)
        self.__timeEntryFrame.pack(side=LEFT, anchor=E, fill=BOTH)

        self.__timeString = StringVar()
        self.__timeString.set("1")

        self.__timeEntry = Entry(self.__timeEntryFrame, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                   width=99,
                                   fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                   textvariable = self.__timeString, name = "timeEntry",
                                   font=self.__smallFont, justify = CENTER,
                                   command=None)
        self.__timeEntry.pack_propagate()
        self.__timeEntry.pack(side=TOP, anchor=N, fill=BOTH)

        self.__timeEntry.bind("<KeyRelease>", self.__checkInt)
        self.__timeEntry.bind("<FocusOut>", self.__checkInt)

        w = self.__topLevel.getTopLevelDimensions()[0]
        h = self.__topLevel.getTopLevelDimensions()[1]//5*3

        self.__micFrame = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width=  w,
                                height= h)

        self.__micFrame.pack_propagate(False)
        self.__micFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__micOff = self.__loader.io.getImg("micOff", (h//2, h//2))
        self.__micOn = self.__loader.io.getImg("micOn", (h//2, h//2))
        self.__one = self.__loader.io.getImg("01", (h//2, h//2))
        self.__two = self.__loader.io.getImg("02", (h//2, h//2))
        self.__three = self.__loader.io.getImg("03", (h//2, h//2))

        self.__micButton = Button(self.__micFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image= self.__micOff, width=9999, height = 9999, name="record",
                                   command=self.__recordThread)
        self.__micButton.pack_propagate(False)
        self.__micButton.pack(fill=BOTH)

        self.__micButton.bind("<Enter>", self.__mouseEnter)
        self.__micButton.bind("<Leave>", self.__mouseLeave)

    def __checkInt(self, event):

        name = str(event.widget).split(".")[-1]

        if self.__mode == "record":
            itemList = {
                "timeEntry": (self.__timeString, self.__timeEntry, self.__micButton)
            }

            teszt = self.__checkEntry(itemList[name][0], itemList[name][1], itemList[name][2])

            if teszt != None and teszt < 1:
               self.__timeString.set('1')
        else:
            itemList = {
                "pitch": (self.__pitchEntry.var, self.__pitchEntry.entry),
                "throat": (self.__throatEntry.var, self.__throatEntry.entry),
                "mouth": (self.__mouthEntry.var, self.__mouthEntry.entry),
                "speed": (self.__speedEntry.var, self.__speedEntry.entry)
            }

            __turnOff = False

            for item in itemList.keys():
                teszt = self.__checkEntry(itemList[item][0], itemList[item][1], None)

                if teszt != None:
                   if teszt < 0:
                       itemList[item][0].set('0')
                   elif teszt > 255:
                       itemList[item][0].var.set('255')
                else:
                    __turnOff = True

            if self.__textEntryVal.get() == "":
                __turnOff = True

            if __turnOff == True:
               self.__previewButton.config(state = DISABLED)
               self.__saveButton.config(state = DISABLED)
               self.__playButton.config(state = DISABLED)
            else:
               self.__previewButton.config(state = NORMAL)
               if self.__loader.io.checkIfValidFileName(self.__title.get()) == True:
                    self.__saveButton.config(state = NORMAL)
               self.__playButton.config(state = NORMAL)

               self.__generateRoboSound()

    def __checkEntry(self, val, entry, button):
        while True:
            try:
                teszt = int(val.get())
                break
            except:
                val.set(val.get()[:-1])
                if val.get() == "":
                    entry.config(bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                                            fg=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                                            )
                    if button != None:
                        button.config(state=DISABLED)
                    return None

        entry.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                fg=self.__loader.colorPalettes.getColor("boxFontNormal")
                                )
        if button != None:
            button.config(state=NORMAL)
        return teszt

    def __recordThread(self):

        t = Thread(target = self.__recordSound)
        t.daemon = True
        t.start()

    def __recordSound(self):

        import sounddevice as sd
        from scipy.io.wavfile import write

        self.__micButton.config(image = self.__three)
        self.__micButton.config(state = DISABLED)
        self.__openButton.config(state = DISABLED)
        self.__recordButton.config(state = DISABLED)
        self.__robotButton.config(state = DISABLED)
        self.__playButton.config(state = DISABLED)
        self.__saveButton.config(state = DISABLED)
        self.__previewButton.config(state = DISABLED)
        self.__timeEntry.config(state = DISABLED)

        from time import sleep

        sleep(1)
        self.__micButton.config(image = self.__two)
        sleep(1)
        self.__micButton.config(image = self.__one)
        sleep(1)
        self.__micButton.config(image = self.__micOn)

        fs = 44100
        try:
            seconds = int(self.__timeString.get())
        except:
            seconds = 1

        record = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        write('temp/temp.wav', fs, record)

        self.__micButton.config(image = self.__micOff, state = NORMAL)
        self.__openButton.config(state = NORMAL)
        self.__recordButton.config(state = NORMAL)
        self.__robotButton.config(state = NORMAL)
        self.__timeEntry.config(state = NORMAL)
        self.__openWavAndConvertToLO("temp/temp.wav")

    def __robotMenu(self):
        self.__deleteMiddle()
        self.__mode = "robot"

        self.__previewButton.config(state = DISABLED)
        self.__saveButton.config(state = DISABLED)
        self.__playButton.config(state = DISABLED)

        h = (self.__topLevel.getTopLevelDimensions()[1]//5) //2

        self.__speechImg = self.__loader.io.getImg("speech", (h, h))


        self.__robotSpeechFrame1 = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  self.__topLevel.getTopLevelDimensions()[0],
                                height= h)
        self.__robotSpeechFrame1.pack_propagate(False)
        self.__robotSpeechFrame1.pack(side=TOP, anchor=N, fill=X)

        self.__robotSpeechFrame2 = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  self.__topLevel.getTopLevelDimensions()[0],
                                height= h)
        self.__robotSpeechFrame2.pack_propagate(False)
        self.__robotSpeechFrame2.pack(side=TOP, anchor=N, fill=X)

        self.__robotSpeechFrame3 = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  self.__topLevel.getTopLevelDimensions()[0],
                                height= h*2)
        self.__robotSpeechFrame3.pack_propagate(False)
        self.__robotSpeechFrame3.pack(side=TOP, anchor=N, fill=X)


        self.__robotSpeechFrame4 = Frame(self.__middleFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                width =  self.__topLevel.getTopLevelDimensions()[0],
                                height= h)
        self.__robotSpeechFrame4.pack_propagate(False)
        self.__robotSpeechFrame4.pack(side=TOP, anchor=N, fill=BOTH)

        from RobotFrameLabelEntry import RobotFrameLabelEntry

        self.__speedEntry = RobotFrameLabelEntry(self.__loader, self.__robotSpeechFrame1,
                                                 self.__topLevel.getTopLevelDimensions()[0] //2, h,
                                                 self.__smallFont, self.__checkInt, "72", "speed"
                                                 )

        self.__pitchEntry = RobotFrameLabelEntry(self.__loader, self.__robotSpeechFrame1,
                                                 self.__topLevel.getTopLevelDimensions()[0] //2, h,
                                                 self.__smallFont, self.__checkInt, "64", "pitch"
                                                 )

        self.__throatEntry = RobotFrameLabelEntry(self.__loader, self.__robotSpeechFrame2,
                                                 self.__topLevel.getTopLevelDimensions()[0] //2, h,
                                                 self.__smallFont, self.__checkInt, "128", "throat"
                                                 )
        self.__mouthEntry = RobotFrameLabelEntry(self.__loader, self.__robotSpeechFrame2,
                                                 self.__topLevel.getTopLevelDimensions()[0] //2, h,
                                                 self.__smallFont, self.__checkInt, "128", "mouth"
                                                 )

        self.__textEntryVal = StringVar()
        self.__textEntryVal.set("Have you played your Atari today?")

        self.__textEntry = Entry(self.__robotSpeechFrame4, bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                 width=999999,
                                 fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                                 textvariable=self.__textEntryVal,
                                 font=self.__tinyFont,
                                 command=None)
        self.__textEntry.pack_propagate()
        self.__textEntry.pack(side=TOP, anchor=N, fill=BOTH)

        self.__textEntry.bind("<KeyRelease>", self.__checkInt)
        self.__textEntry.bind("<FocusOut>", self.__checkInt)

        from RoboButton import RoboButton

        entries = (self.__speedEntry, self.__pitchEntry, self.__throatEntry, self.__mouthEntry)

        self.__defaultRobo = RoboButton(self.__loader, "default", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (72,64,128,128), entries, self.__generateRoboSound)

        self.__elfRobo = RoboButton(self.__loader, "elf", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (72,64,110,160), entries, self.__generateRoboSound)

        self.__roboRobo = RoboButton(self.__loader, "robo", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (92,60,190,190), entries, self.__generateRoboSound)

        self.__guyRobo = RoboButton(self.__loader, "guy", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (82,72,110,105), entries, self.__generateRoboSound)

        self.__ladyRobo = RoboButton(self.__loader, "lady", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (82,32,145,145), entries, self.__generateRoboSound)

        self.__ufoRobo = RoboButton(self.__loader, "ufo", self.__robotSpeechFrame3,
                                        self.__topLevel.getTopLevelDimensions()[0]//6,
                                        h*2, (100,64,150,200), entries, self.__generateRoboSound)

        self.__generateRoboSound()

    def __generateRoboSound(self):
        self.__loader.executor.execute("sam",
                                       [
                                            "-wav temp/temp.wav",
                                            '"'+self.__textEntryVal.get()+'"',
                                            "-pitch " + self.__pitchEntry.var.get(),
	                                        "-speed " + self.__speedEntry.var.get(),
                                            "-throat "+ self.__throatEntry.var.get(),
	                                        "-mouth " + self.__mouthEntry.var.get(),
                                       ], True)

        self.openWavAndConvertDown("temp/temp.wav")

        self.__previewButton.config(state=NORMAL)
        if self.__loader.io.checkIfValidFileName(self.__title.get()) == True:
            self.__saveButton.config(state=NORMAL)
        self.__playButton.config(state=NORMAL)