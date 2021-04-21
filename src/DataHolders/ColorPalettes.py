class ColorPalettes:

    def __init__(self, loader):
        self.__loader = loader
        self.__config = loader.config
        self.__dateReader = self.__loader.dataReader

        self.__colors = {}
        import os

        for root, dirs, files in os.walk("config/ColorPalettes/"):
            for file in files:
                self.__colors[".".join(file.split(".")[:-1])] = self.__dateReader.readDataFile(
                    root+os.sep+file
                )


    def getColor(self, key):
        return(self.__colors[self.__config.getValueByKey("colorPalette")][key])