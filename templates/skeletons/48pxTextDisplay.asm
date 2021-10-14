48pxTextBegin
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
	
48pxTextPrepareForDarkness
	LDA	TextBackColor	
	STA	WSYNC
	STA	HMOVE		; 3	
	STA	COLUBK		; 3 (6)
	STA	COLUPF

	LDY	#4		
	STY	temp02		

48pxTextFillerLine1
	LDA	counter	
	AND	#%00000010
	CMP	#%00000010
	BEQ	48pxTextCalculateDataStart
	STA	WSYNC
	STA	WSYNC

48pxTextCalculateDataStart
	STA	WSYNC
	LDX	#0
48pxTextResetGRP
	STX	GRP0
	STX	GRP1

	LDA	#2
	STA	ENABL
	LDA	TextBackColor
	STA	COLUPF

48pxTextCalculateData
	TYA
	EOR	counter		  	; Seems like the best way to decide
	AND	#%00000001		; which lines to draw.
	CMP	#%00000001
	BEQ	48pxTextEvenLine

48pxTextOddLine
	LDA	Letter01
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp03
	
	LDA	Letter03
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp04

	LDA	Letter05
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp05

	LDA	Letter07
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp06

	LDA	Letter09
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp07

	LDA	Letter11
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%11110000
	STA	temp08

	JMP	48pxTextThisLineIsCalculated	
48pxTextEvenLine
	LDA	Letter02
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp03
	
	LDA	Letter04
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp04

	LDA	Letter06
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp05

	LDA	Letter08
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp06

	LDA	Letter10
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp07

	LDA	Letter12
	TAX
	LDA	BankXX5Table,x		; Got the starting address
	CLC
	ADC	temp02
	TAX
	LDA	BankXXFont,x		; Got the font data
	AND	#%00001111
	STA	temp08

	JMP	48pxTextThisLineIsCalculated

	align 	256

48pxTextThisLineIsCalculated	
	LDA	TextColor
	ADC	BankXXColors,y
	STA	COLUP0
	STA	COLUP1

	BIT	temp08
	BPL	48pxTextNoReColor
	STA	COLUPF
48pxTextNoReColor

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
	BMI	48pxTextFillerLine2	; 2 
	JMP	48pxTextCalculateDataStart   ; 3

48pxTextFillerLine2
	LDA	#0
	STA	GRP0
	STA	GRP1
	STA 	ENABL		

	LDA	counter	
	AND	#%00000010
	CMP	#%00000010
	BNE	48pxTextReset
	STA	WSYNC
	STA	WSYNC

48pxTextReset