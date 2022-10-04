raw = """	byte	#%11111111
	byte	#%11111111
	byte	#%11011111
	byte	#%10001111
	byte	#%00000111
	byte	#%00000111
	byte	#%00000010
	byte	#%00000000
	byte	#%11111111
	byte	#%11101111
	byte	#%10001111
	byte	#%00000110
	byte	#%00000110
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11110111
	byte	#%11100011
	byte	#%01100011
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11110011
	byte	#%11110001
	byte	#%01100000
	byte	#%01100000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11111111
	byte	#%11111110
	byte	#%01111100
	byte	#%00110000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11111111
	byte	#%01111100
	byte	#%00111000
	byte	#%00011000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%10111111
	byte	#%00011100
	byte	#%00011000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11111111
	byte	#%10011111
	byte	#%00001110
	byte	#%00000110
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000"""

raw = raw.replace("\r","").split("\n")
retek = []

for line in raw:
    line = line.split("%")
    line[1] = line[1][::-1]
    retek.append("%".join(line))
retek = "\n".join(retek)

print(retek)