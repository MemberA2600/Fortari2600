from tkinter import *


class EmuTestFrame:

    def __init__(self, loader, motherFrame, ten, font, w, func, side, anchor):
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.__testWithEmulatorFrame = Frame(motherFrame, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__testWithEmulatorFrame.pack_propagate(False)

        self.__testWithEmulatorFrame.pack(side=side, anchor=anchor, fill=X)

        self.__emulatorTestLabel = Label(self.__testWithEmulatorFrame, text=self.__dictionaries.getWordFromCurrentLanguage("testWithEmulator")+" ",
                                   font=font,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.__emulatorTestLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.__emuImagePic = self.__loader.io.getImg("stella", None)
        self.__emuImagePicture = Button(self.__testWithEmulatorFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.__emuImagePic, width=w,
                                   command=func)

        self.__emuImagePicture.pack(side = RIGHT, anchor = W, fill=Y)