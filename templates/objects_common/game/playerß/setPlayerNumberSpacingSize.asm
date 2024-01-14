* params=variable|stringConst|number
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	PßSettings
	AND	#%11111000
	STA	PßSettings
	LDA	#VAR01#		
!!!to8bit!!!
	AND	#%00000111
	ORA	PßSettings
	STA	PßSettings

	
