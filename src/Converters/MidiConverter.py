import mido
from mido import MidiFile
import re
from MidiNote import MidiNote
from time import sleep
from copy import deepcopy
from math import sqrt

class MidiConverter:

    def __init__(self, path, loader, removeDrums, maxChannels, removeOutside, multi, cutOut):

        #This is the one the main program accesses. The process was
        #successful if it is not None.
        self.result = None
        self.songName = ""
        self.__multi = multi
        self.__removeOutside = removeOutside
        self.__loader = loader
        self.__executor = loader.executor
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

        self.__rawData = {0: "",
                           1: "",
                           2: "",
                           3: "",
                           4: "",
                           5: "",
                           6: "",
                           7: "",
                           8: "",
                           9: "",
                           10: "",
                           11: "",
                           12: "",
                           13: "",
                           14: "",
                           15: "",
                           16: ""
                           }

        self.__seperatedNotes = deepcopy(self.__channels)
        self.__channelList = deepcopy(self.__channels)
        self.__defaultTempo = 50 * 1.1 * self.__multi

        textToSend = ""
        tempo = None
        for message in self.__midiFile:
            message = str(message)
            if "MetaMessage" in message:
                if ("set_tempo" in message):
                    tempo = round(int(re.findall(r"tempo=\d+,", message)[0].replace("tempo=", "")[:-1]) / 10000) * self.__multi * 1.1
                    if self.__defaultTempo == None:
                        self.__defaultTempo = tempo

                elif "MetaMessage" in message:
                    if "track_name" in message:
                        try:
                            self.songName += re.findall(r"name=\'.+\'", message)[0].replace("name='", "")[:-1]
                        except:
                            pass

            else:
                message = message.split(" ")
                if message[0] == "note_off":
                    noteOn = "0"
                elif message[0] == "note_on":
                    noteOn = "1"
                else:
                    continue

                channel = message[1].split("=")[1]
                note = message[2].split("=")[1]

                c = int(channel)+1

                if noteOn == "0":
                    velocity = "0"
                else:
                    velocity = message[3].split("=")[1]


                time = str(float(message[4].split("=")[1])*tempo)
                #print(message[4], tempo)
                textToSend+=noteOn+" "+channel+" "+note+" "+velocity+" "+time+"\n"


        self.songName = re.sub(r'\s+', " ", self.songName)

        #import time as TIME
        #start_time = TIME.time()

        if cutOut == None:
            cutOut = []

        while len(cutOut) < 100:
           cutOut.append(0)

        strCutOut = []
        for num in cutOut:
            strCutOut.append(str(num))

        getChannelsData = self.__executor.callFortran("MidiConverter","ExtractChannels", textToSend, " ".join(strCutOut), True, True)
        for key in getChannelsData.keys():

            if len(getChannelsData[key]) > 2:
                realKey = int(key) - 1

                self.__rawData[realKey] = {
                    "seperated": "",
                    "joined": ""
                }

                for item in getChannelsData[key]:
                    raw = item.replace("\r", "").replace(".","")
                    self.__rawData[realKey]["joined"] += raw+"\n"
                    bigyok = raw.split(" ")
                    if len(bigyok) == 3:
                        bigyok[0] = int(bigyok[0])
                        bigyok[1] = int(bigyok[1])
                        bigyok[2] = int(bigyok[2])

                        tempLen = bigyok[2]
                        midiNote = MidiNote(bigyok[0], bigyok[1], 0)
                        for num in range(0, bigyok[2]):
                            tempNote = deepcopy(midiNote)
                            tempNote.duration = 1
                            self.__seperatedNotes[realKey].append(deepcopy(tempNote))
                            self.__rawData[realKey]["seperated"] += str(tempNote.returnData()[0]) \
                                                        + " " + str(tempNote.returnData()[1]) + "\n"

                            if tempLen>0:
                                while tempLen > 255:
                                    tempNote = deepcopy(midiNote)
                                    tempNote.duration = 255
                                    tempLen -= 255
                                    self.__channels[realKey].append(deepcopy(tempNote))

                                tempNote = deepcopy(midiNote)
                                tempNote.duration = tempLen
                                self.__channels[realKey].append(deepcopy(tempNote))
                                tempLen = 0


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
            self.setAttr(num)

        sorter = {}

        for num in onesToLookAt:
            sorter[num] = self.__channelAttributes[num]["priority"]

        sorter = sorted(sorter.items(), key=lambda x: x[1], reverse=True)

        #for key in sorter:
            
        #    print(key)


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

        for num in range(0, len(self.__seperatedNotes[onesToLookAt[0]])):
            self.__tempResult[1].append(deepcopy(__tiaNote))
            self.__tempResult[2].append(deepcopy(__tiaNote))
            self.__tempResult[3].append(deepcopy(__tiaNote))
            self.__tempResult[4].append(deepcopy(__tiaNote))

        if removeDrums == 0 and self.__channels[9] != []:
            setDrums = self.__executor.callFortran("MidiConverter","SetDrums", self.__rawData[9]["joined"], None, True, True)
            setDrums = setDrums.replace("\r", "").split("\n")
            num = 0

            for line in setDrums:
                if line == "":
                    continue
                line = line.split(" ")
                volume = int(line[0])
                time = int(line[2])

                if volume>0:
                    Y = int(line[1])
                    channel = int(line[3])
                    freq = int(line[4])

                    for n in range(num, time+num):
                        if (n-num)<2:
                            c = 1
                        else:
                            c = 4

                        self.__tempResult[c][n]["volume"] = volume
                        self.__tempResult[c][n]["channel"] = channel
                        self.__tempResult[c][n]["freq"] = freq
                        self.__tempResult[c][n]["Y"] = Y
                        self.__tempResult[c][n]["enabled"] = 1

                num = num+time


        if maxChannels<len(newSorter):
            newSorter = newSorter[0:maxChannels]

        from threading import Thread


        self.__threadNum = 0
        for channel in newSorter:
            getChannel = Thread(target=self.__convertChannelData, args=[channel])
            #getChannel = Process(target=self.__convertChannelData, args=[channel])
            getChannel.daemon = True
            getChannel.start()


        while self.__threadNum > 0:
            sleep(0.00001)

        while(self.__tempResult[1][0]["enabled"] == 0):
            self.__tempResult[1].pop(0)
            self.__tempResult[2].pop(0)
            self.__tempResult[3].pop(0)
            self.__tempResult[4].pop(0)

        while(self.__tempResult[1][-1]["enabled"] == 0):
            self.__tempResult[1].pop()
            self.__tempResult[2].pop()
            self.__tempResult[3].pop()
            self.__tempResult[4].pop()


        self.result = deepcopy(self.__tempResult)



        #print("--- %s seconds ---" % (TIME.time() - start_time))


    def __convertChannelData(self, c):
        self.__threadNum+=1

        for num in range(0, len(self.__seperatedNotes[c])):
            midiNote = self.__seperatedNotes[c][num]
            volume = midiNote.velocity
            if volume == 0:
                continue

            if self.__removeOutside == 1:
                if (midiNote.note<3 or midiNote.note>68 or midiNote.note in [30,31]):
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

            channelsToSort = self.__channelList[c]
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

        monoTones = {0: [0.0, 0.0, 0.0],
                    8: [0.0, 0.0, 0.0],
                    -8: [0.0, 0.0, 0.0]}

        correctNotesPercentsExecutor = self.__executor.callFortran("MidiConverter","GetCorrectNotesPercent", self.__rawData[num]["joined"], None, True, True)
        correctNotesPercentsExecutor = correctNotesPercentsExecutor.replace("\r", "").split("\n")

        __channelList = {
            0: {}, 8: {}, -8: {}
        }

        for lineNum in range(0,6,2):
            if lineNum == 0:
                key = 0
            elif lineNum == 2:
                key = 8
            else:
                key = -8

            channelData = correctNotesPercentsExecutor[lineNum].split(" ")
            channels = correctNotesPercentsExecutor[lineNum+1].split(" ")

            for cNum in range(0,10,2):
                if channels[cNum] != "" and channels[cNum] != "0":
                    __channelList[key][int(channels[cNum])] = int(channels[cNum+1])

            if channelData[0].startswith("."):
                channelData[0] = "0"+channelData[0]

            correctNotesPercents[key] = float(channelData[0])
            monoTones[key][0] = int(channelData[1])

            if channelData[2].startswith("."):
                channelData[2] = "0"+channelData[2]
            monoTones[key][1] = float(channelData[2])

            if channelData[3].startswith("."):
                channelData[3] = "0"+channelData[3]
            monoTones[key][2] = float(channelData[3])

        largest = max(correctNotesPercents, key = correctNotesPercents.get)

        if largest == 8 and (monoTones[8] > monoTones[0]):
            self.__channels[num] = self.__createClone(deepcopy(self.__channels[num]), 8)
        elif largest == -8 and (monoTones[-8] > monoTones[0]):
            self.__channels[num] = self.__createClone(deepcopy(self.__channels[num]), -8)

        self.__channelList[num] = __channelList[largest]

        self.__channelAttributes[num]["dominantTiaChannel"] = monoTones[largest][0]
        self.__channelAttributes[num]["monotony"] = monoTones[largest][1]
        self.__channelAttributes[num]["variety"] = monoTones[largest][2]

        self.__channelAttributes[num]["correctNotePercent"] = correctNotesPercents[largest] * 100
        #self.__channelAttributes[num]["dominantTiaChannel"] = self.__getDominantChannel(self.__channels[num])
        self.__channelAttributes[num]["priority"] *= (((100-self.__channelAttributes[num]["correctNotePercent"])/2+self.__channelAttributes[num]["correctNotePercent"])/100
                                                      * self.__channelAttributes[num]["monotony"] * self.__channelAttributes[num]["variety"])

        self.__threadNum -= 1


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



