from tkinter import *


class ConvertFromImageFrame:

    def __init__(self, loader, motherFrame, ten, font, w, func, side, anchor):
        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.__convertFromImageFrame = Frame(motherFrame, height=ten, bg=self.__loader.colorPalettes.getColor("window"))
        self.__convertFromImageFrame.pack_propagate(False)

        self.__convertFromImageFrame.pack(side=side, anchor=anchor, fill=X)

        self.convertFromImageLabel = Label(self.__convertFromImageFrame, text=self.__dictionaries.getWordFromCurrentLanguage("importImage")+" ",
                                   font=font,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   fg=self.__loader.colorPalettes.getColor("font")
                                   )
        self.convertFromImageLabel.pack(side=LEFT, anchor=W, fill=Y)

        self.pic = self.__loader.io.getImg("image", None)
        self.__convertFromImageButton = Button(self.__convertFromImageFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                   image = self.pic, width=w,
                                   command=func)

        self.__convertFromImageButton.pack(side = RIGHT, anchor = W, fill=Y)