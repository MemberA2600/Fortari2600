#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from threading import Thread

from sys import path as systemPath

if __name__ == "__main__":
    systemPath.insert(1, "src/Scripts/")
    from Collector import Collector
    Collector(systemPath)
    from Loader import Loader
    __loader = Loader()

    tk = Tk()
    tk.withdraw()
    tk.overrideredirect(True)
    tk.resizable(False, False)
    tk.geometry("%dx%d+%d+%d" % (1,1,1,1))
    __loader.tk = tk

    from Monitor import Monitor
    __screenSize = Monitor().get_screensize()
    __loader.screenSize = __screenSize

    from LoadingScreen import LoadingScreen
    __loading = LoadingScreen(__screenSize, tk, __loader)


    from time import sleep
    from MainWindowHandler import MainWindowHandler
    MainWindowHandler(__loader)