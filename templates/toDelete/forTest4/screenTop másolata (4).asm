48pxText
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

	sleep	7		

	STA	RESP0		; 3 	
	STA	RESP1		; 3 Set the X pozition of sprites.

	LDA	TextColor	; 3 
	STA	COLUP0		; 3 
	LDA	#$88
	STA	COLUP1		; 3 
	
	LDA	#$00		; 2 
	STA	HMP0		; 3 
	LDA	#$10		; 2 
	STA	HMP1		; 3 

	LDA	#$03		; 2 			
	STA	NUSIZ0		; 3 
	STA	NUSIZ1		; 3 
	
48pxTextCursorBlinking
	LDX	#0
	BIT	counter
	BVS	48pxTextOtherWayAround	;  turn every 64 frame
	LDY	#41
	LDA	#40
	JMP	48pxTextCheckForBlinking
48pxTextOtherWayAround
	LDY	#40
	LDA	#41
48pxTextCheckForBlinking
	CPX	#12
	BCC	48pxTextPrepareForDarkness
	CMP	Letter01,x
	BNE	48pxTextNoChangeForBlinking
	STY	Letter01,x	
48pxTextNoChangeForBlinking
	INX
	JMP 	48pxTextCheckForBlinking

48pxTextPrepareForDarkness
	LDA	BackColor	
	STA	WSYNC
	STA	HMOVE		
	STA	COLUBK	
	
	LDY	#4		
	STY	temp02		
	TSX			
	STX	item		

48pxTextFillerLines1
	LDA	counter	
	AND	#%00000011
	TAX
48pxTextFillerLines1Counter
	CPX	#0
	BEQ	48pxTextCalculateDataStart
	STA	WSYNC
	DEX
	JMP	48pxTextFillerLines1Counter


48pxTextCalculateDataStart
	LDX	#0
48pxTextResetGRP
	STX	GRP0
	STX	GRP1

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


	sleep	3
48pxTextThisLineIsCalculated	
	STA	WSYNC

	LDA	temp03		; 3 (6)
	STA	GRP0		; 3 (9)
	LDA	temp04		; 3 (12)
	STA	GRP1		; 3 (15)

	sleep	45

	DEC	temp02		; 5
	LDY	temp02		; 3
	BMI	48pxTextFillerLines2	; 2 
	JMP	48pxTextCalculateDataStart   ; 3

48pxTextFillerLines2
	LDA	#0
	STA	GRP0
	STA	GRP1
	LDA	counter	
	AND	#%00000011
	TAX
48pxTextFillerLines2Counter
	CPX	#4
	BEQ	48pxTextReset
	STA	WSYNC
	INX
	JMP	48pxTextFillerLines2Counter

48pxTextReset
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK		
	LDA	#0		
	STA	PF0
	STA	PF1		
	STA	PF2		
	STA	GRP0		
	STA	GRP1		
	STA	VDELP0		
	STA	VDELP1	

	LDX	item		
	TXS	

	JMP	EndTest

	align	256

BankXXFont
BankXX_0
	BYTE	#%01000100
	BYTE	#%10101010
	BYTE	#%10101010
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_1
	BYTE	#%01000100
	BYTE	#%01000100
	BYTE	#%01000100
	BYTE	#%01000100
	BYTE	#%01000100
BankXX_2
	BYTE	#%11101110
	BYTE	#%10001000
	BYTE	#%01000100
	BYTE	#%10101010	
	BYTE	#%01000100
BankXX_3
	BYTE	#%01000100
	BYTE	#%10101010
	BYTE	#%01100110
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_4
	BYTE	#%00100010
	BYTE	#%11101110
	BYTE	#%10101010
	BYTE	#%01000100	
	BYTE	#%00100010
BankXX_5
	BYTE	#%11001100
	BYTE	#%00100010
	BYTE	#%11001100
	BYTE	#%10001000	
	BYTE	#%11101110
BankXX_6
	BYTE	#%01100110
	BYTE	#%10101010
	BYTE	#%01100110
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_7
	BYTE	#%10001000
	BYTE	#%01000100
	BYTE	#%00100010
	BYTE	#%00100010
	BYTE	#%11101110
BankXX_8	
	BYTE	#%01000100
	BYTE	#%10101010	
	BYTE	#%01000100
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_9
	BYTE	#%11001100
	BYTE	#%00100010
	BYTE	#%01100110
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_A
	BYTE	#%10101010
	BYTE	#%11101110
	BYTE	#%10101010
	BYTE	#%10101010
	BYTE	#%01000100
BankXX_B
	BYTE	#%11001100
	BYTE	#%10101010
	BYTE	#%11001100
	BYTE	#%10101010
	BYTE	#%11001100

BankX_Space
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000

BankXX5Table
	BYTE	#0
	BYTE	#5
	BYTE	#10
	BYTE	#15
	BYTE	#20
	BYTE	#25
	BYTE	#30
	BYTE	#35
	BYTE	#40
	BYTE	#45
	BYTE	#50
	BYTE	#55
	BYTE	#60
	BYTE	#65
	BYTE	#70
	BYTE	#75
	BYTE	#80
	BYTE	#85
	BYTE	#90
	BYTE	#95
	BYTE	#100
	BYTE	#105
	BYTE	#110
	BYTE	#115
	BYTE	#120
	BYTE	#125
	BYTE	#130
	BYTE	#135
	BYTE	#140
	BYTE	#145
	BYTE	#150
	BYTE	#155
	BYTE	#160
	BYTE	#165
	BYTE	#170
	BYTE	#175
	BYTE	#180
	BYTE	#185
	BYTE	#190
	BYTE	#195
	BYTE	#200
	BYTE	#205
	BYTE	#210
	BYTE	#215
	BYTE	#220
	BYTE	#225
	BYTE	#230
	BYTE	#235
	BYTE	#240
	BYTE	#245
	BYTE	#250
EndTest



