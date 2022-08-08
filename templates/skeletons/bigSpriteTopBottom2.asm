
* BigSprite_0: 		temp03 - temp04
* BigSprite_1: 		temp05 - temp06
* BigSpriteColor_0:     temp07 - temp08
* BigSpriteColor_1:   	temp09 - temp10
* BigSpriteBG: 		temp11 - temp12
* Height:		temp13
* LineHeight:		temp14
* xPoz:			temp15
* bgColorMod: 		temp16
* spriteSettings:	temp17
* X2Offset:		temp18
* mono:			temp19

	LDA	#<#NAME#_BigSprite_0
	STA	temp03
	LDA	#>#NAME#_BigSprite_0
	STA	temp04

	LDA	#<#NAME#_BigSprite_1
	STA	temp05
	LDA	#>#NAME#_BigSprite_1
	STA	temp06

	LDA	#<#NAME#_BigSpriteColor_0
	STA	temp07
	LDA	#>#NAME#_BigSpriteColor_0
	STA	temp08

	LDA	#<#NAME#_BigSpriteColor_1
	STA	temp09
	LDA	#>#NAME#_BigSpriteColor_1
	STA	temp10

	LDA	#<#NAME#_BigSpriteBG
	STA	temp11
	LDA	#>#NAME#_BigSpriteBG
	STA	temp12

	LDA	temp15
	CMP	#255
	BNE	#NAME#_NoTurnOff

	LDA	temp17
	AND	#%00001111
	STA	temp17
	
	LDA	#<#NAME#_Empty
	STA	temp03
	STA	temp05
	LDA	#>#NAME#_Empty
	STA	temp04
	STA	temp06

#NAME#_NoTurnOff
