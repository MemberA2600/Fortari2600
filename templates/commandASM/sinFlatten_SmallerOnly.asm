	STA	#TEMPVAR#
	LDA	#128
	SEC
	SBC	#TEMPVAR#
#BANK#_#MAGIC#_DECRLoop_Before
	LSR
	CLC
#BANK#_#MAGIC#_DECRLoop
	STA	#TEMPVAR#
	DEX
	CPX	#0
	BNE	#BANK#_#MAGIC#_DECRLoop_END
	LSR	
	JMP	#BANK#_#MAGIC#_DECRLoop
#BANK#_#MAGIC#_DECRLoop_END
	TAY
	
	LDA	#128
	SEC
	SBC	#TEMPVAR#	
#BANK#_#MAGIC#_Finished
