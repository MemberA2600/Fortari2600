import os

class AutoSetter:

    def __init__(self, config, fileDialogs):
        self.__config = config
        self.__fileDialogs = fileDialogs

        from AppSearcher import AppSearcher
        self.__appSearcher = AppSearcher()

        self.__config.setAutoSetter(self, self.__fileDialogs)

    def run(self):
        if self.__config.getValueByKey("emulator") == "" or os.path.exists(self.__config.getValueByKey("emulator")) == False:
            self.__setEmulator()
            self.__detectProjects()


    def __setEmulator(self):
        result =self.__appSearcher.getLocationOfExe("Stella")
        if result =="":
            result = "emulator/"+str(self.__detectOsBits())+"-bit/Stella.exe"

        if os.path.exists(result) == False:
            result = ""

        if result == "":
            if self.__fileDialogs.askYesOrNo("emulator", "emulatorNotFound") == "Yes":
                self.__config.setKey("emulator", self.__fileDialogs.askForFileName("openEmulator", False, ["exe", "*"], "*"))


        self.__config.setKey("emulator", result)

    def __detectProjects(self):
        if len(self.__config.getProjects()) == 0:
            for root, dirs, files in os.walk("projects/", topdown=False):
                if root!="projects/":
                    continue
                for dir in dirs:
                    self.__config.addProject(dir, str(root+dir)+"/")

    def __detectOsBits(self):
        import struct
        return(struct.calcsize("P") * 8)