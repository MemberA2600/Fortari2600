* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=TO
*
	LDA	TileSelected
	AND	#%11000000
	ROR
	ROR
!!!from8bit!!!
	STA	TileSelected

	
