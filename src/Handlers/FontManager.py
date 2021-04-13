class FontManager:

    def __init__(self, boss):
        from pyglet import font as PyFont
        from threading import Thread

        self.__boss = boss
        self.__lastScaleX = 1
        self.__lastScaleY = 1


        PyFont.add_file('others/font/HammerFat.ttf')
        self.__normalSize = 22
        self.__sizing()
        sizes= Thread(target=self.autoSizes)
        sizes.start()

    def autoSizes(self):
        from time import sleep
        while True:
            if (self.__lastScaleX==self.__boss.getScales()[0] and self.__lastScaleX==self.__boss.getScales()[1]):
                sleep(0.05)
                continue
            self.__lastScaleX = self.__boss.getScales()[0]
            self.__lastScaleX = self.__boss.getScales()[1]
            self.__sizing()
            sleep(0.02)

    def __sizing(self):
        baseW = 1600
        baseH = 1200
        baseS = 22
        self.__normalSize = round((self.__boss.getWindowSize()[0]/baseW) *
                                  ((self.__boss.getWindowSize()[1]/baseH)) * baseS)

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
        __font.config(size=size)
        __font.config(weight=bold)
        __font.config(slant=italic)
        __font.config(underline=underline)

        return(__font)