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
                self.codes[bankNum]["enter"] = DataItem()
                self.codes[bankNum]["leave"] = DataItem()
                self.codes[bankNum]["local_variables"] = DataItem()
                self.codes[bankNum]["overscan"] = DataItem()
                self.codes[bankNum]["screen_elements"] = DataItem()
                self.codes[bankNum]["special_read_only"] = DataItem()
                self.codes[bankNum]["subroutines_and_functions"] = DataItem()
                self.codes[bankNum]["vblank"] = DataItem()
