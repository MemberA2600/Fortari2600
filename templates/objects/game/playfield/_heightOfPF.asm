	LDA	#!!!Max!!!
	CMP	#255
	BEQ	#BANK#_#MAGIC#_Exit

	CMP	pfIndex
	BCS	#BANK#_#MAGIC#_SmallerThan
	LDA	#!!!Max!!!
	STA	pfIndex
#BANK#_#MAGIC#_SmallerThan
	LDA	pfIndex
	CMP	#!!!Min!!!
	BCS	#BANK#_#MAGIC#_Exit
	LDA	#!!!Min!!!
	STA	pfIndex
#BANK#_#MAGIC#_Exit
