from tkinter import Toplevel

class SubMenu:

    def __init__(self, loader, name, w, h, checker, addElements):
        self.__loader = loader
        self.__subMenu = self

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize

        self.__topLevel = Toplevel()
        self.__topLevel.title(self.__dictionaries.getWordFromCurrentLanguage(name))
        self.__topLevel.geometry("%dx%d+%d+%d" % (w, h, (self.__screenSize[0]/2-w/2), (self.__screenSize[1]/2-h/2-50)))
        self.__topLevel.resizable(False, False)

        self.__topLevel.iconbitmap("others/img/"+name+".ico")


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

    def getTopLevel(self):
        return(self.__topLevel)

    def getTopLevelDimensions(self):
        return(self.__topLevel.winfo_width(), self.__topLevel.winfo_height())