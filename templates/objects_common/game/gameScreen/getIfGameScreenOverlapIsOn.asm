* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	OverLapIndicator
	AND	#%00100000
	ROL
	ROL
	ROL
!!!from8bit!!!
	STA	#VAR01#	


	
