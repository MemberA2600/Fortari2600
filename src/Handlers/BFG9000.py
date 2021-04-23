from tkinter import *

class BFG9000:

    def __init__(self, loader, editor, editorHandler, minus):
        self.__loader = loader
        self.__editor = editor
        self.__editorHandler = editorHandler

        self.__w = self.__editorHandler.getWindowSize()[0]*0.66
        self.__h = self.__editorHandler.getWindowSize()[1]-minus-25

        self.__lastScaleX = self.__editorHandler.getScales()[0]
        self.__lastScaleY = self.__editorHandler.getScales()[1]

        self.__mainFrame = Frame(self.__editor, width=self.__w, height=self.__h,
                                 bg = self.__loader.colorPalettes.getColor("window"),
                                 #fg=self.__loader.colorPalettes.getColor("font"),
                                 )

        #self.__mainFrame.config(bg="red")

        self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
        self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()


        self.__mainFrame.pack(side=BOTTOM, anchor=S, fill=Y)
        self.__first = True

        from threading import Thread
        t = Thread(target=self.checker)
        t.daemon = True
        t.start()

        r = Thread(target=self.resizer)
        r.daemon = True
        r.start()


    def checker(self):
        from time import sleep
        while self.__editorHandler.dead==False:
            if self.__first == True or (
                    self.__selectedBank != self.__loader.listBoxes["bankBox"].getSelectedName() or
                    self.__selectedSection != self.__loader.listBoxes["sectionBox"].getSelectedName()
            ):
                self.__first = False
                self.__selectedBank = self.__loader.listBoxes["bankBox"].getSelectedName()
                self.__selectedSection = self.__loader.listBoxes["sectionBox"].getSelectedName()
                print(self.__selectedBank, self.__selectedSection)

            sleep(0.4)

    def resizer(self):
        from time import sleep
        while self.__editorHandler.dead == False:
            if (self.__lastScaleX != self.__editorHandler.getScales()[0] or
                self.__lastScaleY != self.__editorHandler.getScales()[1]):
                    self.__lastScaleX = self.__editorHandler.getScales()[0]
                    self.__lastScaleY = self.__editorHandler.getScales()[1]

                    self.__mainFrame.config(
                        width=self.__w * self.__lastScaleX,
                        height=self.__h * self.__lastScaleY
                    )
                    sleep(0.02)
                    continue

            sleep(0.05)