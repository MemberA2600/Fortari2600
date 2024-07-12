def convertToCommands2(statement, line, saveHere):
    """
    newT = []
    for temp in self.__temps:
        if temp not in statement:
            newT.append(temp)

    self.__temps = newT
    """
    statement = statement.replace("\t", "").replace(" ", "")
    arrList = (self.__loader.config.getValueByKey(
        "validArithmetics") + " ** | || .OR. & && .AND. & && .XOR. ^ ! ~").split(" ")
    while "" in arrList: arrList.remove("")

    sorted(arrList, key=len)

    print(arrList)

if __name__ == "__main__":
    convertToCommands2("5 * (temp01 * temp02) // 3 ** 4", None, None)