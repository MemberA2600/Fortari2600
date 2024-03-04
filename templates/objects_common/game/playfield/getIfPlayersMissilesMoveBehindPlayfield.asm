* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	pfSettings
	AND	#%00000100
	LSR
	LSR
!!!from8bit!!!
	STA	#VAR01#

