class Dictionary:

    def __init__(self, dataReader, config):
        self.__dataReader = dataReader
        self.__languages = {}
        self.__config = config
        self.__createDictionaries()


    def __createDictionaries(self):
        import os
        for root, dirs, files in os.walk("dictionaries", False):
            for file in files:
                lang = ".".join(file.split(".")[0:-1])
                self.__languages[lang] = self.__dataReader.readDataFile("dictionaries/"+file)

    def getWordFromCurrentLanguage(self, word):
        return(self.__languages[self.__config.getValueByKey("language")][word])

    def saveDictionary(self, name):
        self.__dataReader.writeDataFile("dictionaries/"+name+".txt", self.__languages[name])