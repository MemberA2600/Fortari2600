	LDA	#!!!Max!!!
	CMP	PßHeight
	BCS	#BANK#_#MAGIC#_SmallerThan
	LDA	#!!!Max!!!
	STA	PßHeight
#BANK#_#MAGIC#_SmallerThan
