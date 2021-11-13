from tkinter.filedialog import *
from tkinter import messagebox
from tkinter.simpledialog import *

class FileDialogs:

    def __init__(self, dict, config, loader):
        self.__dicts = dict
        self.__config = config
        self.__loader = loader

    def askForInteger(self, title, p):

        return askinteger(self.__dicts.getWordFromCurrentLanguage(title), self.__dicts.getWordFromCurrentLanguage(p))


    def askYesOrNo(self, title, text):
        mbox = messagebox.askyesno(self.__dicts.getWordFromCurrentLanguage(title),
                                   self.__dicts.getWordFromCurrentLanguage(text))

        if mbox==True:
            return("Yes")
        else:
            return("No")

    def askYesNoCancel(self, title, text):
        mbox = messagebox.askyesnocancel(self.__dicts.getWordFromCurrentLanguage(title),
                                   self.__dicts.getWordFromCurrentLanguage(text))

        if mbox==True:
            return("Yes")
        elif mbox == False:
            return("No")
        else:
            return("Cancel")

    def askForFileName(self, title, save, fileTypes, initdir):
        types = []

        for t in fileTypes:

            if isinstance(t, list):
                rrr = []
                for item in t:
                    rrr.append("*."+item)
                typesString=", ".join(rrr)

                tempWord = None
                for item in t:
                    try:
                        testing = self.__dicts.getWordFromCurrentLanguage(item)
                    except:
                        word = self.__dicts.getWordFromCurrentLanguage("multiple")
                        break

                    if tempWord == None:
                        word = self.__dicts.getWordFromCurrentLanguage(item)
                        tempWord = word
                    elif tempWord != self.__dicts.getWordFromCurrentLanguage(item):
                        word = self.__dicts.getWordFromCurrentLanguage("multiple")
                        break

                for item in t:
                    temp = []

                    temp.append(word + " (" + typesString + ")")
                    temp.append("*." + item)
                    types.append(tuple(temp))

            else:
                temp = []
                temp.append(self.__dicts.getWordFromCurrentLanguage(t) + " (*."+t+")")
                temp.append("*."+t)
                types.append(tuple(temp))
        types = tuple(types)

        if os.path.exists(initdir) == False or initdir == None:
            test = os.getcwd()+os.sep+initdir
            print(test)
            if os.path.exists(test) == False:
                initdir = "*"
            else:
                initdir = test

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

        from random import randint

        number = randint(0,1000)
        if number > 995:
            self.__loader.soundPlayer.playSound("Gas")
        elif number < 5:
            self.__loader.soundPlayer.playSound("Pylons")
        else:
            self.__loader.soundPlayer.playSound("Error")
        if systemText != None:
            message += str("\n"+self.__dicts.getWordFromCurrentLanguage("errorSystemText")+"\n"+systemText)
        messagebox.showerror(self.__dicts.getWordFromCurrentLanguage(title),
                             message)