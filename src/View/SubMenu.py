from tkinter import Toplevel
from threading import Thread

class SubMenu:

    def __init__(self, loader, name, w, h, checker, addElements, maxNum):
        self.__loader = loader
        #self.__loader.subMenus.append(self)
        #self.__loader.subMenuDict[name] = self
        self.__name = name

        """
        if len(self.__loader.subMenus)>maxNum:
            t = Thread(target=self.killOther)
            t.daemon = True
            t.start()
        """

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize

        self.__topLevel = Toplevel()
        self.__topLevel.title(self.__dictionaries.getWordFromCurrentLanguage(name))
        self.__topLevel.geometry("%dx%d+%d+%d" % (w, h, (self.__screenSize[0]/2-w/2), (self.__screenSize[1]/2-h/2-50)))
        self.__topLevel.resizable(False, False)

        self.__topLevel.config(bg=self.__loader.colorPalettes.getColor("window"))
        #self.__topLevel.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        try:
            self.__topLevel.iconbitmap("others/img/"+name+".ico")
        except:
            self.__topLevel.iconbitmap("others/img/icon.ico")

        self.__loader.topLevels.append(self.__topLevel)
        self.__topLevel.deiconify()
        self.__topLevel.focus()

        if checker!=None:
            self.__checker = checker
            self.__loader.threadLooper.addToThreading(self, self.__checker, [], 1)
            
            #check = Thread(target=self.__checker)
            #check.daemon = True
            #check.start()

        if addElements!=None:
            self.__addElements = addElements
            add = Thread(target=self.__addElements, args=[self])
            add.daemon=True
            add.start()

        #self.changeWindowState(True, maxNum-1)
        self.__topLevel.wait_window()
        #try:
        #    self.changeWindowState(False, maxNum-1)
        #except:
        #    pass

        """
        try:
            self.__loader.subMenus.pop(-1)
            self.__loader.subMenus.remove(self)
        except Exception as e:
            self.__loader.logger.errorLog(e)
        """

        #t = Thread(target=self.__killIfKilled)
        #t.daemon = True
        #t.start()

    """
    def __killIfKilled(self):
        if self.__topLevel.winfo_exists() == False and self.__name in self.__loader.subMenuDict:
              del self.__loader.subMenuDict[self.__name]
              self.stopThread = True
              if self.__topLevel in self.__loader.topLevels:
                 self.__loader.topLevels.remove(self.__topLevel)
              if self in self.__loader.stopThreads:
                 self.__loader.stopThreads.remove(self)
   
    def killOther(self):
        num = 10

        from time import sleep

        while num > 0:
            sleep(1)

            try:
                self.__loader.subMenus[-2].dead = True
                self.__loader.subMenus[-2].getTopLevel().destroy()
                self.__loader.subMenus.pop(-2)
                num = 0
            except:
                num -= 1
    """

    def getTopLevel(self):
        return(self.__topLevel)

    def getTopLevelDimensions(self):
        return(self.__topLevel.winfo_width(), self.__topLevel.winfo_height())

    #def __closeWindow(self):

    #    self.__topLevel.destroy()