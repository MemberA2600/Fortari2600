from threading import Thread
from time import sleep
import traceback

class ThreadLooper:

    def __init__(self, loader):
        self.__loader = loader

        self.__listOfThreads = []
        self.__running      = False

        self.__base = 0.01
        self.__wait = self.__base
        self.__mainInited = False

        t = Thread(target=self.__loop)
        t.daemon = True
        t.start()

    def addToThreading(self, object, function, args):
        for item in self.__listOfThreads:
            if item[0] == object and item[1] == function and item[2] == args:
               return

        self.__listOfThreads.append([object, function, args])

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

                          if stop or dead:
                             #print(self.__listOfThreads[number][0])
                             self.__listOfThreads.pop(number)
                             if number > 0: number -= 1
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