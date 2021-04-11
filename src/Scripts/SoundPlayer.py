class SoundPlayer:

    def __init__(self, config):
        self.__config = config

    def playSound(self, path):
        from threading import Thread
        self.path = path
        if self.__config.getValueByKey("soundOn")=="True":
            sound = Thread(target=self.playThread)
            sound.start()

    def playThread(self):
        from playsound import playsound
        playsound(self.path)


