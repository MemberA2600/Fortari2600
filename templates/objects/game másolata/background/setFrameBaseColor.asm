* params=variable|stringConst|number
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	frameColor
	AND	#$0F
	STA	frameColor

	LDA	#VAR01#		; &COLOR
!!!to8bit!!!
	AND	#$F0
	ORA	frameColor
	STA	frameColor


