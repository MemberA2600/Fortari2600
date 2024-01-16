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


    def __removeTemp(self):
        try:
            from shutil import rmtree
            rmtree('temp/')

        except:
            pass

    def createMain(self):
        from MainWindow import MainWindow
        MainWindow(self.__loader)
