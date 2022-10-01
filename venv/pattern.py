def generatePattern(numOfLines):
    from datetime import datetime
    from random import randint

    time = datetime.now()
    importantNum = int(str(time).split(".")[-1]) % 2

    patternSize = (numOfLines // 2 + numOfLines % 2) - 1

    patterns = {
        0: "$00",
        1: "$02",
        2: "$04",
        3: "$06",
        4: "$08",
        5: "$0A",
        6: "$0C",
        7: "$0E",
    }

    changer = [[1, 1, -1], [1, -1, -1]]

    currentNum = importantNum * 7
    changerList = changer[importantNum]

    listOfNums = [patterns[currentNum]]

    for num in range(0, patternSize):
        r = randint(0, 2)
        currentNum += changerList[r]
        if currentNum < 0: currentNum = 1
        if currentNum > 7: currentNum = 6

        listOfNums.append(patterns[currentNum])

    result = ""
    if numOfLines % 2 == 0:
        result = "|".join(listOfNums) + "|" + "|".join(listOfNums[::-1])
    else:
        result = "|".join(listOfNums[:-1]) + "|" + "|".join(listOfNums[::-1])

    print(result)

if __name__ == "__main__":
    generatePattern(11)