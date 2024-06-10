def sliceToNumberOfTwoAndRemainder(num):
    remainder = num
    powerOfTwo = 0

    while (remainder%2 == 0):
        powerOfTwo += 1
        remainder  /= 2

    return powerOfTwo, remainder

if __name__ == "__main__":
   print(sliceToNumberOfTwoAndRemainder(48))