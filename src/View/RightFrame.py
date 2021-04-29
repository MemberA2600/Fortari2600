from tkinter import *
from threading import Thread
from SideFrameListBoxWithButtonAndLabel import SideFrameListBoxWithButtonAndLabel

class RightFrame:

    def __init__(self, loader, frame, validity):
        self.__loader = loader
        self.__frame = frame
        self.__selectedValidity = validity


        baseSize = 18

        self.variables = SideFrameListBoxWithButtonAndLabel(loader, frame,
                         baseSize, "variables", 0.45,
                         self.fillListBoxWithVariableNames,
                         self.loadVariableData)



    def fillListBoxWithVariableNames(self, listBox, dataList):

        self.variableListBox = listBox
        self.variableList = []

        for address in self.__loader.virtualMemory.memory.keys():
            for var in self.__loader.virtualMemory.memory[address].variables.keys():
                if self.__loader.virtualMemory.memory[address].variables[var].validity == self.__selectedValidity:
                    #print(var, self.__loader.virtualMemory.memory[address].variables[var].validity)
                    self.variableList.append(var+" ("+address+", "+
                         self.__loader.virtualMemory.memory[address].variables[var].type+")")

        self.variableList.sort()
        self.variableListBox.select_clear(0, END)
        self.variableListBox.delete(0, END)
        for item in self.variableList:
            self.variableListBox.insert(END, item)

        dataList = self.variableList

    def loadVariableData(self, listBox, data):
        pass
