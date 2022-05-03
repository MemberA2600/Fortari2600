def shiftAndTruncateCode(bits):
    if len(bits) == 8: return ""

    txt = ""
    minNum = min(bits)
    maxNum = max(bits)

    numForROL = len(bits) + (7 - maxNum)

    if minNum <= numForROL:
        counter = minNum
        shift = "LSR"
    else:
        counter = numForROL
        shift = "ROL"

    while counter > 0:
        txt += "\t" + shift + "\n"
        counter -= 1

    num = "0" * (8 - len(bits))
    while len(num) < 8:
        num += "1"

    txt += "\tAND\t#%" + num + "\n"
    return txt

while True:
    print("--------------------")
    data = input(">").split(" ")
    for itemNum in range(0, len(data)):
        data[itemNum] = int(data[itemNum])

    print(shiftAndTruncateCode(data))

