from tkinter import *

class PianoButton:

    def __init__(self, loader, color, mother, w, note, channel, font, x, y, h):
        self.__loader = loader
        self.__piaNotes = self.__loader.piaNotes
        self.__note = note
        self.__channel = channel

        fontColor = {"black": "white", "white": "black"}[color]

        self.__frame = Frame(mother, width=w, height=h, bg = color)
        self.__frame.pack_propagate(False)
        self.__frame.place(x=x, y=y)


        self.__button = Button(self.__frame, width=9999, bg = color, fg = fontColor,
                               font=font, command=self.__playNote,
                               text=str(channel)+":"+str(note))
        self.__button.pack_propagate(False)
        self.__button.config(text = channel+": "+note)
        self.__button.pack(fill=BOTH)


    def __playNote(self):
        self.__piaNotes.playTia(self.__note, self.__channel)