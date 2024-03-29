class FontManager:

    def __init__(self, loader):
        from pyglet import font as PyFont
        self.__loader = loader
        self.__loader.fontManager = self

        self.__lastScaleX = 1
        self.__lastScaleY = 1

        self.__chars = {}
        lastChar = None

        f = open("config/letters.txt")
        txt = f.readlines()
        f.close()

        for line in txt:
            line = line.replace("\n", "").replace("\r", "")
            if line != "":
                if len(line) == 1:
                    lastChar = line[0]
                    self.__chars[lastChar] = []
                else:
                    self.__chars[lastChar].append(line)

        PyFont.add_file('others/font/HammerFat.ttf')
        self.__normalSize = 22
        self.__sizing()

        #sizes= Thread(target=self.autoSizes)
        #sizes.start()

    def getAtariChar(self, char):
        if char.upper() in self.__chars.keys():
           return(self.__chars[char.upper()])
        else:
           return(None)

    def __sizing(self):
        baseW = 1600
        baseH = 1200
        baseS = 22

        try:
            self.__normalSize = round((self.__loader.mainWindow.getWindowSize()[0]/baseW) *
                                      ((self.__loader.mainWindow.getWindowSize()[1]/baseH)) * baseS)
        except:
            self.__normalSize = 22

        if self.__normalSize<10:
            self.__normalSize = 10


    def getFont(self, size, bold, italic, underline):
        from tkinter.font import Font, families

        if size == "normal":
            size = self.__normalSize
        elif size == "small":
            size = self.__normalSize*0.75
        elif size == "xs":
            size = self.__normalSize*0.5
        elif size == "large":
            size = self.__normalSize*1.5
        elif size == "xl":
            size =self.__normalSize*2

        if bold == True:
            bold = "bold"
        elif bold == False:
            bold = "normal"

        if italic == True:
            italic = "italic"
        elif italic == False:
            italic = "roman"

        if underline == True:
            underline = 1
        elif italic == False:
            underline = 0

        __font = Font(font='HammerFat_Hun')
        __font.config(size=round(size))
        __font.config(weight=bold)
        __font.config(slant=italic)
        __font.config(underline=underline)

        return(__font)

    def getCharacterLenghtFromPixels(self, font, len):
        num = 1
        while True:
            temp = font.measure(num*"0")
            if temp<len:
                num+=1
                continue
            else:
                return(num-2)