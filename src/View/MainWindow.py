#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MenuLabel import MenuLabel
from ButtonMaker import ButtonMaker
from tkinter.filedialog import *

class MainWindow:

    def __init__(self, loader):
        self.dead = False
        self.__loader = loader
        self.__loader.mainWindow = self

        self.__loopColor = "#000000"
        self.__colorNum  = 0

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__colorDict = self.__loader.colorDict
        self.__colors = self.__loader.colorPalettes

        self.__mainFocus = None
        self.__menuLabel = []
        self.__created   = False

        self.__subMenuOpened = False
        self.__setProjectPath(None)

        self.focused = None
        self.clipBoardText = None

        self.__loader.mainWindowHander.mainWindow = self
        self.editor = self.__loader.tk

        self.__scaleX=1
        self.__scaleY=1

        self.editor.protocol('WM_DELETE_WINDOW', self.__closeWindow)
        self.editor.title("Fortari2600 v"+self.__config.getValueByKey("version"))
        __w = self.__loader.screenSize[0]-150
        __h = self.__loader.screenSize[1]-200
        self.editor.geometry("%dx%d+%d+%d" % (__w, __h, (
                self.__loader.screenSize[0] / 2-__w/2), (self.__loader.screenSize[1]/2-__h/2-25)))

        self.editor.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.editor.attributes('-toolwindow', True)


        self.editor.overrideredirect(False)
        #self.editor.resizable(True, True)
        self.editor.minsize(1000,720)
        self.editor.pack_propagate(False)
        self.editor.grid_propagate(False)
        self.editor.iconbitmap("others/img/icon.ico")

        self.__originalW = self.getWindowSize()[0]
        self.__originalH = self.getWindowSize()[1]
        self.__lastW = self.getWindowSize()[0]
        self.__lastH = self.getWindowSize()[1]

        from FontManager import FontManager
        self.__fontManager = FontManager(self.__loader)

        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)
        self.__halfFont = self.__fontManager.getFont(int(self.__fontSize*0.57), False, False, False)

        self.__createFrames()
        #self.selectedItem = ["bank1", "global_variables"]
        self.bindThings()

        self.__soundPlayer.playSound("Start")

        self.editor.deiconify()
        self.editor.focus()
        self.__loader.tk.iconify()

        self.__loader.threadLooper.addToThreading(self, self.__loopColorThread, [], -1)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def getLoopColor(self):
        return self.__loopColor

    def bindThings(self):
        self.__pressedHome = False
        self.__pressedShiftL = False

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.editor, "<Key>"       , self.pressed, 0)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.editor, "<KeyRelease>", self.released, 0)

        #self.editor.bind("<Key>", self.pressed)
        #self.editor.bind("<KeyRelease>", self.released)

    def __setProjectPath(self, path):
        self.projectPath=path
        self.__loader.bindedVariables["projectPath"] = path

    def __closeWindow(self):
        self.editor.destroy()

    def getWindowSize(self):
        return (self.editor.winfo_width(), self.editor.winfo_height())

    def __killRemaining(self):
        import gc
        #self.__loader.subMenus = []

        for item in gc.get_objects():
            if "filedialog" in str(type(item)):
                print(str(type(item)))

    def getScales(self):
        return([self.__scaleX, self.__scaleY])

    def __createFrames(self):
         self.__fullEditor = Frame(self.editor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1],
                                   bg=self.__colors.getColor("window"))
         self.__fullEditor.pack_propagate(False)
         self.__fullEditor.pack(side=TOP, anchor = N, fill=BOTH)

         self.__buttonMenu = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//11.25,
                                   bg=self.__colors.getColor("window"))
         self.__buttonMenu.pack_propagate(False)
         self.__buttonMenu.pack(side=TOP, anchor = N, fill=X)

         self.__createMenuFrame()

         self.__controllerMenu = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
         self.__controllerMenu.pack_propagate(False)
         self.__controllerMenu.pack(side=TOP, anchor = N, fill=X)

         self.changerButtons = []

         for num in range(1,9):
             f = Frame(self.__controllerMenu, width=self.getWindowSize()[0]//8,
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
             f.pack_propagate(False)
             f.pack(side=LEFT, anchor = E, fill=Y)

             if num == 1:
               name = "global"
             else:
               name = 'bank'+str(num)

             b = Button(f, bg=self.__loader.colorPalettes.getColor("window"),
                        text = name[0].upper()+name[1:], name = name,
                        fg = self.__loader.colorPalettes.getColor("font"),
                        width=99999, font=self.__normalFont,
                        state=DISABLED, command = None)
             b.pack_propagate(False)
             b.pack(side=LEFT, anchor=E, fill=BOTH)

             self.changerButtons.append(b)

         __keys = list(self.__loader.virtualMemory.codes["bank2"].keys())
         __keys.remove('local_variables')
         __keys.remove('special_read_only')
         __keys.remove('screen_top')
         __keys.remove('screen_bottom')
         self.validSections = __keys

         self.__controllerMenu2 = Frame(self.__fullEditor, width=self.getWindowSize()[0],
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
         self.__controllerMenu2.pack_propagate(False)
         self.__controllerMenu2.pack(side=TOP, anchor = N, fill=X)

         self.sectionButtons = []

         for num in range(0, len(__keys)):
             f = Frame(self.__controllerMenu2, width=self.getWindowSize()[0]//len(__keys),
                                   height=self.getWindowSize()[1]//30,
                                   bg=self.__colors.getColor("window"))
             f.pack_propagate(False)
             f.pack(side=LEFT, anchor = E, fill=Y)

             try:
                 text = self.__dictionaries.getWordFromCurrentLanguage(__keys[num])
             except:
                 text = __keys[num][0].upper() + __keys[num][1:]

             b = Button(f, bg=self.__loader.colorPalettes.getColor("window"),
                        text = text, name = __keys[num],
                        fg = self.__loader.colorPalettes.getColor("font"),
                        width=99999, font=self.__normalFont,
                        state=DISABLED, command = None)
             b.pack_propagate(False)
             b.pack(side=LEFT, anchor=E, fill=BOTH)

             self.sectionButtons.append(b)

         from EditorBigFrame import EditorBigFrame

         self.__bigFrame = EditorBigFrame(self.__loader, self.__fullEditor)
         self.__loader.bigFrame = self.__bigFrame
         self.sectionNames = __keys

    def __createMenuFrame(self):
        #self.__buttonMenu = FrameContent(self.__loader, "buttonMenu",
        #                                 self.getWindowSize()[0]/3*2, self.getWindowSize()[1]/11.25, 5, 5,
        #                                 99999, 150, 400, 60)

        self.__places = {}
        __vals = [0]

        self.__buttonMaker = ButtonMaker(self.__loader, self.__buttonMenu, self.__createLabel, self.__destroyLabel)

        currentPoz = [0]

        self.__newButton = self.__buttonMaker.createButton("new", currentPoz,
                                      self.__newButtonFunction, "projectPath" ,
                                       True, None, self.__places, __vals[0], False)
        self.__openButton = self.__buttonMaker.createButton("open", currentPoz,
                                       self.__openButtonFunction, "projectPath",
                                        True, None, self.__places,  __vals[0], False)
        self.__saveButton = self.__buttonMaker.createButton("save", currentPoz,
                                       self.__saveButtonFunction, "projectPath",
                                        False, None, self.__places,  __vals[0], False)
        self.__saveAllButton = self.__buttonMaker.createButton("saveAll", currentPoz,
                                          self.__saveAllButtonFunction, "projectPath",
                                            False, None, self.__places,  __vals[0], False)
        self.__closeProjectButton = self.__buttonMaker.createButton("closeProject", currentPoz,
                                          self.__closeProjectButtonFunction, "projectPath",
                                            False, None, self.__places,  __vals[0], False)
        self.__archiveButton = self.__buttonMaker.createButton("archive", currentPoz,
                                          self.__achiveButtonFunction, "projectPath",
                                            False, None, self.__places,  __vals[0], False)
        self.__buildProjectButton    = self.__buttonMaker.createButton("build", currentPoz,
                                          self.__buildProject, "projectPath",
                                            False, None, self.__places, __vals[0], False)

        currentPoz[0] += 0.5
        __vals.append(currentPoz[0])

        self.__copyButton = self.__buttonMaker.createButton("copy", currentPoz,
                                          self.__copyButtonFunction, None,
                                            False, self.setCopyButton, self.__places,  __vals[1], False)
        self.__pasteButton = self.__buttonMaker.createButton("paste", currentPoz,
                                          self.__pasteButtonFunction, None,
                                            False, self.setPasteButton, self.__places, __vals[1], False)
        self.__undoButton = self.__buttonMaker.createButton("undo", currentPoz,
                                          self.__undoButtonFunction, None,
                                            False, self.__undoButtonHandler, self.__places, __vals[1], False)
        self.__redoButton = self.__buttonMaker.createButton("redo", currentPoz,
                                          self.__redoButtonFunction, None,
                                            False, self.__redoButtonHandler, self.__places, __vals[1], False)
        currentPoz[0] += 0.5
        __vals.append(currentPoz[0])

        self.__spriteButton = self.__buttonMaker.createButton("spriteEditor", currentPoz,
                                          self.__openSpriteEditor, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__pfButton = self.__buttonMaker.createButton("playfieldEditor", currentPoz,
                                          self.__openPFEditor, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__musicButton = self.__buttonMaker.createButton("music", currentPoz,
                                          self.__openMusicComposer, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__64pxPictureButton = self.__buttonMaker.createButton("64pxPicture", currentPoz,
                                          self.__openPictureConverter, "projectPath",
                                            False, None, self.__places, __vals[2], False)
        self.__48pxPictureButton = self.__buttonMaker.createButton("48pxPicture", currentPoz,
                                          self.__open48pxEditor, "projectPath",
                                            False, None, self.__places, __vals[2], False)
        self.__soundPlayerButton = self.__buttonMaker.createButton("noiseMaker", currentPoz,
                                          self.__openNoiseMaker, "projectPath",
                                            False, None, self.__places, __vals[2], False)
        self.__noiseMaker = self.__buttonMaker.createButton("soundPlayer", currentPoz,
                                          self.__openSoundPlayer, "projectPath",
                                            False, None, self.__places, __vals[2], False)
        self.__bigSpriteButton = self.__buttonMaker.createButton("bigSprite", currentPoz,
                                          self.__openBigSpriteEditor, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__menuMaker = self.__buttonMaker.createButton("menuMaker", currentPoz,
                                          self.__openMenuMaker, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__miniMapMaker = self.__buttonMaker.createButton("minimapMaker", currentPoz,
                                          self.__openMiniMapMaker, "projectPath",
                                            False, None, self.__places, __vals[2], False)

        self.__rawDateEditor = self.__buttonMaker.createButton("rawData", currentPoz,
                                          self.__openRawDataMaker, "projectPath",
                                            False, None, self.__places, __vals[2], True)

        currentPoz[0] += 0.5
        __vals.append(currentPoz[0])

        self.__memoryManagerButton = self.__buttonMaker.createButton("memoryManager", currentPoz,
                                          self.openMemoryManager, "projectPath",
                                            False, None, self.__places, __vals[3], False)

        self.__memoryManagerButton = self.__buttonMaker.createButton("constant", currentPoz,
                                          self.openConstantWindow, "projectPath",
                                            False, None, self.__places, __vals[3], False)

        self.__screenTopBottomButton = self.__buttonMaker.createButton("screenTopBottom", currentPoz,
                                          self.__openScreenTopBottom, "projectPath",
                                            False, None, self.__places, __vals[3], False)


        self.__menuLabel    = []
        self.__menuLabel.append(MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager))
        self.__created      = True


    def __loopColorThread(self):
        try:
            self.__colorNum += 1
            if self.__colorNum == 256: self.__colorNum = 0
            hexaNum = hex(self.__colorNum - self.__colorNum % 2).replace("0x", "$")
            if len(hexaNum) == 2: hexaNum = "$0" + hexaNum[1]
            self.__loopColor = self.__colorDict.getHEXValueFromTIA(hexaNum)
        except:
            pass

        for item in self.__loader.stopThreads:
            try:
                if item.stopThread == True:
                    self.__loader.stopThreads.remove(item)
                    break
            except:
                self.__loader.stopThreads.remove(item)
                break

    def __createLabel(self, event):

        if self.__created == False: return

        try:
            name = str(event.widget).split(".")[-1]
            button = self.__loader.menuButtons[name].getButton()
            if button.cget("state") == DISABLED:
                self.__menuLabel[0].changeColor(self.__loader.colorPalettes.getColor("fontDisabled"))
            else:
                self.__menuLabel[0].changeColor(self.__loader.colorPalettes.getColor("font"))

            self.__menuLabel[0].setText(self.__dictionaries.getWordFromCurrentLanguage(name))
            self.__menuLabel[0].changePlace(self.__places[name])

        except Exception as e:
            try:
                self.__menuLabel[0].setText("")
                self.__menuLabel[0].dead = True
            except:
                pass

            try:
                self.__menuLabel[0]  = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)
            except:
                self.__menuLabel.append(MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager))

    def setMode(self, mode):
        self.__bigFrame.setMode(mode)

    def __destroyLabel(self, event):
        try:
            self.__menuLabel[0].setText("")
        except:
            try:
                self.__menuLabel[0].setText("")
                self.__menuLabel[0].dead = True
            except:
                pass
            # self.__menuLabel[0] = MenuLabel(self.__loader, self.__buttonMenu, "", 0, self.__fontManager)

    def __newButtonFunction(self):
        from NewProjectWindow import NewProjectWindow
        NewProjectWindow(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def projectOpenedWantToSave(self):
        if self.projectPath!=None and self.__getIfThereIsUnsavedItem() == True:
            return(self.__fileDialogs.askYesOrNo("unsaved","unsavedText"))
        else:
            return("No")

    def __getIfThereIsUnsavedItem(self):
        for bank in self.__loader.virtualMemory.codes.keys():
            for item in self.__loader.virtualMemory.codes[bank].keys():
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    return True
        return False

    def checkIfBankChanged(self, listBox):
        if self.projectPath == None:
            self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].config(state=DISABLED)
        else:
            self.__loader.listBoxes["bankBox"].getListBoxAndScrollBar()[0].config(state=NORMAL)
        num = 0
        for bank in self.__loader.virtualMemory.codes.keys():
            num += 1
            color1 = self.__loader.colorPalettes.getColor("boxBackNormal")
            color2 = self.__loader.colorPalettes.getColor("boxFontNormal")

            for item in self.__loader.virtualMemory.codes[bank].keys():
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    color1=self.__loader.colorPalettes.getColor("boxBackUnSaved")
                    color2=self.__loader.colorPalettes.getColor("boxFontUnSaved")
                    break
            listBox.itemconfig(num-1, {"bg": color1})
            listBox.itemconfig(num-1, {"fg": color2})

    def checkIfSectionChanged(self, listBox):
        if (self.__loader.listBoxes["bankBox"].getSelectedName() == "bank1" or
            self.projectPath == None or
                self.__loader.virtualMemory.locks[self.__loader.listBoxes["bankBox"].getSelectedName()]!=None):
            self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].config(state=DISABLED)
        else:
            self.__loader.listBoxes["sectionBox"].getListBoxAndScrollBar()[0].config(state=NORMAL)

            num=0
            bank =self.__loader.listBoxes["bankBox"].getSelectedName()
            for item in self.__loader.virtualMemory.codes[bank].keys():
                if item == "special_read_only":
                    continue
                num += 1
                if self.__loader.virtualMemory.codes[bank][item].changed == True:
                    color1 = self.__loader.colorPalettes.getColor("boxBackUnSaved")
                    color2 = self.__loader.colorPalettes.getColor("boxFontUnSaved")
                else:
                    color1 = self.__loader.colorPalettes.getColor("boxBackNormal")
                    color2 = self.__loader.colorPalettes.getColor("boxFontNormal")

                listBox.itemconfig(num-1, {"bg": color1})
                listBox.itemconfig(num-1, {"fg": color2})

    def __listBoxChanges(self):
        bankBox = self.__loader.listBoxes["bankBox"]
        sectionBox = self.__loader.listBoxes["sectionBox"]
        self.__bankSelected = bankBox.getSelectedName()
        self.__sectionSelected = sectionBox.getSelectedName()

        while self.dead == False:
            from time import sleep
            if self.__bankSelected != bankBox.getSelectedName() or self.__sectionSelected != sectionBox.getSelectedName():

                self.__bankSelected = bankBox.getSelectedName()
                try:
                    self.__sectionSelected = sectionBox.getSelectedName()
                except:
                    continue
            sleep(0.05)

    def changeAliasInCodes(self):
        for bank in self.__loader.virtualMemory.codes.keys():
            for section in self.__loader.virtualMemory.codes[bank].keys():
                for command in self.__loader.syntaxList.keys():
                    self.__loader.virtualMemory.codes[bank][section].code = (
                    self.__loader.syntaxList[command].changeAliasToName(
                        command, self.__loader.virtualMemory.codes[bank][section].code
                    ))


    def openProject(self, path):
        try:
        #if True:
            projectPath=path.replace("\\", "/")
            kernelOld = self.__loader.virtualMemory.kernel
            from re import sub
            projectPath = sub("/+", "/", projectPath)
            self.__setProjectPath(projectPath)
            #file = open(self.projectPath+os.sep+name+".project2600", "w")
            #file.write(self.projectPath)
            #file.close()
            self.__loader.config.addProjectPath(projectPath)

            #self.__setVirtualMemoryItem("bank1", "bank_configurations")
            #self.__setVirtualMemoryItem("bank1", "global_variables")

            for section in self.__loader.bank1Sections:
                self.__setVirtualMemoryItem("bank1", section)

            for num in range(2,9):
                bank = "bank"+str(num)
                for section in self.__loader.sections:
                    self.__setVirtualMemoryItem(bank, section)

            if kernelOld != self.__loader.virtualMemory.kernel:
               self.__loader.virtualMemory.objectMaster.loadKernelObjects()

            self.__loader.virtualMemory.setLocksAfterLoading()
            self.__loader.virtualMemory.setVariablesFromMemory("all")
            self.__loader.virtualMemory.archieve()
            self.__soundPlayer.playSound("Success")
            self.__bigFrame.setMode("job")


        except Exception as e:
            self.__fileDialogs.displayError("projectOpenError", "projectOpenErrorText",
                                            {
                                                "name": self.projectPath.split("/")[-2]
                                            },
                                            str(e)
                                            )
            try:
                self.__closeProject()
            except Exception as e:
                print(str(e))
                self.projectPath=""


    def __setVirtualMemoryItem(self, bank, variable):
        path = str(self.projectPath+bank+os.sep+variable+".a26")
        item = self.__loader.virtualMemory.codes[bank][variable]
        # item.code = self.__loader.io.loadWholeText(path).replace("%DELIMINATOR%", self.__config.getValueByKey("deliminator"))
        item.code = self.__loader.io.loadWholeText(path)
        if bank=="bank1" and variable =="bank_configurations":
            old     = self.__loader.virtualMemory.kernel
            oldJuke = self.__loader.virtualMemory.includeJukeBox
            oldIncl = self.__loader.virtualMemory.includeKernelData
            oldColl = self.__loader.virtualMemory.includeCollisions

            for line in item.code.split(os.linesep):
                if line.startswith("bank1"):
                    line = line.split("=")[1].replace("\n", "").replace("\r", "").split(",")
                    self.__loader.virtualMemory.kernel  = line[0]
                    #if old != new:
                    #   self.__loader.virtualMemory.changeKernelMemory(old, new)
                    self.__loader.virtualMemory.includeKernelData(bool(line[1]))
                    self.__loader.virtualMemory.includeJukeBox(bool(line[2]))
                    self.__loader.virtualMemory.includeCollisions(bool(line[3]))

                    if old     != self.__loader.virtualMemory.kernel            \
                    or oldIncl != self.__loader.virtualMemory.includeKernelData \
                    or oldJuke != self.__loader.virtualMemory.includeJukeBox    \
                    or oldColl != self.__loader.virtualMemory.includeCollisions:
                       self.__loader.virtualMemory.resetMemory()
                       #self.__loader.virtualMemory.addSystemMemory()

        item.changed = False

    def __saveProject(self):
        #self.__saveOnlyOne("bank1", "bank_configurations", False)
        #self.__saveOnlyOne("bank1", "global_variables", False)

        for section in self.__loader.bank1Sections:
            self.__saveOnlyOne("bank1", section, False)

        for num in range(2, 9):
            bank = "bank" + str(num)
            for section in self.__loader.sections:
                self.__saveOnlyOne(bank, section, False)

        self.__soundPlayer.playSound("Success")

    def __saveOnlyOne(self, bank, section, playsound):
        path = self.projectPath + bank + "/" + section + ".a26"
        code = self.__loader.virtualMemory.codes[bank][section]

        f = open(path, "w")
        f.write(code.code)
        f.close()

        code.changed = False
        if playsound: self.__soundPlayer.playSound("Success")


    def closeProject(self):
        self.__soundPlayer.playSound("Close")
        self.__setProjectPath(None)
        self.__loader.virtualMemory.emptyArchieved()
        self.__loader.virtualMemory.resetMemory()
        self.stopThreads()
        self.__bigFrame.setMode("intro")

    def stopThreads(self):
        for item in self.__loader.stopThreads:
            item.stopThread=True
        self.__loader.stopThreads = []

    def __openButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.__saveProject()

        from OpenProjectWindow import OpenProjectWindow

        OpenProjectWindow(self.__loader, self, self.openProject)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openMusicComposer(self):
        from MusicComposer import MusicComposer

        MusicComposer(self.__loader, self, None)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openPictureConverter(self):
        from PictureToCode import PictureToCode

        PictureToCode(self.__loader, "common", "64pxPicture" , None, None)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __open48pxEditor(self):
        from Pic48Editor import Pic48Editor

        Pic48Editor(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openNoiseMaker(self):
        from NoiseMaker import NoiseMaker

        NoiseMaker(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openSoundPlayer(self):
        from SoundPlayerEditor import SoundPlayerEditor

        SoundPlayerEditor(self.__loader, self)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openPFEditor(self):
        from PlayfieldEditor import PlayfieldEditor

        PlayfieldEditor(self.__loader, self)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openSpriteEditor(self):
        from SpriteEditor import SpriteEditor

        SpriteEditor(self.__loader, self)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openBigSpriteEditor(self):
        from BigSpriteMaker import BigSpriteMaker

        BigSpriteMaker(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openScreenTopBottom(self):
        from TopBottomEditor import TopBottomEditor

        TopBottomEditor(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openMenuMaker(self):
        from MenuMaker import MenuMaker

        MenuMaker(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openMiniMapMaker(self):
        from MiniMapMaker import MiniMapMaker

        MiniMapMaker(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __openRawDataMaker(self):
        from RawDataCooker import RawDataCooker

        RawDataCooker(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()
        
    def __buildProject(self):
        pass

    def __saveButtonFunction(self):
        #self.__saveOnlyOne(self.selectedItem[0], self.selectedItem[1])
        current = self.__bigFrame.returnCurrentBankSection()

        self.__saveOnlyOne(current[0], current[1], True)

    def __saveAllButtonFunction(self):
        self.__saveProject()

    def __closeProjectButtonFunction(self):
        if self.projectOpenedWantToSave()=="Yes":
            self.__saveProject()
        self.closeProject()

    def __achiveButtonFunction(self):
        from ArchiveWindow import ArchiveWindow

        ArchiveWindow(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def __copyButtonFunction(self):
        import clipboard
        clipboard.copy(self.focused.selection_get())
        self.clipBoardText = clipboard.paste()

    def __pasteButtonFunction(self):
        self.focused.insert(INSERT, self.clipBoardText)

    def __undoButtonFunction(self):
        self.__loader.virtualMemory.getArcPrev()

    def __redoButtonFunction(self):
        self.__loader.virtualMemory.getArcNext()

    def __undoButtonHandler(self, button):
        try:
            if len(self.__loader.virtualMemory.archieved) > 0 and self.__loader.virtualMemory.cursor > 0:
                self.__undoButton.getButton().config(state=NORMAL)

            else:
                self.__undoButton.getButton().config(state=DISABLED)
        except:
            pass

    def __redoButtonHandler(self, button):
        try:
            if self.__loader.virtualMemory.cursor < len(self.__loader.virtualMemory.archieved) - 1:
                self.__redoButton.getButton().config(state=NORMAL)

            else:
                self.__redoButton.getButton().config(state=DISABLED)
        except:
            pass

    def getConstant(self):
        scalerX = self.getWindowSize()[0]/1300
        scalerY = self.getWindowSize()[1]/1150
        num = round(32*scalerX*scalerY)
        if num>32:
            num=32
        elif num<18:
            num=18
        return(num)

    def focusIn(self, event):
        self.focused = event.widget

    def focusOut(self, event):
        self.focused = None


    def setCopyButton(self, button):
        try:
            if self.focused == None:
                self.__copyButton.getButton().config(state=DISABLED)
            else:
                self.__copyButton.getButton().config(state=NORMAL)
        except:
            pass

    def setPasteButton(self, button):
        try:
            if self.focused == None:
                self.__pasteButton.getButton().config(state=DISABLED)
            else:
                if self.clipBoardText == None:
                    self.__pasteButton.getButton().config(state=DISABLED)
                else:
                    self.__pasteButton.getButton().config(state=NORMAL)
        except:
            pass

    def pressed(self, event):
        key = event.keysym

        if key == "Home":
            self.__pressedHome = True
        elif key == "Shift_L" or key == "Shift_R":
            self.__pressedShiftL = True
 

    def released(self, event):
        key = event.keysym
        if key == "Home":
            self.__pressedHome = False
        elif key == "Shift_L" or key == "Shift_R":
            self.__pressedShiftL = False

    def __openLockManager(self):
        from LockManagerWindow import LockManagerWindow
        LockManagerWindow(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def openMemoryManager(self):
        from MemoryManagerWindow2 import MemoryManagerWindow

        MemoryManagerWindow(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()

    def openConstantWindow(self):
        from ConstantWindow import ConstantWindow

        ConstantWindow(self.__loader)
        self.__loader.tk.deiconify()
        self.__loader.tk.focus()
