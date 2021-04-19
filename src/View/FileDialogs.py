from tkinter.filedialog import *
from tkinter import messagebox

class FileDialogs:

    def __init__(self, dict, config, loader):
        self.__dicts = dict
        self.__config = config
        self.__loader = loader

    def askYesOrNo(self, title, text):
        mbox = messagebox.askyesno(self.__dicts.getWordFromCurrentLanguage(title),
                                   self.__dicts.getWordFromCurrentLanguage(text))

        if mbox==True:
            return("Yes")
        else:
            return("No")

    def askForFileName(self, title, save, fileTypes, initdir):
        types = []

        for type in fileTypes:
            temp = []
            temp.append(self.__dicts.getWordFromCurrentLanguage(type))
            temp.append("*."+type)
            types.append(tuple(temp))
        types = tuple(types)

        if os.path.exists(initdir) == False or initdir == None:
            initdir = "*"

        if save == True:
            openname = asksaveasfilename(initialdir=initdir,
                                       title=self.__dicts.getWordFromCurrentLanguage(title),
                                       filetypes=types)
        else:
            openname = askopenfilename(initialdir=initdir,
                                       title=self.__dicts.getWordFromCurrentLanguage(title),
                                       filetypes=types)
        return(openname)


    def askForDir(self, init):
        openname = askdirectory(initialdir=init,
                                       title=self.__dicts.getWordFromCurrentLanguage("openFolder"),
                                       )
        return(openname)

    def displayError(self, title, message, data, systemText):
        message = self.__dicts.getWordFromCurrentLanguage(message)
        if data!=None:
            for item in data.keys():
                message = message.replace(str("#"+item+"#"), data[item])

        self.__loader.soundPlayer.playSound("Error")
        if systemText != None:
            message += str("\n"+self.__dicts.getWordFromCurrentLanguage("errorSystemText")+"\n"+systemText)
        messagebox.showerror(self.__dicts.getWordFromCurrentLanguage(title),
                             message)