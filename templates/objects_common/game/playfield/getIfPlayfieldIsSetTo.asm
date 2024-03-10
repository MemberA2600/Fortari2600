* params=variable|stringConst|number|register,data
* param1=#VAR01#,!!!from8bit!!!
* param2=#NAME#,playfields,##NAME##
* direction=FROM
*

	LDA	#0

	LDX	#<#NAME#_00
	CPX	pf0Pointer
	BNE	#BANK#_GetIfSetToWasNope_#MAGIC#

	LDX	#>#NAME#_00
	CPX	pf0Pointer+1
	BNE	#BANK#_GetIfSetToWasNope_#MAGIC#

	LDA	#1

#BANK#_GetIfSetToWasNope_#MAGIC#
!!!from8bit!!!
	STA	#VAR01#