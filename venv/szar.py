import re

text = "###Start-Bank3\nsas98fsddfsfiodjfosd\n\nsdddfada\t\n###End-Bank3"

print(text)

text = re.findall(r'###Start-Bank3.+###End-Bank3', text, re.DOTALL)

print(text)