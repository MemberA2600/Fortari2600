* params=variable|register,variable|stringConst|number|register
* param1=#VAR01#,!!!from8bit!!!
* param2=#VAR02#,!!!to8bit!!!
* direction=FROM
* ifConstParams=2
* ifConstFunc=getSubMenuTileData
*

	LDA	#VAR02#	
	TAY
!!!to8bit!!!
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
