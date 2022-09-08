
import random

firstNum = random.randint(0, 256)

num = firstNum
while True:
    if num == 256:
        num = 0
    else:
        num = num + 1

    ggg = bin(num).replace("0b", "")
    while len(ggg) < 8:
        ggg = "0" + ggg

    print(ggg)