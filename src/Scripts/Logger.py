import os
from datetime import datetime


class Logger:

    def __init__(self, loader):
        self.__loader = loader
        self.deleteOld()

        self.logFileName = "logs"+os.sep+str(datetime.now())[0:10]+"_"+str(datetime.now())[11:19].replace(":","")+".txt"
        file = open(self.logFileName, "w", encoding="latin-1")
        file.close()

    def deleteOld(self):

        for root, dirs, files in os.walk("logs"+os.sep):
            for file in files:
                self.getDaysAndDelete(file[0:10], str(datetime.now())[0:10], root+os.sep+file)


    def getDaysAndDelete(self, filedate, today, file):
        if (self.dateInDays(today) - self.dateInDays(filedate)).days>=int(self.__loader.config.getValueByKey("keepLogs")):
            os.remove(file)

    def dateInDays(self, date):
        years = date.split("-")[0]
        months = date.split("-")[1]
        days = date.split("-")[2]
        from datetime import date

        d = date(int(years), int(months), int(days))
        return(d)


    def addToLog(self, text):
        if self.__loader.config.getValueByKey("debug") == "True":
            try:
                string= "**********************************"+os.linesep
                string+="*** "+ str(datetime.now()) + " ***"+os.linesep
                string+= "**********************************"+os.linesep+os.linesep
                string+=text+os.linesep
                file = open(self.logFileName, "a", encoding="latin-1")
                file.write(string+os.linesep)
                file.close()
            except:
                pass


    def errorLog(self, e):
        text = ""
        text += "Exception: "+str(e)+os.linesep
        text += "Error Class: " + str(e.__class__)+os.linesep
        text += "Variables: " + os.linesep


        for key in ["__name__", "__file__"]:
            var = e.__traceback__.tb_frame.f_globals[key]
            text += key + " = " + str(var) + os.linesep
        for key in e.__traceback__.tb_frame.f_locals:
            if key == "e":
                continue
            var = e.__traceback__.tb_frame.f_locals[key]
            text += key + " = " + str(var) + os.linesep

        self.addToLog(text)
