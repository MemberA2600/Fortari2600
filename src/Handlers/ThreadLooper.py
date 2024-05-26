from threading import Thread
from time import sleep
import traceback
import psutil

class ThreadLooper:

    def __init__(self, loader):
        self.__loader = loader

        self.__listOfThreads = []
        self.__running      = False

        self.__base = 0.001
        self.__wait = self.__base
        self.__mainInited = False
        self.__maxLevel    = -1
        self.disableAll    = False
        self.wasDisableAll = False

        self.__numOfTopLevels = 0

        from BindingMaster import BindingMaster
        self.bindingMaster = BindingMaster(loader, self)

        t = Thread(target=self.__loop)
        t.daemon = True
        t.start()

    def returnLevel(self):
        if self.__maxLevel < 0: return 0
        return self.__maxLevel

    def addToThreading(self, object, function, args, level):
        for item in self.__listOfThreads:
            if item[0] == object and item[1] == function and item[2] == args:
               return

        if level > self.__maxLevel: self.__maxLevel = level

        self.__listOfThreads.append([object, function, args, level])

    def enableDisable(self):
        forceIt = False

        if self.disableAll != self.wasDisableAll:
           self.wasDisableAll = self.disableAll
           if self.disableAll == True:
               self.__loader.mainWindow.editor.attributes('-disabled', True)
               try:
                   for top in self.__loader.topLevels:
                       top.attributes('-disabled', True)
               except Exception as e:
                  print(str(e))
           else:
               forceIt = True

        if forceIt or self.__numOfTopLevels != len(self.__loader.topLevels):
           self.__numOfTopLevels = len(self.__loader.topLevels)

           if self.__numOfTopLevels == 0:
              self.__loader.mainWindow.editor.attributes('-disabled', False)
              self.__loader.mainWindow.editor.deiconify()
              self.__loader.mainWindow.editor.focus()
           else:
              self.__loader.mainWindow.editor.attributes('-disabled', True)
              for num in range(0, len(self.__loader.topLevels)):
                  if num < len(self.__loader.topLevels) - 1:
                     self.__loader.topLevels[num].attributes('-disabled', True)
                  else:
                     self.__loader.topLevels[num].attributes('-disabled', False)
                     self.__loader.topLevels[num].deiconify()
                     self.__loader.topLevels[num].focus()

    """    
    def track_memory_usage(self):
        import psutil

        # Get the process ID of the current Python process
        pid = psutil.Process().pid
        last_memory = 0

        memory_usage = {}

        while True:
            # Get memory usage of the Python process
            memory_info = psutil.Process(pid).memory_info()
            memory_usage = memory_info.rss

            # Calculate memory increment
            memory_increment = memory_usage - last_memory
            if memory_increment > 0:
                print(f"Python process increased memory by {memory_increment / (1024 * 1024):.2f} MB")

            last_memory = memory_usage
            sleep(0.00005)

    """

    def printInto(self):
        memory_info = psutil.Process().memory_info()
        memory_usage_mb = memory_info.rss / (1024 * 1024)
        print(f"Current memory usage: {memory_usage_mb:.2f} MB")
        # print(len(self.__listOfThreads))
        python_processes = [p for p in psutil.process_iter() if 'python' in p.name()]
        total_threads = sum(p.num_threads() for p in python_processes)
        print("Number of threads:", total_threads)

    def __loop(self):
        number = 0
        t = None

        #from datetime import datetime
        #now = datetime.now()
        #runningTimes = {}
        #debugTime    = False

        #trackMemory = Thread(target=self.track_memory_usage)
        #trackMemory.daemon = True
        #trackMemory.start()

        while True:
            try:
                while self.__loader.mainWindow.dead == False:
                    self.__mainInited = True
                    self.enableDisable()



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

                          """  
                          try:
                              if self.__listOfThreads[number][0].stopMe == True:
                                 stop = True
                              dead = False

                          except:
                              pass
                          """

                          try:
                              if self.__listOfThreads[number][0].stopThread == True:
                                 stop = True
                              dead = False
                          except:
                              pass

                          #print("does:", self.__listOfThreads[number][0], self.__listOfThreads[number][1])
                          #print(self.__maxLevel)
                          if stop or dead:
                             #print(self.__listOfThreads[number][0])
                             currLevel = self.__listOfThreads[number][3]
                             #print("delete:", self.__listOfThreads[number][0], self.__listOfThreads[number][1])
                             if self.__listOfThreads[number][0] in self.__loader.stopThreads:
                                self.__loader.stopThreads.remove(self.__listOfThreads[number][0])
                                try:
                                    if self.__listOfThreads[number][0].getTopLevel() in self.__loader.topLevels:
                                       self.__loader.topLevels.remove(self.__listOfThreads[number][0].getTopLevel())
                                except:
                                    pass

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
                             self.bindingMaster.loop()
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
                                 #if debugTime:
                                 #   if str(self.__listOfThreads[number][1]) not in runningTimes:
                                 #      runningTimes[str(self.__listOfThreads[number][1])] = 0
                                 #      now = datetime.now()

                                 self.__listOfThreads[number][1](*self.__listOfThreads[number][2])

                                 #if debugTime:
                                 #   t = (datetime.now() - now).total_seconds()
                                 #   if t > runningTimes[str(self.__listOfThreads[number][1])]:
                                 #       runningTimes[str(self.__listOfThreads[number][1])] = t
                                 #   print(str(self.__listOfThreads[number][1]), str(runningTimes[str(self.__listOfThreads[number][1])]))
                       else:
                           self.__wait = self.__base
                    else:
                        if self.__loader.config.getValueByKey("runThreads") == "True":
                            try:
                                if t.isAlive() == False:
                                   self.__running = False
                            except:
                                self.__running = False

                    self.bindingMaster.loop()
                    sleep(self.__wait)
                break
            except Exception as e:
                if self.__mainInited: traceback.print_exc()
                sleep(self.__wait)