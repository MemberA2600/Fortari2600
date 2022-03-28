
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
	
	BIT	SWCHA
	BVS	Test_NO_LEFT
	DEC	temp15	

	LDA	#%11110111
	AND	temp17
	STA	temp17
	
	JMP	Test_MOVE_END
Test_NO_LEFT	
	BIT	SWCHA
	BMI	Test_MOVE_END
	INC	temp15

	LDA	#%00001000
	ORA	temp17
	STA	temp17

Test_MOVE_END
	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	Test_NOSHOOT

	BIT	INPT4
	BMI 	Test_NOSHOOT
	LDA	temp17
	AND	#%00000111
	TAX
	INX
	TXA
	AND	#%00000111
	STA	temp19
	
	LDA	temp17
	AND	#%11111000
	ORA	temp19
	STA	temp17


Test_NOSHOOT

	LDA	#$02
	BIT	SWCHB
	BNE	Test_NoReset
	
	INC	temp16

Test_NoReset

	LDA	counter
Test_NoINCRofNUSIZ
	AND	#%0000111
	CMP	#%0000111
	BNE	Test_Ends

	LDA	temp17
	AND	#%00001111
	STA	temp19

	LDA	temp17	; spriteSettings
	lsr
	lsr
	lsr
	lsr	
	TAX
	INX
	TXA
	CMP	#Test_BigSprite_frameNum
	BCS	Test_NotSmaller

	ASL
	ASL
	ASL
	ASL
	ORA	temp19

	JMP	Test_SpriteNumDone

Test_NotSmaller
	LDA	temp19

Test_SpriteNumDone
	STA	temp17

Test_Ends