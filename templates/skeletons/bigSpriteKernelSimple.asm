* Possible Keys:
****************
* ##BigSprite_0##, ##BigSprite_1##
* ##BigSpriteColor_0##, ##BigSpriteColor_1##, 
* ##BigSpriteBG##, ##Height##, ##LineHeight##
* ##xPoz##
* ##bgColorMod## 
* ##spriteSettings##
*

##BANK##_BigSprite_Kernel_Begin
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)

	LDA	#0		; 2 (8)
	STA	PF0		; 3 (11)
	STA	PF1		; 3 (14)
	STA	PF2		; 3 (17)
	STA	GRP0		; 3 (20)
	STA	GRP1		; 3 (23)
	STA	VDELP0		; 3 (26)
	STA	VDELP1		; 3 (29)

	
	

	