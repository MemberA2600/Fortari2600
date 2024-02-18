* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	#VAR01#		
!!!to8bit!!!
	AND 	#%00000001
	ROR
	ROR
	STA	temp01
	LDA	SubMenu
	AND	#%10111111
	ORA	temp01
	STA	SubMenu
