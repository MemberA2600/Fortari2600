
while 1:
    try:
        usedBits = int(input("Number of bits?> "))
    except:
        continue

    usedBits = usedBits%9
    if usedBits < 1: continue

    from random import randint
    binary = bin(randint(0, 256)).replace("0b", "")
    binary = ((8 - len(binary)) * "0" + binary)[-1 * (usedBits):]

    startBit = randint(0, 8-usedBits)
    binary   = ((8 - startBit - len(binary)) * "X") + binary + ((startBit) * "X")

    print(binary)
