*
*	temp01:		DataVar
*	temp02:		Number of Lines
*	temp03:		ColorVar
*	temp04+temp05:	Back Pointer
*	temp06+temp07:  Gradient Pattern
*
*

	align	256

#BANK#_Gradient
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STX	PF0
	STX	GRP0
	STX	GRP1
	STX	PF1
	STX	PF2

	LDY	temp02
	DEY

#BANK#_Gradient_Loop
	LDA	(temp06),y	; 5
	CLC			; 2 (7)
	ADC	temp01		; 3 (10)
	TAX			; 2 (12)
	LDA	temp03		; 3 (15)
	CMP	#255		; 2 (17)
	BNE	#BANK#_Gradient_Change ; 2 (19)
	TXA			; 2 (21)
	sleep	7
	
	JMP	#BANK#_Gradient_Changed	; 3 (31)
#BANK#_Gradient_Change
	AND	#%11110000	; 2 (21)
	STA	temp19		; 3 (24)
	TXA			; 2 (26)
	AND	#%00001111	; 2 (28)
	ORA	temp19		; 3 (31)
#BANK#_Gradient_Changed	
	STA	WSYNC		; 76
	STA	COLUBK		; 3
	DEY			; 2
	BPL	#BANK#_Gradient_Loop	; 2

#BANK#_Gradient_Reset
	LDA 	frameColor
	STA	WSYNC
	STA	COLUBK

#BANK#_Gradient_Back
	JMP	(temp04)