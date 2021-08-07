from SubMenu import SubMenu
from tkinter import *
import os

class NewProjectWindow:

    def __init__(self, loader):

        self.dead = False
        self.__loader=loader
        self.OK = False

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*18)

        self.__screenSize = self.__loader.screenSize

        self.__window = SubMenu(self.__loader, "new", self.__screenSize[0] / 3, self.__screenSize[1] / 4 - 25,
                           self.__checker, self.__addElements, 1)
        self.dead = True

    def getDimensions(self):
        return(self.__window.getTopLevelDimensions())

    def __addElements(self, top):
        from SubMenuLabel import SubMenuLabel

        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.9), False, False, False)

        self.__folderLabel = SubMenuLabel(self.__topLevelWindow,
                                       self.__loader,
                                       "projectPath",
                                       self.__normalFont)

        from SubMenuEntryWithButton import SubMenuEntryWithButton
        self.__folderEntryWithButton = SubMenuEntryWithButton(self.__topLevel,
                                                              self.__loader,
                                                              self.__smallFont)

        self.__folderEntryWithButton.addButton("open", self.openFolder)

        import os
        self.__folderEntryWithButton.setText(str(os.getcwd()+"/projects/").replace("\\", "/"))

        self.__projectLabel = SubMenuLabel(self.__topLevelWindow,
                                       self.__loader,
                                       "projectName",
                                       self.__normalFont)

        self.__projectEntryWithButton = SubMenuEntryWithButton(self.__topLevel,
                                                              self.__loader,
                                                              self.__smallFont)

        from SubMenuOkCancelButtons import SubMenuOkCancelButtons
        from PitFallHarry import PitFallHarry
        from SetKernelLabel import SetKernelLabel

        self.__okCancel = SubMenuOkCancelButtons(self, self.__topLevel, self.__loader, self.__normalFont, self.__newProject, self.getOK)
        if len(self.__loader.virtualMemory.kernel_types)>1:
            self.__setKernelLabel = SetKernelLabel(self.__loader, self, self.__topLevel, self.__topLevel.getTopLevelDimensions()[1]/9, self.__smallFont)

        self.__harry = PitFallHarry(self, self.__topLevel, self.__loader, self.__normalFont)

    def getOK(self):
        return(self.OK)

    def __checker(self):
        from time import sleep
        import os
        while self.dead == False and self.stopThread==False:
            try:
                path = str(self.__folderEntryWithButton.getText()+os.sep+self.__projectEntryWithButton.getText())
                if os.path.exists(self.__folderEntryWithButton.getText()) == True and os.path.exists(path) == False and self.__loader.io.checkIfValidFileName(self.__projectEntryWithButton.getText()) == True:
                    self.OK = True
                else:
                    self.OK = False
            except Exception as e:
                self.__loader.logger.errorLog(e)
            sleep(0.05)

    def __getPath(self):
        return(str(self.__folderEntryWithButton.getText()+os.sep+self.__projectEntryWithButton.getText()+os.sep).replace("\\","/"))

    def openFolder(self):
        text = self.__folderEntryWithButton.getText()
        self.__folderEntryWithButton.setText(self.__loader.fileDialogs.askForDir(text))
        if self.__folderEntryWithButton.getText()=="":
            self.__folderEntryWithButton.setText(text)
        self.__focus()

    def __focus(self):
        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def __newProject(self, bool):
        if bool == True:
            try:
                self.__soundPlayer.playSound("OK")
                #temp = self.virtualMemory.kernel
                #self.virtualMemory.kernel = self.__setKernelLabel.optionValue.get()
                #self.virtualMemory.changeKernelMemory(temp)

                self.__loader.io.copyDirWithFiles("templates/new_project/", self.__getPath())
                for num in range(2,9):
                    self.__loader.io.copyDirWithFiles("templates/bank2_8/",
                                                      self.__getPath()+"bank"+str(num)+"/")
                os.rename(str(self.__getPath()+"project_name.project2600"),
                          str(self.__getPath()+self.__projectEntryWithButton.getText()+".project2600"))

                bank1_config = open(self.__getPath()+"/bank1/bank_configurations.a26", "r")
                lines = bank1_config.readlines()
                bank1_config.close()
                num = -1
                for line in lines:
                    num+=1
                    if line.startswith("bank1="):
                        k = line.split("=")[1]
                        lines[num] = line.replace(k, self.__setKernelLabel.optionValue.get())
                        break
                bank1_config = open(self.__getPath()+"/bank1/bank_configurations.a26", "w")
                bank1_config.writelines(lines)
                bank1_config.close()

                self.__loader.mainWindow.openProject(self.__getPath())
                self.__topLevel.getTopLevel().destroy()

            except Exception as e:
                self.__fileDialogs.displayError("projectNewError", "projectNewErrorText",
                                                {
                                                    "name": self.__projectEntryWithButton.getText()
                                                },
                                                str(e)
                                                )
                self.__loader.io.removeDirWithFiles(self.__getPath())
                self.__focus()
        else:
            self.__topLevel.getTopLevel().destroy()
