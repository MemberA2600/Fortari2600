!!!BCDon!!!
	LDY	#VAR02#
	LDA	#VAR01#
!!!to8Bit1!!!
!!!ASLs!!!
	STA	#VARTEMP#
	CMP	#0
	BNE	#BANK#_Multiply_#MAGIC#_Not0
	LDA	#0
	JMP	#BANK#_Multiply_#MAGIC#_End
#BANK#_Multiply_#MAGIC#_Not0
	DEY	
	CPY	#0
	BEQ	#BANK#_Multiply_#MAGIC#_End
	CLC
#BANK#_Multiply_#MAGIC#_Back
	ADC	#VARTEMP#
	DEY	
	BPL	#BANK#_Multiply_#MAGIC#_Back
#BANK#_Multiply_#MAGIC#_End
!!!from8bit!!!
	STA	#VAR03#
!!!BCDoff!!!