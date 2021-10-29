from tkinter import *
from PIL import Image as IMAGE

class LoadingScreen():
    """This class only opens a loading screen image and swaits for 3 seccnds,
    then destroys the window and then goes back to the main window."""

    def __init__(self, size, tk, loader):

        from PIL import ImageTk, Image
        self.__loader = loader

        self.__w_Size=round(800*(size[0]/1600))
        self.__h_Size=round(self.__w_Size*0.56)
        self.__Loading_Window=Toplevel()
        self.bindThings()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (self.__w_Size, self.__h_Size,
                                                        (size[0]/2)-self.__w_Size/2,
                                                        (size[1]/2)-self.__h_Size/2-50))

        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)

        self.__Img = ImageTk.PhotoImage(Image.open("others/img/loading.png").resize((self.__w_Size,self.__h_Size)))

        self.__ImgLabel = Label(self.__Loading_Window, image=self.__Img)
        self.__ImgLabel.pack()


        #self.__Loading_Window.after(3000, self.destroySelf)
        self.__Loading_Window.after(1, self.loadAndDestroy)
        self.__Loading_Window.wait_window()




    def loadAndDestroy(self):
        from Config import Config
        from DataReader import DataReader
        from Dictionary import Dictionary

        self.__loader.dataReader = DataReader()
        self.__loader.config = Config(self.__loader.dataReader)
        self.__loader.dictionaries = Dictionary(self.__loader.dataReader, self.__loader.config)

        from FileDialogs import FileDialogs
        self.__loader.fileDialogs = FileDialogs(self.__loader.dictionaries, self.__loader.config, self.__loader)

        from AutoSetter import AutoSetter
        self.__loader.autoSetter = AutoSetter(self.__loader.config, self.__loader.fileDialogs)


        from SoundPlayer import SoundPlayer
        self.__loader.soundPlayer = SoundPlayer(self.__loader.config)

        from IO import IO
        self.__loader.io = IO(self.__loader.dictionaries, self.__loader.config, self.__loader)

        self.__loader.sections = self.__loader.io.getFileNamesInDir("templates/bank2_8/")

        from VirtualMemory import VirtualMemory
        self.__loader.virtualMemory = VirtualMemory(self.__loader)

        from ColorPalettes import ColorPalettes
        self.__loader.colorPalettes = ColorPalettes(self.__loader)

        from Logger import Logger
        self.__loader.logger = Logger(self.__loader)

        self.__loader.io.loadSyntax()

        for num in range(1, 20):
            num = str(num)
            if len(num) == 1:
                num = "0" + str(num)
            self.__loader.atariFrames.append(IMAGE.open("others/img/logo/"+num+".gif"))


        for num in range(1, 67):
            num = str(num)
            if len(num) == 1:
                num = "0" + num
            self.__loader.rocketFrames.append(
                IMAGE.open(str("others/img/rocket/r" + num + ".png"))
            )

        from ColorDict import ColorDict
        self.__loader.colorDict = ColorDict(self.__loader)

        from TiaTone import TiaTone
        self.__loader.tiaTone = TiaTone()

        from PiaNotes import PiaNotes
        self.__loader.piaNotes = PiaNotes(self.__loader)

        from Executor import Executor
        self.__loader.executor = Executor(self.__loader)

        self.__Loading_Window.after(1000, self.__Loading_Window.destroy)



    def bindThings(self):
        from threading import Thread

        self.__clicked = 0
        self.__Loading_Window.bind("<Button-1>", self.pressed)


    def pressed(self, event):
        self.__clicked +=1
        self.__loader.soundPlayer.playSound("Click")


    def getPresses(self):
        if (self.__clicked>1):
            return(True, self.__clicked)
        else:
            return(False, self.__clicked)