* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	pfSettings
	AND	#%00001000
	LSR
	LSR
	LSR
!!!from8bit!!!
	STA	#VAR01#	


	
