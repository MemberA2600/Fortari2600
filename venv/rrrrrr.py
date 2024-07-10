bases = ["PlayerNumberSpacing", "PLAYERNUMBERSPACING", "playerNumberSpacing"]
alreadyDone = []
value = -1

numbers = []

for num in range(1, 32):
    num  = bin(num).replace("0b", "")
    num1 = ""
    num2 = ""

    if len(num) < 5:
       if len(num) < 4:
          num1 = num + ((3 - len(num)) * "0")
          num3 = "00" + num1
       num2 = num + ((5-len(num)) * "0")
       num  = ""

    for n in [num, num1, num2, num3]:
        if n == ""         : continue
        if n in alreadyDone: continue

        if len(n) == 5 and (n[3] == "1" or n[1] == "1"): continue

        alreadyDone.append(n)

        key    =  bases[0] + "_" + n
        alias  = [bases[1] + "_" + n, bases[2] + "_" + n]
        value += 1

        if   len(n) == 3:
             alias.append(bases[1] + "_" + num2)
             alias.append(bases[2] + "_" + num2)
             alreadyDone.append(num2)

        print(key, "|" , value, "|", alias)