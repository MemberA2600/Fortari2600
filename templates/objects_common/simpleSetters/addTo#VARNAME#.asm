* params=variable|stringConst|number|register
* param1=#VAR01#,!!!to8bit!!!
* direction=TO
*
	LDA	#VAR01#		; &COLOR
!!!to8bit!!!
	CLC
	ADD	#SYSVAR#
	STA	#SYSVAR#
