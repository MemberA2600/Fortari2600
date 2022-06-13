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
*	
*	PF1 and PF2 is set in the Toplevel section.
*	Since we don't have enough memory for both sprites,
*	we have to flicker them. If the spritedata is
*	just copied, there won't be any flicker at all.
*
*

#BANK#_TwoIconsTwoLines_Kernel
	LDA	#0			; 2 (64)
	LDX	frameColor		; 3 (67)
	STA	HMP0			; 3 (70)
	STA	HMP1			; 3 (73)
	STA	WSYNC			; 3 (76)
	STA	HMOVE			; 3 
	STX	COLUBK			; 3 (6)
	STX	COLUPF			; 3 (9)

	STA	GRP0			; 3 (12)
	STA	GRP1			; 3 (15)
	STA	HMCLR			; 3 (18)

*
*	Set horizontal position. Sprite settings are done
*	in the Screen Top / Bottom section.
*
	LDA	#1			; 2 (20)
	STA	CTRLPF			; 3 (25)	

	STA	WSYNC			; 76
	LDA	temp05			; 3
	CMP	#0			; 2 (5)
	BEQ	#BANK#_TwoIconsTwoLines_P0_0
					; 2 (7)
	CMP	#5			; 2 (9)
	BEQ	#BANK#_TwoIconsTwoLines_P0_5
					; 2 (11)
	sleep	2
	JMP	#BANK#_TwoIconsTwoLines_P0_7
					; 3 (16)

#BANK#_TwoIconsTwoLines_P0_0
	sleep	2
#BANK#_TwoIconsTwoLines_P0_5
	sleep	3
#BANK#_TwoIconsTwoLines_P0_7
	sleep	18
	STA	RESP0			; 3 

	STA	WSYNC			; 76
	LDY	#7			; 2

*
*	Preload gradient
*
	LAX	(temp07),y		; 5 (7)
	CLC				; 2 (9)

	LDA	temp06			; 3 (12)
	CMP	#0			; 2 (14)
	BEQ	#BANK#_TwoIconsTwoLines_P1_0
					; 2 (16)
	CMP	#5			; 2 (18)
	BEQ	#BANK#_TwoIconsTwoLines_P1_5
					; 2 (20)
	sleep	2
	JMP	#BANK#_TwoIconsTwoLines_P1_7
					; 3 (25)

#BANK#_TwoIconsTwoLines_P1_0
	sleep	2
#BANK#_TwoIconsTwoLines_P1_5
	sleep	3
#BANK#_TwoIconsTwoLines_P1_7
	sleep	30
	STA	RESP1			; 3 


	LDA	frameColor		; 3 
	STA	COLUPF			; 3 

	JMP	#BANK#_TwoIconsTwoLines_Loop

	align 	256

#BANK#_TwoIconsTwoLines_Loop
	STA	WSYNC			; 76
#BANK#_TwoIconsTwoLines_Loop_NOSYNC

	LDA	(temp09),y		; 5  
	STA	GRP0			; 3 (8)
	LDA	(temp11),y		; 5 (13)
	STA	COLUP0			; 3 (16)	
	LDA	(temp13),y		; 5 (21)
	STA	GRP1			; 3 (24)
	LDA	(temp15),y		; 5 (29)
	STA	COLUP1			; 3 (32)
	
	TXA				; 2 (34)
	ADC	temp03			; 3 (37)
	STA 	COLUPF			; 3 (40)

	LDA	frameColor		; 3 (43)
	DEY				; 2 (45)
	sleep	2

	STA	COLUPF			; 3 (50)
	sleep 	2

	TXA				; 2 (56)
	ADC	temp04			; 3 (59)	
	STA	COLUPF			; 3 (62)

	LAX	(temp07),y		; 5 

	LDA	frameColor		; 3 
	STA	COLUPF			; 3 

	CPY	#255			; 2
	BNE	#BANK#_TwoIconsTwoLines_Loop_NOSYNC
					; 2

#BANK#_TwoIconsTwoLines_Ended
	LDX	frameColor
	LDA	#0
	STA	WSYNC			; 76
	STX	COLUPF
	STX	COLUP0
	STX	COLUP1
	STA	GRP0
	STA	GRP1

	JMP	(temp01)