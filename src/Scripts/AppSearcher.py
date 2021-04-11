class AppSearcher:

    def __init__(self):
        pass

    def getLocationOfExe(self, exe):
        import winapps

        for app in winapps.search_installed(exe):
            if app!="":
                result=self.__Get_App_Path(self.__regexGetInstallLocation(app), exe)
                if result!="":
                    return(result)
        return("")

    def __getAppPath(self, result, application):
        for root, dirs, files in os.walk(result):
            for file in files:
                if file.upper()==application.upper()+".EXE" or str(application.upper()+".EXE") in file.upper():
                    return(str(root + "/" + file).replace("\\", "/"))
        return("")

    def __regexGetInstallLocation(self, app):
        import re
        FindRegex = re.findall(r"install_location=WindowsPath\(\'[a-zA-Z0-9:\/\s\(\)]+\'\)", str(app))
        if len(FindRegex) > 0:
            return(FindRegex[0].replace("install_location=WindowsPath('", "").replace("')", ""))
        return("")

