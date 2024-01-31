* params=variable|stringConst|number,variable|stringConst|number
* param1=#VAR01#,!!!to8bit1!!!
* param2=#VAR02#,!!!to8bit2!!!
* direction=TO
* ifConstParams=2
* ifConstFunc=setSubMenuTitleData
*
	LDY	#VAR02#
	LDA	#VAR01#
!!!to8bit1!!!
	AND	#%00001111
	TAX
	TYA	
	ROR	
	BPL	#BANK#_#MAGIC#_ItIsOdd_1
	TXA
	ASL
	ASL
	ASL
	ASL
	JMP	#BANK#_#MAGIC#_WasEven_1
#BANK#_#MAGIC#_ItIsOdd_1
	TXA
#BANK#_#MAGIC#_WasEven_1
	STA	#TEMPVAR#	

	TYA	
!!!to8bit2!!!
	CMP 	#24
	BCC	#BANK#_#MAGIC#_No24Load
	LDA	#23
#BANK#_#MAGIC#_No24Load
****	SEC
****	SBC	#1
	LSR
	TAX

	TYA	
	ROR	
	BPL	#BANK#_#MAGIC#_ItIsOdd_2
	LDA	Tile1_1,x
	AND	#$0F
	JMP	#BANK#_#MAGIC#_WasEven_2
#BANK#_#MAGIC#_ItIsOdd_2
	LDA	Tile1_1,x
	AND	#$F0
#BANK#_#MAGIC#_WasEven_2
	ORA	#TEMPVAR#
	STA	Tile1_1,x
