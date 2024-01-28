	LDA	#!!!Max!!!
	CMP	#TEMPVAR#
	BCS	#BANK#_#MAGIC#_SmallerThan
	LDA	#!!!Max!!!
	STA	#TEMPVAR#
#BANK#_#MAGIC#_SmallerThan
