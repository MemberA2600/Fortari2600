* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	PßSettings
	AND	#%00000111
!!!from8bit!!!
	STA	#VAR01#


	
