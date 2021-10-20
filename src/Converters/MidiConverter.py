import mido
from mido import MidiFile
import re
from MidiNote import MidiNote
from time import sleep
from copy import deepcopy
from math import sqrt

class MidiConverter:

    def __init__(self, path, loader):

        #This is the one the main program accesses. The process was
        #successful if it is not None.
        self.result = None
        self.songName = ""

        self.__piaNotes = loader.piaNotes

        self.__midiFile = MidiFile(path)

        self.__threadNum = 0
        self.__channels = {0: [],
                           1: [],
                           2: [],
                           3: [],
                           4: [],
                           5: [],
                           6: [],
                           7: [],
                           8: [],
                           9: [],
                           10: [],
                           11: [],
                           12: [],
                           13: [],
                           14: [],
                           15: [],
                           16: []
                           }

        self.__seperatedNotes = deepcopy(self.__channels)

        from threading import Thread

        titleGetter = Thread(target=self.getTitle)
        titleGetter.daemon=True
        titleGetter.start()

        for num in self.__channels.keys():
            getChannel = Thread(target=self.getChannelData, args=[num])
            getChannel.daemon = True
            getChannel.start()

        while self.__threadNum > 0:
            sleep(0.00001)

        """
        for midiNote in self.__channels[9]:
            if midiNote.note!=0:
                print(midiNote.note)
        """

        self.equalLen()

        onesToLookAt = []

        for num in range(0,len(self.__channels)):
            if len(self.__channels[num]) > 1 and num!=9:
                onesToLookAt.append(num)


        __channelAttributes = {
            "priority": 0,
            "numberOfNotes": 0,
            "totalLenOfNotes": 0,
            "dominantTiaChannel": 0,
            "correctNotePercent": 0,
            "monotony": 0,
            "variety": 0
        }

        self.__channelAttributes = {}
        for num in onesToLookAt:
            self.__channelAttributes[num] = deepcopy(__channelAttributes)
            setAttr = Thread(target=self.setAttr, args=[num])
            setAttr.daemon = True
            setAttr.start()


        while self.__threadNum > 0:
            sleep(0.00001)

        #print(self.__channelAttributes)
        #for num in onesToLookAt:
        #    print(self.__channelAttributes[num])

        sorter = {}

        for num in onesToLookAt:
            sorter[num] = self.__channelAttributes[num]["priority"]

        sorter = sorted(sorter.items(), key=lambda x: x[1], reverse=True)
        newSorter = []
        for item in sorter:
            newSorter.append(item[0])

        self.__tempResult = {1: [],
                             2: [],
                             3: [],
                             4: []}

        __tiaNote = {
            "volume": 0,
            "channel": 0,
            "freq": 0,
            "enabled": 0,
            "Y": 0
        }
        """
        for channel in self.__seperatedNotes:
            print(str(channel)+"\n"+"-----")
            for midiNote in self.__seperatedNotes[channel]:
                if midiNote.note!=0:
                    print(midiNote.note)
        """

        for num in range(0, len(self.__seperatedNotes[onesToLookAt[0]])):
            self.__tempResult[1].append(deepcopy(__tiaNote))
            self.__tempResult[2].append(deepcopy(__tiaNote))
            self.__tempResult[3].append(deepcopy(__tiaNote))
            self.__tempResult[4].append(deepcopy(__tiaNote))

        self.__createDrums()

        self.__threadNum = 0
        for channel in newSorter:
            getChannel = Thread(target=self.__convertChannelData, args=[channel])
            getChannel.daemon = True
            getChannel.start()

        while self.__threadNum > 0:
            sleep(0.00001)

        while(self.__tempResult[1][0]["enabled"] == 0):
            self.__tempResult[1].pop(0)
            self.__tempResult[2].pop(0)
            self.__tempResult[3].pop(0)
            self.__tempResult[4].pop(0)



        self.result = deepcopy(self.__tempResult)

        """
        for channel in self.result:
            print(str(channel)+"\n------")
            for note in self.result[channel]:
                print(note["Y"], note["enabled"])
        """

    def __convertChannelData(self, c):
        self.__threadNum+=1

        for num in range(0, len(self.__seperatedNotes[c])):
            midiNote = self.__seperatedNotes[c][num]
            if midiNote.note<32:
                volume = midiNote.velocity//24
            else:
                volume = midiNote.velocity//12
            if volume == 0:
                continue

            saveNum = None
            for channelNum in range(1,5):
                if self.__tempResult[channelNum][num]["enabled"] == 0:
                    saveNum = channelNum
                    break

            if saveNum == None:
                continue

            self.__tempResult[saveNum][num]["volume"] = volume
            self.__tempResult[saveNum][num]["Y"] = midiNote.note
            self.__tempResult[saveNum][num]["enabled"] = 1

            filler1, filler2, channelsToSort, filler3 = self.__getMonotones(self.__channels[c])
            channelsToSort = sorted(channelsToSort.items(), key=lambda x: x[1], reverse=True)

            for item in channelsToSort:
                data = self.__piaNotes.getTiaValue(midiNote.note, item[0])
                if data != None:
                    self.__tempResult[saveNum][num]["channel"] = item[0]
                    if type(data) != list:
                        self.__tempResult[saveNum][num]["freq"] = int(data)
                    else:
                        temp = 0
                        for item in data:
                            temp+=int(item)

                        self.__tempResult[saveNum][num]["freq"] = temp//len(data)
                    break

        self.__threadNum-=1



    def __createDrums(self):
        #"15,20" 89 (drum), "8,0" 90 (hi-hat), "15,2" 91(hi-hat),
        #"8,8" 92 (snare), "2,0" 93(horn), "3,0" 94(buzz), "3,1" 95(buzz)

        drumsDict = {
            89: [35, 36, 41, 43, 45, 47, 48, 50, 64, 65, 66, 78, 79],
            90: [42, 44, 51, 73, 76],
            91: [46, 52, 55, 74, 77],
            92: [38, 54, 56, 57, 69, 70, 75],
            93: [37, 53, 59],
            94: [39, 48, 57, 60, 62, 67, 71, 80],
            95: [40, 49, 61, 63, 68, 72, 81]
        }

        channelCodes = {89: (15, 20),
                        90: (8, 0),
                        91: (15, 2),
                        92: (8, 8),
                        93: (2, 0),
                        94: (3, 0),
                        95: (3, 1)
                        }

        counter = 0
        last = -1
        for num in range(0, len(self.__seperatedNotes[9])):
            midiNote = self.__seperatedNotes[9][num]
            if midiNote.note != 0:
                Y = self.__getDrumY(midiNote.note, drumsDict)
                velocity = midiNote.velocity//24
                if velocity == 0:
                    last = 0
                    continue

                if last == Y:
                    counter+=1
                else:
                    counter=0
                last = Y

                if counter<2:
                    saveNum = 1
                else:
                    saveNum = 4

                self.__tempResult[saveNum][num]["volume"] = velocity
                self.__tempResult[saveNum][num]["Y"] = Y
                self.__tempResult[saveNum][num]["freq"] = channelCodes[Y][1]
                self.__tempResult[saveNum][num]["channel"] = channelCodes[Y][0]
                self.__tempResult[saveNum][num]["enabled"] = 1

            else:
                counter = 0

    def __getDrumY(self, note, drumsDict):
        for drumKey in drumsDict:
            for n in drumsDict[drumKey]:
                if n == note+20:
                    return(drumKey)

    def equalLen(self):
        lens = []
        M = 0

        for channel in range(0,16):
            FFF = 0
            for item in self.__channels[channel]:
                FFF+=item.duration

            lens.append(FFF)

            if FFF > M:
                M = FFF

        for channel in range(0, 16):
            if lens[channel] < M:
                self.__channels[channel].append(MidiNote(0,0,M-lens[channel]))
                for num in range(0, M-lens[channel]):
                    self.__seperatedNotes[channel].append(MidiNote(0,0,1))

    def setAttr(self, num):
        self.__threadNum+=1

        for item in self.__channels[num]:
            if item.velocity>0:
                self.__channelAttributes[num]["totalLenOfNotes"]+=item.duration
                self.__channelAttributes[num]["numberOfNotes"]+=1

        self.__channelAttributes[num]["priority"] = (
            sqrt(self.__channelAttributes[num]["totalLenOfNotes"]) * self.__channelAttributes[num]["numberOfNotes"])

        correctNotesPercents = {0: 0.0,
                                8: 0.0,
                                -8: 0.0}

        clonePlus8 = self.__createClone(deepcopy(self.__channels[num]), 8)
        cloneMinus8 = self.__createClone(deepcopy(self.__channels[num]), -8)

        correctNotesPercents[0] = self.__getPercentOfCorrectNotes(self.__channels[num])
        correctNotesPercents[8] = self.__getPercentOfCorrectNotes(clonePlus8)
        correctNotesPercents[-8] = self.__getPercentOfCorrectNotes(cloneMinus8)

        monoTones = {0: [0.0, 0.0, 0.0],
                    8: [0.0, 0.0, 0.0],
                    -8: [0.0, 0.0, 0.0]}

        monoTones[0][0], monoTones[0][1], filler, monoTones[0][2] = self.__getMonotones(self.__channels[num])
        monoTones[8][0], monoTones[8][1], filler, monoTones[8][2] = self.__getMonotones(clonePlus8)
        monoTones[-8][0], monoTones[-8][1], filler, monoTones[-8][2] = self.__getMonotones(cloneMinus8)

        largest = max(correctNotesPercents, key = correctNotesPercents.get)

        if largest == 8 and (monoTones[8] > monoTones[0]):
            self.__channels[num] = clonePlus8
        elif largest == -8 and (monoTones[-8] > monoTones[0]):
            self.__channels[num] = cloneMinus8

        self.__channelAttributes[num]["dominantTiaChannel"] = monoTones[largest][0]
        self.__channelAttributes[num]["monotony"] = monoTones[largest][1]
        self.__channelAttributes[num]["variety"] = monoTones[largest][2]

        self.__channelAttributes[num]["correctNotePercent"] = correctNotesPercents[largest] * 100
        #self.__channelAttributes[num]["dominantTiaChannel"] = self.__getDominantChannel(self.__channels[num])
        self.__channelAttributes[num]["priority"] *= (((100-self.__channelAttributes[num]["correctNotePercent"])/2+self.__channelAttributes[num]["correctNotePercent"])/100
                                                      * self.__channelAttributes[num]["monotony"] * self.__channelAttributes[num]["variety"])

        self.__threadNum -= 1

    def __getMonotones(self, source):
        channels = {}
        notes = []

        for item in source:
            if item.note>0:
                note = self.__piaNotes.getTiaValue(item.note, None)
                notes.append(item.note)
                #print(item.note)

                for n in note:
                    if n not in channels.keys():
                        channels[n] = 0
                    channels[n]+=1
        maxi = max(channels, key=channels.get)
        mono = int(maxi) / len(source)

        variety = len(set(notes)) / len(source)

        return(maxi, mono, channels, variety)
    """
    def __getDominantChannel(self, source):
        channels = {}
        for item in source:
            if item.note>0:
                note = self.__piaNotes.getTiaValue(item.note, None)
                for n in note:
                    if n not in channels.keys():
                        channels[n] = 0
                    channels[n]+=1
        return(max(channels, key=channels.get))
    """


    def __getPercentOfCorrectNotes(self, source):
        good = 0
        all = 0
        for item in source:
            #if len(self.__piaNotes.getTiaValue(item.note), None)>1:
            if item.note>0:
                all+=1
                data = self.__piaNotes.getTiaValue(item.note, None)
                if data != None:
                    firstKey = list(data.keys())[0]
                    if type(data[firstKey])!=list:
                        good+=1

        if all == 0:
            return(0.0)
        else:
            return(good/all)


    def __createClone(self, source, add):
        for item in source:
            if item.note!=0:
                item.note+=add
        return(source)

    def __testPrint(self):
        for channel in self.__channels:
            print(str(channel)+"\n"+"---------"+"\n")
            for item in self.__channels[channel]:
                print(item.velocity, item.note, item.duration)
            print("\n")

    def getTitle(self):
        self.__threadNum+=1

        for track in self.__midiFile.tracks:
            for message in track:
                message = str(message)
                if "MetaMessage" in message:
                    if "track_name" in message:
                        self.songName += re.findall(r"name=\'.+\'", message)[0].replace("name='", "")[:-1]
        self.songName = re.sub(r'\s+', " ", self.songName)

        self.__threadNum-=1

    def getChannelData(self, channelNum):
        self.__threadNum+=1
        tempo = 50
        duration = 0
        remainder = 0

        self.__channels[channelNum] = [MidiNote(0, 0, 0)]

        for message in self.__midiFile:
            message = str(message)
            if "MetaMessage" in message:
                if "set_tempo" in message:
                    tempo = round(int(re.findall(r"tempo=\d+,", message)[0].replace("tempo=", "")[:-1]) / 10000)
            else:
                if "channel=" in message:
                    d = {}
                    for item in message.split(" "):
                        if "=" in item:
                            item = item.split("=")
                            if "." in item[1]:
                                d[item[0]] = float(item[1])
                            else:
                                d[item[0]] = int(item[1])
                        else:
                            if item == "note_off":
                                d["Note_On"] = False
                            elif item == "note_on":
                                d["Note_On"] = True

                    duration += d["time"]
                    if d["channel"] != channelNum or ("Note_On" not in d.keys()):
                        continue
                    else:

                        d["note"]-=20
                        if d["Note_On"] == True:
                            self.__channels[channelNum].append(MidiNote(d["velocity"], d["note"], 0))
                        else:
                            self.__channels[channelNum].append(MidiNote(0, 0, 0))

                        tempoDuration = (duration * tempo) + remainder
                        remainder = tempoDuration - int(tempoDuration)
                        duration = 0
                        self.__channels[channelNum][-2].duration = int(tempoDuration)
                        for xyz in range(0, int(tempoDuration)):
                            self.__seperatedNotes[channelNum].append(MidiNote(self.__channels[channelNum][-2].velocity,
                                                                              self.__channels[channelNum][-2].note,
                                                                              1))
        #Remove the ones with 0 duration.
        __temp = []
        for item in self.__channels[channelNum]:
            if item.duration>0:
                if item.velocity == 0:
                    item.note = 0
                elif item.note == 0:
                    item.velocity = 0
                __temp.append(deepcopy(item))
        self.__channels[channelNum] = deepcopy(__temp)

        self.__threadNum-=1



