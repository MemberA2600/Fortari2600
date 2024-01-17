from tkinter import *

class Rainbow:

    def __init__(self, loader, sizes, frame):
        self.__rainbow = []

        for num in range(0, 39):
            num = str(num)
            if len(num) == 1:
                num = "0" + num
            path = "rainbow/" + num

            self.__rainbow.append(loader.io.getImg(path, sizes))

        self.__label = Label(frame, bg=loader.colorPalettes.getColor("window"),
                             width= sizes[0], height=sizes[1],
                             borderwidth=0, highlightthickness=0)
        self.__label.pack_propagate(False)
        self.__label.pack(side=TOP, anchor=N, fill=BOTH)
        self.dead = False
        self.__num = 0

        loader.threadLooper.addToThreading(self, self.loopThings, [], 1)
        #from threading import Thread

        #t = Thread(target=self.loopThings)
        #t.daemon = True
        #t.start()

    def loopThings(self):
            try:
                self.__label.config(image=self.__rainbow[self.__num])
                self.__num += 1
                if self.__num == 39:
                    self.__num = 0
            except:
                self.dead = True