#Using VMG modules of https://github.com/cdodd/vgmparse

from copy import deepcopy

class VGMConverter:

    def __init__(self, loader, path, removePercuss, maxChannels, removeOutside, cutOut):

        self.__loader = loader
        self.__piaNotes = loader.piaNotes
        from threading import Thread
        import os

        txt  = ".".join(path.split(".")[:-1])+".txt"
        txt2 = "/".join(txt.split("/")[:-1])+"/renamed.txt"
        try:
            os.remove(txt)
        except:
            pass

        try:
            os.remove(txt2)
        except:
            pass

        t = Thread(target=self.vgm2textThread, args=[path])
        t.daemon = True
        t.start()

        from time import sleep
        counter = 0

        while True:
            if counter == 500:
                break

            if os.path.exists(txt):
                try:
                    os.rename(txt, txt2)
                    break
                except:
                    pass
            else:
                counter+=1
            sleep(0.01)

        self.__loader.executor.killByForce("vgm2txt")

        file = open(txt2, "r")
        data = file.read().replace("\r","").split("VGMData:")
        file.close()

        os.remove(txt2)

        from VGMDataItem import VGMDataItem

        data[0] = data[0].replace("NES APU", "NES_APU").replace("GB DMG", "GB_DMG")

        headerData = data[0].split("\n")[1:]
        processData = data[1].split("\n")

        self.__vgmHeader = {}
        self.__vgmData = []

        self.__unused = []
        self.__used = []

        self.__GD3offset = None

        for line in headerData:
            line = line.replace("\t", " ").split(" ")
            newLine = []
            for item in line:
                if item != "":
                    newLine.append(item)

            line = newLine
            if line!=[]:
                if "Version:" in line:
                    self.__vgmHeader["version"] = float(line[-1][1:-1])
                if line[0] in self.__unused:
                    continue

                if "GD3" in line:
                    self.__GD3offset = int(line[3], 16)

                if line[-1] == "unused":
                    self.__unused.append(line[0])
                    continue

                if "Rate:" in line:
                    self.__vgmHeader["rate"] = float(line[-2])

                if line[1] == "Clock:":
                    self.__vgmHeader[line[0]] = {}
                    self.__vgmHeader[line[0]]["clock"] = int(line[2])
                    self.__used.append(line[0])

                if line[0] in self.__used and line[1] != "Clock:":
                    if line[2] == "Flags:":
                        self.__vgmHeader[line[0]][line[1].lower()+"_flags"] = int(line[3], 16)
                    else:
                        self.__vgmHeader[line[0]][line[1].lower().replace(":","")] = int(line[2],16)

                if line[0] == "Volume":
                    self.__vgmHeader["volume"] = float(line[-1])

        self.__noteNum = 0

        for line in processData:
            if line != "":
                self.__vgmData.append(VGMDataItem(line))
                if "Key On" in line:
                    self.__noteNum+=1

        #print(self.__vgmHeader)
        #for item in self.__vgmData:
        #    print(item.command, item.dataBytes, item.dataByteStrings, item.extraData)

        # OPL2 is fully compatible with OPL, OPL3 is handled as OPL2

        vibr = self.__loader.fileDialogs.askYesOrNo("vibratioSettings", "vibratioSettingsMessage")
        if vibr == "Yes":
            vibrSets = False
        else:
            vibrSets = True

        if (("YM3812" in self.__used) or ("YM3526" in self.__used) or
            ("YMF262" in self.__used) or ("YMF262A" in self.__used)
            or ("YMF262B" in self.__used)):
            #self.__oplData = self.callVGMExtractor("YM3812", ["OPL2"], ("5A", "5B", "5E", "5F"))
            if cutOut == None:
               cutOut = []
            self.__oplData = self.emulateYM3812(removeOutside, removePercuss, cutOut, vibrSets)

        NTSC_frameRate  = 29.97 # /seconds
        constant = NTSC_frameRate / 500

        self.__dataChannels = {}

        for channel in range(0,9):
            if ((self.__oplData.channels[channel].slots[0].hasNote == True or
               self.__oplData.channels[channel].slots[1].hasNote == True) and
               channel not in self.__dataChannels.keys()):
                    self.__dataChannels[channel] = {}

            for slot in range(0,2):
                if (self.__oplData.channels[channel].slots[1-slot].hasNote
                    and slot not in self.__dataChannels[channel].keys()):
                    self.__dataChannels[channel][slot] = []

                if (self.__oplData.channels[channel].slots[1-slot].hasNote):
                    for item in self.__oplData.channels[channel].channelData[slot]:
                        if len(self.__dataChannels[channel][slot]) == 0:
                            self.__dataChannels[channel][slot].append(
                                {
                                    "volume": item[0],
                                    "note":   item[1],
                                    "duration": 1
                                }
                            )
                        elif (self.__dataChannels[channel][slot][-1]["volume"] != item[0] or
                              self.__dataChannels[channel][slot][-1]["note"]   != item[1] ):
                              self.__dataChannels[channel][slot].append(
                                {
                                    "volume": item[0],
                                    "note":   item[1],
                                    "duration": 1
                                }
                              )
                        else:
                              self.__dataChannels[channel][slot][-1]["duration"] += 1

        remainder = 0

        sums = {}
        largest = 0

        for channel in self.__dataChannels.keys():
            if channel not in sums.keys():
               sums[channel] = {}

            for slot in self.__dataChannels[channel].keys():
                if slot not in sums[channel].keys():
                    sums[channel][slot] = 0

                for item in self.__dataChannels[channel][slot]:

                    temp = (item["duration"] * constant)+remainder
                    item["duration"] = int(temp)

                    remainder = temp - item["duration"]
                    sums[channel][slot] += item["duration"]
                if sums[channel][slot] > largest: largest = sums[channel][slot]

        for channel in self.__dataChannels.keys():
            for slot in self.__dataChannels[channel].keys():
                if sums[channel][slot] < largest:
                    self.__dataChannels[channel][slot].append(
                        {"volume"  : 0,
                         "note"    : 0,
                         "duration": largest - sums[channel][slot]
                         })

        self.__channelAttr = {
            "numberOfNotes": 0,
            "dominantTiaChannel": 0,
            "correctNotes": 0,
            "variety": 0,
            "monotony": 0,
            "priority": 0

        }

        self.__channelAttributes = {}

        for channel in self.__dataChannels.keys():
            if self.__oplData.rythmMode == True and channel > 5:
                break
            self.__channelAttributes[channel] = deepcopy(self.__channelAttr)
            self.__getChannelAttr(channel)

        __tiaNote = {
            "volume": 0,
            "channel": 0,
            "freq": 0,
            "enabled": 0,
            "Y": 0
        }

        self.__tempResult = {1: [],
                             2: [],
                             3: [],
                             4: []}

        ch = 0

        self.__drumNotes = []

        while True:
            try:
                for note in self.__dataChannels[ch][0]:
                    for num in range(0,note["duration"]):
                        self.__tempResult[1].append(deepcopy(__tiaNote))
                        self.__tempResult[2].append(deepcopy(__tiaNote))
                        self.__tempResult[3].append(deepcopy(__tiaNote))
                        self.__tempResult[4].append(deepcopy(__tiaNote))
                        self.__drumNotes.append(deepcopy(__tiaNote))
                break
            except:
                ch += 1
                if ch == 18:
                    break

        forSort = {}

        if self.__oplData.rythmMode == True and removePercuss == False:
           for channel in self.__dataChannels.keys():
               if channel < 6:
                   continue
               for slot in self.__dataChannels[channel]:
                   currentPoz = 0
                   for note in self.__dataChannels[channel][slot]:

                       if note["note"] > 88 and note["note"] < 96:
                          for counter in range(0, note["duration"]):

                              if counter > 6:
                                  break

                              if counter < 2:
                                 cPoz = 1
                              else:
                                 cPoz = 4

                              savePoz = currentPoz + counter

                              if self.__drumNotes[savePoz]["enabled"]  == 0:
                                  self.__drumNotes[savePoz]["enabled"]  = 1
                                  self.__drumNotes[savePoz]["volume"]   = note["volume"]
                                  self.__drumNotes[savePoz]["note"]     = note["note"]
                                  self.__drumNotes[savePoz]["Y"]        = note["note"]
                                  self.__drumNotes[savePoz]["cPoz"]     = cPoz

                                  drums = self.__piaNotes.getTiaValue(note["note"],  None)
                                  self.__drumNotes[savePoz]["channel"]  = drums[0]
                                  self.__drumNotes[savePoz]["freq"]     = drums[1]

                       currentPoz += note["duration"]

        for key in self.__channelAttributes.keys():
            forSort[key] = self.__channelAttributes[key]["priority"]

        f = sorted(forSort.items(), key=lambda x: x[1], reverse=True)

#        for note in self.__drumNotes:
#            print(note)

        from ChangeDrumsAndOrder import ChangeDrumsAndOrder

        changeDrumsAndOrder = ChangeDrumsAndOrder(self.__loader, self.__loader.mainWindow,
                                                      self.__channelAttributes, f,
                                                      self.__drumNotes, removePercuss, "vgm"
                                                      )


        if self.__oplData.rythmMode == True and removePercuss == False:
            for noteNum in range(0, len(self.__drumNotes)):

                if self.__drumNotes[noteNum]["enabled"] == 1:
                    cPoz = self.__drumNotes[noteNum]["cPoz"]
                    self.__tempResult[cPoz][noteNum]["enabled"]  = 1
                    self.__tempResult[cPoz][noteNum]["volume"]   = self.__drumNotes[noteNum]["volume"]
                    self.__tempResult[cPoz][noteNum]["note"]     = self.__drumNotes[noteNum]["note"]
                    self.__tempResult[cPoz][noteNum]["Y"]        = self.__drumNotes[noteNum]["Y"]
                    self.__tempResult[cPoz][noteNum]["channel"]  = self.__drumNotes[noteNum]["channel"]
                    self.__tempResult[cPoz][noteNum]["freq"]     = self.__drumNotes[noteNum]["freq"]

        am = self.__loader.fileDialogs.askYesOrNo("amModulation", "amDisable")
        if am == "Yes":
            slotChange = False
        else:
            slotChange = True


        for item in f:
            currentPoz = 0
            if len(self.__dataChannels[item[0]].keys()) > 1:
                slot    = 1
                counter = 0
                fetched = [[],[]]
                for slot in range(0,2):
                    for note in self.__dataChannels[item[0]][slot]:
                        if note["duration"] > 0:
                            newNote = deepcopy(__tiaNote)
                            if note["volume"] > 0:
                                newNote["enabled"] = 1
                                newNote["volume"] = note["volume"]
                                newNote["note"] = note["note"]
                                newNote["Y"] = note["note"]
                                (newNote["channel"],
                                 newNote["freq"]) = self.__getChannelNote(note["note"],
                                                    self.__channelAttributes[item[0]]["dominantTiaChannel"])
                            for d in range(0, note["duration"]):
                               fetched[slot].append(deepcopy(newNote))
                #print(len(self.__dataChannels[item[0]][0]), len(self.__dataChannels[item[0]][1]), len(fetched[0]), len(fetched[1]))

                for noteNum in range(0, largest):
                    if slotChange == True:
                        if counter > 1:
                           slot    = 1 - slot
                           counter = 0
                        else:
                           counter += 1
                    if fetched[0][noteNum]["enabled"] == 1 and fetched[1][noteNum]["enabled"] == 1:
                        if slotChange == True:
                            realSlot = slot
                        else:
                            realSlot = 0
                    elif fetched[0][noteNum]["enabled"] == 1:
                        realSlot = 0
                    elif fetched[1][noteNum]["enabled"] == 1:
                        realSlot = 1
                    else:
                        continue

                    note = fetched[realSlot][noteNum]
                    if (note["enabled"] == 0 or note["note"] in cutOut or
                    (removeOutside == True and (note["note"] in [30, 31 ]) or note["note"] > 68 or note["note"] < 3)):
                        note = fetched[1 - realSlot][noteNum]

                    for num in range(1, 5):
                        if self.__tempResult[num][noteNum]["enabled"]   == 0:
                            self.__tempResult[num][noteNum]["enabled"]  = 1
                            self.__tempResult[num][noteNum]["volume"]   = note["volume"]

                            try:
                                self.__tempResult[num][noteNum]["note"] = note["note"]
                                self.__tempResult[num][noteNum]["Y"]    = note["note"]

                            except:
                                self.__tempResult[num][noteNum]["note"] = note["Y"]
                                self.__tempResult[num][noteNum]["Y"]    = note["Y"]

                            self.__tempResult[num][noteNum]["channel"]  = note["channel"]
                            self.__tempResult[num][noteNum]["freq"]     = note["freq"]
                            break

            else:
                key = list(self.__dataChannels[item[0]].keys())[0]
                for note in self.__dataChannels[item[0]][key]:
                    for poz in range(currentPoz, currentPoz+note["duration"]):
                        for num in range(1,5):
                            if self.__tempResult[num][poz]["enabled"]    == 0 and note["volume"] > 0:
                                self.__tempResult[num][poz]["enabled"]   = 1
                                self.__tempResult[num][poz]["volume"]    = note["volume"]

                                try:
                                    self.__tempResult[num][poz]["note"]  = note["note"]
                                    self.__tempResult[num][poz]["Y"]     = note["note"]
                                except:
                                    self.__tempResult[num][poz]["note"]  = note["Y"]
                                    self.__tempResult[num][poz]["Y"]     = note["Y"]


                                (self.__tempResult[num][poz]["channel"],
                                 self.__tempResult[num][poz]["freq"])    = self.__getChannelNote(note["note"],
                                                                           self.__channelAttributes[item[0]]["dominantTiaChannel"])
                                break
                    currentPoz += note["duration"]


        self.result = self.__tempResult

        self.artistName = ""
        self.songName = ""
        if self.__GD3offset != None:
            self.artistName, self.songName = self.__getSongMetaData(path, self.__GD3offset, False)
            if self.artistName == "" or self.songName == "":
                self.artistName, self.songName = self.__getSongMetaData(path, self.__GD3offset, True)

        #for key in self.result:
        #    print(self.result[key])

        #print("--- %s seconds ---" % (time.time() - start_time))

    def __openVGM(self, path, force):
        import gzip
        from io import BytesIO as ByteBuffer

        file = open(path, "rb")
        data = file.read()
        file.close()

        extension = path.split(".")[-1]

        if extension == "vgz" or force == True:
            data = gzip.GzipFile(fileobj=ByteBuffer(data), mode='rb')
            data = data.read()
        return data


    def __getSongMetaData(self, path, offset, force):

        artistName = ""
        songData   = ""

        data = self.__openVGM(path, force)
        data = data[offset:]

        try:
            if (self.__getAscii(data[0])+self.__getAscii(data[1])+self.__getAscii(data[2])) != "Gd3":
                return (artistName, songData)
        except:
            return (artistName, songData)

        version = self.__getAscii(data[3]) + self.__getAscii(data[4]) + self.__getAscii(data[5]) + self.__getAscii(data[6])
        #should be 00010000

        lenght = int("0x"+(hex(data[10])+hex(data[9])+hex(data[8])+hex(data[7])).replace("0x", ""), 16)
        #data = data[:lenght]

        meta = {
            "title": ["", ""],
            "game": ["", ""],
            "system": ["", ""],
            "artist": ["", ""]
        }

        index = 0
        lang = 0
        tempString = ""

        for num in range(12, lenght, 2):

            h1 = hex(data[num+1]).replace("0x", "")
            if len(h1) == 1:
               h1 = "0" + h1
            h2 = hex(data[num]).replace("0x", "")
            if len(h2) == 1:
               h2 = "0" + h2

            hexa = "0x"+h1+h2
            #print(hexa)
            if hexa == "0x0000":
               key = list(meta.keys())[index]
               meta[key][lang] = tempString

               tempString = ""
               if lang == 1:
                  index+=1
                  lang = 0
               else:
                  lang += 1
               if index > 3:
                  break
            else:
                tempString += chr(int(hexa, 16))

            if meta["artist"][0] != "":
                artistName = meta["artist"][0]
            else:
                artistName = meta["artist"][1]

            if meta["title"][0] != "":
                songData = meta["title"][0]
            else:
                songData = meta["title"][1]

            bonusInfo = []

            if meta["game"][0] != "":
                bonusInfo.append(meta["game"][0])
            elif meta["game"][1] != "":
                bonusInfo.append(meta["game"][1])

            if meta["system"][0] != "":
                bonusInfo.append(meta["system"][0])
            elif meta["system"][1] != "":
                bonusInfo.append(meta["system"][1])

            if bonusInfo == []:
                pass
            elif len(bonusInfo) == 1:
               songData += " (" + bonusInfo[0] + ")"
            else:
               songData += " (" + " :: ".join(bonusInfo) + ")"

        return(artistName, songData)

    def __getAscii(self, hex):
        return(chr(hex))

    def __getChannelNote(self, input, dominant):
        notes = self.__loader.piaNotes.getTiaValue(input, dominant)

        if notes != None:
           if type(notes) == list:
               szum = 0
               for num in notes:
                   szum += int(num)
               note = szum // len(notes)
           else:
               note = int(notes)

           channel = int(dominant)
        else:
            if input > 88:
               return(0,0)
            notes = self.__loader.piaNotes.getTiaValue(input, None)
            if notes != None:
                key = list(notes.keys())[0]
                if type(notes[key]) == list:
                    szum = 0
                    for num in notes[key]:
                        szum += int(num)
                    note = szum // len(notes[key])
                else:
                    note = int(notes[key])


                channel = int(key)
            else:
                #print(input)
                channel = 0
                note    = 0

        return (channel, note)


    def __getChannelAttr(self, channel):
        channelCount = {
            1: 0, 4: 0, 6: 0, 12: 0, 14: 0
        }
        noteCount = {}

        for num in range(1, 96):
            noteCount[num] = 0

        one = {
            "channelCount": deepcopy(channelCount),
            "correctNotes": 0,
            "noteCount": deepcopy(noteCount),
            "variety": 0,
            "monotony": 0,
            "numberOfNotes": 0,
            "priority": 0,
            "dominantTiaChannel": 0,
            "bonus": 0
        }

        allThree = []
        for n in range(0,3):
            allThree.append(deepcopy(one))

        for slot in self.__dataChannels[channel].keys():
            for pair in [[0,0], [1,8], [2,-8]]:
                for note in self.__dataChannels[channel][slot]:
                    self.__calculateChannelAttr(note, pair[0], pair[1], allThree, channel)

                allThree[pair[0]]["correctNotes"] = allThree[pair[0]]["correctNotes"] / allThree[pair[0]]["numberOfNotes"]

                temp = 0
                largest = 0
                largestKey = 0
                for key in allThree[pair[0]]["channelCount"].keys():
                    if allThree[pair[0]]["channelCount"][key] > largest:
                       largest    =  allThree[pair[0]]["channelCount"][key]
                       largestKey =  key

                try:
                    allThree[pair[0]]["monotony"]           = largest / allThree[pair[0]]["numberOfNotes"]
                except:
                    allThree[pair[0]]["monotony"]           = 0

                allThree[pair[0]]["dominantTiaChannel"] = largestKey

                for key in allThree[pair[0]]["channelCount"].keys():
                    if allThree[pair[0]]["channelCount"][key] > 0:
                        allThree[pair[0]]["variety"] += 1

                allThree[pair[0]]["variety"]  = allThree[pair[0]]["variety"] / 95
                allThree[pair[0]]["bonus"]    = allThree[pair[0]]["bonus"] / allThree[pair[0]]["numberOfNotes"]
                allThree[pair[0]]["priority"] = ((allThree[pair[0]]["variety"]*2) + \
                                                (allThree[pair[0]]["monotony"]*1.5)+\
                                                (allThree[pair[0]]["correctNotes"]*2.5))+\
                                                 allThree[pair[0]]["bonus"]



        #for item in allThree:
        #    print(item)

        if (allThree[0]["priority"] > allThree[1]["priority"]) and (allThree[0]["priority"] > allThree[2]["priority"]):
           add = 0
           self.__setMainData(channel, 0, allThree)

        elif (allThree[1]["priority"] > allThree[2]["priority"]):
           add = 8
           self.__setMainData(channel, 1, allThree)

        else:
           add = -8
           self.__setMainData(channel, 2, allThree)

        for slot in self.__dataChannels[channel].keys():
            for note in self.__dataChannels[channel][slot]:
                if note["note"] != 0:
                    note["note"] += add



    def __setMainData(self, channel, num, allThree):
        self.__channelAttributes[channel]["numberOfNotes"]      = allThree[num]["numberOfNotes"]
        self.__channelAttributes[channel]["variety"]            = allThree[num]["variety"]
        self.__channelAttributes[channel]["monotony"]           = allThree[num]["monotony"]
        self.__channelAttributes[channel]["priority"]            = allThree[num]["priority"]
        self.__channelAttributes[channel]["numberOfNotes"]      = allThree[num]["numberOfNotes"]
        self.__channelAttributes[channel]["dominantTiaChannel"] = allThree[num]["dominantTiaChannel"]
        self.__channelAttributes[channel]["correctNotes"]       = allThree[num]["correctNotes"]


    def __calculateChannelAttr(self, note, place, add, allThree, channel):
        tiaNotes = self.__piaNotes.getTiaValue(note["note"]+add, None)

        if note["note"] < 52 and note["note"] > 16:
            allThree[place]["bonus"]+=1

        if note["note"]+add > 88 or note["note"]+add < 1:
           tiaNotes = None

        if tiaNotes != None:

            for channelKey in tiaNotes:
                allThree[place]["channelCount"][int(channelKey)] += 1

            if type(tiaNotes[list(tiaNotes.keys())[0]]) == str:
                allThree[place]["correctNotes"] += 1

            allThree[place]["numberOfNotes"] += 1
            allThree[place]["noteCount"][note["note"]+add] += 1

    def emulateYM3812(self, removeOutside, removePercuss, cutOut, vibrSets):
        from YM3812 import YM3812

        bytes = []
        for item in self.__vgmData:
            if item.dataByteStrings != [] and item.dataByteStrings[0] in ("5A", "5B", "5E", "5F", "61", "62", "63"):
                bytes.append(item.dataByteStrings)

        ym3812Data = YM3812(self.__loader, bytes, removeOutside, removePercuss, cutOut, vibrSets)
        return ym3812Data.stream

    """
    def callVGMExtractor(self, program, extraData, codeBytes):
        bytes = ""
        for item in self.__vgmData:
            if item.dataByteStrings[0] in codeBytes or item.dataByteStrings[0] == "61":
                bytes += " ".join(item.dataByteStrings) + "\n"

        data = self.__loader.executor.callFortran("VGMConverter",
                                                program, bytes,
                                                str(self.__vgmHeader["volume"]) + " " + str(
                                                self.__vgmHeader["rate"]) + " " + str(self.__noteNum) + " "+"|".join(extraData),
                                                True, True)
        return(data)

    """
    def vgm2textThread(self, path):
        self.__loader.executor.execute("vgm2txt", ['"'+path+'"', '"'+"0"+'"', '"'+"0"+'"'], True)
