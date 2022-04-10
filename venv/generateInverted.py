
for num in range(0,256):
    binary = bin(num).replace("0b", "")
    while len(binary)<8:
        binary = "0" + binary

    print("\tBYTE\t#%"+binary[::-1])