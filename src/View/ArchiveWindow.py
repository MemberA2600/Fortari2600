from tkinter import *
from SubMenu import SubMenu
from threading import Thread
from shutil import rmtree
import os
from distutils.dir_util import copy_tree
from py7zr import py7zr
from datetime import datetime

class ArchiveWindow:

    def __init__(self, loader):
        self.__loader = loader

        try:
            rmtree("temp/archive/")
        except:
            pass

        self.dead = False
        self.__counter = 0
        self.changed = False
        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize*0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize*0.65), False, False, False)
        self.__tinyFont = self.__fontManager.getFont(int(self.__fontSize*0.45), False, False, False)

        self.__sizes = {
            "common": [self.__screenSize[0] // 3, self.__screenSize[1]//2]
        }
        self.__buffer = self.__loader.tapeFrames
        self.__imgIndex = 0
        self.__mode = ""
        self.__finished = True
        self.__archivedDone = False

        self.__window = SubMenu(self.__loader, "archive", self.__sizes["common"][0],
                                self.__sizes["common"][1], None, self.__addElements, 1)

        self.__loader.collector.restoreSystemPath()
        self.dead = True

    def __closeWindow(self):
        if self.__finished == True:
            self.dead = True
            self.__topLevelWindow.destroy()
            self.__loader.topLevels.remove(self.__topLevelWindow)

    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()
        self.__topLevelWindow.protocol('WM_DELETE_WINDOW', self.__closeWindow)

        self.__tapeFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= self.__screenSize[1]//4 )
        self.__tapeFrame.pack_propagate(False)
        self.__tapeFrame.pack(side=TOP, anchor=N, fill=X)

        self.__tapeLabel = Label(self.__tapeFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width=999999                                 ,
                                 image = self.__buffer[0],
                                 height= 999999999)
        self.__tapeLabel.pack_propagate(False)
        self.__tapeLabel.pack(side=LEFT, fill=Y, anchor=W)

        self.__bottomFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"),
                                 height= self.__screenSize[1]//4 )
        self.__bottomFrame.pack_propagate(False)
        self.__bottomFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__frame1 = Frame(self.__bottomFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width = self.__screenSize[0] // 6 )
        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=LEFT, anchor=E, fill=Y)

        self.__frame2 = Frame(self.__bottomFrame, bg=self.__loader.colorPalettes.getColor("window"),
                                 width = self.__screenSize[0] // 6 )
        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=LEFT, anchor=E, fill=Y)

        self.__dateLabel = Label(self.__frame1, bg=self.__loader.colorPalettes.getColor("window"),
                                 fg = self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("archivedDates"),
                                 font = self.__normalFont)
        self.__dateLabel.pack_propagate(False)
        self.__dateLabel.pack(side=TOP, anchor=N, fill=X)

        self.__listBoxFrame = Frame(self.__frame1, bg=self.__loader.colorPalettes.getColor("window"),
                                 width = self.__screenSize[0] // 6, height = 99999999 )
        self.__listBoxFrame.pack_propagate(False)
        self.__listBoxFrame.pack(side=BOTTOM, anchor=S, fill=BOTH)

        self.__scrollBar = Scrollbar(self.__listBoxFrame)
        self.__listBox = Listbox(   self.__listBoxFrame, width=100000,
                                    height=1000,
                                    yscrollcommand=self.__scrollBar.set,
                                    selectmode=BROWSE,
                                    exportselection = False,
                                    font = self.__smallFont
                                    )
        self.__listBox.config(bg=self.__loader.colorPalettes.getColor("boxBackNormal"))
        self.__listBox.config(fg=self.__loader.colorPalettes.getColor("boxFontNormal"))
        self.__listBox.pack_propagate(False)

        self.__scrollBar.pack(side=RIGHT, anchor=W, fill=Y)
        self.__listBox.pack(side=LEFT, anchor=W, fill=BOTH)

        self.__scrollBar.config(command=self.__listBox.yview)

        self.__title1 = Label(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 fg = self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("numberOfFiles"),
                                 font = self.__normalFont)
        self.__title1.pack_propagate(False)
        self.__title1.pack(side=TOP, anchor=N, fill=X)

        self.__var1 = StringVar()
        self.__dataLabel1 = Label(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 fg = self.__loader.colorPalettes.getColor("font"),
                                 textvariable = self.__var1,
                                 font = self.__normalFont)
        self.__dataLabel1.pack_propagate(False)
        self.__dataLabel1.pack(side=TOP, anchor=N, fill=X)


        self.__title2 = Label(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 fg = self.__loader.colorPalettes.getColor("font"),
                                 text = self.__dictionaries.getWordFromCurrentLanguage("sizeOfFiles"),
                                 font = self.__normalFont)
        self.__title2.pack_propagate(False)
        self.__title2.pack(side=TOP, anchor=N, fill=X)

        self.__var2 = StringVar()
        self.__dataLabel2 = Label(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 fg = self.__loader.colorPalettes.getColor("font"),
                                 textvariable = self.__var2,
                                 font = self.__normalFont)
        self.__dataLabel2.pack_propagate(False)
        self.__dataLabel2.pack(side=TOP, anchor=N, fill=X)

        self.__buttonFrame1 = Frame(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 width = 999999999,
                                 height =   self.__screenSize[1] // 20 )
        self.__buttonFrame1.pack_propagate(False)
        self.__buttonFrame1.pack(side=BOTTOM, anchor=S, fill=X)

        self.__buttonFrame2 = Frame(self.__frame2, bg=self.__loader.colorPalettes.getColor("window"),
                                 width = 999999999,
                                 height =   self.__screenSize[1] // 20 )
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=BOTTOM, anchor=S, fill=X)

        self.__button1 = Button(self.__buttonFrame1, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=9999, height = 9999,
                                   text = self.__dictionaries.getWordFromCurrentLanguage("archieveCurrent"),
                                   command = self.__archive, font = self.__normalFont)
        self.__button1.pack_propagate(False)
        self.__button1.pack(fill=BOTH)

        self.__button2 = Button(self.__buttonFrame2, bg=self.__loader.colorPalettes.getColor("window"),
                                   width=9999, height = 9999,
                                   text = self.__dictionaries.getWordFromCurrentLanguage("restore"),
                                   command = self.__restore, font = self.__normalFont)
        self.__button2.pack_propagate(False)
        self.__button2.pack(fill=BOTH)

        self.fillListBox()

        self.__loader.threadLooper.addToThreading(self, self.loop, [])
        #t = Thread(target=self.loop)
        #t.daemon = True
        #t.start()

    def __archive(self):
        self.__mode = ">>"
        self.__finished = False

        t = Thread(target=self.__archiveThread)
        t.daemon = True
        t.start()

    def __restore(self):
        self.__mode = "<<"
        self.__finished = False

        t = Thread(target=self.__restoreThread)
        t.daemon = True
        t.start()

    def __restoreThread(self):
        self.__soundPlayer.playSound("rewind")
        try:
            name = self.__fileNames[self.__listBox.curselection()[0]]
            name = name[0:4] + name[5:7] + name[8:10] + name[11:13] + name[14:16] + name[17:19] + ".7z"

            from time import sleep

            sleep(1)

            archive = py7zr.SevenZipFile(self.__loader.mainWindow.projectPath+"archives/"+name, mode='r')
            archive.extractall(path=self.__loader.mainWindow.projectPath)
            archive.close()

            self.__mode = ""
            self.fillListBox()
        except Exception as e:
            print(str(e))

        self.__finished = True

    def __archiveThread(self):
        self.__soundPlayer.playSound("forward")
        try:
            os.mkdir("temp/archive")
            copy_tree(self.__loader.mainWindow.projectPath, "temp/archive")
            for root, dirs, files in os.walk("temp/archive/", topdown=False):
                if root == "temp/archive/archives":
                    for file in files:
                        os.remove("temp/archive/archives/"+file)
                    os.removedirs(root)

            name = str(datetime.now())
            name = name[0:4] + name[5:7] + name[8:10] + name[11:13] + name[14:16] + name[17:19] + ".7z"

            with py7zr.SevenZipFile(self.__loader.mainWindow.projectPath+"/archives/"+name, 'w') as archive:
                archive.writeall("temp/archive", self.__loader.mainWindow.projectPath.split("/")[-1])

            rmtree("temp/archive/")
            self.__button1.config(state = DISABLED)
            self.__archivedDone = True
            self.__mode = ""
            self.fillListBox()
        except Exception as e:
            print(str(e))

        self.__finished = True

    def getNumAndSize(self):
        import os
        num = 0
        size = 0

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath, topdown=False):
            if root != self.__loader.mainWindow.projectPath+"archives":
               for file in files:
                   num  += 1
                   size += os.path.getsize(root +     "/" + file)

        self.__var1.set(str(num))
        sizes = ("bytes", "KB", "MB")
        ind = 0
        if size > 1024:
           size /= 1024
           ind = 1

        if size > 1024:
           size /= 1024
           ind = 2

        dot = 0
        stopDot = False
        more = 0

        for char in str(size):
            if char == '.':
               stopDot = True
               more = dot
            else:
               if stopDot == False:
                  dot += 1
               else:
                  more +=1
                  if more > dot + 3:
                      break



        self.__var2.set(str(size)[:more+1] + " "+sizes[ind])


    def fillListBox(self):
        import os

        self.__listBox.select_clear(0, END)
        self.__listBox.delete(0, END)
        self.__fileNames = []

        for root, dirs, files in os.walk(self.__loader.mainWindow.projectPath+"/archives/", topdown=False):
            for name in files:
                if ".7z" in name:
                    name =  name[0:4]+"-"+name[4:6]+"-"+name[6:8]+"_"+name[8:10]+":"+name[10:12]+":"+name[12:14]

                    self.__fileNames.append(name)

            if len(self.__fileNames) > 0:
                self.__fileNames.sort(reverse=True)
                for name in self.__fileNames:
                    self.__listBox.insert(END, name)

                self.__listBox.select_set(0)

        self.__data = self.getNumAndSize()

    def loop(self):
                if self.__mode == "<<":
                    c = 25
                else:
                    c = 65

                if self.__counter > c:
                    self.__counter = 0
                    if self.__mode == "<<":
                       self.__imgIndex -= 1

                       if self.__imgIndex < 0: self.__imgIndex = 29
                       self.__tapeLabel.config(image = self.__buffer[self.__imgIndex])
                    elif self.__mode == ">>":
                       self.__imgIndex += 1
                       if self.__imgIndex > 29: self.__imgIndex = 0

                       self.__tapeLabel.config(image = self.__buffer[self.__imgIndex])
                else:
                    self.__counter+=1

                if self.__finished == True:
                   self.__button2.config(state = NORMAL)
                   if self.__archivedDone == False:
                      self.__button1.config(state=NORMAL)
                else:
                    self.__button1.config(state=DISABLED)
                    self.__button2.config(state=DISABLED)
