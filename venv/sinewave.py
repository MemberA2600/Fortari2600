from math import sin, pi

jumper = (2 * pi) / 256

listOfNums = []

for num in range(0, 256):
    listOfNums.append(sin(num * jumper) + 1)

listOfNums[128] = 1

jumper2 = 255 / 2

byteNums = []

for num in listOfNums:
    byteNums.append(round(jumper2 * num))
    print("\tBYTE\t#" + str(byteNums[-1] ))