from tkinter.filedialog import *
from tkinter import messagebox

class FileDialogs:

    def __init__(self, dict, config):
        self.__dicts = dict
        self.__config = config

    def askYesOrNo(self, title, text):
        mbox = messagebox.askyesno(self.__dicts.getWordFromCurrentLanguage(title),
                                   self.__dicts.getWordFromCurrentLanguage(text))

        if mbox==True:
            return("Yes")
        else:
            return("No")

    def askForFileName(self, title, save, fileTypes):
        types = []

        for type in fileTypes:
            temp = []
            temp.append(self.__dicts.getWordFromCurrentLanguage(type))
            temp.append("*."+type)
            types.append(tuple(temp))
        types = tuple(types)


        if save == True:
            openname = asksaveasfilename(initialdir="*",
                                       title=self.__dicts.getWordFromCurrentLanguage(title),
                                       filetypes=types)
        else:
            openname = askopenfilename(initialdir="*",
                                       title=self.__dicts.getWordFromCurrentLanguage(title),
                                       filetypes=types)
        return(openname)