
*	JumpBack Pointer: temp01 (+ temp02)
*	Data		: temp03	
*	ColorAdd	: temp04
*	Color1:		: temp05
*	Color2:		: temp12
*	Color3:		: temp13
*	Gradient Pointer: temp06 (+ temp07)
*
*	PF1_1		: temp08 (Normal)
*	PF2_1		: temp09 (Reflected)
*	PF2_2		: temp10 (Normal)
*	PF1_2		: temp11 (Reflected)
*
*	temp14		: Y
*

#BANK#_FullBar_Kernel
	LDA	frameColor
	STA	WSYNC		; 76
	STA	COLUBK		; 3
	
	LDA	#0		; 2 (5)
	STA	PF0		; 3 (8)
	STA	PF1		; 3 (11)
	STA	PF2		; 3 (14)
	STA	GRP0		; 3 (17)
	STA	GRP1		; 3 (20)

	LDY	#0		; 2 (22)
	LDX	#255		; 2 (24)	

	LDA	temp03					; 3 (27)
	CMP	#8					; 2 (29)
	BCS	#BANK#_FullBar_LargerThan7		; 2 (31)
	STY	temp09					; 3 (34)
	STY	temp10					; 3 (37)
	STY	temp11					; 3 (40)
	TAY						; 2 (42)
	LDA	#BANK#_Bar_Normal,y			; 5 (47)
	STA	temp08					; 3 (50)
	JMP	#BANK#_FullBar_Kernel_Values_Done	; 3 (53)
#BANK#_FullBar_LargerThan7
	SEC						; 2 (33)
	SBC	#8					; 2 (35)
	CMP	#8					; 2 (37)
	BCS	#BANK#_FullBar_LargerThan15		; 2 (39)
	STX	temp08					; 3 (42)
	STY	temp10					; 3 (45)
	STY	temp11					; 3 (48)
	TAY						; 2 (50)
	LDA	#BANK#_Bar_Inverted,y			; 5 (55)
	STA	temp09					; 3 (58)
	JMP	#BANK#_FullBar_Kernel_Values_Done	; 3 (61)
#BANK#_FullBar_LargerThan15
	SEC						; 2 (41)
	SBC	#8					; 2 (43)
	CMP	#8					; 2 (45)
	BCS	#BANK#_FullBar_LargerThan23		; 2 (47)
	STX	temp08					; 3 (50)
	STX	temp09					; 3 (53)
	STY	temp11					; 3 (56)
	TAY						; 2 (58)
	LDA	#BANK#_Bar_Normal,y			; 5 (63)
	STA	temp10					; 3 (67)
	JMP	#BANK#_FullBar_Kernel_Values_Done	; 3 (70)

#BANK#_FullBar_LargerThan23
	SEC						; 2 (49)
	SBC	#8					; 2 (51)
	STX	temp08					; 3 (54)
	STX	temp09					; 3 (57)
	STX	temp10					; 3 (60)
	TAY						; 2 (62)
	LDA	#BANK#_Bar_Inverted,y			; 5 (67)
	STA	temp11					; 3 (70)
#BANK#_FullBar_Kernel_Values_Done
	LDY	#7				; 2 (72)
	LDA	#1				; 2 (74)
	STA	CTRLPF				; 3 (1)
	LDA	temp03				; 3 (4)
	LSR					; 2 (6)
	LSR					; 2 (8)
	STA	temp04				; 3 (11)
	LDA	#7				; 2 (13)
	CMP	temp04				; 3 (16)
	BCS	#BANK#_FullBar_Kernel_NoLimit	; 2 (18)
	STA	temp04				; 3 (21)
#BANK#_FullBar_Kernel_NoLimit
	LDA	temp05	
	CLC		
	ADC	temp04	
	STA	temp05 		; 11 (32)

	LDA	temp12	
	CLC		
	ADC	temp04	
	STA	temp12 		; 11 (43)

	LDA	temp13	
	CLC		
	ADC	temp04	
	STA	temp13 		; 11 (54)

	STY	temp14		; 3  (57)

	JMP	#BANK#_FullBar_Kernel_Loop 	; 3 (73)
	
	_align	30

#BANK#_FullBar_Kernel_Loop
	STA	WSYNC			; 3 (76)
	LDA	(temp06),y		; 5
	TAX				; 2 (7)
	ADC	temp05			; 3 (10)
	STA	COLUPF			; 3 (13)

	LDA	temp08			; 3 (16)
	STA	PF1			; 3 (19)
	LDA	temp09			; 3 (21)
	STA	PF2			; 3 (24)

	sleep	2

	TXA				; 2 (26)
	ADC	temp13			; 3 (29)
	TAY				; 2 (31)

	TXA				; 2 (33)
	ADC	temp12			; 3 (36)
	STA	COLUPF			; 3 (39)
	
	LDA	temp10			; 3 (46)
	STA	PF2			; 3 (49)
	LDA	temp11			; 3 (52)
	STA	PF1			; 3 (55)
	STY	COLUPF			; 3 (58)

	DEC	temp14			; 5 (63)
	LDY	temp14			; 3 (66)
	CPY	#255			; 2 (68)

	BNE	#BANK#_FullBar_Kernel_Loop ; 2 (70)
	LDA	#0
	STA	WSYNC
	STA	PF1
	STA	PF2
	JMP	(temp01)
	
	