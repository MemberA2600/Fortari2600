from ColorItem import ColorItem

class ColorDict:

    def __init__(self, loader):

        self.__loader = loader
        self.ValidColors = {}

        file = open("config/ValidColors.txt")
        for line in file.readlines():
            line = line.replace("\r","").replace("\n","")
            colorName = line.split(",")[0]
            self.ValidColors[colorName] = {}
            self.ValidColors[colorName]["red"] = int(line.split(",")[1])
            self.ValidColors[colorName]["blue"] = int(line.split(",")[2])
            self.ValidColors[colorName]["green"] = int(line.split(",")[3])
        file.close()
        #print(self.ValidColors)

        self.TIAColors = {}
        file = open("config/TIAColors.txt")
        for line in file.readlines():
            line = line.replace("\r","").replace("\n","")
            self.TIAColors[line.split("=")[0]] = ColorItem(line.split("=")[1])
        file.close()
        #for key in self.TIAColors.keys():
        #    print(key, self.getHEXValueFromTIA(key))


    def getHEXValue(self, red, blue, green):
        i = int(red)
        if i>255:
            i-=255

        red = hex(i)[2:]
        if len(red) == 1:
            red = "0"+red
        i = int(blue)
        if i>255:
            i-=255

        blue = hex(i)[2:]
        if len(blue) == 1:
            blue = "0"+blue
        i = int(green)
        if i>255:
            i-=255

        green = hex(i)[2:]
        if len(green) == 1:
            green = "0"+green

        return("#"+red+blue+green)

    def getHEXValueFromTIA(self, tia):
        that = self.TIAColors[tia.lower()]
        return self.getHEXValue(that.red, that.blue, that.green)

    def getRGBValueFromTIA(self, tia):
        that = self.TIAColors[tia.lower()]
        return (that.red, that.blue, that.green)

    def getClosestTIAColor(self, r, g, b):
        from math import sqrt

        difference = 1

        while difference<256:
            for colorNum in self.TIAColors:

                d = abs(sqrt((self.TIAColors[colorNum].red - r) ** 2 +
                                  (self.TIAColors[colorNum].green - g) ** 2 +
                                  (self.TIAColors[colorNum].blue - b) ** 2))

                if  d < difference:

                    return(colorNum)
            difference+=1

    def getDominantColor(self, biglist):

        occurences = {}

        for array in biglist:
            if array in occurences.keys():
                occurences[array]+=1
            else:
                occurences[array]=1

        s = dict(sorted(occurences.items(), key=lambda item: item[1]))

        largestName = ""
        largestNum = 0

        for key in s.keys():
            if s[key] > largestNum:
                largestNum = s[key]
                largestName = key

        if biglist == []:
            return(None)
        elif largestNum < 3:
            biglist.sort()

            return(biglist[round(len(biglist)/2)])

        else:
            return(largestName)

    def getTIAfromRGB(self, rgb):
        return self.getClosestTIAColor(rgb[0], rgb[1], rgb[2])


