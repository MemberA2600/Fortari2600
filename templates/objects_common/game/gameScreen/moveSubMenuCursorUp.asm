* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
* addManuallyToSysVars=TileSelected
*
	LDA	TileSelected
	AND	#%11100000
	STA	#TEMPVAR1#

***	LDA	SubMenuLines
***	AND	#%00000011
***	STA	#TEMPVAR4#	

	LDA	#VAR01#		
!!!to8bit!!!
	STA	#TEMPVAR2#	

#BANK#_#MAGIC#_GetCurrentLine
	LDA	#TEMPVAR1#
	LDX	#255
#BANK#_#MAGIC#_GetCurrentLine_Loop
	INX
	SEC
	SBC	#6
	BPL	#BANK#_#MAGIC#_GetCurrentLine_Loop	
	STA	#TEMPVAR3#	

	TXA
	SEC
	SBC	#TEMPVAR2#	
	BPL	#BANK#_#MAGIC#_Multi_OK
	LDX	#0	
#BANK#_#MAGIC#_Multi_OK
	TAX
	CLC
#BANK#_#MAGIC#_Multi_Loop
	DEX
	BMI 	#BANK#_#MAGIC#_Multi_Loop_End
	ADC	#6
	JMP	#BANK#_#MAGIC#_Multi_Loop
#BANK#_#MAGIC#_Multi_Loop_End
	ADC	#TEMPVAR3#
	ORA	#TEMPVAR1#
	STA	TileSelected

