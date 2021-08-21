#based on https://www.biglist.com/lists/stella/archives/200311/msg00156.html

from threading import Thread
from time import sleep

class TiaState:
    def __init__(self):
        self.init()

    def init(self):
        self.offset = 0
        self.count = 0
        self.last = 1
        self.f = 0
        self.rate = 0


class TiaTone:

    def __init__(self, AUDV, AUDC, AUDF, tv):

        self.poly0 =    [1, -1]
        self.poly1 =    [1, 1, -1]
        self.poly2 =    [16, 15, -1]
        self.poly4 =    [1, 2, 2, 1, 1, 1, 4, 3, -1]
        self.poly5 =    [1, 2, 1, 1, 2, 2, 5, 4, 2,
                        1, 3, 1, 1, 1, 1, 4, -1]
        self.poly9 =    [1, 4, 1, 3, 2, 4, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1,
                        2, 4, 2, 1, 4, 1, 1, 2, 2, 1, 3, 2, 1, 3, 1, 1,
                        1, 4, 1, 1, 1, 1, 2, 1, 1, 2, 6, 1, 2, 2, 1, 2,
                        1, 2, 1, 1, 2, 1, 6, 2, 1, 2, 2, 1, 1, 1, 1, 2,
                        2, 2, 2, 7, 2, 3, 2, 2, 1, 1, 1, 3, 2, 1, 1, 2,
                        1, 1, 7, 1, 1, 3, 1, 1, 2, 3, 3, 1, 1, 1, 2, 2,
                        1, 1, 2, 2, 4, 3, 5, 1, 3, 1, 1, 5, 2, 1, 1, 1,
                        2, 1, 2, 1, 3, 1, 2, 5, 1, 1, 2, 1, 1, 1, 5, 1,
                        1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 2, 1, 1, 1, 1,
                        4, 2, 1, 1, 3, 1, 3, 6, 3, 2, 3, 1, 1, 2, 1, 2,
                        4, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 2, 1, 4, 2, 2,
                        3, 4, 1, 1, 4, 1, 2, 1, 2, 2, 2, 1, 1, 4, 3, 1,
                        4, 4, 9, 5, 4, 1, 5, 3, 1, 1, 3, 2, 2, 2, 1, 5,
                        1, 2, 1, 1, 1, 2, 3, 1, 2, 1, 1, 3, 4, 2, 5, 2,
                        2, 1, 2, 3, 1, 1, 1, 1, 1, 2, 1, 3, 3, 3, 2, 1,
                        2, 1, 1, 1, 1, 1, 3, 3, 1, 2, 2, 3, 1, 3, 1, 8,
                        -1]
        self.poly68 =   [5, 6, 4, 5, 10, 5, 3, 7, 4, 10, 6, 3, 6, 4, 9,
                         6, -1]

        self.poly465 =  [2, 3, 2, 1, 4, 1, 6, 10, 2, 4, 2, 1, 1, 4, 5,
                         9, 3, 3, 4, 1, 1, 1, 8, 5, 5, 5, 4, 1, 1, 1,
                         8, 4, 2, 8, 3, 3, 1, 1, 7, 4, 2, 7, 5, 1, 3,
                         1, 7, 4, 1, 4, 8, 2, 1, 3, 4, 7, 1, 3, 7, 3,
                         2, 1, 6, 6, 2, 2, 4, 5, 3, 2, 6, 6, 1, 3, 3,
                         2, 5, 3, 7, 3, 4, 3, 2, 2, 2, 5, 9, 3, 1, 5,
                         3, 1, 2, 2, 11, 5, 1, 5, 3, 1, 1, 2, 12, 5, 1,
                         2, 5, 2, 1, 1, 12, 6, 1, 2, 5, 1, 2, 1, 10, 6,
                         3, 2, 2, 4, 1, 2, 6, 10, -1]

        self.divisors = [1, 1, 15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1]

        self.polys = [  self.poly0, self.poly4, self.poly4, self.poly465,
                        self.poly1, self.poly1, self.poly2, self.poly5,
                        self.poly9, self.poly5, self.poly2, self.poly0,
                        self.poly1, self.poly1, self.poly2, self.poly68 ]

        if tv == "PAL":
            self.tiaFreq = 31200  #31113.1 ?
        else:
            self.tiaFreq = 31440  #31399.5 ?

        self.outputFreq = 44100
        self.size = 44100

        self.buffer = "0"*self.size
        self.state = TiaState()
        self.i = 0
        self.AUDV = AUDV
        self.AUDC = AUDC
        self.AUDF = AUDF

        self.position = 0

        self.fillBuffer()

    def fillBuffer(self):
        self.value = 0
        while (self.size>0):
            self.state.f+=1
            if (self.state.f == self.divisors[self.AUDC] * (self.AUDF + 1)):
                self.poly = self.polys[self.AUDC]
                self.state.f = 0

                self.state.count+=1
                if (self.state.count == self.poly[self.state.offset]):
                    self.state.offset+=1
                    self.state.count = 0
                    if (self.poly[self.state.offset] == -1):
                        self.state.offset = 0

                if (self.state.offset&0x01) == 0:
                    self.state.last = 1
                else:
                    self.state.last = 0

            self.state.rate+=self.outputFreq

            while((self.state.rate >= self.tiaFreq) and self.size>0):
                if self.state.last:
                    self.buffer += str(self.AUDV << 3)
                    #self.buffer += bin(self.AUDV << 3).replace("0b","")

                    
                else:
                    self.buffer += "0"

                self.state.rate -= self.tiaFreq
                self.size -= 1


    def playBuffer(self):
        import numpy as np
        import simpleaudio as sa
        pass


if __name__ == "__main__":
    T = TiaTone(8,4,4,"NTSC")
    print(T.buffer)
    T.playBuffer()