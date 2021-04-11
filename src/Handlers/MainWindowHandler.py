class MainWindowHandler:
    def __init__(self, config, dictionaries, screensize, tk, soundplayer, fileDialogs):
        self.__config = config
        self.__dictionaries = dictionaries
        self.__screenSize = screensize
        self.__soundPlayer = soundplayer
        self.__fileDialogs = fileDialogs

        from threading import Thread

        self.__tk = tk

        self.mainWindow = None
        main = Thread(target=self.createMain)
        main.start()
        tk.focus_force()
        tk.focus()
        tk.mainloop()
        soundplayer.playSound("others/snd/Exit.wav")

    def createMain(self):
        from MainWindow import MainWindow
        MainWindow(self.__config, self.__dictionaries, self.__screenSize, self, self.__tk, self.__soundPlayer, self.__fileDialogs)
