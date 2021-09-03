def loadToDict(f, defItem):
    from copy import deepcopy
    temp = {}

    file = open(f)
    for item in file.read().replace("\r","").split("\n"):
        if item != "":
            if defItem == "=":
                item = item.split("=")
                temp[item[0]] = float(item[1])
            else:
                temp[item] = deepcopy(defItem)

    file.close()
    return(temp)

def getPair()


if __name__ == "__main__":
    channel1 = loadToDict("1.txt", "=")
    channel4 = loadToDict("4.txt", "=")
    channel6 = loadToDict("6.txt", "=")
    channel12 = loadToDict("12.txt", "=")