* params=variable|register,variable|stringConst|number|register,variable|stringConst|number|register
* param1=#VAR01#,!!!from8bit!!!
* param2=#VAR02#,!!!to8bit1!!!
* param3=#VAR03#,!!!to8bit2!!!
* direction=FROM
* ifConstParams=2,3
* ifConstFunc=getSubMenuTileData
*
	LDA	#VAR02#
!!!to8bit1!!!
	TAY

	LDA	#VAR03#
!!!to8bit2!!!
#BANK#_#MAGIC#_Loop
	DEY
	BMI	#BANK#_#MAGIC#_Loop_End
	CLC
	ADC	#6
	JMP	#BANK#_#MAGIC#_Loop
#BANK#_#MAGIC#_Loop_End
	TAY	
	
!!!to8bit1!!!
	CMP 	#24
	BCC	#BANK#_#MAGIC#_No24Load
	LDA	#23
#BANK#_#MAGIC#_No24Load
	LSR
	TAX

	TYA	
	ROR	
	BPL	#BANK#_#MAGIC#_ItIsOdd_2
	LDA	Tile1_1,x
	AND	#$F0
	LSR
	LSR
	LSR
	LSR
	JMP	#BANK#_#MAGIC#_WasEven_2
#BANK#_#MAGIC#_ItIsOdd_2
	LDA	Tile1_1,x
	AND	#$0F
#BANK#_#MAGIC#_WasEven_2
!!!from8bit!!!
	STA	#VAR01#
