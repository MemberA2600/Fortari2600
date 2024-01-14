* params=data
* param1=#NAME#,sprites,##NAME##
* direction=TO
*
	LDA	#<#NAME#_Sprite
	STA	PßSpritePointer

	LDA	#>#NAME#_Sprite
	STA	PßSpritePointer+1

	LDA	#<#NAME#_SpriteColor
	STA	PßColorPointer

	LDA	#>#NAME#_SpriteColor
	STA	PßColorPointer+1