!!!TEMPVARLOAD!!!
	LDX	#VAR#
!!!INCR!!!
!!!to8Bit1!!!
#BANK#_Pow_#MAGIC#_Loop
!!!DECR!!!
!!!Multi!!!
	JMP	#BANK#_Pow_#MAGIC#_Loop
#BANK#_Pow_#MAGIC#_End
!!!TEMPVARSAVE!!!
