* params=variable|stringConst|number|register,variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit1!!!
* param1=#VAR02#,!!!to8bit2!!!
* direction=TO
*
	LDA	#VAR01#		
!!!to8bit1!!!
	STA	P�X

	LDA	#VAR02#		
!!!to8bit2!!!
	STA	P�Y