from SubMenu import SubMenu
from SubMenuLabel import SubMenuLabel
from NewListBoxInFrame import NewListBoxInFrame
from SubMenuFrame import SubMenuFrame
from SubMenuEntryWithButton import SubMenuEntryWithButton
from SubMenuOkCancelButtons import SubMenuOkCancelButtons
from tkinter import *

class OpenProjectWindow:

    def __init__(self, loader, master, opener):
        self.__loader = loader
        self.__master = master
        self.__opener = opener

        self.dead = False
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



        self.__window = SubMenu(self.__loader, "open", self.__screenSize[0] / 3, self.__screenSize[1] / 3 - 45,
                           None, self.__addElements, 1)
        self.dead = True

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.75), False, False, False)

        self.__frame1 = SubMenuFrame(self.__loader, self.__topLevel, self.__topLevelWindow,
                                     self.__topLevel.getTopLevelDimensions()[0]*0.33)

        self.__listBoxLabel = SubMenuLabel(self.__frame1.getFrame(),
                                       self.__loader,
                                       "projectList",
                                       self.__smallFont)


        self.__listBox = NewListBoxInFrame("openListBox", self.__loader, self.__frame1,
                                        list(self.__loader.config.getProjects()), None, LEFT)


        self.__frame2 = SubMenuFrame(self.__loader, self.__topLevel, self.__topLevelWindow,
                                     self.__topLevel.getTopLevelDimensions()[0] * 0.66)

        self.__projectPathLabel = SubMenuLabel(self.__frame2.getFrame(),
                                       self.__loader,
                                       "projectPath",
                                       self.__smallFont)

        self.__projectPathEntry = SubMenuEntryWithButton(self.__frame2, self.__loader, self.__smallFont)
        self.__projectPathEntry.addButton("open", self.openDialog)
        from threading import Thread

        try:
            self.__getAndSelect()


            self.__chg = Thread(target=self.checkIfListBoxSelectChanged)
            self.__chg.daemon = True
            self.__chg.start()
        except:
            pass
        self.__okCancel = SubMenuOkCancelButtons(self, self.__frame2, self.__loader, self.__normalFont, self.func, self.getOK)
        self.__okThread = Thread(target=self.checkIfOK)
        self.__okThread.daemon=True
        self.__okThread.start()
        from ET import ET
        self.__et = ET(self, self.__frame2, self.__loader, self.__topLevel)



    def openDialog(self):
        projectPath = "/".join(self.__fileDialogs.askForFileName("openProjectIndex", False,
                        ["project2600"], "projects/").replace("\\", "/").split("/")[0:-1])+"/"

        if projectPath!="":
            self.__projectPathEntry.setText(projectPath)

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

    def func(self, bool):
        if bool == True:
            path = self.__projectPathEntry.getText()
            if path.endswith("/") == False:
                path += "/"
            self.__opener(path)
        self.dead = True
        self.__topLevelWindow.destroy()

    def __getAndSelect(self):
        self.__selected = self.__listBox.getSelectedName()
        self.__projectPathEntry.setText(
            self.__config.getProjectPath(
                self.__selected
            )
        )

    def getWindowSize(self):
        return(self.__window.getTopLevelDimensions())

    def getScales(self):
        return(1,1)

    def getFrameSize(self):
        return(self.__topLevel.getTopLevelDimensions())

    def getOK(self):
        return(self.OK)

    def checkIfListBoxSelectChanged(self):
        from time import sleep
        while self.dead == False and self.stopThread==False:
            try:
                if self.__selected!=self.__listBox.getSelectedName():
                    self.__getAndSelect()
            except Exception as e:
                self.__loader.logger.errorLog(e)

            sleep(0.05)

    def checkIfOK(self):
        from time import sleep
        while self.dead == False and self.stopThread == False:
            try:
                import os
                if os.path.exists(self.__projectPathEntry.getText()):
                    self.OK = True
                else:
                    self.OK = False
            except Exception as e:
                self.__loader.logger.errorLog(e)

            sleep(0.05)