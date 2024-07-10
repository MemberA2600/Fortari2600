* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
* addManuallyToSysVars=TileSelected
*
	LDA	TileSelected
	AND	#%11100000
	STA	#TEMPVAR1#

	LDA	SubMenuLines
	AND	#%00000011
	TAX	
	LDA	#BANK#_#MAGIC#_Set_Num_Table,x
	STA	#TEMPVAR3#	

	LDA	#VAR01#		
!!!to8bit!!!
#BANK#_#MAGIC#_Decrement_Loop
	CMP	#TEMPVAR3#
	BCC	#BANK#_#MAGIC#_Was_Smaller

	SEC
	SBC	#TEMPVAR3#
	JMP	#BANK#_#MAGIC#_Decrement_Loop
#BANK#_#MAGIC#_Was_Smaller
	STA	#TEMPVAR2#

	JMP	#BANK#_#MAGIC#_Set_Last_One_Jump
#BANK#_#MAGIC#_Set_Num_Table
	BYTE	#6
	BYTE	#12
	BYTE	#18
	BYTE	#24	

#BANK#_#MAGIC#_Set_Last_One_Jump
	LDA	TileSelected
	AND	#%00011111
	CLC
	ADC	#TEMPVAR2#

	CMP	#TEMPVAR3#
	BCC	#BANK#_#MAGIC#_No_Problem

	SEC
	SBC	#TEMPVAR3#	
	SBC	#1
#BANK#_#MAGIC#_No_Problem
	ORA	#TEMPVAR1#
	STA	TileSelected
	