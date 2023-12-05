!!!NumOfShifting!!!
	DEX
	BMI	#BANK#_Shift_#MAGIC#_Loop_Nothing
	LDA	#VAR02#
!!!to8bit!!!
#BANK#_Shift_#MAGIC#_Loop
!!!Sub!!!		
	#COMMAND#						
	AND	#MASK3#						
!!!ORA!!!						
	DEX							
	BPL	#BANK#_Shift_#MAGIC#_Loop			
!!!from8bit!!!
	STA	#VAR02#
#BANK#_Shift_#MAGIC#_Loop_Nothing
