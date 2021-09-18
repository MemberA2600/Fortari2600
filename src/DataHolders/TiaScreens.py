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

        self.__colors = {}

        self.__tiaNote = {
            "volume": 0,
            "channel": 0,
            "freq": 0,
            "enabled": 0,
            "color": "white"
        }

        row = []
        row2 = []

        for X in range(0, self.numOfFieldsW):
            row.append(deepcopy(self.__tiaNote))
            row2.append(-1)


        self.__screen = {
            "screen": [],
            "Y": deepcopy(row2)
        }

        for Y in range(0,100):
            self.__screen["screen"].append(deepcopy(row))

        self.currentChannel = 1
        self.currentScreen = 0
        self.screenMax = 0

        self.allData = []

        screen = [deepcopy(self.__screen)]
        for n in range(0, 4):
            self.allData.append(deepcopy(screen))

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
            """
            for row in self.allData[channelNum][self.currentScreen]["screen"]:
                for cell in row:
                    if cell["volume"]>0:
                        num = 1
                        break
            """
            for X in self.allData[num-1][self.currentScreen]["Y"]:
                if self.allData[num-1][self.currentScreen]["Y"][X] != -1:
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

    def getWholeChannelDate(self, num):
        from copy import deepcopy

        data = []

        for screen in range(0, self.screenMax+1):
            S = []
            for X in range(0, self.numOfFieldsW):
                Y = self.allData[num - 1][screen]["Y"][X]

                if Y == -1:
                    S.append("#")
                else:
                    item = self.allData[num-1][screen]["screen"][Y][X]
                    txt = str(Y)+" "+str(item["volume"])+" "+str(item["channel"])+" "+str(item["freq"])
                    S.append(txt)

            data.append(",".join(S))

        return(";".join(data))

    def getLoadedInputAndSetData(self, musicComposer, data):
        from time import sleep
        from threading import Thread
        for c in range(0, 4):
            if ";" in data[c]:
                data[c] = data[c].split(";")
            else:
                data[c] = [data[c]]

            for i in range(0, len(data[c])):
                data[c][i] = data[c][i].split(",")

        # If you got here without exception, the data seems to be correct.
        self.screenMax = len(data[0])-1
        musicComposer.reset = True

        # Here must be a lot of precessing so the Music Composer has enough time on resetting the variables.


        self.__all = 4
        self.allData = [
            [], [], [], []
        ]

        t1 = Thread(target=self.channelThread, args=(data[0], 0))
        t2 = Thread(target=self.channelThread, args=(data[1], 1))
        t3 = Thread(target=self.channelThread, args=(data[2], 2))
        t4 = Thread(target=self.channelThread, args=(data[3], 3))

        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        while self.__all>0:
            sleep(0.0001)

        #sleep(0.5)
        musicComposer.reColorAll()

    def channelThread(self, data, num):
        from copy import deepcopy
        from threading import Thread
        from time import sleep

        for s in data:
            self.allData[num].append(deepcopy(self.__screen))
            for noteNum in range(0, self.numOfFieldsW):
                if s[noteNum] != "#":
                    d = s[noteNum].split(" ")
                    Y = int(d[0])
                    self.allData[num][-1]["Y"] = Y

                    field = self.allData[num][-1]["screen"][Y][noteNum]
                    field["volume"] = int(d[1])
                    field["channel"] = int(d[2])
                    field["freq"] = int(d[3])
                    field["enabled"] = 1

        self.__all-=1



    def __insert(self, N):
        from copy import deepcopy

        for num in range(0,4):
            self.allData[num].insert(N, deepcopy(self.__screen))


    def getIfUpperIsOccupied(self, X):
        thereIsOne = False


        for num in range(1, self.currentChannel):
            Y = self.allData[num-1][self.currentScreen]["Y"][X]
            if Y != -1:
                if thereIsOne == False:
                    thereIsOne = True
                else:
                    return (True)

            """
            for Y in range(0,100):
                if self.allData[num-1][self.currentScreen]["screen"][Y][X]["enabled"] == 1:
                    if thereIsOne == False:
                        thereIsOne = True
                        break
                    else:
                        return (True)
            """

        return (False)

    def playTone(self, X, Y):
        note = self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X]
        self.__piaNotes.playTia(note["volume"], note["channel"], note["freq"])

    def getTileValue(self, X, Y):
        return(self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X])

    def setTileValue(self, X, Y, V, C, F, enabled):
        self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X]["volume"] = V
        self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X]["channel"] = C
        self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X]["freq"] = F
        self.allData[self.currentChannel-1][self.currentScreen]["screen"][Y][X]["enabled"] = enabled
        if enabled == 1:
            self.allData[self.currentChannel-1][self.currentScreen]["Y"][X] = Y

    def setMinusOne(self, X):
        self.allData[self.currentChannel - 1][self.currentScreen]["Y"][X] = -1

    def setColorValue(self, X, Y, color):
        for num in range(0,4):
            self.allData[num][self.currentScreen]["screen"][Y][X]["color"] = color
        self.__screen["screen"][Y][X]["color"] = color
        #self.__colors[str(Y)] = color

    def getDomimantChannel(self):
        channels = {
            1: 0, 4: 0, 6: 0, 12: 0
        }

        for channel in self.allData:
            for screen in channel:
                for X in range(0, self.numOfFieldsW):
                    Y = screen["Y"][X]
                    cell = screen["screen"][Y][X]
                    if cell["channel"] in channels.keys():
                        channels[cell["channel"]] += 1



                """
                for row in screen["screen"]:
                    for cell in row:
                        if cell["channel"] in channels.keys():
                            channels[cell["channel"]]+=1
                """

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

