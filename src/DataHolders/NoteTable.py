from copy import deepcopy

class NoteTable:

    def __init__(self, loader, maxH):

        self.__loader = loader
        self.__piaNotes = self.__loader.piaNotes

        self.__maxH = maxH

        self.screenMax = 1
        self.selected = 0
        self.table = []

        self.__row = []
        for num in range(0, self.__maxH):
            self.__row.append(0)

        self.__screen = []
        for num in range(0,88):
            self.__screen.append(deepcopy(self.__row))

        self.addNewScreen()
        self.addNewScreen()

    def addNewScreen(self):
        self.table.append(deepcopy(self.__screen))

    def getDominantChannelsOfScreen(self, keys):
        channels = {
            1: 0,
            4: 0,
            6: 0,
            12: 0
        }

        for lineNum in range(88,0,-1):
            line = self.table[self.selected][88-lineNum]
            #print(line)
            notes = self.__piaNotes.getTiaValue(str(lineNum), None)
            #print(lineNum)
            #print(notes)

            if notes!=None:
                for note in line:
                    #print(note)
                    if note == 1:
                        for n in notes.keys():
                            channels[int(n)]+=1
        if keys == "tremble":
            try:
                del channels["1"]
            except:
                pass
            try:
                del channels["6"]
            except:
                pass
        else:
            try:
                del channels["4"]
            except:
                pass
            try:
                del channels["12"]
            except:
                pass
        return(channels)

    def flipField(self, X, Y):
        if self.table[self.selected][Y][X] != 0:
            self.table[self.selected][Y][X] = 0
        else:
            self.table[self.selected][Y][X] = 8
        #self.table[self.selected][Y][X] = 1 - self.table[self.selected][Y][X]
        #print(self.table[self.selected][Y][X])

    def setField(self, X, Y, volume):
        self.table[self.selected][Y][X] = volume

    def clearField(self, X, Y):
        self.table[self.selected][Y][X] = 0

    def getValue(self, X, Y):
        return self.table[self.selected][Y][X]
