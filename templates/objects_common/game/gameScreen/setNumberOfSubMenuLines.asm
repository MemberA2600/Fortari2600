* params=variable|stringConst|number
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	#VAR01#		
!!!to8bit!!!
	AND 	#%00000011
	STA	temp01
	LDA	SubMenuLines	
	AND	#%11111100
	ORA	temp01
	STA	SubMenuLines
