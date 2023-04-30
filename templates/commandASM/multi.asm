	LDA	#VAR02#
!!!to8Bit2!!!	
	TAY
	LDA	#VAR01#
!!!to8Bit1!!!
!!!staTEMP!!!
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
