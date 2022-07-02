*
* Digit1 Pointer:		temp01 (+ temp02)
* Digit2 Pointer:		temp03 (+ temp04)
* Digit3 Pointer:		temp05 (+ temp06)
* Digit4 Pointer:		temp07 (+ temp08) 
* Digit5 Pointer:		temp09 (+ temp10)
* Digit6 Pointer:		temp11 (+ temp12)
* Digit7 Pointer:		temp13 (+ temp14)
* JumpBack Pointer:		temp15 (+ temp16)
* Gradient:			temp17 (+ temp18) 
* Color:			temp19
*				0-2: Store the number of digits!
*

#BANK#_SevenDigits_Kernel
	LDA	frameColor
	STA	WSYNC		; 76
	STA	COLUBK		; 3

	LDA	#0		; 2 (5)
	STA	GRP0		; 3 (8)
	STA	GRP1		; 3 (11)
	STA	PF0		; 3 (14)
	STA	PF1		; 3 (17)
	STA	PF2		; 3 (20)
	STA	HMCLR		; 3 (32)
	STA	REFP0		; 3 (35)
	STA	REFP1		; 3 (38)

	LDA	temp19		; 3 (41)
	sleep	2
	STA	RESP0		; 3 (46)
	sleep	3
	STA	RESP1		; 3 (52)

	AND	#%00000111	; 2 (54)
	CMP	#$06		; 2 (56)
	BCC	#BANK#_SevenDigits_5_digits_Mode   ; 2 (58)
	
	LDA	temp19		; 3 (59)
	AND	#%11110000	; 2 (61)
	ORA	#$06		; 2 (63)
	STA	temp19		; 3 (66)

	LDA	#$02		; 2 (68)
	STA	NUSIZ0		; 3 (71)
	LDA	#$02		; 2 (73)
	STA	NUSIZ1		; 3 (76)

	LDY	#7		; 2 
	CLC			; 2 (4)
	
	LDA	#$00		; 2 (6)
	STA	HMP0		; 3 (9)
	LDA	#$20		; 2 (11)
	STA	HMP1		; 3 (14)

	STA	WSYNC		; 76		
	STA	HMOVE		; 3

	LDA	counter		; 3 
	AND	#%00000001	; 2 
	TAX			; 2 
	LDA	#BANK#_SevenDigits_Offsets,x ; 5 
	STA	HMP0		; 3 
	STA	HMP1		; 3 

	LDA	frameColor	; 3 
	STA	COLUPF		; 3 
	LDA	#%000100	; 2
	STA	CTRLPF		; 3

	LDA	#%00000011	; 2
	STA	PF2		; 3

	STA	WSYNC		; 76		
	STA	HMOVE		; 3

	LDA	counter		; 3 (6)
	AND	#%00000001	; 2 (8) 
	CMP	#%00000001	; 2 (10)
	BEQ	#BANK#_SevenDigits_Odd_Init	; 2 (12)
	
	LDA	#$80
	STA	HMP0
	STA	HMP1

	
	JMP	#BANK#_SevenDigits_Even_Loop

	_align	90

#BANK#_SevenDigits_Even_Loop
	STA	WSYNC		; 76
	STA	HMOVE		; 3
	LDA	(temp17),y	; 5 (8)
	ADC	temp19		; 3 (11)
	STA	COLUP0		; 3 (14)
	STA	COLUP1		; 3 (17)

	LDA 	(temp13),y	; 5 (22)
	STA	GRP0		; 3 (25)

	LDA 	(temp09),y	; 5 (30)
	STA	GRP1		; 3 (33)

	sleep	5

	LAX 	(temp01),y	; 5
	LDA 	(temp05),y	; 5 
	STA	GRP0		; 3 
	STX	GRP1		; 3

	sleep	7
		
	LDA	#$00		; 2 (63)
	STA	HMP0		; 3 (66)
	STA	HMP1		; 3 (69)
	DEY			; 2 (71)

#BANK#_SevenDigits_Even_SecondLine
	STA	HMOVE		; 3 (74)

	LDA	(temp17),y	; 5 (3)
	ADC	temp19		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)
	
	LDA 	(temp11),y	; 5 (17)
	STA	GRP1		; 3 (20)

	LDA 	(temp07),y	; 5 (25)
	STA	GRP0		; 3 (28)

	sleep	15

	LDA 	(temp03),y	; 5 
	STA	GRP1		; 3 

	sleep	5

	LDA	#$80		; 2 (61)
	STA	HMP0		; 3 (64)
	STA	HMP1		; 3 (67)

	DEY
		
	BPL	#BANK#_SevenDigits_Even_Loop	; 2 (71)
	JMP	#BANK#_SevenDigits_Finish	
	
#BANK#_SevenDigits_Odd_Init	
	
	LDA	#$00		; 2 (14)
	STA	HMP0		; 3 (17)
	STA	HMP1		; 3 (20)

	
	_sleep	34
	sleep	3

	JMP	#BANK#_SevenDigits_Odd_Loop	; 3 (71)


	_align	86	

#BANK#_SevenDigits_Odd_Loop	
	STA	HMOVE		; 3 (74)
	LDA	(temp17),y	; 5 (3)
	ADC	temp19		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)
	
	LDA 	(temp11),y	; 5 (17)
	STA	GRP1		; 3 (20)

	LDA 	(temp07),y	; 5 (25)
	STA	GRP0		; 3 (28)

	sleep	15

	LDA 	(temp03),y	; 5 
	STA	GRP1		; 3 

	LDA	#$80		; 2 (65)
	STA	HMP0		; 3 (68)
	STA	HMP1		; 3 (71)
	DEY			; 2 (73)
	LAX 	(temp01),y	; 5
#BANK#_SevenDigits_Odd_SecondLine
	STA	WSYNC		; 76
	STA	HMOVE		; 3
	LDA	(temp17),y	; 5 (8)
	ADC	temp19		; 3 (11)
	STA	COLUP0		; 3 (14)
	STA	COLUP1		; 3 (17)

	LDA 	(temp13),y	; 5 (22)
	STA	GRP0		; 3 (25)

	LDA 	(temp09),y	; 5 (30)
	STA	GRP1		; 3 (33)

	sleep	3
	
	LDA 	(temp05),y	; 5 
	STA	GRP0		; 3 
	sleep	4
	STX	GRP1		; 3

	sleep	5

	LDA	#$00		; 2 (61)
	STA	HMP0		; 3 (64)
	STA	HMP1		; 3 (67)
	DEY			; 2 (69)
	
	BPL	#BANK#_SevenDigits_Odd_Loop	; 2 (71)
	JMP	#BANK#_SevenDigits_Finish

	_align	90

#BANK#_SevenDigits_5_digits_Mode 
	LDA	temp19		; 3 (59)
	AND	#%11110000	; 2 (61)
	ORA	#$06		; 2 (63)
	STA	temp19		; 3 (66)

	LDA	#$03		; 2 (68)
	STA	NUSIZ0		; 3 (71)
	LDA	#$01		; 2 (73)
	STA	NUSIZ1		; 3 (76)
	
	LDY	#7		; 2 
	CLC			; 2 (4)
	
	LDA	#$00		; 2 (6)
	STA	HMP0		; 3 (9)
	STA	ENABL		; 3 (12)
	LDA	#$10		; 2 (14)
	STA	HMP1		; 3 (17)

	sleep	22

	
	LAX	(temp01),y	; 5 
	TXS			; 2 

	STA	RESP0
	STA	RESP1

	STA	WSYNC		; 76		
	STA	HMOVE		; 3

#BANK#_SevenDigits_5_Loop
	STA	WSYNC		; 76
	LDA	(temp17),y	; 5 
	ADC	temp19		; 3 (8)
	STA	COLUP0		; 3 (11)
	STA	COLUP1		; 3 (14)

	LDA	(temp09),y	; 5 (17)
	STA	GRP0		; 3 (20)

	LDA	(temp07),y	; 5 (25)
	STA	GRP1		; 3 (28)

	sleep	6

	LAX	(temp03),y	; 5 
	LDA	(temp05),y	; 5 
	STA	GRP0		; 3 
	STX	GRP1		; 3 
	TSX			; 2 
	STX	GRP0		; 3 
	DEY			; 2 
	LAX	(temp01),y	; 5 
	TXS			; 2 
	INY
	DEY

	BPL	#BANK#_SevenDigits_5_Loop	; 2 (59)


#BANK#_SevenDigits_Finish
	LDA	#0
	STA	GRP0
	STA	GRP1
	STA	HMCLR
	STA	PF2
	STA	CTRLPF
	JMP	(temp15)

#BANK#_SevenDigits_Offsets
	BYTE	#$00
	BYTE	#$80

