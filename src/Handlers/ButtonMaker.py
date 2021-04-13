from MenuButton import MenuButton

class ButtonMaker:

    def __init__(self, boss, master, frame, functionEnter, functionLeave):
        self.__boss = boss
        self.__master = master
        self.__frame = frame

        self.__functionEnter = functionEnter
        self.__functionLeave = functionLeave

    def createButton(self, image, XPoz, function, bindedVar, invertedBinding, bindedOut):
        return(MenuButton(
            self.__boss, self.__master, self.__frame, image, XPoz, function,
            self.__functionEnter, self.__functionLeave, bindedVar, invertedBinding,
            bindedOut
        ))