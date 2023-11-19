!!!BCDon!!!
	LDY	#0
!!!LDAVAR2!!!
!!!to8Bit2!!!	
!!!staTEMP!!!
	LDA	#VAR01#
!!!to8Bit1!!!
	CMP	#VARTEMP#
	BCS	#BANK#_Divide_#MAGIC#_End
	SEC
#BANK#_Divide_#MAGIC#_Back
	SBC	#VARTEMP#
	CMP	#VARTEMP#
	BCS	#BANK#_Divide_#MAGIC#_End	
	INY
	BPL	#BANK#_Divide_#MAGIC#_Back
#BANK#_Divide_#MAGIC#_End
!!!TYA!!!
!!!from8bit!!!
!!!TAY!!!	
	#SAVECOMMAND#	#VAR03#
!!!BCDoff!!!