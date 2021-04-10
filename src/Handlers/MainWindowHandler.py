class MainWindowHandler:
    def __init__(self, config, dictionaries, screensize, LSH, tk, soundplayer):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screensize
        self.__soundPlayer = soundplayer

        from threading import Thread

        self.__lSH=LSH
        self.__tk = tk

        self.mainWindow = None
        main = Thread(target=self.createMain)
        main.start()
        tk.focus_force()
        tk.mainloop()
        soundplayer.playSound("others/snd/Exit.wav")

    def createMain(self):
        from MainWindow import MainWindow
        MainWindow(self.__config, self.__dictionaries, self.__screenSize, self, self.__lSH, self.__tk, self.__soundPlayer)
