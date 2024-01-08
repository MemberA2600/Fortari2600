* params=variable|stringConst|number
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	#VAR01#		
!!!to8bit!!!
	AND 	#%00000001
	ROR
	STA	temp01
	LDA	NoGameMode
	AND	#01111111
	ORA	temp01
	STA	NoGameMode
