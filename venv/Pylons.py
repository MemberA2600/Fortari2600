def __generateMiniMapGradient(Y):
    patternLen = Y // 2
    step = 8 // patternLen
    if step < 1: step = 1

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

    pattern = {}

    for num in range(0, 8, step):
        pattern[num] = 1

    if step == 1:
        add = patternLen - 8
        keyNum = -1
        while add > 0:
            keyNum += 1
            if keyNum > 7: keyNum = 0
            add -= 1

            pattern[keyNum] += 1

    patternText = ""
    for key in pattern.keys():
        patternText += ("\tBYTE\t#" + patterns[key] + "\n") * pattern[key]

    return (patternText + "\n".join(patternText.split("\n")[::-1]))

print(__generateMiniMapGradient(24))