* params=data
* param1=#NAME#,sprites,##NAME##
* direction=TO
*
	LDA	#<#NAME#_Sprite
	STA	P�SpritePointer

	LDA	#>#NAME#_Sprite
	STA	P�SpritePointer+1

	LDA	#<#NAME#_SpriteColor
	STA	P�ColorPointer

	LDA	#>#NAME#_SpriteColor
	STA	P�ColorPointer+1