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

    from pyglet import font as PyFont
    PyFont.add_file('others/font/HammerFat.ttf')

    tk = Tk()
    tk.withdraw()
    tk.overrideredirect(True)
    tk.resizable(False, False)
    tk.geometry("%dx%d+%d+%d" % (1,1,1,1))

    from Monitor import Monitor
    __screenSize = Monitor().get_screensize()

    from LoadingScreenHandler import LoadingScreenHandler
    __lSH = LoadingScreenHandler(__screenSize, tk)

    from Config import Config
    from DataReader import DataReader
    from Dictionary import Dictionary
    from SoundPlayer import SoundPlayer

    __dataReader = DataReader()
    __config = Config(__dataReader)
    __dictionaries = Dictionary(__dataReader, __config)
    __soundPlayer = SoundPlayer(__config)

    from time import sleep
    from MainWindowHandler import MainWindowHandler
    MainWindowHandler(__config, __dictionaries, __screenSize, __lSH, tk, __soundPlayer)
