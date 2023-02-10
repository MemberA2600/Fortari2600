
def contertDECtoVLQ(num):

    binary = bin(num).replace("0b","")
    while(len(binary) % 7 != 0):
        binary = "0" + binary

    listOf7bits = []

    for indexNum in range(0, len(binary)-6, 7):
        firstBit = "1"
        if indexNum == len(binary)-7:
           firstBit = "0"

        listOf7bits.append(firstBit + binary[indexNum:indexNum+7])

    return(" ".join(listOf7bits))

def convertVLQbitsToDec(bits):
    bitLine = ""
    for indexNum in range(0, len(bits)-7, 8):
        currentByte = bits[indexNum:indexNum+8]
        bitLine    += currentByte[1:]

        if currentByte[0] == "0":
           break

    return int("0b" + bitLine, 2)

if __name__ == "__main__":
    print(contertDECtoVLQ(0))
    print(contertDECtoVLQ(1))
    print(contertDECtoVLQ(16383))
    print(contertDECtoVLQ(2097152))

    print(convertVLQbitsToDec("10000001100000001000000000000000"))