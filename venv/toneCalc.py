
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

def getClosest(freq, channel1, channel4, channel6, channel12):
    from copy import deepcopy

    closestOnes = {}
    linking = {1: channel1, 4: channel4, 6: channel6, 12: channel12}
    pairs = {1: 6, 6: 1, 4: 12, 12: 4}

    #lotsOfData = {}
    full = {}
    compare = []

    for num in [1,4,6,12]:
        closestOnes[num] = {}

        for subNum in linking[num]:
            full[str(num)+"|"+subNum] = abs(linking[num][subNum] - freq)
            compare.append(full[str(num)+"|"+subNum])

        for subNum in linking[pairs[num]]:
            full[str(pairs[num])+"|"+subNum] = abs(linking[num][subNum] - freq)
            compare.append(full[str(pairs[num])+"|"+subNum])

        #print(num, full)
        compare.sort()
        compare = deepcopy(compare[0:5])

    closest5 = {}
    for freq in compare:
        for key in full:
           if full[key] == freq:
               closest5[key] = freq

    return(closest5)

def getNotes(freq, listOfNotes):
    array = []

    border = freq / 1000

    level = 0
    smallest = 9999999

    #1
    for freqComp in listOfNotes:
        if abs(listOfNotes[freqComp]-freq)<border:
            return([freqComp])
        else:
            if smallest > abs(listOfNotes[freqComp]-freq):
                level = 1
                smallest = abs(listOfNotes[freqComp]-freq)
                array = [freqComp]

    #2
    for N1 in listOfNotes:
        for N2 in listOfNotes:
            if N1 == N2:
                continue
            freqComp = (listOfNotes[N1] + listOfNotes[N2]) / 2

            if abs(freq-freqComp)<border:
                return([N1, N2])
            else:
                if smallest > abs(freq-freqComp):
                    level = 2
                    smallest = abs(freq-freqComp)
                    array = [N1, N2]
    #3
    for N1 in listOfNotes:
        for N2 in listOfNotes:
            for N3 in listOfNotes:
                if N1 == N2 and N1 == N3:
                    continue
                freqComp = (listOfNotes[N1] + listOfNotes[N2] + listOfNotes[N3]) / 3

                if abs(freq-freqComp)<border:
                    return([N1, N2, N3])
                else:
                    if smallest > abs(freq - freqComp):
                        level = 3
                        smallest = abs(freq - freqComp)
                        array = [N1, N2, N3]

    #4
    for N1 in listOfNotes:
        for N2 in listOfNotes:
            for N3 in listOfNotes:
                for N4 in listOfNotes:
                    if len(set([N1, N2, N3, N4])) < 2:
                        continue
                    freqComp = (listOfNotes[N1] + listOfNotes[N2] + listOfNotes[N3]+ listOfNotes[N4]) / 4

                    if abs(freq-freqComp)<border:
                        return([N1, N2, N3, N4])
                    else:
                        if smallest > abs(freq - freqComp):
                            level = 4
                            smallest = abs(freq - freqComp)
                            array = [N1, N2, N3, N4]

    #5
    for N1 in listOfNotes:
        for N2 in listOfNotes:
            for N3 in listOfNotes:
                for N4 in listOfNotes:
                    for N5 in listOfNotes:

                        if len(set([N1, N2, N3, N4, N5])) < 2:
                            continue
                        freqComp = (listOfNotes[N1] + listOfNotes[N2] + listOfNotes[N3]+ listOfNotes[N4]+listOfNotes[N5]) / 5

                        if abs(freq-freqComp)<border:
                            return([N1, N2, N3, N4, N5])
                        else:
                            if smallest > abs(freq - freqComp):
                                level = 5
                                smallest = abs(freq - freqComp)
                                array = [N1, N2, N3, N4, N5]

    #5
    for N1 in listOfNotes:
        for N2 in listOfNotes:
            for N3 in listOfNotes:
                for N4 in listOfNotes:
                    for N5 in listOfNotes:
                        for N6 in listOfNotes:

                            if len(set([N1, N2, N3, N4, N5, N6])) < 2:
                                continue
                            freqComp = (listOfNotes[N1] + listOfNotes[N2]
                                        + listOfNotes[N3]+ listOfNotes[N4]
                                        +listOfNotes[N5] + listOfNotes[N6]) / 6

                            if abs(freq-freqComp)<border:
                                return([N1, N2, N3, N4, N5, N6])
                            else:
                                if smallest > abs(freq - freqComp):
                                    level = 6
                                    smallest = abs(freq - freqComp)
                                    array = [N1, N2, N3, N4, N5, N6]
    return (array)

if __name__ == "__main__":
    missingOnes = loadToDict("MissingOnes.txt", {})
    channel1 = loadToDict("1.txt", "=")
    channel4 = loadToDict("4.txt", "=")
    channel6 = loadToDict("6.txt", "=")
    channel12 = loadToDict("12.txt", "=")
    pianoKeys = loadToDict("pianoKeys.txt", "=")

    for key in missingOnes:
        missingOnes[key]["freq"] = pianoKeys[key]
        missingOnes[key]["closeNotes"] = getClosest(pianoKeys[key],
                                               channel1, channel4,
                                               channel6, channel12,
                                               )
        missingOnes[key]["solution"] = getNotes(missingOnes[key]["freq"] ,missingOnes[key]["closeNotes"])
        print(key, missingOnes[key]["solution"])
