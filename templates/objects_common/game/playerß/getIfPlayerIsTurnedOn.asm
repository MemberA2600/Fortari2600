* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	PßSettings
	AND	#%01000000
	ROR
	ROR
!!!from8bit!!!
	STA	#VAR01#

