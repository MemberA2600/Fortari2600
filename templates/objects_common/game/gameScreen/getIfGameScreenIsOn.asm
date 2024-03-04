* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	NoGameMode
	AND	#%10000000
	ROL
!!!from8bit!!!
	STA	#VAR01#	


	
