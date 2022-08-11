path = "F:\PyCharm\P\Fortari2600\\templates\skeletons\\48pxTextDisplay.asm"

f = open(path, "r")
text = f.read()
f.close()

import re

listOf = re.findall(r'temp\d\d', text, re.IGNORECASE)
listOf = set(listOf)
listOf = list(listOf)
listOf.sort()

print(listOf)