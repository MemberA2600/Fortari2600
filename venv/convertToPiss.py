data = open("fuck.txt", "r").read().replace("\r","").split("\n")

string = ""

for line in data:
    line = line.split(" ")

