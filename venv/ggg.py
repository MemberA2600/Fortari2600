def checkConst(num, min_, max_, bits):
    startIndex = min(bits)
    endIndex = max(bits)

    as8bits = bin(num).replace("0b", "")

    as8bits = (8 - len(as8bits)) * "0" + as8bits

    if len(bits) != 8:
        slice = as8bits[7 - endIndex: 8 - startIndex]
    else:
        slice = as8bits

    __8bitVal = int("0b" + slice, 2)
    if __8bitVal > max_:
        __8bitVal = max_

    if __8bitVal < min_:
        __8bitVal = min_

    if len(bits) == 8:
        return __8bitVal
    else:
        thatBits = bin(__8bitVal).replace("0b", "")
        if len(thatBits) > len(bits):
            thatBits = thatBits[:-1 * (len(bits))]
        elif len(thatBits) < len(bits):
            thatBits = (len(bits) - len(thatBits)) * "0" + thatBits

        as8bits = as8bits[:7 - endIndex] + thatBits + as8bits[8 - startIndex:]
        return int("0b" + as8bits, 2)


if __name__ == "__main__":
    print(bin(checkConst(int("0b00001110", 2), 2, 8, [4,5,6,7])).replace("0b", "%"))