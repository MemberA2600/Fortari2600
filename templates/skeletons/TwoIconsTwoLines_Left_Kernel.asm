*
*	JumpBack Pointer: temp01 (+ temp02)
*	Color1		: temp03	
*	Color2		: temp04
*	NUSIZ0		: temp05
*	NUSIZ1		: temp06
*	GradientPointer : temp07 (+ temp08)
*	sprite0_Pixels	: temp09 (+ temp10)
*	sprite0_Colors	: temp11 (+ temp12)
*	sprite1_Pixels	: temp13 (+ temp14)
*	sprite1_Color	: temp15 (+ temp16)
*	ENABL		: temp17
*
*	PF1 and PF2 is set in the Toplevel section.
*	Since we don't have enough memory for both sprites,
*	we have to flicker them. If the spritedata is
*	just copied, there won't be any flicker at all.
*
*

#BANK#_TwoIconsTwoLines_Left_Kernel
	LDA	#0			; 2 (64)
	LDX	frameColor		; 3 (67)
	STA	WSYNC			; 3 (76)
	STA	HMCLR			; 3 
	STX	COLUBK			; 3 (6)
	STX	COLUPF			; 3 (9)

	STA	GRP0			; 3 (12)
	STA	GRP1			; 3 (15)

	STA	NUSIZ0			; 3 (18)
	STA	NUSIZ1			; 3 (21)

	STA	ENABL
	STA	RESP0			; 3 (27)
	STA	RESBL			; 3 (30)

	LDA	#$20			; 2 
	STA	HMP0			; 3 
	LDA	#$a0			; 2
	STA	HMBL			; 3

	STA	RESP1			; 3
	LDA	#$10			; 2
	STA	HMP1			; 3

	STA	WSYNC			; 76
	STA	HMOVE			; 3

	LDY	#7			; 2 (5) 
	LDA	#$20			; 2 (7)
	STA	CTRLPF			; 3 (10)

*
*	Eary things. Love timing issues.
*

	LAX 	(temp07),y		; 5

	LDA	temp17			; 2
	STA	ENABL			; 3

	LDA	(temp15),y		; 5 
	STA 	COLUP1			; 3
		
	JMP	#BANK#_TwoIconsTwoLines_Left_Loop

	_align	45

#BANK#_TwoIconsTwoLines_Left_Loop
	STA 	WSYNC			; 76
	LDA	(temp09),y		; 5
	STA	GRP0			; 3 (8)
	LDA	(temp11),y		; 5 (13)
	STA	COLUP0			; 3 (16)	
	
	LDA	(temp13),y		; 5 (21)
	STA	GRP1			; 3 (24)

	TXA				; 2 (26)
	ADC	temp03			; 3 (29)

	sleep	2
	STA	COLUPF			

	sleep	3
	tXA				; 2 (37)
	ADC	temp04			; 3 (40)
	STA	COLUPF			; 3 (43)

	DEY				; 2 (45)
	LAX 	(temp07),y		; 5 (50)

	sleep	2

	LDA	frameColor		; 3 (55)
	STA	COLUPF			; 3 (58)


	LDA	(temp15),y		; 5 (63)
	STA 	COLUP1			; 3 (66)

	CPY	#255					; 2 (70)
	BNE	#BANK#_TwoIconsTwoLines_Left_Loop	; 2 (72)



#BANK#_TwoIconsTwoLines_Left_Ended
	LDA	frameColor
	LDX	#0	

	STA	WSYNC			; 76
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1
	STX	GRP0
	STX	GRP1
	STX	ENABL
	STX	HMCLR
	STX	REFP0
	STX	REFP1
	STX	CTRLPF

	JMP	(temp01)