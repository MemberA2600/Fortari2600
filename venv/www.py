import re

name    = "common"
element = "main_kernel"
p       = "D:\PyCharm\P\Fortari2600\\"

txt = open(p + "templates/skeletons/" + name + "_" + element + ".asm", "r").read()
remove1 = re.findall(r'###Start-Main-Kernel.+###End-Main-Kernel', txt, re.DOTALL)[0]
remove2 = re.findall(r'###Start-Main-Kernel-Sub.+###End-Main-Kernel-Sub', txt, re.DOTALL)[0]

print(remove1)
print(remove2)

