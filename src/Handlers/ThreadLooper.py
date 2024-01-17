from threading import Thread
from time import sleep
import traceback

class ThreadLooper:

    def __init__(self, loader):
        self.__loader = loader

        self.__listOfThreads = []
        self.__running      = False

        self.__base = 0.001
        self.__wait = self.__base
        self.__mainInited = False
        self.__maxLevel = -1

        t = Thread(target=self.__loop)
        t.daemon = True
        t.start()

    def addToThreading(self, object, function, args, level):
        for item in self.__listOfThreads:
            if item[0] == object and item[1] == function and item[2] == args:
               return

        if level > self.__maxLevel: self.__maxLevel = level

        self.__listOfThreads.append([object, function, args, level])

    def __loop(self):
        number = 0
        t = None

        while True:
            try:
                while self.__loader.mainWindow.dead == False:
                    self.__mainInited = True
                    if self.__running == False:
                       number += 1
                       if number > len(self.__listOfThreads) - 1: number = 0

                       if len(self.__listOfThreads) > 0:
                          self.__wait = self.__base / len(self.__listOfThreads)

                          if self.__listOfThreads[number][3] < self.__maxLevel and self.__listOfThreads[number][3] != -1:
                             sleep(self.__wait)
                             continue

                          stop = False
                          dead = True

                          try:
                              if self.__listOfThreads[number][0].diesWithMainOnly == True:
                                 dead = False
                          except:
                              pass


                          try:
                              if self.__listOfThreads[number][0].dead == True:
                                 stop = True
                              dead = False
                          except:
                              pass

                          try:
                              if self.__listOfThreads[number][0].dead[0] == True:
                                 stop = True
                              dead = False
                          except:
                              pass

                          try:
                              if self.__listOfThreads[number][0].caller.dead == True:
                                 stop = True
                              dead = False
                          except:
                              pass

                          try:
                              if self.__listOfThreads[number][0].stopMe == True:
                                 stop = True
                              dead = False

                          except:
                              pass

                          try:
                              if self.__listOfThreads[number][0].stopThread == True:
                                 stop = True
                              dead = False
                          except:
                              pass

                          #print("does:", self.__listOfThreads[number][0], self.__listOfThreads[number][1])
                          print(self.__maxLevel)

                          if stop or dead:
                             #print(self.__listOfThreads[number][0])
                             currLevel = self.__listOfThreads[number][3]
                             #print("delete:", self.__listOfThreads[number][0], self.__listOfThreads[number][1])
                             self.__listOfThreads.pop(number)

                             found    = False
                             maxLevel = -1
                             for itemNum in range(0, len(self.__listOfThreads)):
                                 if self.__listOfThreads[itemNum][3] > maxLevel: maxLevel = self.__listOfThreads[itemNum][3]
                                 if self.__listOfThreads[itemNum][3] == currLevel:
                                    found = True
                                    #print("found:", self.__listOfThreads[itemNum][0], self.__listOfThreads[itemNum][1])
                                    break

                             if found == False: self.__maxLevel = maxLevel

                             if number > 0: number -= 1
                             sleep(self.__wait)
                             continue
                          else:
                             if self.__loader.config.getValueByKey("runThreads") == "True":
                                 t = Thread(target=self.__listOfThreads[number][1], args=self.__listOfThreads[number][2])
                                 t.daemon = True
                                 t.start()
                                 self.__running = True
                             else:
                                 #print(self.__listOfThreads[number][1])
                                 self.__listOfThreads[number][1](*self.__listOfThreads[number][2])
                       else:
                           self.__wait = self.__base
                    else:
                        if self.__loader.config.getValueByKey("runThreads") == "True":
                            try:
                                if t.isAlive() == False:
                                   self.__running = False
                            except:
                                self.__running = False

                    sleep(self.__wait)
                break
            except Exception as e:
                if self.__mainInited: traceback.print_exc()
                sleep(self.__wait)