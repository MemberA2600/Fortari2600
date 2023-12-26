from datetime import datetime

rand          = datetime.now().microsecond%256
counter       = (rand * 34894135474168464869461354684768768)%256

numberOfTests = 0
results       = {}

while numberOfTests < 100000000:
    numberOfTests += 1
    counter += 1

    counter %= 256

    rem    = rand%2
    rand //= 2

    if rem: rand  ^= 0xd4
    rand  %= 256

    #rand ^= counter
    if rand not in results:
       results[rand] = 0

    results[rand] += 1
    if numberOfTests%1000000 == 0: print(str(numberOfTests//1000000) + "%")

min = 999999999999999
max = 0
for item in results:
    if min > results[item]: min = results[item]
    if max < results[item]: max = results[item]

    print(item, results[item])

print(">>", str(min), str(max), str(max-min))
