
x = 0
y = 1

for num in range(0,24):



    first = bin(x).replace("0b", "")
    while len(first)<4:
        first = "0"+first

    second = bin(y).replace("0b", "")
    while len(second)<4:
        second = "0"+second

    print("\tLDX\t#"+str(num)+"\n\tLDA\t#%"+first+second+"\n\tSTA\tTile1_1,x\t; "+str(str(x)+", "+str(y))+"\n")

    x+=2
    y+=2

    if x>15:
        x = x-16

    if y>15:
        y = y-16