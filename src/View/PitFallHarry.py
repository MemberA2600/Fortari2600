from PIL import ImageTk, Image as thisIsTheImage
from threading import Thread
from tkinter import *

class PitFallHarry:

    def __init__(self, window, master, loader, font):
        self.__window = window
        self.__loader = loader
        self.__master = master
        self.__font = font
        self.setBuffer()

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__bg = "gold"
        self.__spriteNum = 0
        self.dead = False

        self.__mainFrame = master.getTopLevel()
        self.__master    = master
        """
        self.__harryFrame = Frame(master.getTopLevel(),
                                  width=master.getTopLevelDimensions()[0], height=10000)
        self.__harryFrame.pack(side=TOP, anchor=N, fill=Y)
        self.__harryFrame.pack_propagate(False)
        self.__harryFrame.config(bg=self.__bg)
        """

        t = Thread(target=self.initMe)
        t.daemon = True
        t.start()

        self.__loader.threadLooper.addToThreading(self, self.__move, [], 1)
        #m = Thread(target=self.__move)
        #m.daemon = True
        #m.start()

    def initMe(self):
        self.__finished = False

        self.__canvas = Canvas(self.__mainFrame, bg = self.__bg,
                               height=9999, width=self.__master.getTopLevelDimensions()[0])
        self.__canvas.pack_propagate(False)
        self.__canvas.grid_propagate(False)
        self.__canvas.pack(side=TOP, fill=BOTH, anchor=N)
        self.__canvas.config(bd=0, highlightthickness=0, relief='ridge')

        while self.__canvas.winfo_height() < 2:
            from time import sleep
            sleep(0.0005)

        self.__h = self.__canvas.winfo_height()
        self.__w = round(self.__h * 0.76)

        self.__spriteCounter = 0
        self.__harryPoz = self.__master.getTopLevelDimensions()[0] / 2 - self.__w / 2

        self.__getDifference()

        # self.__harryLabel = Label(self.__harryFrame, bg=self.__bg)
        self.__setSprite(1)

        self.__harryMaxX = self.__master.getTopLevelDimensions()[0] - self.__w
        self.__placer()

        self.__drawHarry()
        self.__finished = True

    def setBuffer(self):
        self.__imageBuffer = []
        for num in range(1,7):
            self.__imageBuffer.append(thisIsTheImage.open(str("others/img/harry" + str(num) + ".png")))

    def __placer(self):
        if self.__window.dead==False and self.stopThread==False:
            try:
                # self.__harryLabel.place(x=self.__harryPoz, y=0)
                pass
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def __setSprite(self, num):
        if self.__spriteNum != num:
            self.__spriteNum = num
            i = self.__imageBuffer[num-1].resize((self.__w, self.__h), thisIsTheImage.ANTIALIAS)
            if self.__difference>0:
                self.__img = ImageTk.PhotoImage(i.transpose(thisIsTheImage.FLIP_LEFT_RIGHT))
            else:
                self.__img = ImageTk.PhotoImage(i)

            """    
            try:
                self.__harryLabel.config(image = self.__img)

            except Exception as e:
                self.__loader.logger.errorLog(e)
            """

    def __getDifference(self):
        import mouse
        if self.__window.dead==False and self.stopThread==False:
            try:
                self.__difference = mouse.get_position()[0] - (self.__w*0.5+self.__harryPoz+self.__master.getTopLevel().winfo_x())
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def __increment(self):
        if self.__spriteCounter>4:
            self.__spriteCounter = 0
        else:
            self.__spriteCounter+=1

    def __harryStop(self):
        self.__setSprite(1)
        self.__spriteCounter = 0

    def __harryMove(self, num):
        self.__setSprite(self.__spriteCounter + 1)
        self.__increment()
        self.__harryPoz += num
        self.__placer()

    def __drawHarry(self):
        try:
            self.__canvas.delete("all")
            self.__canvas.create_image(
                self.__harryPoz, 0, image=self.__img, anchor=NW
            )
        except:
            pass

    def __move(self):
        if self.__mainFrame.winfo_exists() == False:
           self.stopThread = True
           self.dead       = True

        if self.__finished:
            self.__getDifference()
            if abs(self.__difference)<15:
                self.__harryStop()
            elif self.__difference>14:
                if self.__harryPoz<self.__harryMaxX:
                    self.__harryMove(10)
                else:
                    self.__harryStop()
            elif self.__difference<-15:
                if self.__harryPoz>0:
                    self.__harryMove(-10)
                else:
                    self.__harryStop()

            if self.__harryPoz>self.__harryMaxX:
                self.__harryPoz = self.__harryMaxX
            elif self.__harryPoz<0:
                self.__harryPoz = 0

            self.__drawHarry()
