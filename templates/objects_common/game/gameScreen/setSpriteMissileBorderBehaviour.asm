* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	pfSettings
	AND	#%00111111
	STA	pfSettings
	LDA	#VAR01#		
!!!to8bit!!!
	AND	#%00000011
	ROR
	ROR
	ORA	pfSettings
	STA	pfSettings

	
