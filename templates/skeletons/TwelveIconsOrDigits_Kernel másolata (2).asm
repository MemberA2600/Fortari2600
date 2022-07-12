
*
* JumpBack Kernel:	temp01 (+ temp02)
* Icon_Pointer:		temp03 (+ temp04)
* Icon_Color_Pointer:	temp05 (+ temp06)
* Digit01_Pointer:	temp07 (+ temp08)	
* Digit02_Pointer:	temp09 (+ temp10)	
* Gradient_Pointer:	temp11 (+ temp12)
* Font_BaseColor	temp13
* Data			temp14
* dataBDC		temp15
* Digit03_Pointer:	temp16 (+ temp17)
* dataBDC_100		temp18	
*

#BANK#_TwelveIconsOrDigits_Kernel

*
* Preset things.
*

	LDX	frameColor
	LDA	#0
	STX	WSYNC		 ; 76
	STX	COLUBK		  
	STX	COLUPF
	STA	GRP0
	STA	GRP1
	STA	PF0
	STA	PF1
	STA	PF2
	sleep	2
	STA	RESP0		
	STA  	ENABL
	STA  	ENAM0	
	STA  	ENAM1
	STA	HMCLR		; 12 x 3 (36)
	

	LDA	temp14		; 3 (39)
	CMP	#7		; 2 (41)
	BCC	#BANK#_TwelveIconsOrDigits_Basic_Mode ; 2 (40)
	CMP	#13		; 2 (43)
	BCC	#BANK#_TwelveIconsOrDigits_Interlaced_Mode ; 2 (45)
#BANK#_TwelveIconsOrDigits_Digits_Mode
	CLC			; 2 (47)
	LDA	temp15		; 3 (50)
	AND	#%00001111	; 2 (52)
	ASL			; 2 (54)
	ASL			; 2 (56)
	ASL			; 2 (58)
	ADC	temp07		; 3 (61)
	STA	temp07		; 3 (64)	
	LDA	temp15		; 3 (67)
	AND	#%11110000	; 2 (69)
	LSR			; 2 (71)
	ADC	temp09		; 3 (74)
	STA	temp09		; 3 (1)		; One line wasted.
	LDA	temp18		; 3 (4)
	ASL			; 2 (6)	
	ASL			; 2 (8)	
	ASL			; 2 (10)
	ADC	temp16		; 3 (13)
	STA	temp16 		; 3 (16)

	LDA	#$00		; 2 (18)
	sleep	2
	STA	RESP1		; 3 (23)	
	STA	HMP1		; 3 (26)
	LDA	#$F0		; 2 (28)	
	STA	HMP0		; 3 (31)
	LDY	#7		; 2 (33)

	LDA	#$04		; 2 (35)
	STA	CTRLPF		; 3 (38)
	LDA	#%00111100	; 2 (40)
	STA	PF1		; 3 (43)

	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	#$03		; 2 
	STA	NUSIZ0		; 3 
	STA	NUSIZ1		; 3 

	LAX	(temp07),y	; 5
	TXS			; 2
	
	LDA 	(temp11),y	; 5 
	ADC	temp13		; 3 
	TAX			; 2

	LDA 	(temp16),y	; 5 
	STA	GRP1		; 3 

	JMP	#BANK#_TwelveIconsOrDigits_Digits_Loop

	align 	256

#BANK#_TwelveIconsOrDigits_Digits_Loop
	STA	WSYNC		; 76
	LDA	(temp03),y	; 5
	STA	GRP0		; 3 (8)
	LDA	(temp05),y	; 5 (13)
	STA	COLUP0		; 3 (16)	

	LDA	(temp09),y	; 5 (21)
	STX	COLUP1		; 3 (24)
	DEY			; 2 (26)
	sleep	2
	STX	COLUP0		; 3 (31)

	STA	GRP0		; 3 (34)
	TSX			; 2 (36)
	STX	GRP1		; 3 (39)

	LAX	(temp07),y	; 5 (44)
	TXS			; 2 (46)

	LDA 	(temp11),y	; 5 (51)
	ADC	temp13		; 3 (54)
	TAX			; 2 (56)

	LDA 	(temp16),y	; 5 (61)
	STA	GRP1		; 3 (64)

	CPY	#255		; 2 (66)
	BNE	#BANK#_TwelveIconsOrDigits_Digits_Loop ; 2 (68)
	JMP	#BANK#_ResetAll	; 3 (72)

#BANK#_TwelveIconsOrDigits_Basic_Mode

	LDA	#$03		; 2 (44)
	STA	NUSIZ0		; 3 (47)
	STA	NUSIZ1		; 3 (50)

	LDA	#$04		; 2 (52)
	STA	CTRLPF		; 3 (55)

	LDA	#$F0		; 2 (57)
	STA	HMP0		; 3 (60)
	LDA	#$00 		; 2 (62)
	STA	HMP1		; 3 (65)

	STA	WSYNC		; 76
	LDX	temp14		; 3

	sleep	21	
	LDY	#7		; 2 
	STA	RESP1		; 3

	LDA	#BANK#_TwelveIconsOrDigits_Basic_PF1_Table,x	; 4
	STA	PF1		; 3
	LDA	#BANK#_TwelveIconsOrDigits_Basic_PF2_Table,x	; 4
	STA	PF2		; 3

	STA	WSYNC		; 76
	STA	HMOVE		; 3

	JMP	#BANK#_TwelveIconsOrDigits_Basic_Loop

#BANK#_TwelveIconsOrDigits_Basic_PF1_Table
	BYTE	#%11111111
	BYTE	#%00111111
	BYTE	#%00001111
	BYTE	#%00000011
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000
#BANK#_TwelveIconsOrDigits_Basic_PF2_Table
	BYTE	#%00001111
	BYTE	#%00001111
	BYTE	#%00001111
	BYTE	#%00001111
	BYTE	#%00001111
	BYTE	#%00001100
	BYTE	#%00000000

	align	256

#BANK#_TwelveIconsOrDigits_Basic_Loop
	STA	WSYNC		; 76
	LDA	(temp03),y	; 5
	STA	GRP0		; 3 (8)
	STA	GRP1		; 3 (11)
	LDA	(temp05),y	; 5 (16)
	STA	COLUP0		; 3 (19)	
	STA	COLUP1		; 3 (22)

	_sleep	26

	DEY			; 2
	BPL	#BANK#_TwelveIconsOrDigits_Basic_Loop
	JMP	#BANK#_ResetAll

#BANK#_TwelveIconsOrDigits_Interlaced_Mode
	LDA	#$06		; 2 (44)
	STA	NUSIZ0		; 3 (47)
	STA	NUSIZ1		; 3 (50)

	LDA	#$04		; 2 (52)
	STA	CTRLPF		; 3 (55)

	LDA	counter		; 3 (58)
	AND	#%00000010	; 3 (61)
	TAX			; 2 (63)

	LDA	#BANK#_TwelveIconsOrDigits_Interlaced_Init_HMOVE_Table,x ; 5 (68)
	STA	HMP0		; 3 (71)

	STA	WSYNC		; 76		
	LDA	#BANK#_TwelveIconsOrDigits_Interlaced_Init_HMOVE_Table+1,x ; 5 
	STA	HMP1		; 3 (8)

	CPX	#0		; 2 (10)
	BEQ 	#BANK#_TwelveIconsOrDigits_Interlaced_RESP_Even ; 2 (12)
	sleep	12
	LDY	#7		; 2 
	STA	RESP0		; 3
	sleep	3
	STA	RESP1		; 3

	JMP	#BANK#_TwelveIconsOrDigits_Interlaced_RESP_JumpHere
#BANK#_TwelveIconsOrDigits_Interlaced_RESP_Even
	sleep	12	
	LDY	#7		; 2 
	STA	RESP0		; 3
	sleep	3
	STA	RESP1		; 3

#BANK#_TwelveIconsOrDigits_Interlaced_RESP_JumpHere
	LDA	#255
	STA	GRP0
	STA	GRP1
	
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	counter		; 3 (6)
	AND	#%00000010	; 2 (8)
	LSR			; 2 (10)
	TAX			; 2 (12)
	LDA	#BANK#_TwelveIconsOrDigits_Interlaced_HMOVE_Table,x	; 5 (17)
	CPX	#0		; 2 (19)
	BNE	#BANK#_TwelveIconsOrDigits_Interlaced_Odd_Dummy		; 2 (21)
	JMP	#BANK#_TwelveIconsOrDigits_Interlaced_Even_Loop		; 2 (23)

#BANK#_TwelveIconsOrDigits_Interlaced_Init_HMOVE_Table
	BYTE	#$00
	BYTE	#$10
	BYTE	#$F0
	BYTE	#$00

#BANK#_TwelveIconsOrDigits_Interlaced_HMOVE_Table
	BYTE	#$80
	BYTE	#$10

#BANK#_TwelveIconsOrDigits_Interlaced_Odd_Dummy
	sleep	45	

	JMP	#BANK#_TwelveIconsOrDigits_Interlaced_Even_SecondLine

#BANK#_TwelveIconsOrDigits_Interlaced_Even_Loop
	STA	WSYNC		; 3
	STA	HMOVE		; 3 (6)	

	LDA	(temp03),y 	; 5 (11)
	STA	GRP0		; 3 (14)
	STA	GRP1		; 3 (17)

	LDA	(temp05),y	; 5 (22)
	STA	COLUP0		; 3 (25)
	STA	COLUP1		; 3 (28)

	sleep	32

	LDA	#$10
	STA	HMP0
	STA	HMP1

	DEY	
	BMI	#BANK#_ResetAll

#BANK#_TwelveIconsOrDigits_Interlaced_Even_SecondLine
	STA	HMOVE		; 3 (74)	

	LDA	(temp03),y 	; 5 (3)
	STA	GRP0		; 3 (6)
	STA	GRP1		; 3 (9)

	LDA	(temp05),y	; 5 (14)
	STA	COLUP0		; 3 (17)
	STA	COLUP1		; 3 (20)

	sleep	40

	LDA	#$80
	STA	HMP0
	STA	HMP1

	DEY	
	BPL	#BANK#_TwelveIconsOrDigits_Interlaced_Even_Loop

#BANK#_ResetAll
	LDA	frameColor
	LDX	#0
	STX	GRP1
	STX	GRP0
	STA	WSYNC
	STA	COLUBK
	STX	PF0
	STX	PF1
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1
	STX	CTRLPF

	STX	HMCLR
	STX	ENABL

	JMP	(temp01)