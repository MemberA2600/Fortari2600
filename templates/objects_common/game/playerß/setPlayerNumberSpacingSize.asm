* params=variable|stringConst|number
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	P�Settings
	AND	#%11111000
	STA	P�Settings
	LDA	#VAR01#		
!!!to8bit!!!
	AND	#%00000111
	ORA	P�Settings
	STA	P�Settings

	
