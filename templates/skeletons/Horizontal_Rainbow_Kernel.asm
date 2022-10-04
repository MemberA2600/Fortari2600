*
*	temp01:		DataVar
*	temp02: 	Number of Lines
*	temp03+temp04:	Gradient Pointer
*	temp05+temp06:	Back Pointer
*	temp07:		Direction
*
	_align	127
#BANK#_Horizontal_Rainbow

	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK		
	STX	PF0		
	STX	PF1	
	STX	PF2
	STX	GRP0	
	STX	GRP1
	STA	COLUPF

	LDY	temp02

****	direction
	LDA	temp07
	CMP	#0
	BEQ	#BANK#_Horizontal_Rainbow_Loop_ASC_Start
	JMP	#BANK#_Horizontal_Rainbow_Loop_DESC_Start

#BANK#_Horizontal_Rainbow_Loop_ASC
	DEY					; 2 (8)
	BMI	#BANK#_Horizontal_Rainbow_Reset	; 2 (10)

	LDA	(temp03),y	; 5
	ADC	temp01		; 3
	STA	COLUBK		; 3
	TAX			; 3 (13)

	INX		
	INX		; 4 (26)
	STX	COLUBK	; 3 (29)
	
	INX		
	INX		; 4 (33)
	STX	COLUBK	; 3 (36)

	INX		
	INX		; 4 (40)
	STX	COLUBK	; 3 (43)

	INX		
	INX		; 4 (47)
	STX	COLUBK	; 3 (50)

	INX		
	INX		; 4 (54)
	STX	COLUBK	; 3 (57)

	INX		
	INX		; 4 (61)
	STX	COLUBK	; 3 (64)

	INX		
	INX		; 4 (68)
	STX	COLUBK	; 3 (72)

#BANK#_Horizontal_Rainbow_Loop_ASC_Start
	STA	WSYNC
	JMP	#BANK#_Horizontal_Rainbow_Loop_ASC

#BANK#_Horizontal_Rainbow_Loop_DESC
	DEY					; 2 (8)
	BMI	#BANK#_Horizontal_Rainbow_Reset	; 2 (10)

	LDA	(temp03),y	; 5

	BYTE	#$6D
	BYTE	#temp01
	BYTE	#0		; ADC with temp01, forced to 4 cycles

	STA	COLUBK		; 3
	TAX			; 3 (13)
	
	DEX		
	DEX		; 4 (26)
	STX	COLUBK	; 3 (29)
	
	DEX		
	DEX		; 4 (33)
	STX	COLUBK	; 3 (36)

	DEX		
	DEX		; 4 (40)
	STX	COLUBK	; 3 (43)

	DEX		
	DEX		; 4 (47)
	STX	COLUBK	; 3 (50)

	DEX		
	DEX		; 4 (54)
	STX	COLUBK	; 3 (57)

	DEX		
	DEX		; 4 (61)
	STX	COLUBK	; 3 (64)

	DEX		
	DEX		; 4 (68)
	STX	COLUBK	; 3 (72)

#BANK#_Horizontal_Rainbow_Loop_DESC_Start
	STA	WSYNC
	JMP	#BANK#_Horizontal_Rainbow_Loop_DESC

#BANK#_Horizontal_Rainbow_Reset

*****	STA	WSYNC
	JMP	(temp05)
