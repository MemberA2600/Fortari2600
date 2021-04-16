from tkinter import Label, TOP, NW, NORMAL, DISABLED

class SubMenuLabel:

    def __init__(self, master, loader, text, font):
        self.__label = Label(master,
                             text = loader.dictionaries.getWordFromCurrentLanguage(text),
                             font=font)
        self.__label.pack(side=TOP, anchor = NW)

    def enabled(self, bool):
        if bool == True:
            self.__label.config(state = NORMAL)
        else:
            self.__label.config(state = DISABLED)
