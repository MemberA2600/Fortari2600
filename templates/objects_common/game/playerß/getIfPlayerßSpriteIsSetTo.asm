* params=variable|stringConst|number|register,data
* param1=#VAR01#,!!!from8bit!!!
* param2=#NAME#,sprites,##NAME##
* direction=FROM
*

	LDA	#0

	LDX	#<#NAME#_Sprite
	CPX	PßSpritePointer
	BNE	#BANK#_GetIfSetToWasNope_#MAGIC#

	LDX	#>#NAME#_Sprite
	CPX	PßSpritePointer+1
	BNE	#BANK#_GetIfSetToWasNope_#MAGIC#

	LDA	#1

#BANK#_GetIfSetToWasNope_#MAGIC#
!!!from8bit!!!
	STA	#VAR01#