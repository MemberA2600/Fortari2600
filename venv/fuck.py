

text = open("f.txt", "r").read().split("\n")

out = ""

for num in range(0, len(text), 2):
	out += text[num]+"\n"

t = open("o.txt", "w")
t.write(out)
t.close()