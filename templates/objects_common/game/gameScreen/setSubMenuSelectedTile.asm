* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	TileSelected
	AND	#%00111111
	STA	TileSelected
	LDA	#VAR01#		
!!!to8bit!!!
	AND	#%00011111
	ORA	TileSelected
	STA	TileSelected

	
