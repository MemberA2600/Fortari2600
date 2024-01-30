* params=variable|stringConst|number,{data}
* param1=#VAR01#,!!!to8bit!!!
* param2=#NAME#,sprites,##NAME##
* direction=TO
* optional=_indexOfPlayer
* addManuallyToSysVars=P0SpriteIndex
*
	LDA	#VAR01#		
!!!to8bit!!!
	STA	#TEMPVAR#
!!!Optional!!!
::import=_savePlayerﬂIndex.asm

