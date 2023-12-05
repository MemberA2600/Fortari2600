	LDA	#VAR01#
!!!to8bit1!!!
	TAX
	DEX
	BMI	#BANK#_Shift_#MAGIC#_Loop_Nothing
	LDA	#VAR02#
!!!to8bit2!!!
#BANK#_Shift_#MAGIC#_Loop
	#COMMAND#
	DEX	
	BPL	#BANK#_Shift_#MAGIC#_Loop
!!!from8bit!!!
	STA	#VAR02#
#BANK#_Shift_#MAGIC#_Loop_Nothing
