from tkinter import *
from threading import Thread
from SideFrameListBoxWithButtonAndLabel import SideFrameListBoxWithButtonAndLabel
from threading import Thread

class RightFrameEditor:

    def __init__(self, loader, frame, validity, view):
        self.__loader = loader
        self.__frame = frame
        self.__selectedValidity = validity

        self.__originalW = self.__frame.winfo_width()
        self.__originalH = self.__frame.winfo_height()
        self.__loader.frames["rightFrame"] = self

        baseSize = 13

        buttonText="insertVar"
        if view == "MemorySetter":
            buttonText = "selectVar"

        self.variables = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "variables", 0.50,
                         self.fillListBoxWithVariableNames,
                         self.loadVariableData,
                         self.insertStuff,
                         buttonText)

        buttonText="insertArray"
        if view == "MemorySetter":
            buttonText = "selectArray"

        self.arrays = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "arrays", 0.25,
                         self.fillListBoxWithArrays,
                         self.loadArrayData,
                         self.insertStuff,
                         buttonText)

        buttonText="insertSub"
        if view == "SubroutineEditor":
            buttonText = "selectSub"

        self.subs = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "subs", 0.25,
                         self.fillListBoxWithSubs,
                         self.loadSubRoutineData,
                         self.insertStuff,
                         buttonText)

        """
        self.banklinks = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "bankLinks", 0.20,
                         self.fillListBoxWithBankLinks,
                         self.loadBankLinkData,
                         self.insertStuff,
                         "insertBankLinks")
        """
    def destroy(self):
        del self

    def insertStuff(self, listBox, data):
        self.__loader.currentEditor.insert(INSERT, data[listBox.curselection()[0]].split(" ")[0])


    def fillListBoxWithSubs(self, listBox, handler):
        pass

    """
    def fillListBoxWithBankLinks(self, listBox, handler):
        pass
    """

    def loadSubRoutineData(self, listBox, data):
        pass

    def loadBankLinkData(self, listBox, data):
        pass

    def fillListBoxWithVariableNames(self, listBox, handler):

        self.variableListBox = listBox
        self.variableList = []

        for address in self.__loader.virtualMemory.memory.keys():
            for var in self.__loader.virtualMemory.memory[address].variables.keys():
                if ((self.__loader.virtualMemory.memory[address].variables[var].validity == self.__selectedValidity or
                     self.__loader.virtualMemory.memory[address].variables[var].validity == "global"
                )
                     and
                        self.__loader.virtualMemory.memory[address].variables[var].iterable == True):
                    #print(var, self.__loader.virtualMemory.memory[address].variables[var].validity)
                    self.variableList.append(var+" ("+address+", "+
                         self.__loader.virtualMemory.memory[address].variables[var].type+")")

        self.variableList.sort()
        self.variableListBox.select_clear(0, END)
        self.variableListBox.delete(0, END)
        for item in self.variableList:
            self.variableListBox.insert(END, item)

        handler.data = self.variableList

    def loadVariableData(self, listBox, data):
        variableFrame = self.__loader.frames["VariableFrame"]
        variableFrame.varName.setEntry(
            self.variables.getSelectedName().split(" ")[0]
        )


    def fillListBoxWithArrays(self, listBox, handler):
        self.arrayListBox = listBox
        self.arrayList = []

        for name in self.__loader.virtualMemory.arrays.keys():
            if self.__loader.virtualMemory.getArrayValidity(name) == self.__selectedValidity\
                    or self.__loader.virtualMemory.getArrayValidity(name) == "global":
                self.arrayList.append(name+" (" +self.__loader.virtualMemory.getArrayValidity(name)+ ")")

        self.arrayList.sort()
        self.arrayListBox.select_clear(0, END)
        self.arrayListBox.delete(0, END)
        for item in self.arrayList:
            self.arrayListBox.insert(END, item)

        handler.data = self.arrayList

    def loadArrayData(self, listBox, data):
        arrayFrame = self.__loader.frames["ArrayFrame"]
        arrayFrame.arrName.setEntry(
            self.arrays.getSelectedName().split(" ")[0]
        )

    def getScales(self):
        return(
            self.__frame.winfo_width()/self.__originalW,
            self.__frame.winfo_height() / self.__originalH,
        )

    def checker(self):
        pass