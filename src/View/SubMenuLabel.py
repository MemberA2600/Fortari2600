from tkinter import Label, TOP, NW, NORMAL, DISABLED

class SubMenuLabel:

    def __init__(self, master, loader, text, font):
        self.__loader = loader
        try:
            self.__label = Label(master,
                                 text = loader.dictionaries.getWordFromCurrentLanguage(text),
                                 font=font)
        except:
            self.__label = Label(master,
                                 text = text,
                                 font=font)
        self.__label.pack(side=TOP, anchor = NW)
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__label.config(fg=self.__loader.colorPalettes.getColor("font"))


    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)
