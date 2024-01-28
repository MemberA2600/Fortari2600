* params=variable|stringConst|number,{data}
* param1=#VAR01#,!!!to8bit!!!
* param2=#NAME#,sprites,##NAME##
* direction=TO
* optional=_indexOfPlayer
* 0or1=_savePlayerﬂIndex
* addManuallyToSysVars=P0SpriteIndex
*
	LDA	#VAR01#		
!!!to8bit!!!
	STA	#TEMPVAR#
!!!Optional!!!
!!!0or1!!!

