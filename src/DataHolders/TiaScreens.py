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
                    self.allData[num][-1]["Y"][noteNum] = Y

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


    def composeData(self, correctNotes, buzz, fadeOutLen, frameLen, vibratio, tv):
        from TiaNote import TiaNote
        #compress the 4 channels into two
        from copy import deepcopy

        data1 = [
            [],
            [],
            [],
            []
        ]

        """
        for screenNum in range(0, self.screenMax+1):
            for noteNum in range(0, self.numOfFieldsW):
                # self.allData[0][screenNum]["Y"][noteNum]
                nums = []

                for channelNum in range(0,4):
                    if self.allData[channelNum][screenNum]["Y"][noteNum] != -1:
                        nums.append([channelNum, self.allData[channelNum][screenNum]["Y"][noteNum]])

                if len(nums)<4:
                    while len(nums)<4:
                        nums.append(-1)

                if nums[0] == -1:
                    for filler in range(0, frameLen):
                        data1[0].append(TiaNote(0,0,0,1,-1))
                        data1[1].append(TiaNote(0,0,0,1,-1))
                else:
                    note = self.allData[nums[0][0]][screenNum]["screen"][nums[0][1]][noteNum]
                    for filler in range(0, frameLen):
                        data1[0].append(TiaNote(note["volume"], note["channel"], note["freq"], 1,
                                                self.allData[nums[0][0]][screenNum]["Y"][noteNum]))
                        if buzz == 1 and note["channel"] == 6:
                            data1[0][-1].channel = 7

                    if nums[-1] == -1:
                        for filler in range(0, frameLen):
                            data1[1].append(TiaNote(0, 0, 0, 1, 0))
                    else:
                        note = self.allData[nums[1][0]][screenNum]["screen"][nums[1][1]][noteNum]
                        for filler in range(0, frameLen):
                            data1[1].append(TiaNote(note["volume"], note["channel"], note["freq"], 1,
                                                    self.allData[nums[1][0]][screenNum]["Y"][noteNum]))
                            if buzz == 1 and note["channel"] == 6:
                                data1[1][-1].channel = 7
        """
        for screenNum in range(0, self.screenMax + 1):
            for noteNum in range(0, self.numOfFieldsW):
                nums = [
                    TiaNote(0, 0, 0, 1, -1),
                    TiaNote(0, 0, 0, 1, -1),
                    TiaNote(0, 0, 0, 1, -1),
                    TiaNote(0, 0, 0, 1, -1)
                ]
                for channelNum in range(0, 4):
                    if self.allData[channelNum][screenNum]["Y"][noteNum] != -1:
                        Y = self.allData[channelNum][screenNum]["Y"][noteNum]
                        note = self.allData[channelNum][screenNum]["screen"][Y][noteNum]

                        nums[channelNum] = TiaNote(note["volume"], note["channel"], note["freq"], 1, Y)
                    data1[channelNum].append(deepcopy(nums[channelNum]))


        #buzz and framelen is processed during the first run.
        dominants = [
            {1: 0, 4: 0, 6: 0, 7: 0, 12: 0},
            {1: 0, 4: 0, 6: 0, 7: 0, 12: 0},
            {1: 0, 4: 0, 6: 0, 7: 0, 12: 0},
            {1: 0, 4: 0, 6: 0, 7: 0, 12: 0}
        ]

        #get dominants
        for num in range(0,4):
            channel = data1[num]
            for tiaNote in channel:
                if tiaNote.channel in [1,4,6,7,12]:
                    dominants[num][tiaNote.channel]+=1

            if buzz == 1:
                del dominants[num][6]
                if dominants[num][1]<dominants[num][7]:
                    del dominants[num][1]
                else:
                    del dominants[num][7]

            else:
                del dominants[num][7]
                if dominants[num][1]<dominants[num][6]:
                    del dominants[num][1]
                else:
                    del dominants[num][6]

            if dominants[num][4]<dominants[num][12]:
                del dominants[num][4]
            else:
                del dominants[num][12]


        pairs = {
            4: 12, 12: 4, 1: 6, 6: 1, 7: 1

        }


        #print(data1[0][0].piaNote)
        #return(data1)
        #change one to the dominant pair
        for num in range(0,4):
            channel = data1[num]
            for tiaNote in channel:
                if tiaNote.channel in [1,4,6,7,12]:
                    if tiaNote.channel not in dominants[num]:
                        if tiaNote.channel in [4,12]:
                            if 4 in dominants[num]:
                                dominantChannel = 4
                                dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, 4)
                            else:
                                dominantChannel = 12
                                dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, 12)
                        else:
                            if 1 in dominants[num]:
                                dominantChannel = 1
                                dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, 1)
                            elif 6 in dominants[num]:
                                dominantChannel = 6
                                dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, 6)
                            else:
                                dominantChannel = 7
                                dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, 7)

                        if dominantNote != None:
                            if type(dominantNote) != list:
                                tiaNote.channel = dominantChannel
                                tiaNote.freq = int(dominantNote)
                            else:
                                tiaNote.channel = dominantChannel
                                N = 0
                                for num2 in dominantNote:
                                    N+=int(num2)
                                tiaNote.freq=round(N/len(dominantNote))
                        else:
                            newChannel = pairs[dominantChannel]
                            if newChannel == 6 and buzz == 1:
                                newChannel = 7
                            dominantNote = self.__piaNotes.getTiaValue(tiaNote.piaNote, newChannel)
                            if dominantNote != None:
                                if type(dominantNote) != list:
                                    tiaNote.channel = newChannel
                                    tiaNote.freq = int(dominantNote)
                                else:
                                    tiaNote.channel = newChannel
                                    N = 0
                                    for num2 in dominantNote:
                                        N += int(num2)
                                    tiaNote.freq = round(N / len(dominantNote))

        #correction
        #print(data1[0][0].piaNote)


        # print(data1[0][0].piaNote)
        # processing vibratio
        if vibratio == 1:
            for channel in data1:
                counter = 0
                sum = 0
                for tiaNote in channel:
                    if tiaNote.channel in [4, 12]:
                        sum += tiaNote.piaNote

                if (sum // len(channel)) < 33:
                    changer = -8
                else:
                    changer = 8

                # Get the average to decide vibrate over or under.

                tempChannel = None
                tempNote = None
                counter = 0

                for tiaNote in channel:
                    if tiaNote.channel not in [4, 12]:
                        tempChannel = None
                        tempNote = None
                        counter = 0
                    else:
                        if counter == 5 or (tempChannel != tiaNote.channel or tempNote != tiaNote.piaNote):
                            counter = 0
                        else:
                            counter += 1

                        tempChannel = tiaNote.channel
                        tempNote = tiaNote.piaNote

                        if counter > 2:
                            note = tiaNote.piaNote
                            if note < 32:
                                continue
                            else:
                                note += changer
                                if note > 30 or note < 66:
                                    newNote = self.__piaNotes.getTiaValue(note, tiaNote.channel)
                                    if newNote != None:
                                        if type(newNote) != list:
                                            tiaNote.piaNote = note
                                            tiaNote.freq = int(newNote)
                                        else:
                                            N = 0
                                            for num2 in newNote:
                                                N += int(num2)

                                            tiaNote.piaNote = note
                                            tiaNote.freq = round(N / len(newNote))
                                    else:
                                        newChannel = pairs[tiaNote.channel]
                                        newNote = self.__piaNotes.getTiaValue(note, newChannel)
                                        if newChannel == 6 and buzz == 1:
                                            newChannel = 7
                                        if newNote != None:
                                            if type(newNote) != list:
                                                tiaNote.piaNote = note
                                                tiaNote.channel = newChannel
                                                tiaNote.freq = int(newNote)
                                            else:
                                                N = 0
                                                for num2 in newNote:
                                                    N += int(num2)
                                                tiaNote.channel = newChannel
                                                tiaNote.piaNote = note
                                                tiaNote.freq = round(N / len(newNote))


        #return(data1)

        if fadeOutLen > 0:
            for channel in data1:
                tiaNoteNum = 0
                while tiaNoteNum < (len(channel) - fadeOutLen):
                    tiaNote = channel[tiaNoteNum]
                    nextNote1 = channel[tiaNoteNum + 1]
                    if fadeOutLen > 1:
                        nextNote2 = channel[tiaNoteNum + 2]
                    if fadeOutLen > 2:
                        nextNote3 = channel[tiaNoteNum + 3]
                    if fadeOutLen > 3:
                        nextNote4 = channel[tiaNoteNum + 4]

                    jobdone = False

                    if (fadeOutLen == 4
                            and tiaNote.volume != 0
                            and nextNote1.volume == 0
                            and nextNote2.volume == 0
                            and nextNote3.volume == 0
                            and nextNote4.volume == 0
                            and jobdone == False):

                        nextNote1 = self.getNextNote(tiaNote, 2, tiaNote.volume-1, 3)
                        channel[tiaNoteNum + 1] = nextNote1
                        nextNote2 = self.getNextNote(tiaNote, 3, tiaNote.volume-2, 2)
                        channel[tiaNoteNum + 2] = nextNote2
                        nextNote3 = self.getNextNote(tiaNote, 5, tiaNote.volume-3, 2)
                        channel[tiaNoteNum + 3] = nextNote3
                        nextNote4 = self.getNextNote(tiaNote, 9, tiaNote.volume-4, 1)
                        channel[tiaNoteNum + 4] = nextNote4
                        tiaNoteNum += 4
                        jobdone = True

                    if (fadeOutLen > 2
                            and tiaNote.volume != 0
                            and nextNote1.volume == 0
                            and nextNote2.volume == 0
                            and nextNote3.volume == 0
                            and jobdone == False):
                        nextNote1 = self.getNextNote(tiaNote, 2, tiaNote.volume-1, 3)
                        channel[tiaNoteNum + 1] = nextNote1
                        nextNote2 = self.getNextNote(tiaNote, 4, tiaNote.volume-2, 2)
                        channel[tiaNoteNum + 2] = nextNote2
                        nextNote3 = self.getNextNote(tiaNote, 7, tiaNote.volume-3, 1)
                        channel[tiaNoteNum + 3] = nextNote3
                        tiaNoteNum += 3
                        jobdone = True

                    if (fadeOutLen > 1
                            and tiaNote.volume != 0
                            and nextNote1.volume == 0
                            and nextNote2.volume == 0
                            and jobdone == False):
                        nextNote1 = self.getNextNote(tiaNote, 2, tiaNote.volume-2, 3)
                        channel[tiaNoteNum + 1] = nextNote1
                        nextNote2 = self.getNextNote(tiaNote, 5, tiaNote.volume-3, 1)
                        channel[tiaNoteNum + 2] = nextNote2
                        tiaNoteNum += 2
                        jobdone = True

                    if (tiaNote.volume != 0
                            and nextNote1.volume == 0
                            and jobdone == False):
                        nextNote1 = self.getNextNote(tiaNote, 3, tiaNote.volume-3, 2)
                        channel[tiaNoteNum + 1] = nextNote1
                        tiaNoteNum += 1
                        jobdone = True

                    tiaNoteNum += 1

        #return(data1)

        tempChannel = None
        tempNote = None
        counter = 0

        if correctNotes > 0:
            for channel in data1:
                for tiaNoteNum in range(0, len(channel)):
                    tiaNote = channel[tiaNoteNum]

                    try:
                        nextNote = channel[tiaNoteNum+1]
                    except:
                        nextNote = None

                    try:
                        prevNote = channel[tiaNoteNum-1]
                    except:
                        prevNote = None

                    notes = self.__piaNotes.getTiaValue(tiaNote.piaNote, tiaNote.channel)
                    if notes == None:
                        continue

                    if type(notes) != list:
                        tempChannel = None
                        tempNote = None
                        counter = 0
                    else:
                        if counter == len(notes) - 1 or (tempChannel != tiaNote.channel or tempNote != tiaNote.piaNote):
                            counter = 0
                        else:
                            counter += 1

                        tempChannel = tiaNote.channel
                        tempNote = tiaNote.piaNote



                        if ((tiaNote.piaNote != nextNote.piaNote or nextNote == None) and
                                (tiaNote.piaNote != prevNote.piaNote or prevNote == None)):
                            N = 0
                            for num in notes:
                                N+=int(num)
                            N = round(N/len(notes))
                            tiaNote.freq = N
                        else:
                            tiaNote.freq = notes[counter]

        #print(data1[0][0].piaNote)


        data2 = [
            [],
            []
        ]

        for noteNum in range(0, len(data1[0])):
            nums = [
                    TiaNote(0, 0, 0, 1, -1),
                    TiaNote(0, 0, 0, 1, -1)
                ]
            for channelNum in range(0, 4):
                if data1[channelNum][noteNum].piaNote != -1:
                    if nums[0].piaNote == -1:
                        nums[0] = deepcopy(data1[channelNum][noteNum])
                    elif nums[1].piaNote == -1:
                        nums[1] = deepcopy(data1[channelNum][noteNum])
            data2[0].append(deepcopy(nums[0]))
            data2[1].append(deepcopy(nums[1]))

        data3 = [
            [],
            []
        ]

        for channelNum in range(0,2):
            channel = data2[channelNum]
            tempVolume = None
            tempChannel = None
            tempFreq = None

            for tiaNote in channel:

                if buzz == 1 and tiaNote.channel == 6:
                    tiaNote.channel = 7

                if (tiaNote.volume != tempVolume or
                    tiaNote.channel != tempChannel or
                    tiaNote.freq != tempFreq or data3[channelNum][-1].duration==255):

                    tempVolume = tiaNote.volume
                    tempChannel = tiaNote.channel
                    tempFreq = tiaNote.freq

                    newTiaTone = TiaNote(tiaNote.volume, tiaNote.channel, tiaNote.freq, 1, tiaNote.piaNote)
                    data3[channelNum].append(newTiaTone)
                else:
                    data3[channelNum][-1].duration+=1


        if tv == "PAL":
            for channel in data3:
                for tiaNote in channel:
                    tiaNote.duration = round(tiaNote.duration*262/314)

        deleteChannel1 = True
        for tiaNote in data3[1]:
            if tiaNote.volume > 0:
                deleteChannel1 = False
                break

        if deleteChannel1 == True:
            data3.pop(1)

        return(data3)


    def getNextNote(self, tiaNote, divider, max, min):
        from TiaNote import TiaNote
        nextNote = TiaNote(0,0,0,1,0)
        nextNote.volume = tiaNote.volume // divider
        nextNote.channel = tiaNote.channel
        nextNote.piaNote = tiaNote.piaNote
        nextNote.freq = tiaNote.freq


        """
        notes = self.__piaNotes.getTiaValue(tiaNote.piaNote, tiaNote.channel)

        if type(notes) != list:
            nextNote.freq = tiaNote.freq
        else:
            while num>len(notes)-1:
                num -= (len(notes)-1)

            nextNote.freq = int(notes[num])
        """

        if nextNote.volume<min:
            nextNote.volume = min


        if nextNote.volume>max:
            nextNote.volume = max



        if nextNote.volume>tiaNote.volume:
            nextNote.volume = tiaNote.volume - 1

        if nextNote.volume == 0:
            nextNote.volume = 1

        return(nextNote)

