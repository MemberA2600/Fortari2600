from TiaTone import TiaTone

class PiaNotes:
    def __init__(self, loader):
        self.__loader = loader
        self.__tiaTone = self.__loader.tiaTone
        self.__loadPiaNotes()

    def __loadPiaNotes(self):
        self.__piaNotes = {}
        file = open("config/PiaNotes.txt")
        text = file.read()
        file.close()

        text = text.replace("\r","").split("\n")

        for line in text:
            line = line.split("=")
            if line[1]!="":
                self.__piaNotes[line[0]] = {}
                __list = line[1].split(",")
                for item in __list:
                    item = item.split(":")
                    self.__piaNotes[line[0]][item[0]] = item[1]

    def getTiaValue(self, note, channel):
        try:
            if channel == None:
                return(self.__piaNotes[note])
            else:
                return(self.__piaNotes[note][channel])
        except:
            return None

    def playTia(self, note, channel):
        from threading import Thread
        t = Thread(target=self.playTiaThread, args=[note, channel])
        t.daemon = True
        t.start()

    def playTiaThread(self, note, channel):
        self.__tiaTone.setAndPlay(8, int(channel), int(note), "NTSC", 1)
