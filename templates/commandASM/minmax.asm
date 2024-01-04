!!!convertCompare!!!	
	LDA	#VAR01#
!!!to8bit!!!
	CMP	#VARTEMP#
	BCS	#BANK#_#MAGIC#_Not_Smaller
!!!extraLDA!!!
!!!from8bit!!!
	STA	#VAR03#
#BANK#_#MAGIC#_Not_Smaller
