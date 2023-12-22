* params=variable|stringConst|number,{data}
* param1=#VAR01#,!!!to8bit!!!
* param2=#NAME#,playfields,##NAME##
* direction=TO
* optional=_heightOfPF
*
	LDA	#VAR01#		
!!!to8bit!!!
	STA	pfIndex
!!!Optional!!!

