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

        from threading import Thread

        t = Thread(target=self.loopThings)
        t.daemon = True
        t.start()

    def loopThings(self):
        from time import sleep
        num = 0

        while self.dead == False:
            try:
                self.__label.config(image=self.__rainbow[num])
                num += 1
                if num == 39:
                   num = 0

                sleep(0.05)
            except:
                pass