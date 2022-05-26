
*	JumpBack Pointer: temp01 (+ temp02)
*	Data		: temp03	
*	Color		: temp04
*	TextColor	: temp05	
*	Gradient Pointer: temp06 (+ temp07)
*
*	sprite1		: temp08 (+ temp10)
*	sprite2		: temp10 (+ temp11)
*	sprite3		: temp12 (+ temp13)
*	sprite4		: temp14 (+ temp15)
*	sprite5		: temp16 (+ temp17)
*	sprite5		: temp18 (+ temp19)
*	

#BANK#_HalfBarWithText_Kernel
	LDA	frameColor	; 3
	STA	WSYNC		; 76
	STA	HMCLR		; 3 
	STA	COLUBK		; 3 (6)
	STA	COLUPF		; 3 (9)

	LDA	#0		; 2 (11)
	STA	GRP0		; 3 (14)
	STA	GRP1		; 3 (17)

*
*	P0: +0 pixels
*	P1: -1 pixels
*

	LDA	#$00		; 2 (19)
	STA	HMP0		; 3 (21)
	LDA	#$10		; 2 (23)
	STA	HMP1		; 3 (26)	

	STA	RESP0		; 3 (29)
	STA	RESP1		; 3 (32)

	LDA	#$03		; 2 (34)
	STA	NUSIZ0		; 3 (37)
	STA	NUSIZ1		; 3 (40)

	STA	WSYNC		; 76
	STA	HMOVE		; 3

*******************************
*TestOnly
*******************************
	LDA	#255
	STA	GRP0
	STA	GRP1

	LDA	#$1e
	STA	COLUP0
	LDA	#$44
	STA	COLUP1

*******************************