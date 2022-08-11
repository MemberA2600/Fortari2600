*
*	temp02-temp09	: Letters
*	#GRADIENT#   	: Physical address of 5 lines gradient
*	#VAR01#		: Letter01
*	#VAR02#		: Letter02
*	#VAR03#		: Letter03
*	#VAR04#		: Letter04
*	#VAR05#		: Letter05
*	#VAR06#		: Letter06
*	#VAR07#		: Letter07
*	#VAR08#		: Letter08
*	#VAR09#		: Letter09
*	#VAR10#		: Letter10
*	#VAR11#		: Letter11
*	#VAR12#		: Letter12
*	#TextColor#	: Text Front Color
*	#TextBackColor#	: Text Back  Color
*

#NAME#_Begin
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

	LDA	#%00000101	; 3
	STA	CTRLPF		; 3 (32)

	sleep	2		

	STA	RESP0		; 3 	
	STA	RESP1		; 3 Set the X pozition of sprites.

	LDA	#$00		; 2 
	STA	HMP0		; 3 

	LDA	#$10		; 2 
	STA	RESBL
	STA	HMP1		; 3 

	LDA	#$E0
	STA	HMBL

	LDA	#$03		; 2 			
	STA	NUSIZ0		; 3 
	STA	NUSIZ1		; 3 
	
#NAME#_PrepareForDarkness
	LDA	#TextBackColor#	
	STA	WSYNC
	STA	HMOVE		; 3	
	STA	COLUBK		; 3 (6)
	STA	COLUPF

	LDY	#4		
	STY	temp02		

#NAME#_FillerLine1
	LDA	counter	
	AND	#%00000010
	CMP	#%00000010
	BEQ	#NAME#_CalculateDataStart
	STA	WSYNC
	STA	WSYNC

#NAME#_CalculateDataStart
	STA	WSYNC
	LDX	#0
#NAME#_ResetGRP
	STX	GRP0
	STX	GRP1

	LDA	#2
	STA	ENABL
	LDA	#TextBackColor#
	STA	COLUPF

#NAME#_CalculateData
	TYA
	EOR	counter		  	; Seems like the best way to decide
	AND	#%00000001		; which lines to draw.
	CMP	#%00000001
	BEQ	#NAME#_EvenLine

#NAME#_OddLine
	LDA	#VAR01#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp03
	
	LDA	#VAR03#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp04

	LDA	#VAR05#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp05

	LDA	#VAR07#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp06

	LDA	#VAR09#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp07

	LDA	#VAR11#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp08

	JMP	#NAME#_ThisLineIsCalculated	
#NAME#_EvenLine
	LDA	#VAR02#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp03
	
	LDA	#VAR04#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp04

	LDA	#VAR06#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp05

	LDA	#VAR08#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp06

	LDA	#VAR10#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp07

	LDA	#VAR12#
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp08

	JMP	#NAME#_ThisLineIsCalculated

	align 	256

#NAME#_ThisLineIsCalculated	
	LDA	#TextColor#
	ADC	#GRADIENT#,y
	STA	COLUP0
	STA	COLUP1

	BIT	temp08
	BPL	#NAME#_NoReColor
	STA	COLUPF
#NAME#_NoReColor

	STA	WSYNC
	LDA	temp03		; 3 (6)
	STA	GRP0		; 3 (9)
	LDA	temp04		; 3 (12)
	STA	GRP1		; 3 (15)

	LDX	temp08
	TXS
	TXA	
	LDY	temp06
	LDX	temp07

	sleep	12

	LDA	temp05		; 3 
	STA	GRP0		; 3 
	
	STY	GRP1
	STX	GRP0
	TSX
	STX	GRP1


	DEC	temp02		; 5
	LDY	temp02		; 3
	BMI	#NAME#_FillerLine2	; 2 
	JMP	#NAME#_CalculateDataStart   ; 3

#NAME#_FillerLine2
	LDA	#0
	STA	GRP0
	STA	GRP1
	STA 	ENABL		

	LDA	counter	
	AND	#%00000010
	CMP	#%00000010
	BNE	#NAME#_Reset
	STA	WSYNC
	STA	WSYNC

#NAME#_Reset