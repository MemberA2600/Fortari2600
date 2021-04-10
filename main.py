#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from threading import Thread

from sys import path as systemPath


if __name__ == "__main__":
    systemPath.insert(1, "src/App/")
    from Collector import Collector
    Collector(systemPath)

    from Monitor import Monitor
    __screenSize = Monitor().get_screensize()

    from LoadingScreenHandler import LoadingScreenHandler
    __lSH = LoadingScreenHandler(__screenSize)

    from Config import Config
    from DataReader import DataReader
    from Dictionary import Dictionary

    __dataReader = DataReader()
    __config = Config(__dataReader)
    __dictionaries = Dictionary(__dataReader, __config)

    from time import sleep
    from MainWindowHandler import MainWindowHandler
    MainWindowHandler(__config, __dictionaries, __screenSize)

    sleep(0.2)
    try:
        __lSH.destroyScreen()
    except:
        pass
