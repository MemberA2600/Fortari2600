#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from threading import Thread

from sys import path as systemPath

if __name__ == "__main__":

    nope = False
    systemPath.insert(1, "src/Scripts/")
    from Collector import Collector
    collector = Collector(systemPath)
    from Loader import Loader
    __loader = Loader()

    tk = Tk()
    tk.withdraw()
    tk.overrideredirect(True)
    tk.resizable(False, False)
    tk.geometry("%dx%d+%d+%d" % (1,1,1,1))

    __loader.tk = tk
    __loader.collector = collector

    from Monitor import Monitor
    __screenSize = Monitor().get_screensize()
    __loader.screenSize = __screenSize

    from LoadingScreen import LoadingScreen
    __loading = LoadingScreen(__screenSize, tk, __loader)

    if __loader.screenSize[0]<1024 or __loader.screenSize[1]<768:
        answer = __loader.fileDialogs.askYesOrNo("screenSizeError", "screenSizeErrorMessage")
        if answer == "No":
            nope = True

    from time import sleep
    if nope == False:

        if __loading.getPresses()[0] == False:
            from MainWindowHandler import MainWindowHandler
            MainWindowHandler(__loader)

        else:
            from KernelTester import KernelTester
            kernelTesterWindow = KernelTester(__loader, __loading.getPresses()[1])
            tk.destroy()
