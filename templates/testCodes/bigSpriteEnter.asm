
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

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#FRAME_COLOR
	STA	frameColor

	LDA	#72		; Set the starting position.
	STA	temp15

	LDA	#0		; Initialize sprite settings
	STA	temp16

	LDA	#$00		; Disable color modification
	STA	temp17