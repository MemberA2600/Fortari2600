from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from copy import deepcopy
from time import sleep

class ChangeFrameColor:

    def __init__(self, loader, baseFrame, data):

        self.__loader = loader
        self.__baseFrame = baseFrame
        self.__data = data

        print(data)

