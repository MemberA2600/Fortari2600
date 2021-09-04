class TiaScreens:

    def __init__(self, loader):
        self.__loader = loader
        self.__piaNotes = loader.piaNotes


        self.numOfFieldsW = 52
        self.__runningThreads = 2

        from copy import deepcopy
        self.__noteTable = []

        self.__tiaNote = {
            "volume": 0,
            "channel": 0,
            "freq": 0,
            "enabled": 0,
            "color": "white"
        }

        row = []
        for X in range(0, self.numOfFieldsW):
            row.append(deepcopy(self.__tiaNote))

        self.__screen = []
        for Y in range(0,100):
            self.__screen.append(deepcopy(row))

        self.currentChannel = 1
        self.currentScreen = 0
        self.screenMax = 1

        self.allData = []

        screens = [deepcopy(self.__screen)]
        for n in range(0, 4):
            self.allData.append(deepcopy(screens))


    def playTone(self, X, Y):
        note = self.allData[self.currentChannel-1][self.currentScreen][Y][X]
        self.__piaNotes.playTia(note["volume"], note["channel"], note["freq"])

    def getTileValue(self, X, Y):
        return(self.allData[self.currentChannel-1][self.currentScreen][Y][X])

    def setTileValue(self, X, Y, V, C, F, enabled):
        self.allData[self.currentChannel-1][self.currentScreen][Y][X]["volume"] = V
        self.allData[self.currentChannel-1][self.currentScreen][Y][X]["channel"] = C
        self.allData[self.currentChannel-1][self.currentScreen][Y][X]["freq"] = F
        self.allData[self.currentChannel-1][self.currentScreen][Y][X]["enabled"] = enabled

    def setColorValue(self, X, Y, color):
        self.allData[self.currentChannel-1][self.currentScreen][Y][X]["color"] = color

    def getDomimantChannel(self):
        channels = {
            1: 0, 4: 0, 6: 0, 12: 0
        }

        for channel in self.allData:
            for screen in channel:
                for column in screen:
                    for cell in column:
                        if cell["channel"] in channels.keys():
                            channels[cell["channel"]]+=1

        forSort = []
        for key in channels.keys():
            forSort.append(channels[key])

        forSort.sort(reverse=True)

        sendBack = []

        for num in forSort:
            for key in channels.keys():
                if channels[key] == num and (key not in sendBack):
                    sendBack.append(key)


        return(sendBack)

