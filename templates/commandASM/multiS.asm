!!!BCDon!!!
	LDA	#VAR01#
!!!to8Bit1!!!	
!!!staTEMP!!!
	TAY
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