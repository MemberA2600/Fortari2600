* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	PßSettings
	AND	#%11001111
	STA	PßSettings
	LDA	#VAR01#		
!!!to8bit!!!
	AND	#%00000011
	ASL
	ASL
	ASL
	ASL
	ORA	PßSettings
	STA	PßSettings

	
