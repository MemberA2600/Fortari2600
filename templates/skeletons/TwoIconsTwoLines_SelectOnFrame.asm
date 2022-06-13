	LDA	counter
	AND	#%00000001
	CMP	#%00000001
	BEQ	##SCREENITEM##_Odd_Frame

	LDA	#<##NAME1##_BigSprite_1
	STA	temp09
	LDA	#>##NAME1##_BigSprite_1
	STA	temp10
	LDA	#<##NAME1##_BigSpriteColor_1
	STA	temp11
	LDA	#>##NAME1##_BigSpriteColor_1
	STA	temp12

	LDA	#<##NAME2##_BigSprite_1
	STA	temp13
	LDA	#>##NAME2##_BigSprite_1
	STA	temp14
	LDA	#<##NAME2##_BigSpriteColor_1
	STA	temp15
	LDA	#>##NAME2##_BigSpriteColor_1
	STA	temp16

	JMP	##SCREENITEM##_Even_Frame
##SCREENITEM##_Odd_Frame
	LDA	#<##NAME1##_BigSprite_0
	STA	temp09
	LDA	#>##NAME1##_BigSprite_0
	STA	temp10
	LDA	#<##NAME1##_BigSpriteColor_0
	STA	temp11
	LDA	#>##NAME1##_BigSpriteColor_0
	STA	temp12

	LDA	#<##NAME2##_BigSprite_0
	STA	temp13
	LDA	#>##NAME2##_BigSprite_0
	STA	temp14
	LDA	#<##NAME2##_BigSpriteColor_0
	STA	temp15
	LDA	#>##NAME2##_BigSpriteColor_0
	STA	temp16

##SCREENITEM##_Even_Frame
