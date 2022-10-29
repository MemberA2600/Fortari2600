p      = """        BYTE    #$22
        BYTE    #$24
        BYTE    #$26
        BYTE    #$24
        BYTE    #$26
        BYTE    #$28
        BYTE    #$b6
        BYTE    #$28
        BYTE    #$26
        BYTE    #$b8

        BYTE    #$b6
        BYTE    #$b8
        BYTE    #$c6
        BYTE    #$c8
        BYTE    #$c6
        BYTE    #$c4
        BYTE    #$c6
        BYTE    #$b8
        BYTE    #$b6
        BYTE    #$c6

        BYTE    #$c8
        BYTE    #$d8	
        BYTE    #$da
        BYTE    #$c8
        BYTE    #$c6
        BYTE    #$da
        BYTE    #$d8
        BYTE    #$da
        BYTE    #$dc
        BYTE    #$da
                       
        BYTE    #$dc
        BYTE    #$dc"""

p = p.split("\n")

from copy import deepcopy

y = deepcopy(p)

for item in p[::-1]:
    y.append(item)

pattern = "\n".join(y)

print(pattern)
import clipboard

clipboard.copy(pattern)
