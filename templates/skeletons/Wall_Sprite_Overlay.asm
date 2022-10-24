	LDA	counter
	AND	#%00000001
	CMP	#%00000001
	BEQ	#NAME#_Select_Sprite1

	LDA	#<##NAME##_BigSprite_0
	STA	temp09
	LDA	#>##NAME##_BigSprite_0
	STA	temp10	

	LDA	#<##NAME##_BigSpriteColor_0
	STA	temp11
	LDA	#>##NAME##_BigSpriteColor_0
	STA	temp12	

	JMP	#NAME#_Select_Sprite0
#NAME#_Select_Sprite1
	sleep	3
	LDA	#<##NAME##_BigSprite_1
	STA	temp09
	LDA	#>##NAME##_BigSprite_1
	STA	temp10	

	LDA	#<##NAME##_BigSpriteColor_1
	STA	temp11
	LDA	#>##NAME##_BigSpriteColor_1
	STA	temp12	

#NAME#_Select_Sprite0
