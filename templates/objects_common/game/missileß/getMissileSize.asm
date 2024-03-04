* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	PßSettings
	AND	#%00110000
	LSR
	LSR
	LSR
	LSR	
!!!from8bit!!!
	STA	#VAR01#

	
