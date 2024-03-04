* params=variable|register
* param1=#VAR01#,!!!from8bit!!!
* direction=FROM
*
	LDA	SubMenuLines
	AND	#%00000011	
!!!from8bit!!!
	STA	#VAR01#
