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
            if line[1]!="" and ("#" not in line[1]):
                self.__piaNotes[line[0]] = {}
                __list = line[1].split(",")
                for item in __list:
                    item = item.split(":")
                    self.__piaNotes[line[0]][item[0]] = item[1]
            elif line[1]!="":
                line[1] = line[1][2:-1]
                temp = line[1].split(",")

                channel = temp[0].split(":")[0]
                notes = []
                self.__piaNotes[line[0]] = {}

                for item in temp:
                    item = item.split(":")
                    notes.append(item[1])

                self.__piaNotes[line[0]][channel] = notes

    def getTiaValue(self, note, channel):
        drums =        {89: (15, 20),
                        90: (8, 0),
                        91: (15, 2),
                        92: (8, 8),
                        93: (2, 0),
                        94: (3, 0),
                        95: (3, 1)
                        }

        try:
            if channel == None:
                if (int(note) > 88):
                    return (drums[int(note)])
                else:
                    return(self.__piaNotes[str(note)])
            else:
                return(self.__piaNotes[str(note)][str(channel)])
        except:
            return None


    def getPianoKey(self, note, channel):
        for key in self.__piaNotes:
            if channel in self.__piaNotes[key]:
                if type(self.__piaNotes[key][channel]) == list:
                    N = 0
                    for item in self.__piaNotes[key][channel]:
                        N += int(item)

                    brokenNote = str(N // len(self.__piaNotes[key][channel]))

                    if note == brokenNote:
                        return(key)
                else:
                    if self.__piaNotes[key][channel] == note:
                        return(key)


    def playTia(self, volume, channel, note):
        from threading import Thread
        t = Thread(target=self.playTiaThread, args=[volume, channel, note])
        t.daemon = True
        t.start()

    def playTiaThread(self, volume, channel, note):
        self.__tiaTone.setAndPlay(int(volume), int(channel), int(note), "NTSC", 1)


