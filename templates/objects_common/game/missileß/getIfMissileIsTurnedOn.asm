* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	PßSettings
	AND	#%10000000
	ROR	
!!!from8bit!!!
	STA	#VAR01#

	
