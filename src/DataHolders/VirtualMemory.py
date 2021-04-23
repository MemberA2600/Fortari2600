from DataItem import DataItem

class VirtualMemory:

    def __init__(self, loader):

        self.__loader = loader
        self.codes = {}
        self.locks = {}

        for num in range(1,9):
            bankNum = "bank"+str(num)
            self.locks[bankNum] = ""
            self.codes[bankNum] = {}
            if (num == 1):
                self.locks[bankNum] = "System"
                self.codes[bankNum]["bank_configurations"] = DataItem()
                self.codes[bankNum]["global_variables"] = DataItem()
            else:
                for section in self.__loader.sections:
                    self.codes[bankNum][section] = DataItem()

