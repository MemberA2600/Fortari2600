class MainWindow:

    def __init__(self, config, dictionaries, screemsize, super):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screemsize

        super.mainWindow = self