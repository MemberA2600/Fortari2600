longFos = open("C:\\temp_NTSC_0089.txt", "r").read().split("\n")

fosok = ["0e", "86", "8a", "88", "06", "03", "09", "0e", "08", "0c"]

index = -1
for oline in longFos:
    index += 1
    firstLineNum = oline[7:12]
    bytes = []

    for lineNum in range(index, len(longFos)):
        if len(bytes) >= len(fosok): break
        fosLine = longFos[lineNum]

        line = fosLine[12:18].split(" ")
        for item in line:
            if item == "" or item.startswith(">>") or len(item) > 2: break
            bytes.append(item)

    if bytes[0] == fosok[0] and  bytes[1] == fosok[1]: print(firstLineNum)