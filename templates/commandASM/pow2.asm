	LDA	#VAR01#
!!!to8bit!!!
	AND	#%00000111
	TAX
	LDA	#%00000001	; Basically X**0

	CPX	#0
	BEQ	#BANK#_Pow2_#MAGIC#_End

#BANK#_Pow2_#MAGIC#_Loop
!!!ASL!!!
	DEX
	BPL	#BANK#_Pow2_#MAGIC#_Loop
	
#BANK#_Pow2_#MAGIC#_End
!!!from8bit!!!
	STA	#VAR02#
