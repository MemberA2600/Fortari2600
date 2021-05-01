from tkinter import *
from threading import Thread
from SideFrameListBoxWithButtonAndLabel import SideFrameListBoxWithButtonAndLabel
class RightFrame:

    def __init__(self, loader, frame, validity, view):
        self.__loader = loader
        self.__frame = frame
        self.__selectedValidity = validity

        baseSize = 18


        buttonText="insertVar"
        if view == "MemorySetter":
            buttonText = "selectVar"

        self.variables = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "variables", 0.65,
                         self.fillListBoxWithVariableNames,
                         self.loadVariableData,
                         self.insertVariable,
                         buttonText)

        buttonText="insertArray"
        if view == "MemorySetter":
            buttonText = "selectArray"

        self.arrays = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "arrays", 0.33,
                         self.fillListBoxWithArrays,
                         self.loadArrayData,
                         self.insertArray,
                         buttonText)

        self.__loader.frames["rightFrame"] = self


    def fillListBoxWithVariableNames(self, listBox, handler):

        self.variableListBox = listBox
        self.variableList = []

        for address in self.__loader.virtualMemory.memory.keys():
            for var in self.__loader.virtualMemory.memory[address].variables.keys():
                if (self.__loader.virtualMemory.memory[address].variables[var].validity == self.__selectedValidity and
                        self.__loader.virtualMemory.memory[address].variables[var].system == False):
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

    def insertVariable(self, listBox, data):
        pass

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

    def insertArray(self, listBox, data):
        pass