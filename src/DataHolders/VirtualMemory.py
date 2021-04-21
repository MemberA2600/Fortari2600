from DataItem import DataItem

class VirtualMemory:

    def __init__(self, loader):

        self.__loader = loader
        self.codes = {}
        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.codes[bankNum] = {}
            if (num == 1):
                self.codes[bankNum]["bank_configurations"] = DataItem()
                self.codes[bankNum]["global_variables"] = DataItem()
            else:
                for section in self.__loader.sections:
                    self.codes[bankNum][section] = DataItem()

