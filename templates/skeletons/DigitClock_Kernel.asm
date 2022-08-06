*
* JumpBack Pointer:	temp01 (+ temp02) 
* Digit0_Pointer:	temp03 (+ temp04)
* Digit1_Pointer: 	temp05 (+ temp06)
* Digit2_Pointer: 	temp07 (+ temp08)
* Digit3_Pointer: 	temp09 (+ temp10)
* AM/PM  Pointer: 	temp11 (+ temp12)
* Gradient_Pointer:	temp15 (+ temp16)
* Color:		temp17 (bit 0 is if AM/PM)
*

#BANK#_DigitClock_Kernel
	LDA	frameColor
	STA	WSYNC		; 76
	STA	COLUBK		; 3
	STA	COLUPF		; 3 (6)
	LDA	#0		; 2 (8)

	STA	GRP0		; 3 (11)
	STA	GRP1		; 3 (14)
	STA	ENAM0		; 3 (17)
	STA	ENAM1		; 3 (20)
	STA	PF0		; 3 (23)
	STA	PF1		; 3 (26)
	STA	PF2		; 3 (29)
	STA	ENABL		; 3 (32)

	STA	RESP0		  
	STA	RESP1		 
	STA	RESM0	

	LDA	#$06		; 2 
	STA	NUSIZ0		; 3 
	LDA	#$02		; 2
	STA	NUSIZ1		; 3 

	LDA	#$20		
	STA	HMP0		; 

	LDA	#$30		; 
	STA	HMP1		; 

	LDA	#$C0		; 
	STA	HMM0		; 15

	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDY	#7		; 2 (5)

	LDA	#%00000101	; 2 (7)
	STA	CTRLPF		; 3 (10)
	
	LDA	temp17		; 3 (13)
	AND	#%00000001	; 2 (15)
	ASL
	ASL
	ASL
	STA	temp19
	LDA	#<#BANK#_DigitClock_Kernel_AM
	ADC	temp19
	STA	temp11
	LDA	#>#BANK#_DigitClock_Kernel_AM
	STA	temp12
	
	LDA	#255		; 2
	STA	PF0		; 3
	LDA	#%00001100	; 2
	STA	PF1		; 3
	CLC			; 2 

	LDA	counter		; 3 
	ROL
	ROL
	ROL			; 6 

	AND	#%00000001	; 2 
	TAX			; 2 
	LDA	#BANK#_DigitClock_Kernel_PF2,x	; 4 
	STA	PF2		; 3 

	LAX	(temp09),y			; 5 
	LDA	#0
	STA	REFP0
	STA	REFP1
	
	LDA	temp17
	AND	#%11111110
	STA	temp17

	JMP	#BANK#_DigitClock_Kernel_Loop	; 3 
#BANK#_DigitClock_Kernel_PF2
	BYTE	#%00010000
	BYTE	#%00011100

	_align 	56

#BANK#_DigitClock_Kernel_AM
	BYTE	#%00010001
	BYTE	#%00010001
	BYTE	#%00010101
	BYTE	#%00011011
	BYTE	#%10010000
	BYTE	#%11110000
	BYTE	#%10010000
	BYTE	#%01100000
#BANK#_DigitClock_Kernel_PM
	BYTE	#%00010001
	BYTE	#%00010001
	BYTE	#%00010101
	BYTE	#%00011011
	BYTE	#%10000000
	BYTE	#%11110000
	BYTE	#%10010000
	BYTE	#%11100000

#BANK#_DigitClock_Kernel_Loop
	STA	WSYNC				; 76

	TYA					; 2 
	SBC	#2				; 2 (4)
	STA	ENAM0				; 3 (7)

	LDA	(temp03),y			; 5 (12)
	STA	GRP0				; 3 (15)

	LDA	(temp05),y			; 5 (20)
	STA	GRP1				; 3 (23)	

	LDA	(temp15),y			; 5 (28)
	ADC	temp17				; 3 (31)
	
	STA	COLUP0				; 3 (34)	
	STA	COLUP1				; 3 (37)

	LDA	(temp07),y			; 5 (42)
	STA	GRP0				; 3 (45)
	STX	GRP1				; 3 (48)

	LDA	(temp11),y			; 5 (53)
	STA	GRP0				; 3 (56)

	DEY					; 2 (70)
	LAX	(temp09),y			; 5 (50)
	CPY	#255				; 2 (70)
	BNE	#BANK#_DigitClock_Kernel_Loop	; 2 (72)

#BANK#_DigitClock_Kernel_End
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUP0
	STA	COLUP1
	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STX	HMCLR
	STX	PF0
	STX	PF1
	STX	PF2
	STX	CTRLPF

	JMP	(temp01)