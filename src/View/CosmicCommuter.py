from PIL import ImageTk, Image as IMAGE
from threading import Thread
from tkinter import *

class CosmicCommuter:

    def __init__(self, frame, loader, size, toplevel, caller):
        self.__motherFrame = frame
        self.__loader      = loader
        self.__size        = size
        self.__topLevel    = toplevel
        self.caller        = caller

        self.__spaceCanvas = Canvas(self.__motherFrame, bg = "black", height=self.__size[1], width=self.__size[0])
        self.__spaceCanvas.pack_propagate(False)
        self.__spaceCanvas.grid_propagate(False)
        self.__spaceCanvas.pack(side=TOP, fill=BOTH, anchor=CENTER)
        self.__spaceCanvas.config(bd=0, highlightthickness=0, relief='ridge')
        self.__spaceCanvas.pack(side=TOP, fill=BOTH, anchor=CENTER)

        #self.__testLabel = Label(self.__motherFrame,
        #                   bg="yellow", justify=CENTER, height = 1000000, width = 100000,
        #                   )
        #self.__testLabel.pack_propagate(False)
        #self.__testLabel.pack(side=TOP, fill=BOTH, anchor=CENTER)

        self.__differenceYToMouse       = 0
        self.__differenceYToLandingZone = 0
        self.__shipY                    = 0
        self.__speed                    = 0

        self.__shipSize                 = 0
        self.__first                    = True
        self.__groundIndex              = -1
        self.__shipIndex                = -1
        self.__shipYLast                = -1
        self.__coolDown                 = 0

        self.__shipFrames      = []
        self.__groundFrames    = []
        self.__finishedLoading = False

        self.__groundImage     = None
        self.__shipImage       = None

        buffer = Thread(target=self.__setBufferThread)
        buffer.daemon = True
        buffer.start()

        self.__loader.threadLooper.addToThreading(self, self.createSprites, [])
        #createSprites = Thread(target=self.createSprites)
        #createSprites.daemon = True
        #createSprites.start()

        #draw = Thread(target=self.drawLoop)
        #draw.daemon = True
        #draw.start()

    def __setBufferThread(self):
        from time import sleep

        while self.__spaceCanvas.winfo_width() < 2:
            sleep(0.0005)

        import os
        self.__shipSize = round((161 / self.__size[0]) * 128)

        #print( self.__size[0] / 161, 161 / self.__size[0])

        for root, folders, files in os.walk("others/img/cosmic"):
            for file in files:
                if "Ship" in file:
                    self.__shipFrames.append(
                    IMAGE.open(root + "/" + file).resize((
                        round(self.__size[0]), self.__shipSize), IMAGE.ANTIALIAS))
                    #self.__shipFrames[-1].show()

                else:
                    self.__groundFrames.append(
                    IMAGE.open(root + "/" + file).resize((
                        round(self.__size[0]), self.__shipSize), IMAGE.ANTIALIAS))

        self.__groundImage = ImageTk.PhotoImage(self.__groundFrames[2])
        self.__shipImage   = ImageTk.PhotoImage(self.__shipFrames[0])

        self.__minOnCanvas = 0
        self.__maxOnCanvas = self.__size[1] - round(self.__shipSize)
        self.__minY = self.__topLevel.winfo_y() + self.__minOnCanvas
        self.__maxY = self.__topLevel.winfo_y() + self.__maxOnCanvas

        self.__finishedLoading = True

    def createSprites(self):
        import mouse
        from random import randint

        if self.__shipSize > 0 and self.__finishedLoading:
               if self.__first:
                  self.__shipY = self.__size[1] // 2 - self.__shipSize

               difference = self.__shipY - mouse.get_position()[1]

               adder = round(abs(difference) // 35)

               if   difference < -10: self.__speed += randint(0, adder)
               elif difference >  10: self.__speed -= randint(0, adder)
               else:
                   self.__speed = randint(-1 * adder , adder)

               adder = adder * 8

               if self.__speed >      adder: self.__speed =      adder
               if self.__speed < -1 * adder: self.__speed = -1 * adder

               self.__shipY += self.__speed // 10
               self.__maxYS = self.__maxY - self.__shipSize // 2

               if   self.__shipY < self.__minY : self.__shipY = self.__minY
               elif self.__shipY > self.__maxYS: self.__shipY = self.__maxYS

               limiter = self.__size[1] // round((len(self.__groundFrames) * 1.5 ))
               index   = (self.__maxY - self.__shipY) // limiter
               if index > (len(self.__groundFrames)- 1):
                  index = (len(self.__groundFrames) - 1)

               #self.__spaceCanvas.clipboard_clear()
               #self.__spaceCanvas.delete("all")
               #print(self.__shipY, self.__speed, self.__minY, self.__maxY)

               if self.__coolDown > 0:
                  self.__coolDown -= 1

               if    self.__speed > 0 :
                     shipIndex = 5
                     self.__coolDown = 0
               else:
                     shipIndex = abs(self.__speed) // 5
                     if self.__coolDown == 0:
                        self.__loader.soundPlayer.playSound("cosmic")
                        self.__coolDown = randint(4, 20)

               shipIndex += randint(-2,2)

               if shipIndex < 0                             : shipIndex = 0
               if shipIndex > (len(self.__shipFrames) - 1)  : shipIndex = (len(self.__shipFrames) - 1)

               try:
                   #self.__spaceCanvas.create_rectangle(0, 0, self.__size[0], self.__size[1], fill = "black")
                   if index != self.__groundIndex:
                      self.__groundImage = ImageTk.PhotoImage(self.__groundFrames[index])
                      self.__groundIndex = index
                      if self.__first == False:
                         self.__spaceCanvas.delete(self.__groundThing)

                   if shipIndex != self.__shipIndex or self.__shipYLast != self.__shipY:
                      self.__shipImage = ImageTk.PhotoImage(self.__shipFrames[shipIndex])
                      self.__shipIndex = shipIndex
                      if self.__first == False:
                         self.__spaceCanvas.delete(self.__shipThing)
                         self.__shipYLast = self.__shipY

                   self.__groundThing = self.__spaceCanvas.create_image(
                       0, self.__maxOnCanvas, image=self.__groundImage, anchor=NW
                   )

                   self.__shipThing = self.__spaceCanvas.create_image(
                       0, self.__shipY - self.__topLevel.winfo_y(), image=self.__shipImage, anchor=NW
                   )
               except:
                   pass

               if self.__first: self.__first = False



