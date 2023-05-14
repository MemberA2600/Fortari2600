	LDA	#VAR01#
!!!to8bit!!!
	STA	#TEMP#
	LDX	#255
#BANK#_sqrt_#MAGIC#_Loop
	INX
	CPX	#17
 	BEQ	#BANK#_sqrt_#MAGIC#_End
	
	LDA	#BANK#_sqrt_Table,x
	CMP	#TEMP#
	BCC	#BANK#_sqrt_#MAGIC#_End
	JMP	#BANK#_sqrt_#MAGIC#_Loop

#BANK#_sqrt_#MAGIC#_End
	DEX
	TXA
!!!from8bit!!!
	STA	#VAR02#
