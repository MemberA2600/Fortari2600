from tkinter import *
from PIL import Image, ImageTk

class Loader:
    def __init__(self):
        self.tk = None
        self.dataReader = None
        self.config = None
        self.dictionaries = None
        self.fileDialogs = None
        self.autoSetter = None
        self.soundPlayer = None
        self.screenSize = None
        self.mainWindowHander = None
        self.mainWindow = None
        self.fontManager = None

        self.frames = {}
        self.menuButtons = {}

    def getImg(self, name, size):
        if (size == None):
            return(ImageTk.PhotoImage(Image.open("others/img/"+name+".png")
                                      .resize((self.getConstant(),self.getConstant()), Image.ANTIALIAS)))
        else:
            return(ImageTk.PhotoImage(Image.open("others/img/"+name+".png")
                                      .resize((size, size)), Image.ANTIALIAS))

    def getConstant(self):
        scalerX = self.mainWindow.getWindowSize()[0]/1300
        scalerY = self.mainWindow.getWindowSize()[1]/1150
        num = round(32*scalerX*scalerY)
        if num>32:
            num=32
        elif num<18:
            num=18
        return(num)

    def checkIfValidFileName(self, name):
        from pathvalidate import ValidationError, validate_filename
        try:
            validate_filename(name)
            return(True)
        except ValidationError as e:
            return(False)
