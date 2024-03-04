* params=variable|register
* param1=#VAR01#,!!!fromo8bit!!!
* direction=FROM
*
	LDA	pfSettings
	AND	#%11000000
	ROR
	ROR	
!!!from8bit!!!
	STA	#VAR01#


	
