from MenuButton import MenuButton

class ButtonMaker:

    def __init__(self, loader, frame, functionEnter, functionLeave):
        self.__loader = loader
        self.__frame = frame

        self.__functionEnter = functionEnter
        self.__functionLeave = functionLeave

    def createButton(self, image, curretNumContainer, function, bindedVar, invertedBinding, bindedOut, placer, num):

        XPoz = curretNumContainer[0]
        curretNumContainer[0] += 1

        placer[image] = num
        return(MenuButton(
            self.__loader, self.__frame, image, XPoz, function,
            self.__functionEnter, self.__functionLeave, bindedVar, invertedBinding,
            bindedOut
        ))