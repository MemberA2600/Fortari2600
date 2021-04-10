class LoadingScreenHandler:

    def __init__(self, screensize, tk):
        from threading import Thread

        self.__screenSize = screensize
        self.__tk = tk

        self.__loadingScreen = None
        self.__loading = Thread(target=self.__createLoading)
        self.__loading.daemon = True
        self.__loading.start()

    def __createLoading(self):
        from LoadingScreen import LoadingScreen
        LoadingScreen(self.__screenSize, self, self.__tk)

    def setLoadingScreen(self, item):
        self.__loadingScreen = item

    def destroyScreen(self):
        self.__loadingScreen.destroySelf()