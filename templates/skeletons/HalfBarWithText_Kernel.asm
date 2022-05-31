

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
*	PF1 and PF2 is set in the Top / Bottom section.
*
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
	STA	VDELP0		; 3 (20)
	STA	PF0		; 3 (23)
	STA	RESP0		; 3 (26)

	LDA	counter		; 3 (29)
	AND	#%00000001	; 2 (31)
	CMP	#%00000001	; 2 (33)
	BEQ	#BANK#_HalfBarWithText_EvenStart	; 2 (35)
	LDA	#$80		; 2 (37)
	JMP	#BANK#_HalfBarWithText_OddStart		; 3 (40)
#BANK#_HalfBarWithText_EvenStart
	LDA	#$80		; 2 
	sleep	3		
#BANK#_HalfBarWithText_OddStart

	STA	HMP0		; 3 (43)
	LDA	#$03		; 2 (45)
	STA	NUSIZ0		; 3 (48)

	LDA	#1		; 2 (50)
	STA	CTRLPF		; 3 (53)

	LDY	#7		; 2 (55)
	LDA	counter		; 3 (58)
	AND	#%00000001	; 2 (60)
	CMP	#%00000001	; 2 (62)
	BEQ	#BANK#_HalfBarWithText_Even_PreSet ; 2 (64)
	JMP	#BANK#_HalfBarWithText_Odd_PreSet ; 3 (67)

#BANK#_HalfBarWithText_Even_PreSet
	STA	WSYNC		; 76
	STA	HMOVE		; 3

*
*	Preload sprite data
*
	
	_sleep	38
	sleep	3
*
*	I don't really understand this, since here we
*	had a regular 'sleep 49'...
*
	LAX	(temp16),y	; 5 (8)
	TXS			; 2 (10)
	LAX	(temp12),y	; 5 (15)
	
	LDA	#$00		; 2 (17)
	STA	HMP0		; 3 (20)
	CLC			; 2 (22)
*
*	Should be at cycle 1 as it arrives!
*

	JMP	#BANK#_HalfBarWithText_EvenFrame_NOHMOVE	; 3 (1)

	_align	88

#BANK#_HalfBarWithText_EvenFrame_NOSYNC
	STA	HMOVE		; 3 (1)
#BANK#_HalfBarWithText_EvenFrame_NOHMOVE

	LDA	frameColor	; 3 (4)
	STA	COLUPF		; 3 (7)	

	LDA	(temp08),y	; 5 (12)
	STA	GRP0		; 3 (15)

	LDA	(temp06),y	; 5 (12)
	ADC	temp05		; 3 (15)
	STA	COLUP0		; 3 (18)

	SBC	temp05		; 3 (21)
	ADC	temp04		; 3 (24)	

	DEY

	STX	GRP0		; 3
	TSX			; 2
	STX	GRP0		; 3
	sleep	8
	
*
*	Should be saved at cycle 53!
*
	STA	COLUPF		; 3 (53)
	
	LAX	(temp18),y	; 5 (58)
	TXS			; 2 (60)
	LAX	(temp14),y	; 5 (65)

	LDA	#$80		; 2 (71)
	STA	HMP0		; 3 (73)
	

****	This is the line +8 pixels to the right
#BANK#_HalfBarWithText_EvenFrame_SecondLine
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	frameColor	; 3 (6)
	STA	COLUPF		; 3 (9)	

	LDA	(temp10),y	; 5 (14)
	STA	GRP0		; 3 (17)

	LDA	(temp06),y	; 5 (12)
	ADC	temp05		; 3 (15)
	STA	COLUP0		; 3 (18)

	SBC	temp05		; 3 (21)

	ADC	temp04		; 3 (24)
	STX	GRP0		; 3
	TSX			; 2
	STX	GRP0		; 3
	

	LDX	#$00		; 2 (48)
	STX	HMP0		; 3 (50)

	STA	COLUPF		; 3 (53)

	DEY			; 2
	BMI	#BANK#_HalfBarWithText_Even_JMP ; 2

	sleep	2
	
	LAX	(temp16),y	; 5 (8)
	TXS			; 2 (10)
	LAX	(temp12),y	; 5 (15)

	JMP	#BANK#_HalfBarWithText_EvenFrame_NOSYNC ; 3 (71)

#BANK#_HalfBarWithText_Even_JMP
	JMP	#BANK#_HalfBarWithText_JumpBack

#BANK#_HalfBarWithText_Odd_PreSet
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LAX	(temp18),y	; 5 (8)
	TXS			; 2 (10)
	LAX	(temp14),y	; 5 (15)
	
	LDA	#$80		; 2 (17)
	STA	HMP0		; 3 (20)
	CLC			; 2 (22)	
	JMP	#BANK#_HalfBarWithText_OddFrame


	_align	120

#BANK#_HalfBarWithText_OddFrame
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	frameColor	; 3 (6)
	STA	COLUPF		; 3 (9)	

	LDA	(temp10),y	; 5 (14)
	STA	GRP0		; 3 (17)

	LDA	(temp06),y	; 5 (12)
	ADC	temp05		; 3 (15)
	STA	COLUP0		; 3 (18)

	SBC	temp05
	sleep	3
	STX	GRP0
	TSX
	STX	GRP0

	ADC	temp04		; 6
	DEY			; 2

	STA	COLUPF	

	sleep	4

	LAX	(temp16),y	; 5 (60)
	TXS			; 2 (62)
	LAX	(temp12),y	; 5 (67)

	LDA	#$00		; 2 (69)
	STA	HMP0		; 3 (71)

#BANK#_HalfBarWithText_OddFrame_SecondLine
	STA	HMOVE		; 3 (74)
	
	LDA	frameColor	; 3 (4)
	STA	COLUPF		; 3 (7)	

	LDA	(temp08),y	; 5 (12)
	STA	GRP0		; 3 (15)

	LDA	(temp06),y	; 5 (12)
	ADC	temp05		; 3 (15)
	STA	COLUP0		; 3 (18)

	SBC	temp05
	ADC	temp04		; 6

	sleep	3

	STX	GRP0
	TSX
	STX	GRP0
	DEY

	LDX	#$80		; 2 (68)
	STX	HMP0		; 3 (70)

	STA	COLUPF		; 3 
	LAX	(temp18),y	; 5 (62)
	TXS			; 2 (67)
	LAX	(temp14),y	; 5 (69)
	
	CPY	#255				; 2 (71)
	BNE	#BANK#_HalfBarWithText_OddFrame	; 2 (73)



#BANK#_HalfBarWithText_JumpBack
	LDA	frameColor	; 3
	STA	WSYNC		; 76
	STA	COLUPF		; 3
	LDA	#0		; 2 
	STA	GRP0		; 3 
	STA	GRP1		; 3 
	STA	PF1		; 3
	STA	PF2		; 3

	JMP	(temp01)	; 5
	