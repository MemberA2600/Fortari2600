from SubMenu import SubMenu
from tkinter import *
import os

class NewProjectWindow:

    def __init__(self, loader):

        self.dead = False
        self.__loader=loader
        self.OK = False


        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*18)

        self.__screenSize = self.__loader.screenSize

        self.__window = SubMenu(self.__loader, "new", self.__screenSize[0] / 3, self.__screenSize[1] / 4 - 25,
                           self.__checker, self.__addElements)
        self.dead = True

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

        self.__okCancel = SubMenuOkCancelButtons(self, self.__topLevel, self.__loader, self.__normalFont, self.__newProject, self.getOK)
        self.__harry = PitFallHarry(self, self.__topLevel, self.__loader, self.__normalFont)

    def getOK(self):
        return(self.OK)

    def __checker(self):
        from time import sleep
        import os
        while self.dead == False:
            try:
                path = str(self.__folderEntryWithButton.getText()+os.sep+self.__projectEntryWithButton.getText())
                if os.path.exists(self.__folderEntryWithButton.getText()) == True and os.path.exists(path) == False and self.__loader.io.checkIfValidFileName(self.__projectEntryWithButton.getText()) == True:
                    self.OK = True
                else:
                    self.OK = False
            except Exception as e:
                #print(e)
                pass
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
                self.__loader.io.copyDirWithFiles("templates/new_project/", self.__getPath())
                for num in range(2,9):
                    self.__loader.io.copyDirWithFiles("templates/bank2_8/",
                                                      self.__getPath()+"bank"+str(num)+"/")
                os.rename(str(self.__getPath()+"project_name.project2600"),
                          str(self.__getPath()+self.__projectEntryWithButton.getText()+".project2600"))
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
