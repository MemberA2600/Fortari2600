from MenuButton import MenuButton

class ButtonMaker:

    def __init__(self, loader, frame, functionEnter, functionLeave):
        self.__loader = loader
        self.__frame = frame

        self.__functionEnter = functionEnter
        self.__functionLeave = functionLeave

    def createButton(self, image, XPoz, function, bindedVar, invertedBinding, bindedOut):
        return(MenuButton(
            self.__loader, self.__frame, image, XPoz, function,
            self.__functionEnter, self.__functionLeave, bindedVar, invertedBinding,
            bindedOut
        ))