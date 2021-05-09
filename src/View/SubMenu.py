from tkinter import Toplevel

class SubMenu:

    def __init__(self, loader, name, w, h, checker, addElements):
        self.__loader = loader
        self.__subMenu = self
        self.__loader.subMenus.append(self)
        if len(self.__loader.subMenus)>1:
            from threading import Thread
            t = Thread(target=self.killOther)
            t.daemon = True
            t.start()

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

        try:
            self.__topLevel.iconbitmap("others/img/"+name+".ico")
        except:
            self.__topLevel.iconbitmap("others/img/icon.ico")

        self.__topLevel.deiconify()
        self.__topLevel.focus()

        from threading import Thread
        if checker!=None:
            self.__checker = checker
            check = Thread(target=self.__checker)
            check.daemon = True
            check.start()

        if addElements!=None:
            self.__addElements = addElements
            add = Thread(target=self.__addElements, args=[self])
            add.daemon=True
            add.start()

        self.__topLevel.wait_window()

    def killOther(self):
        self.__loader.subMenus[0].dead = True
        from time import sleep
        sleep(1)

        self.__loader.subMenus[0].getTopLevel().destroy()
        self.__loader.subMenus.pop(0)

    def getTopLevel(self):
        return(self.__topLevel)

    def getTopLevelDimensions(self):
        return(self.__topLevel.winfo_width(), self.__topLevel.winfo_height())