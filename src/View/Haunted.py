from tkinter import *
from copy import deepcopy

class Haunted:

    def __init__(self, loader, frame, toplevel, parent):
        self.__loader = loader
        self.__frame = frame

        self.__colors  = ["black", "dark orange", "orange", "dark orange"]
        self.__counter = 0

        self.__topLevelWindow = toplevel
        self.__step = 16
        self.__yourSize = 12

        self.caller = parent

        self.__maxX =  self.__frame.winfo_width() // self.__step * self.__step
        self.__maxY =  self.__frame.winfo_height() // self.__step * self.__step

        self.__color = "black"

        from time import sleep

        while self.__frame.winfo_width() < 2: sleep(0.000001)

        self.__canvas = Canvas(self.__frame, bg = "black", height=self.__maxY, width=self.__maxX)
        self.__canvas.pack_propagate(False)
        self.__canvas.grid_propagate(False)
        self.__canvas.pack(side=BOTTOM, fill=BOTH, anchor=CENTER)
        self.__canvas.config(bd=0, highlightthickness=0, relief='ridge')

        self.createGrid()

        self.__yourX = self.__maxX // 2 + self.__yourSize // 2
        self.__yourY = self.__maxY // 2 + self.__yourSize // 2

        self.setEyePoses()

        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyPress>"  , self.pressed, 1)
        self.__loader.threadLooper.bindingMaster.addBinding(self, self.__topLevelWindow, "<KeyRelease>", self.released, 1)

        #self.__topLevelWindow.bind("<KeyPress>"   , self.pressed  )
        #self.__topLevelWindow.bind("<KeyRelease>" , self.released )

        self.__eyePoz = 0

        self.__keys = {
            "Left": False,
            "Right": False,
            "Up": False,
            "Down": False
        }

        self.__cooldown = 0

        self.__eyesPositioner = {
            #Left   Right  Up     Down
            (False, False, False, False) : 0,
            (True, False, False, False)  : 1,
            (False, True, False, False)  : 2,
            (False, False, True, False)  : 3,
            (False, False, False, True)  : 4,
            (True, False, True, False)   : 5,
            (True, False, False, True)   : 6,
            (False, True, True, False)   : 7,
            (False, True, False, True)   : 8
        }

        self.__loader.threadLooper.addToThreading(self, self.loop, [], 1)

    def setEyePoses(self):

        self.__eyePozes = {
            0: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 1.2,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 1.2,
                ]
            ],
            # Stay in place

            1: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.0, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 1.2,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 1.2,
                ]
            ],
            # Go left

            2: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 1.2,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 0.8,
                    self.__yourX + self.__yourSize // 2 * 2.0, self.__yourY - self.__yourSize // 2 * 1.2,
                ]
            ],
            # go right

            3: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 1.5,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 1.5,
                ]
            ],
            # go up

            4: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 0.6,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 0.6,
                ]
            ],
            # go down

            5: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.0, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 1.5,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 1.5,
                ]
            ],
            # go up / left

            6: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.0, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 0.6,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.2, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 0.6,
                ]
            ],
            # go down / left

            7: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 1.5,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.6, self.__yourY - self.__yourSize // 2 * 1.1,
                    self.__yourX + self.__yourSize // 2 * 2.0, self.__yourY - self.__yourSize // 2 * 1.5,
                ]
            ],
            # go up / right

            8: [
                [
                    self.__yourX + self.__yourSize // 2 * 0.4, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 0.8, self.__yourY - self.__yourSize // 2 * 0.6,
                ],
                [
                    self.__yourX + self.__yourSize // 2 * 1.5, self.__yourY - self.__yourSize // 2 * 0.2,
                    self.__yourX + self.__yourSize // 2 * 1.9, self.__yourY - self.__yourSize // 2 * 0.6,
                ]
            ]
            # go down / right

        }

    def pressed(self, event):
        self.__keys[str(event.keysym)] = True

    def released(self, event):
        self.__keys[str(event.keysym)] = False

    def loop(self):
            self.__counter += 1
            if self.__counter > 3: self.__counter = 0

            self.setEyePoses()

            try:

                self.__color = self.__colors[self.__counter]
                #self.__canvas.clipboard_clear()
                self.__canvas.delete("all")

                self.drawPixelOval()
                self.drawYou()
                self.drawGrid()
            except:
                pass

            try:
                if (
                    self.__keys["Left"]  ==  True or
                    self.__keys["Right"] ==  True or
                    self.__keys["Up"]    ==  True or
                    self.__keys["Down"]  ==  True
                ):
                    if self.__cooldown == 0:
                        self.__loader.soundPlayer.playSound("walk")
                        self.__cooldown = 17
                    else:
                        self.__cooldown -= 1
            except Exception as e:
                print("1", str(e))

            try:
                self.__eyePoz = self.__eyesPositioner[(
                        self.__keys["Left"],
                        self.__keys["Right"],
                        self.__keys["Up"],
                        self.__keys["Down"])]
            except:
                self.__eyePoz = 0

            self.__direction = {
                1: (-2, 0, - 1                   , 0),
                2: (2,  0, self.__yourSize + 1   , 0),
                3: (0, -2, self.__yourSize*0.5   , -self.__yourSize-1),
                4: (0,  2, self.__yourSize*0.5   , 1),
                5: (-2, -2, - 1, 1),
                6: (-2, 2, -1, -self.__yourSize-1),
                7: (2, -2, self.__yourSize + 1, 1),
                8: (2, 2, self.__yourSize + 1, -self.__yourSize-1),

            }

            if self.__eyePoz > 0:
                try:
                    if (self.isThereAWall(
                            self.__yourX + self.__direction[self.__eyePoz][2],
                            self.__yourY + self.__direction[self.__eyePoz][3],
                        ) == 0):
                        self.__yourX += self.__direction[self.__eyePoz][0]
                        self.__yourY += self.__direction[self.__eyePoz][1]

                        if self.__yourX > self.__maxX:
                           self.__yourX = 0

                        if self.__yourY > self.__maxY:
                           self.__yourY = 0

                        if self.__yourX < 0:
                            self.__yourX = self.__maxX

                        if self.__yourY < 0:
                            self.__yourY = self.__maxY

                except Exception as e:
                    print("2", str(e))

    def drawPixelOval(self):
        self.__canvas.create_rectangle(self.__yourX - self.__yourSize//2, self.__yourY - self.__yourSize,
                                       self.__yourX + self.__yourSize*1.5, self.__yourY,
                                       fill=self.__color, width=0)

        self.__canvas.create_rectangle(self.__yourX - self.__yourSize//4, self.__yourY - self.__yourSize*1.5,
                                       self.__yourX + self.__yourSize*1.25, self.__yourY+self.__yourSize//2,
                                       fill=self.__color, width=0)

    def drawYou(self):
        #self.__canvas.create_rectangle(self.__yourX, self.__yourY,
        #                               self.__yourX + self.__yourSize, self.__yourY - self.__yourSize,
        #                               fill=self.__color, width=0)

        self.__canvas.create_rectangle(self.__yourX, self.__yourY-self.__yourSize//4,
                                       self.__yourX + self.__yourSize//2*0.9, self.__yourY-self.__yourSize//4*3,
                                       fill="white", width=0)

        self.__canvas.create_rectangle(self.__yourX + self.__yourSize//2*1.1, self.__yourY-self.__yourSize//4,
                                       self.__yourX + self.__yourSize, self.__yourY-self.__yourSize//4*3,
                                       fill="white", width=0)

        self.__canvas.create_rectangle(self.__eyePozes[self.__eyePoz][0][0], self.__eyePozes[self.__eyePoz][0][1],
                                       self.__eyePozes[self.__eyePoz][0][2], self.__eyePozes[self.__eyePoz][0][3],
                                       fill="black", width=0)

        self.__canvas.create_rectangle(self.__eyePozes[self.__eyePoz][1][0], self.__eyePozes[self.__eyePoz][1][1],
                                       self.__eyePozes[self.__eyePoz][1][2], self.__eyePozes[self.__eyePoz][1][3],
                                       fill="black", width=0)

    def createGrid(self):
        lineTypes = [
            [1,1,0,1],
            [1,0,0,0],
            [0,0,0,0],
            [1,0,0,0]
        ]

        self.__gridArray = []
        for Y in range(0, self.__maxY//self.__step):
            row = []
            for X in range(0, self.__maxX//self.__step):
                row.append(lineTypes[Y%4][X%4])
            self.__gridArray.append(deepcopy(row))

    def isThereAWall(self, x, y):


        if x < 0: x = self.__maxX - x
        if y < 0: y = self.__maxY - y
        if x > self.__maxX: 0
        if y > self.__maxY: 0

        x = x//self.__step
        y = y//self.__step

        x = round(x)
        y = round(y)

        try:
            return(self.__gridArray[y][x])
        except:
            try:
                return(self.__gridArray[y][0])
            except:
                try:
                    return(self.__gridArray[0][x])
                except:
                    return(self.__gridArray[0][0])


    def drawGrid(self):
        # fromX = 0
        # fromY = 0
        # toX   = self.__maxX//self.__step
        # toY   = self.__maxY//self.__step

        fromX = (self.__yourX - 2 * self.__step) // self.__step
        fromY = (self.__yourY - 2 * self.__step) // self.__step
        toX = (self.__yourX + 3 * self.__step) // self.__step
        toY = (self.__yourY + 3 * self.__step) // self.__step

        for Y in range(fromY, toY):
            for X in range(fromX, toX):
                if (self.__gridArray[Y][X] == 1):
                    self.__canvas.create_rectangle(X*self.__step, Y*self.__step,
                                                   (X+1)*self.__step, (Y+1)*self.__step,
                                                   fill = "blue", width=0)

