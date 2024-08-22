from threading import Thread
from random import randint

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

    def playFail(self):
        number = randint(0,1000)
        if   number > 995:
            self.playSound("Gas")
        elif number > 990:
            self.playSound("Pylons")
        else:
            self.playSound("Error")

    def playAsk(self):
        number = randint(0,1000)
        if   number > 995:
            self.playSound("Probe")
        else:
            self.playSound("Ask")