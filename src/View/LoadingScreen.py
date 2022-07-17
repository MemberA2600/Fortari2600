from tkinter import *
from PIL import Image as IMAGE, ImageTk
from threading import Thread
from time import sleep

class LoadingScreen():
    """This class only opens a loading screen image and swaits for 3 seccnds,
    then destroys the window and then goes back to the main window."""

    def __init__(self, size, tk, loader):

        self.__main = tk

        self.__loader = loader
        self.__w_Size=round(800*(size[0]/1600))
        self.__h_Size=round(self.__w_Size*0.56)

        self.__Loading_Window=Toplevel()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (self.__w_Size, self.__h_Size,
                                                        (size[0]/2)-self.__w_Size/2,
                                                        (size[1]/2)-self.__h_Size/2-50))
        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)

        self.__Img = ImageTk.PhotoImage(IMAGE.open("others/img/loading.png").resize((self.__w_Size,self.__h_Size)))

        self.__ImgLabel = Label(self.__Loading_Window, image=self.__Img)
        self.__ImgLabel.pack()

        self.__Loading_Window.update_idletasks()
        self.__Loading_Window.update()

        #self.__Loading_Window.after(1, self.loadAndDestroy)


    def loadThings(self):

        from Config import Config
        from DataReader import DataReader
        from Dictionary import Dictionary

        self.bindThings()

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

        __w = self.__loader.screenSize[0]-150
        __h = self.__loader.screenSize[1]-200
        __h = __h - (__h // 11.25) - (__h // 30)*2

        self.loadAnimationFrames("logo", 20,
                                 self.__loader.atariFrames, "gif",
                                 (__w, __h, 0.6)
                                 )

        self.loadAnimationFrames("rocket", 67,
                                 self.__loader.rocketFrames, "png",
                                 (__w, __h, 0.2)
                                 )

        self.loadAnimationFrames("tape", 31,
                                 self.__loader.tapeFrames, "gif",
                                 (__w//2.75, __h//2.75, 1)
                                 )

        s = (round(self.__loader.screenSize[0] // 1.15 // 7 * 6),
             round((self.__loader.screenSize[1] // 1.25 - 55) // 20 * 19))

        """
        self.loadAnimationFrames("centipede", 19,
                                 self.__loader.centipedeFrames, "png",
                                 (s[0], s[1], 1)
                                 )
        """

        self.loadAnimationFrames("plasma", 65,
                                 self.__loader.rainbowFrames, "gif",
                                 (s[0], s[1], 1)
                                 )


        self.loadAnimationFrames("lock", 4,
                                 self.__loader.lockedFramesTopLevel, "png",
                                 (s[0], s[1], 1)
                                 )

        self.loadAnimationFrames("jumpman", 7,
                                 self.__loader.jumpman, "png",
                                 (__w // 10, __h // 5, 1)
                                 )

        from ColorDict import ColorDict
        self.__loader.colorDict = ColorDict(self.__loader)

        from TiaTone import TiaTone
        self.__loader.tiaTone = TiaTone()

        from PiaNotes import PiaNotes
        self.__loader.piaNotes = PiaNotes(self.__loader)

        from Executor import Executor
        self.__loader.executor = Executor(self.__loader)

        self.__Loading_Window.destroy()

    def loadAnimationFrames(self, folder, maxNum, dataHolder, format, s):
        for num in range(1, maxNum):
            num = str(num)
            if len(num) == 1:
                num = "0" + num
            dataHolder.append(
                self.returnResized(IMAGE.open(str("others/img/"+folder+"/" + num + "."+format)), s[0], s[1], s[2]))


    def returnResized(self, source, w, h, part):
        return ImageTk.PhotoImage(source.resize((round(w*part), round(h))), IMAGE.ANTIALIAS)

    def bindThings(self):
        from threading import Thread

        self.__clicked = 0
        import keyboard

        keyboard.on_press_key("6", self.pressed)


    def pressed(self, event):

        self.__clicked +=1
        try:
            self.__loader.soundPlayer.playSound("Click")
        except:
            pass

    def getPresses(self):
        if (self.__clicked>2):
            return(True, self.__clicked)
        else:
            return(False, self.__clicked)

