

class AttackDecayTable:
    def __init__(self):
        try:
            file = open("config/attack_decay.txt", "r")
        except:
            #Just testing case
            absPath = "F:/PyCharm/P/Fortari2600/"
            file = open(absPath+"config/attack_decay.txt", "r")

        txt = file.read().split("\n")
        file.close()

        self.__data = []

        for line in txt:
            try:
                dataLine = []

                dataLine.append(int(line[0:2]))
                dataLine.append(int(line[3]))

                dataLine.append(float(line[5:13]))
                dataLine.append(float(line[14:22]))
                dataLine.append(float(line[23:31]))
                dataLine.append(float(line[32:40]))

                self.__data.append(dataLine)
            except Exception as e:
                pass

    def getValue(self, RM, RL, C):
        if RM == 0:
            return 0

        offset = 60 - ((RM-1) * 4 + RL +1)
        return(self.__data[offset][C+2])

class AttenuationTable:

    def __init__(self):
        try:
            file = open("config/attenuation.txt", "r")
        except:
            #Just testing case
            absPath = "F:/PyCharm/P/Fortari2600/"
            file = open(absPath+"config/attenuation.txt", "r")

        txt = file.read().split("\n")
        file.close()

        self.__data = []

        for line in txt:
            try:
                dataLine = []
                dataLine.append(int(line[0]))
                dataLine.append(int(line[2:4]))
                dataLine.append(float(line[5:]))

                self.__data.append(dataLine)
            except:
                pass


    def getValue(self, octave, fnumHi4):
        if type(fnumHi4) == str:
            fnumHi4 = int("0b"+fnumHi4, 2)

        for item in self.__data:
            offset = octave*16 + fnumHi4

        return(self.__data[offset][2])

class ChipStreamSlot:

    def __init__(self):
        self.changed       = False
        self.freq          = 0.0
        self.maxVol        = 0.0
        #0: off, 1: attack, 2: decay, 3: sustain, 4: release
        self.state         = 0
        self.sustainVolume = 0.0
        self.currentVolume = 0.0
        self.firstTime     = 10
        self.attackTime    = 0.0
        self.decayTime     = 0.0
        self.releaseTime   = 0.0
        self.attackTimeF   = 0.0
        self.decayTimeF    = 0.0
        self.releaseTimeF  = 0.0
        self.AMmodulatio   = 0.0
        self.vibratio      = 0.0
        self.vibrBit       = 0
        self.vibrCount       = 0
        self.sustainOn     = False

        self.outputVol     = 0.0
        self.outputFreq    = 0.0

        self.waveform      = 0
        self.hasNote       = False

class ChipStreamChannel:

    def __init__(self):
        self.slots = [
            ChipStreamSlot(),
            ChipStreamSlot()
        ]
        self.newNote       = False
        self.feedback      = 0.0
        self.connection    = False
        self.keyOn         = False
        self.noteNum       = 0

        self.channelData   = [[],[]]

class ChipStream:
    def __init__(self, vibr):

        self.channels =  \
            [
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel(),
                ChipStreamChannel()
            ]

        self.rythmMode  = False
        self.__vibrSets = vibr


        self.rythms = \
            {
            "HH":       False,
            "topCy":    False,
            "Tom":      False,
            "SD":       False,
            "BD":       False
            }


        self.slotNums = \
            {
            "HH":       14,
            "topCy":    17,
            "Tom":      16,
            "SD":       15,
            "BD":       12
            }

        self.drumSet = \
            {
                "HH": 91,
                "topCy": 92,
                "Tom": 94,
                "SD": 93,
                "BD": 90
            }


        self.timeLeft  = 0.0
        self.vibratio  = 0.0
        self.amDepth   = 0.0
        self.remainder = 0.0

    def playChannels(self, loader, specials):

        for channel in range(0,9):
            c = self.channels[channel]
            for slot in range(0,2):
                s = self.channels[channel].slots[slot]
                # Time is in milliseconds
                for t in range(0, int((self.timeLeft/44.1) + self.remainder)):
                    if self.rythmMode == False or channel < 6:
                        if c.keyOn == False and (s.state>0 and s.state<4):
                            s.state     = 4
                            s.firstTime = 10

                        if s.state == 0:
                           s.currentVolume = 0.0
                           s.outputVol     = 0.0
                        elif s.state == 1:
                           try:
                              if s.firstTime > 0:
                                changer = s.maxVol / s.attackTimeF
                                s.firstTime -= 1
                              else:
                                changer = s.maxVol / s.attackTime

                              s.currentVolume += changer

                              if s.currentVolume >= s.maxVol:
                                  s.state = 2
                                  s.currentVolume = s.maxVol
                           except:
                              s.state = 2
                              s.currentVolume = s.maxVol
                              s.firstTime = 10

                           #s.slotData.append(s.currentVolume)
                        elif s.state == 2:
                            try:
                                if s.firstTime > 0:
                                    changer = (s.maxVol - s.sustainVolume) / s.decayTimeF
                                    s.firstTime -= 1
                                else:
                                    changer = (s.maxVol-s.sustainVolume) / s.decayTime
                            except:
                               changer = 0
                            s.currentVolume -= changer

                            if s.currentVolume < s.sustainVolume:
                               if s.sustainOn:
                                  s.state = 3
                                  if s.currentVolume < s.sustainVolume:
                                     s.currentVolume = s.sustainVolume
                                     s.firstTime = 10
                               else:
                                  s.state = 4
                                  s.firstTime = 10
                            #if changer < 0: print(s.maxVol, s.sustainVolume, "2")
                            #s.slotData.append(s.currentVolume)
                        elif s.state == 4:
                            try:
                               if s.firstTime > 0:
                                  s.firstTime -= 1
                                  changer = s.sustainVolume / s.releaseTimeF
                               else:
                                  changer = s.sustainVolume / s.releaseTime
                            except:
                               changer = 0
                            s.currentVolume -= changer
                            if s.currentVolume <= 0:
                               s.currentVolume = 0
                               s.state         = 0
                               s.firstTime     = 10
                            #s.slotData.append(s.currentVolume)
                            #if changer < 0: print(s.sustainVolume, "4")

                        if s.state > 0:
                           s.outputVol  = s.currentVolume
                           s.outputFreq = s.freq
                           if s.vibratio > 0.0 and self.__vibrSets == True:
                              if s.vibrBit == 1:
                                 s.outputFreq *= (s.vibratio+1)
                              if s.vibrCount > 1:
                                s.vibrBit = 1 - s.vibrBit
                                s.vibrCount = 0
                              else:
                                s.vibrCount += 1

                           s.outputVol += s.AMmodulatio

                        if s.state == 0: s.outputVol = 0

                        if slot == 1:
                           note = loader.piaNotes.getClosestPianoKey(c.slots[1].outputFreq)
                           vol  = c.slots[1].outputVol // 7

                           if vol == 0: note = 0

                           if note < 32:
                              vol = vol // 2

                           if (note in specials[2]):
                               vol  = 0
                               note = 0

                           if specials[1] == True and ((note<3 or note>68 or note in [30,31])):
                               vol  = 0
                               note = 0

                           if note > 88:
                               vol = 0
                               note = 0

                           if vol > 0: self.channels[channel].slots[slot].hasNote = True
                           c.channelData[0].append([vol, note])
                        else:
                           if c.connection == True:
                               note = loader.piaNotes.getClosestPianoKey(c.slots[0].outputFreq)
                               vol = c.slots[0].outputVol // 7

                               if (note in specials[2]):
                                   vol = 0
                                   note = 0

                               if specials[1] == True and ((note < 3 or note > 68 or note in [30, 31])):
                                   vol = 0
                                   note = 0

                               if note > 88:
                                   vol = 0
                                   note = 0

                               if note < 32:
                                   vol = vol // 2

                               if vol == 0: note = 0

                               if vol > 0: self.channels[channel].slots[slot].hasNote = True
                               c.channelData[1].append([vol, note])
                           else:
                               c.channelData[1].append([0, 0])

                    else:

                        for key in self.rythms:
                            rythmChannel = self.slotNums[key] // 2
                            rythmSlot    = self.slotNums[key] % 2

                            if rythmChannel == channel and rythmSlot == slot:
                                if self.rythms[key] == True:
                                    vol  = 3
                                    note = self.drumSet[key]
                                else:
                                    vol  = 0
                                    note = 0

                                if vol > 0: self.channels[channel].slots[slot].hasNote = True
                                self.channels[channel].channelData[slot].append([vol, note])

        self.remainder = (self.timeLeft / 44.1) + self.remainder - int((self.timeLeft / 44.1) + self.remainder)

class ChipSlot:
    def __init__(self):
        self.multiplier     = 0
        self.KSL            = 0
        self.KSR            = False
        self.egTyp          = False
        self.Vibr           = False
        self.AMmod          = False

        self.totalLevel        = 0.0
        self.attenuationDegree = 0.0

        self.attackRate     = 0
        self.decayRate      = 0
        self.sustainRate    = 0
        self.sustainLevel   = 0
        self.releaseRate    = 0

        self.attackRateF    = 0
        self.decayRateF     = 0
        self.releaseRateF   = 0


        self.RKS            = 0
        self.keySplitNum    = 0

        self.waveform       = 0

class ChipChannel:
    def __init__(self):
        self.octave_block     = 0
        self.FNum_HI          = "00"
        self.FNum_LO          = "00000000"
        self.Fnum             = 0
        self.feedback         = 0
        self.slotConnetion    = False
        self.keyOn            = False
        self.modulationFactor = 0.0

        self.slots = \
            [
                ChipSlot(),
                ChipSlot()
            ]

#THIS IS THE MAIN CLASS
class YM3812:
    def __init__(self, loader, data, removeOutside, removePercuss, cutOut, vibrSets):

        self.__loader   = loader
        self.data       = data
        self.AT         = AttenuationTable()
        self.ADT        = AttackDecayTable()

        self.__specials = (removePercuss, removeOutside, cutOut)
        self.__vibrSets = vibrSets

        self.rythms = \
            {
            "HH":       False,
            "topCy":    False,
            "Tom":      False,
            "SD":       False,
            "BD":       False
            }

        self.rythmMode = False
        self.noteSel  = False

        self.vibratio = 0.0
        self.amDepth  = 0.0

        self.channels = \
            [
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel(),
                ChipChannel()
            ]

        self.stream = ChipStream(vibrSets)


        #counter = -1

        for line in self.data:
            if type(line) == str:
               line = line.split(" ")

            #counter+=1
            #print(counter, "/", len(self.data))

            if line[0] not in ("61", "62", "63"):
               register = int("0x"+line[1], 16)
               data     = int("0x"+line[2], 16)

               if register == 0x08:
                  self.__setRegister08(data, [line[1], line[2]])
               elif register >= 0x20 and register <= 0x35:
                  self.__setRegister2X(register, data, [line[1], line[2]])
               elif register >= 0x40 and register <= 0x55:
                  self.__setRegister4X(register, data, [line[1], line[2]])
               elif register >= 0x60 and register <= 0x75:
                  self.__setRegister6X(register, data, [line[1], line[2]])
               elif register >= 0x80 and register <= 0x95:
                  self.__setRegister8X(register, data, [line[1], line[2]])
               elif register >= 0xA0 and register <= 0xA8:
                  self.__setRegisterAX(register, data, [line[1], line[2]])
               elif register >= 0xB0 and register <= 0xB8:
                  self.__setRegisterBX(register, data, [line[1], line[2]])
               elif register >= 0xC0 and register <= 0xC8:
                  self.__setRegisterCX(register, data, [line[1], line[2]])
               elif register == 0xbd:
                  self.__setRegisterBD(data, [line[1], line[2]])
               elif register >= 0xe0 and register <= 0xf5:
                   self.__setRegisterEX(register, data, [line[1], line[2]])
            else:
               if line[0] == "61":   time = int("0x"+line[2]+line[1],16)
               elif line[0] == "62": time = 735
               elif line[0] == "63": time = 882

               self.__updateOutput(time)
               self.stream.playChannels(self.__loader, self.__specials)



    def __updateOutput(self, waitTime):
        #seconds = waitTime / 44.1

        self.stream.timeLeft = waitTime
        self.stream.vibratio = self.vibratio
        self.stream.amDepth  = self.amDepth

        freqBases = [ 0.047, 0.094, 0.189, 0.379, 0.758, 1.517, 3.034, 6.068 ]
        freqSteps = [ 0.048, 0.095, 0.190, 0.379, 0.759, 1.517, 3.034, 6.069 ]

        for channel in range(0,9):

            if (self.stream.channels[channel].slots[0].changed == True or
                self.stream.channels[channel].slots[1].changed == True):

                fNumHi4 = int("0b"+self.channels[channel].FNum_HI+self.channels[channel].FNum_LO[0:2], 2)

                if self.channels[channel].Fnum == 0:
                    freq = 0
                else:
                    freq = freqBases[self.channels[channel].octave_block] + \
                           freqSteps[self.channels[channel].octave_block] * (self.channels[channel].Fnum-1)

                decr = self.AT.getValue(self.channels[channel].octave_block,
                                        fNumHi4)

                self.stream.channels[channel].feedback   = self.channels[channel].feedback
                self.stream.channels[channel].connection = self.channels[channel].slotConnetion

                for slot in range(0,2):
                    self.__reCalculate(channel, slot)

                    self.stream.channels[channel].keyOn = self.channels[channel].keyOn

                    if (self.stream.channels[channel].slots[slot].changed == True and
                        self.stream.channels[channel].newNote == True):

                        self.stream.channels[channel].slots[slot].waveform = self.channels[channel].slots[slot].waveform

                        self.stream.channels[channel].slots[slot].vibrBit = 0
                        self.stream.channels[channel].slots[slot].vibrCount = 0
                        self.stream.channels[channel].slots[slot].state   = 1
                        self.stream.channels[channel].slots[slot].freq    = freq * self.channels[channel].slots[slot].multiplier

                        self.stream.channels[channel].slots[slot].maxVol = self.channels[channel].slots[slot].totalLevel
                        if self.stream.channels[channel].slots[slot].maxVol < 0:
                           self.stream.channels[channel].slots[slot].maxVol = 0.0

                        if self.channels[channel].slots[slot].KSL == 1:
                            self.stream.channels[channel].slots[slot].maxVol = \
                                self.stream.channels[channel].slots[slot].maxVol - decr
                        elif self.channels[channel].slots[slot].KSL == 2:
                            self.stream.channels[channel].slots[slot].maxVol = \
                                self.stream.channels[channel].slots[slot].maxVol - (0.5 * decr)
                        elif self.channels[channel].slots[slot].KSL == 3:
                            self.stream.channels[channel].slots[slot].maxVol = \
                                self.stream.channels[channel].slots[slot].maxVol - (2.0 * decr)

                        self.stream.channels[channel].slots[slot].sustainVolume = \
                             self.channels[channel].slots[slot].sustainLevel

                        self.stream.channels[channel].slots[slot].sustainVolume -= \
                            self.channels[channel].slots[slot].totalLevel - self.stream.channels[channel].slots[slot].maxVol

                        if self.stream.channels[channel].slots[slot].sustainVolume < 0:
                            self.stream.channels[channel].slots[slot].sustainVolume = 0

                        self.stream.channels[channel].slots[slot].currentVolume = 0.0

                        if self.channels[channel].slots[slot].KSR == False:
                            timeOffSet = 0

                            self.stream.channels[channel].slots[slot].attackTime = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].attackRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet
                                 )

                            self.stream.channels[channel].slots[slot].decayTime = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].decayRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet+1
                                 )

                            self.stream.channels[channel].slots[slot].releaseTime = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].releaseRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet+1
                                 )

                            timeOffSet = 2

                            self.stream.channels[channel].slots[slot].attackTimeF = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].attackRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet
                                 )

                            self.stream.channels[channel].slots[slot].decayTimeF = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].decayRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet+1
                                 )

                            self.stream.channels[channel].slots[slot].releaseTimeF = \
                                 self.ADT.getValue(
                                      self.channels[channel].slots[slot].releaseRate,
                                      self.channels[channel].slots[slot].RKS, timeOffSet+1
                                 )


                        else:
                            timeOffSet = 0

                            items = self.getRmRl(self.channels[channel].slots[slot].attackRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].attackTime = \
                                self.ADT.getValue(items[0], items[1], timeOffSet)


                            items = self.getRmRl(self.channels[channel].slots[slot].decayRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].decayTime = \
                                self.ADT.getValue(items[0], items[1], timeOffSet+1)

                            items = self.getRmRl(self.channels[channel].slots[slot].releaseRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].releaseTime = \
                                self.ADT.getValue(items[0], items[1], timeOffSet+1)

                            timeOffSet = 2

                            items = self.getRmRl(self.channels[channel].slots[slot].attackRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].attackTimeF = \
                                self.ADT.getValue(items[0], items[1], timeOffSet)

                            items = self.getRmRl(self.channels[channel].slots[slot].decayRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].decayTimeF = \
                                self.ADT.getValue(items[0], items[1], timeOffSet + 1)

                            items = self.getRmRl(self.channels[channel].slots[slot].releaseRate,
                                                 self.channels[channel].slots[slot].RKS)

                            self.stream.channels[channel].slots[slot].releaseTimeF = \
                                self.ADT.getValue(items[0], items[1], timeOffSet + 1)

                    if (self.channels[channel].slots[slot].AMmod == False):
                        self.stream.channels[channel].slots[slot].AMmodulatio = 0.0
                    else:
                        self.stream.channels[channel].slots[slot].AMmodulatio = self.amDepth

                    if (self.channels[channel].slots[slot].Vibr == False):
                        self.stream.channels[channel].slots[slot].vibratio = 0.0
                    else:
                        self.stream.channels[channel].slots[slot].vibratio = self.vibratio

                    self.stream.channels[channel].slots[slot].sustainOn = self.channels[channel].slots[slot].egTyp

                    self.stream.channels[channel].slots[slot].changed = False
                self.stream.channels[channel].newNote = False

        self.stream.rythmMode =  self.rythmMode
        self.stream.rythms["HH"] = self.rythms["HH"]
        self.stream.rythms["topCy"] = self.rythms["topCy"]
        self.stream.rythms["Tom"] = self.rythms["Tom"]
        self.stream.rythms["SD"] = self.rythms["SD"]
        self.stream.rythms["BD"] = self.rythms["BD"]

        self.rythms = \
             {
                 "HH": False,
                 "topCy": False,
                 "Tom": False,
                 "SD": False,
                 "BD": False
             }

    def getRmRl(self, rate, rks):
        r = bin((4 * rate) + rks).replace("0b", "")
        RM = r[:4]
        RL = r[-2:]

        return(int("0b"+RM, 2), int("0b"+RL, 2))

    def __setRegister08(self, data, dataStrings):
        data = self.__createBits(data, 8)

        self.noteSel = False
        if (data[1] == "1"):
            self.noteSel = True

        for channel in range(0,9):
            for slot in range(0,2):
                self.__reCalculate(channel, slot)
                self.stream.channels[channel].slots[slot].changed = True

    def __setRegister2X(self, register, data, dataStrings):
        channel, slot = self.__getChannelSlot(register, 0x20)

        byteString = self.__createBits(data, 8)

        self.channels[channel].slots[slot].KSL   = False
        self.channels[channel].slots[slot].egTyp = False
        self.channels[channel].slots[slot].Vibr  = False
        self.channels[channel].slots[slot].AMmod = False

        if byteString[0] == "1":
            self.channels[channel].slots[slot].AMmod = True
        if byteString[1] == "1":
            self.channels[channel].slots[slot].Vibr  = True
        if byteString[2] == "1":
            self.channels[channel].slots[slot].egTyp = True
        if byteString[3] == "1":
            self.channels[channel].slots[slot].KSL   = True

        multi = int("0b"+byteString[3:], 2)

        if multi == 0:
            self.channels[channel].slots[slot].multiplier = 0.5
        if multi < 11:
            self.channels[channel].slots[slot].multiplier = multi
        elif multi == 11:
            self.channels[channel].slots[slot].multiplier = 10
        elif multi >= 12 and multi <= 13:
            self.channels[channel].slots[slot].multiplier = 12
        else:
            self.channels[channel].slots[slot].multiplier = 15

        self.stream.channels[channel].slots[slot].changed = True

        self.__reCalculate(channel, slot)

        self.stream.channels[channel].slots[0].changed = True
        self.stream.channels[channel].slots[1].changed = True

    def __setRegister4X(self, register, data, dataStrings):
        channel, slot = self.__getChannelSlot(register, 0x40)
        string = self.__createBits(data, 8)

        totalVar = 0
        if string[2] == "1":
            totalVar += 24
        if string[3] == "1":
            totalVar += 12
        if string[4] == "1":
            totalVar += 6
        if string[5] == "1":
            totalVar += 3
        if string[6] == "1":
            totalVar += 1.5
        if string[7] == "1":
            totalVar += 0.75

        self.channels[channel].slots[slot].totalLevel = 96 - totalVar

        self.__calcSustainLevel(channel, slot)

        d = int("0b"+string[0:2], 2)
        if   d == 0:
           self.channels[channel].slots[slot].KSL = 0
        elif d == 1:
           self.channels[channel].slots[slot].KSL = 3
        elif d == 2:
           self.channels[channel].slots[slot].KSL = 1.5
        elif d == 3:
           self.channels[channel].slots[slot].KSL = 6

        self.stream.channels[channel].slots[slot].changed = True

    def __setRegister6X(self, register, data, dataStrings):
        channel, slot = self.__getChannelSlot(register, 0x60)
        string = self.__createBits(data, 8)

        self.channels[channel].slots[slot].attackRate = int("0b"+string[:4], 2)
        self.channels[channel].slots[slot].decayRate = int("0b"+string[4:], 2)

        self.stream.channels[channel].slots[slot].changed = True

    def __setRegister8X(self, register, data, dataStrings):
        channel, slot = self.__getChannelSlot(register, 0x80)
        string = self.__createBits(data, 8)

        self.channels[channel].slots[slot].sustainRate = int("0b"+string[:4], 2)
        self.channels[channel].slots[slot].releaseRate = int("0b"+string[4:], 2)

        self.__calcSustainLevel(channel, slot)

    def __calcSustainLevel(self, channel, slot):
        string = self.__createBits(self.channels[channel].slots[slot].sustainRate, 4)

        sus = 0
        if string[0] == "1":
            sus += 24
        if string[1] == "1":
            sus += 12
        if string[2] == "1":
            sus += 6
        if string[3] == "1":
            sus += 3

        if string[0:4] == "1111":
            sus = 93


        self.channels[channel].slots[slot].sustainLevel = self.channels[channel].slots[slot].totalLevel - sus
        if self.channels[channel].slots[slot].sustainLevel < 0: self.channels[channel].slots[slot].sustainLevel = 0
        self.stream.channels[channel].slots[slot].changed = True



    def __setRegisterAX(self, register, data, dataStrings):
        channel = int("0x"+dataStrings[0][1], 16)

        self.channels[channel].FNum_LO = self.__createBits(data, 8)
        self.channels[channel].Fnum = int("0b"+
                                          self.channels[channel].FNum_HI+
                                          self.channels[channel].FNum_LO,
                                          2)
        self.stream.channels[channel].slots[0].changed = True
        self.stream.channels[channel].slots[1].changed = True

    def __setRegisterBX(self, register, data, dataStrings):
        channel = int("0x"+dataStrings[0][1], 16)
        string = self.__createBits(data, 8)

        self.channels[channel].FNum_HI = string[6:8]
        self.channels[channel].Fnum = int("0b"+
                                          self.channels[channel].FNum_HI+
                                          self.channels[channel].FNum_LO,
                                          2)

        self.channels[channel].octave_block = int("0b"+string[3:6], 2)
        self.channels[channel].keyOn              = False

        if string[2] ==  "1":
            self.channels[channel].keyOn          = True
            self.stream.channels[channel].newNote = True
            for slot in range(0,2):
                self.stream.channels[channel].slots[slot].firstTime = 10

        self.__reCalculate(channel, 0)
        self.__reCalculate(channel, 1)
        self.stream.channels[channel].slots[0].changed = True
        self.stream.channels[channel].slots[1].changed = True

    def __setRegisterCX(self, register, data, dataStrings):
        channel = int("0x"+dataStrings[0][1], 16)
        string = self.__createBits(data, 8)

        self.channels[channel].slotConnetion = False
        if string[7] == "1":
            self.channels[channel].slotConnetion = True

        fb = int("0b"+string[4:7], 2)

        from math import pi
        values = [0, pi/16, pi/8, pi/4, pi/2, pi, pi*2, pi*4]

        self.channels[channel].feedback = values[fb]

        self.stream.channels[channel].slots[0].changed = True
        self.stream.channels[channel].slots[1].changed = True

    def __setRegisterBD(self, data, dataStrings):
        string = self.__createBits(data, 8)

        self.rythms["HH"] = False
        self.rythms["topCy"] = False
        self.rythms["Tom"] = False
        self.rythms["SD"] = False
        self.rythms["BD"] = False

        if string[0] == "1":
            self.amDepth = 4.8
        else:
            self.amDepth = 1

        if string[1] == "1":
            self.vibratio = 14
        else:
            self.vibratio = 7

        if string[2] == "1":
            self.rythmMode = True
        else:
            self.rythmMode = False

        if string[3] == "1":
            self.rythms["BD"] = True
        else:
            self.rythms["BD"] = False

        if string[4] == "1":
            self.rythms["SD"] = True
        else:
            self.rythms["SD"] = False

        if string[5] == "1":
            self.rythms["Tom"] = True
        else:
            self.rythms["Tom"] = False

        if string[6] == "1":
            self.rythms["topCy"] = True
        else:
            self.rythms["topCy"] = False

        if string[7] == "1":
            self.rythms["HH"] = True
        else:
            self.rythms["HH"] = False

        for num in range(0,9):
            for num2 in range(0,2):
                self.stream.channels[num].slots[num2].changed = True

    def __setRegisterEX(self, register, data, dataStrings):
        channel, slot = self.__getChannelSlot(register, 0xe0)
        string = self.__createBits(data, 8)

        self.channels[channel].slots[slot].waveform = int("0b"+string[6:], 2)

        self.stream.channels[channel].slots[slot].changed = True

    def __getChannelSlot(self, register, base):
        #  channel, slot = self.__getChannelSlot(dataStrings, 0x20)
        num  = register - base

        channels = [0, 1, 2, 0, 1, 2, -1, -1, 3, 4, 5, 3, 4, 5, -1, -1, 6, 7, 8, 6, 7, 8 ]
        slots    = [0, 0, 0, 1, 1, 1, -1, -1, 0, 0, 0, 1, 1, 1, -1, -1, 0, 0, 0, 1, 1, 1 ]

        return (channels[num], slots[num])

    def __createBits(self, data, bits):
        data = bin(data).replace("0b","")
        while(len(data)<bits):
             data = "0" + data

        return data

    def __createHex(self, data, hexNum):
        data = hex(data).replace("0x","")
        while(len(data)<hexNum):
             data = "0" + data

        return(data)

    def __reCalculate(self, channel, slot):
        add = 0
        if (self.noteSel == True):
            if self.channels[channel].FNum_HI[0] == "1":
               add = 1
        else:
            if self.channels[channel].FNum_HI[1] == "1":
               add = 1

        self.channels[channel].slots[slot].keySplitNum = (self.channels[channel].octave_block * 2) + add

        if self.channels[channel].slots[slot].KSR == True:
           self.channels[channel].slots[slot].RKS = self.channels[channel].slots[slot].keySplitNum
        else:
           bits = self.__createBits(self.channels[channel].slots[slot].keySplitNum, 8)
           self.channels[channel].slots[slot].RKS = int("0b"+bits[6:8], 2)


