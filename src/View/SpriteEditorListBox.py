from tkinter import *

class SpriteEditorListBox:

    def __init__(self, loader, motherFrame, font):
        self.__loader = loader


        self.__LBFrame1 = Frame(motherFrame, height=99999999, bg=self.__loader.colorPalettes.getColor("window"),
                                width=round(motherFrame.winfo_width() / 2))
        self.__LBFrame1.pack_propagate(False)
        self.__LBFrame1.pack(side=LEFT, anchor=W, fill=Y)

        while(self.__LBFrame1.winfo_width()==1):
            self.__LBFrame1.config(width=round(motherFrame.winfo_width() / 2))
            self.__LBFrame1.pack(side=LEFT, anchor=W, fill=Y)

        self.__scrollBar = Scrollbar(self.__LBFrame1)

        self.__listBox = Listbox(self.__LBFrame1, width=9999,
                                 yscrollcommand=self.__scrollBar.set,
                                 selectmode=BROWSE,
                                 exportselection=False, font=font
                                 )
        self.__scrollBar.pack(side=RIGHT, anchor=SW, fill=Y)
        self.__listBox.pack_propagate(False)
        self.__listBox.pack(side=LEFT, anchor=SW, fill=BOTH)



    def getListBox(self):
        return self.__listBox

    def getSelected(self):
        return self.__listBox.get(self.__listBox.curselection())