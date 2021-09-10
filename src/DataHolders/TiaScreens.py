class TiaScreens:

    def __init__(self, loader):
        self.__loader = loader
        self.__piaNotes = loader.piaNotes
        self.__fileDialogs = self.__loader.fileDialogs
        self.__dictionaries = self.__loader.dictionaries

        self.numOfFieldsW = 48
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
        self.screenMax = 0

        self.allData = []

        screens = [deepcopy(self.__screen)]
        for n in range(0, 4):
            self.allData.append(deepcopy(screens))

    def insertBefore(self):
        self.__insert(self.currentScreen)
        self.currentScreen+=1
        self.screenMax+=1

    def insertAfter(self):
        self.__insert(self.currentScreen+1)
        self.screenMax+=1

    def deleteCurrent(self):
        num = 0
        for channelNum in range(0,4):
            for row in self.allData[channelNum][self.currentScreen]:
                for cell in row:
                    if cell["volume"]>0:
                        num = 1
                        break

        answer = None
        if num > 0:
            answer = self.__fileDialogs.askYesOrNo("notEmpty", "notEmptyMessage")
        if num ==0 or answer == "Yes":
            for num in range(0,4):
                self.allData[num].pop(self.currentScreen)
            self.screenMax-=1
            if self.currentScreen > self.screenMax:
                self.currentScreen-=1


    def __insert(self, N):
        from copy import deepcopy

        for num in range(0,4):
            self.allData[num].insert(N, deepcopy(self.__screen))

    def getIfUpperIsOccupied(self, X):
        thereIsOne = False

        for num in range(1, self.currentChannel):
            for Y in range(0,100):
                if self.allData[num-1][self.currentScreen][Y][X]["enabled"] == 1:
                    if thereIsOne == False:
                        thereIsOne = True
                    else:
                        return (True)

        return (False)

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
        for num in range(0,4):
            self.allData[num][self.currentScreen][Y][X]["color"] = color
        self.__screen[Y][X]["color"] = color

    def getDomimantChannel(self):
        channels = {
            1: 0, 4: 0, 6: 0, 12: 0
        }

        for channel in self.allData:
            for screen in channel:
                for row in screen:
                    for cell in row:
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

