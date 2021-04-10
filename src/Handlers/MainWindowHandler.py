class MainWindowHandler:
    def __init__(self, config, dictionaries, screemsize):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screemsize

        from threading import Thread

        self.mainWindow = None
        from MainWindow import MainWindow
        MainWindow(config, dictionaries, screemsize, self)

