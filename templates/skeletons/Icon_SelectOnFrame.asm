	LDA	counter
	AND	#%00000001
	CMP	#%00000001
	BEQ	##SCREENITEM##_Odd_Frame

	LDA	#<##NAME##_BigSprite_1
	STA	temp03
	LDA	#>##NAME##_BigSprite_1
	STA	temp04
	LDA	#<##NAME##_BigSpriteColor_1
	STA	temp05
	LDA	#>##NAME##_BigSpriteColor_1
	STA	temp06

	JMP	##SCREENITEM##_Even_Frame
##SCREENITEM##_Odd_Frame
	LDA	#<##NAME##_BigSprite_0
	STA	temp03
	LDA	#>##NAME##_BigSprite_0
	STA	temp04
	LDA	#<##NAME##_BigSpriteColor_0
	STA	temp05
	LDA	#>##NAME##_BigSpriteColor_0
	STA	temp06

##SCREENITEM##_Even_Frame
