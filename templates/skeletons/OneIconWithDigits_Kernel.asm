*
*	JumpBack Pointer: temp01 (+ temp02)
*	Icon_Pixels	: temp03 (+ temp04)
*	Icon_Colors	: temp05 (+ temp06)	
*	
*	Digit1_Pixels	: temp07 (+ temp08)
*	Digit2_Pixels	: temp09 (+ temp10)
*	Digit3_Pixels	: temp11 (+ temp12)
*	Digit4_Pixels	: temp13 (+ temp14)
*
*	GradientPointer : temp15 (+ temp16)
*	Color		: temp17
*			  bit 0: 2digits or 4digits mode
*
*	PF1 and PF2 is set in the Toplevel section.
*	Since we don't have enough memory for both sprites,
*	we have to flicker them. If the spritedata is
*	just copied, there won't be any flicker at all.
*
*

#BANK#_OneIconWithDigits_Kernel
	LDA	#0			; 2 (64)
	LDX	frameColor		; 3 (67)
	STA	WSYNC			; 3 (76)
	STA	HMCLR			; 3 
	STX	COLUBK			; 3 (6)
	STX	COLUPF			; 3 (9)

	STA	GRP0			; 3 (12)
	STA	GRP1			; 3 (15)
	STA	HMP0			; 3 (18)

	LDA	#$01			; 2 (20)
	STA	NUSIZ1			; 3 (23)
*
*	Even: $00
*	Odd : $80
*

	LDA	counter			; 3 (26)
	AND	#00000001		; 2 (28)
	STA	RESP1			; 3 (31)
	ROR				; 2 (33)
	STA	HMP1			; 3 (36)

*	TestOnly
*
	LDA	#255
	STA	GRP1

	LDA	#$1e
	STA	COLUP1

	STA	WSYNC			; 76
	STA	HMOVE			; 3 
	LDA	temp05			; 3
	CMP	#0			; 2 (5)
	BEQ	#BANK#_OneIconWithDigits_P0_0
					; 2 (7)
	CMP	#5			; 2 (9)
	BEQ	#BANK#_OneIconWithDigits_P0_5
					; 2 (11)
	LDY	#7			; 2 
	JMP	#BANK#_OneIconWithDigits_P0_7
					; 3 (16)
#BANK#_OneIconWithDigits_P0_0
	sleep	7
#BANK#_OneIconWithDigits_P0_5
	sleep	9
#BANK#_OneIconWithDigits_P0_7
	sleep	4
	STA	RESP0			; 3 (30?)

*
*	Must Sync, since we can be at different cycle depending
*	on the NUSIZ value.
*
	STA	WSYNC			; 76

	LDA	counter			; 3 
	AND	#%00000001		; 2 (5)
	CMP	#%00000001		; 2 (7)
	BEQ	#BANK#_OneIconWithDigits_Prepare_Odd	; 2 (9)
#BANK#_OneIconWithDigits_Prepare_Even
	LDA	#$80			; 2 (11)
	STA	HMP1			; 3 (14)
	JMP	#BANK#_OneIconWithDigits_Loop_Even	; 3 (17)
	
#BANK#_OneIconWithDigits_Prepare_Odd
	LDA	#$00			; 2 (11)
	STA	HMP1			; 3 (14)
	
	sleep	54

	JMP	#BANK#_OneIconWithDigits_Loop_odd	; 3 (71)

	align	255

#BANK#_OneIconWithDigits_Loop_Even
	STA	WSYNC			; 76
	STA	HMOVE			; 3 
	LDA	(temp03),y		; 5 (8)
	STA	GRP0			; 3 (11)
	LDA	(temp05),y		; 5 (16)
	STA	COLUP0			; 3 (19)

	sleep	40

	LDA	#$80			; 2 (61)
	STA	HMP0			; 3 (64)
	LDA	#$00			; 2 (66)
	STA	HMP1			; 3 (69)
	DEY				; 2 (71)
#BANK#_OneIconWithDigits_Loop_Secondline
	STA	HMOVE			; 3 (74)
	LDA	(temp03),y		; 5 (3)
	STA	GRP0			; 3 (6)
	LDA	(temp05),y		; 5 (11)
	STA	COLUP0			; 3 (14)
	
	sleep	42

	LDA	#$80			; 2 (60)
	STA	HMP1			; 3 (63)
	LDA	#$00			; 2 (65)
	STA	HMP0			; 3 (68)

	DEY				; 2 (70)
	BPL	#BANK#_OneIconWithDigits_Loop_Even	; 2 (72)
	JMP	#BANK#_OneIconWithDigits_Ended

	align 	255

#BANK#_OneIconWithDigits_Loop_odd
	STA	HMOVE			; 74
	
	LDA	(temp03),y		; 5 (3)
	STA	GRP0			; 3 (6)
	LDA	(temp05),y		; 5 (11)
	STA	COLUP0			; 3 (14)

	sleep	44

	DEY				; 2 (63)
	LDA	#$00			; 2 (65)
	STA	HMP0			; 3 (68)
	LDA	#$80			; 2 (70)
	STA	HMP1			; 3 (73)
#BANK#_OneIconWithDigits_Loop_SecondLine
	STA	WSYNC			; 76
	STA	HMOVE			; 3
	
	LDA	(temp03),y		; 5 (8)
	STA	GRP0			; 3 (11)
	LDA	(temp05),y		; 5 (16)
	STA	COLUP0			; 3 (19)

	sleep	35

	LDA	#$80			; 2 (60)
	STA	HMP0			; 3 (63)
	LDA	#$00			; 2 (65)
	STA	HMP1			; 3 (68)
	DEY				; 2 (70)
	BPL	#BANK#_OneIconWithDigits_Loop_odd	; 2 (72)	
	
#BANK#_OneIconWithDigits_Ended
	LDA	frameColor
	LDX	#0
	STX	HMCLR
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1
	STX	GRP0
	STX	GRP1
	STA	WSYNC			; 76

	JMP	(temp01)