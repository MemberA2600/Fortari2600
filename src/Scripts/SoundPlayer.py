from threading import Thread

class SoundPlayer:

    def __init__(self, config):
        self.__config = config
        #self.__counter = 0

    def playSound(self, name):
        if self.__config.getValueByKey("soundOn") == "True":
            sound = Thread(target=self.playThread, args = [self.__fullPath(name)])
            sound.start()

    def __fullPath(self, name):
        return "others/snd/" + name + ".wav"

    def play(self, path):
        sound = Thread(target=self.playThread, args = [path])
        sound.start()

    def playThread(self, path):
        from playsound import playsound
        playsound(path)

        #self.__counter += 1
        #print(self.__counter)

    def playOnlyOneAtTime(self, name):
        import winsound
        if self.__config.getValueByKey("soundOn") == "True":
           winsound.PlaySound(self.__fullPath(name), winsound.SND_ASYNC)
