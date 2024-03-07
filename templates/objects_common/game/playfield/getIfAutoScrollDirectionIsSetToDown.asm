* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	ScrollDirection
	AND	#%00100000
	ROR
	ROR
	ROR
!!!from8bit!!!
	STA	#VAR01#

