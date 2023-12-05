	TAY							
	AND	#MASK1#						
	CMP	#0						
	BEQ	#BANK#_Shift_#MAGIC#_Loop_Not_1			
	LDA	#MASK2#						
	STA	#TEMP#						
	JMP	#BANK#_Shift_#MAGIC#_Loop_Back_To_Business	
#BANK#_Shift_#MAGIC#_Loop_Not_1	
	LDA	#0						
	STA	#TEMP#						
#BANK#_Shift_#MAGIC#_Loop_Back_To_Business	
	TYA							
