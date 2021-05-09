from tkinter import *

class LeftFrame:

    def __init__(self, loader, frame):
        self.stopThread = False
        self.__loader.stopThreads.append(self)


    def destroy(self):
        del self