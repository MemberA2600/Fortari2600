class MainWindowHandler:
    def __init__(self, loader):
        self.__loader = loader
        self.__loader.mainWindowHander = self
        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs

        try:
            from os import mkdir
            mkdir("temp/")
        except:
            pass

        from threading import Thread

        self.__tk = self.__loader.tk

        self.mainWindow = None
        main = Thread(target=self.createMain)
        main.start()
        self.__tk.focus_force()
        self.__tk.deiconify()
        self.__tk.focus()
        self.__tk.mainloop()
        self.__loader.mainWindow.dead = True
        self.__loader.soundPlayer.playSound("Exit")
        self.__removeTemp()
        from time import sleep
        sleep(2)

    #def setWaitWindow(self, widget):
    #    widget.wait_window()

    def __removeTemp(self):
        try:
            from shutil import rmtree
            rmtree('temp/')

        except:
            pass


        """
        import os

        toBeDeleted=[]

        for root, dirs, files in os.walk("temp/", False):
            for file in files:
                toBeDeleted.append(root+"/"+file)

        for file in toBeDeleted:
            os.remove(file)
        """

    def createMain(self):
        from MainWindow import MainWindow
        MainWindow(self.__loader)
