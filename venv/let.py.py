L = open("letters.txt", "r")
data = L.readlines()
L.close()

new_Data = [
    [], [], [], [], []
]

counter = -1

for line in data:
    if "BYTE" not in line:
        counter = -1
    else:
        counter += 1
        new_Data[counter].append(line)

counter = -1
name1 = "BankXXFont_Left"
name2 = "BankXXFont_Right"

text1 = name1 + "\n"
text2 = name2 + "\n"

for group in new_Data:
    counter += 1
    text1   += name1 + "_Line"+str(counter) + "\n"
    text2   += name2 + "_Line"+str(counter) + "\n"

    for line in group:
        text1 += "\tBYTE\t#%0000" + line[12:16]+"\n"
        text2 += "\tBYTE\t#%" + line[8:12]+"0000\n"


print(text1)
print(text2)