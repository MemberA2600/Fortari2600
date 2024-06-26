class BindingMaster:

    def __init__(self, loader, looper):
        self.__loader    = loader
        self.__looper    = looper
        self.__lastLevel = 0

        self.__maxLevel  = 3

#   Currently there are 3 levels of windows, and one level that is out of hierarchy (-1).
        self.__bindings = {}

        for lvl in range(-1, self.__maxLevel + 1):
            self.__bindings[lvl] = [[], False]

        #self.__bindings = {
        #    -1: [[], False], 0: [[], False], 1: [[], False], 2: [[], False], 3: [[], False]
        #}

#   Called from ThreadLooper
    def loop(self):
        level   = self.__looper.returnLevel()
        if self.__lastLevel != level:
            for bindingNum in range(0, len(self.__bindings[self.__lastLevel][0])):
                binding = self.__bindings[self.__lastLevel][0][bindingNum]
                if binding[4] == True:
                    binding[1].unbind_all(binding[2])
                    binding[4] = False
            self.__bindings[level][1] = True

        for lvl in range(-1, self.__maxLevel + 1):
            #print(lvl, len(self.__bindings[lvl][0]))
            if self.__bindings[lvl][1] == True:
               self.__bindings[lvl][1] = False
               for bindingNum in range(0, len(self.__bindings[lvl][0])):
                   binding = self.__bindings[lvl][0][bindingNum]
                   #print(binding)
                   if binding[4] == False:
                      if self.__isItOk(binding[0], binding[1]):
                         binding[4] = True
                         try:
                            binding[1].bind(binding[2], binding[3])
                         except Exception as e:
                            print(binding, str(e))

                      else:
                         binding[1].unbind_all(binding[2])
                         #print(binding[0], binding[1])

        if self.__lastLevel > level:
            self.__bindings[self.__lastLevel] = [[], False]
            #print("fuck", self.__lastLevel, level)

        self.__lastLevel = level

    def __isItOk(self, object, screenItem):
        printMe = False
        try:
            if object.dead == True:
               if printMe: print("1")
               return False
        except:
            pass

        try:
            if object.dead[0] == True:
               if printMe: print("2")
               return False
        except:
            pass

        try:
            if object.caller.dead == True:
               if printMe: print("3")
               return False
        except:
            pass

        """
        try:
            if object.stopMe == True:
               if printMe: print("4")
               return False
        except:
            pass
        """

        try:
            if object.stopThread == True:
               if printMe: print("5")
               return False
        except:
            pass

        return screenItem.winfo_exists()

    def addBinding(self, object, screenItem, bindText, function, level):
        self.__bindings[level][0].append([object, screenItem, bindText, function, False])
        self.__bindings[level][1] = True

    def removeBindingManually(self, object, screenItem, bindText, lvl):
        for bindingNum in range(0, len(self.__bindings[lvl][0])):
            binding = self.__bindings[lvl][0][bindingNum]
            if binding[0] == object and binding[1] == screenItem and binding[2] == bindText:
               self.__bindings[lvl][0].pop(bindingNum)
               screenItem.unbind_all(bindText)
               break