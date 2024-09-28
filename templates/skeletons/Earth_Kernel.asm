*
*	temp01:		 Index
*
*	temp02 + temp03: Sprite Pointer1
*	temp04 + temp05: Sprite Pointer2	
*	temp06 + temp07: Sprite Pointer3
*	temp08 + temp09: Sprite Pointer4
*
*

#NAME#_Earth

	LDA	#VAR01#
	AND	#%11100000
	STA	temp19
	AND	#%01100000
	LSR
	LSR
	LSR
	ORA	#%00000011	
	STA	temp18

	LDA	counter
	AND	temp18
	CMP	temp18
	BEQ	#NAME#_Earth_Change
	sleep	14
	LDA	#VAR01#
	JMP	#NAME#_Earth_Index_Done

#NAME#_Earth_Change
	LDA	#VAR01#
	BMI	#NAME#_Earth_DECR
*
*	Must be 0-31, 32%6 > 5
*
	AND	#%00011111
	TAX
	INX	
	TXA
	CMP	#31
	BNE	#NAME#_Earth_NoZero	
	LDA	#0
#NAME#_Earth_NoZero
	JMP	#NAME#_Earth_Index_Done
#NAME#_Earth_DECR
	AND	#%00011111
	TAX
	DEX	
	TXA
	CMP	#255
	BNE	#NAME#_Earth_Index_Done	
	LDA	#30

#NAME#_Earth_Index_Done
	ORA	temp19
	STA	#VAR01#
	AND	#%00011111
	SEC	
#NAME#_Earth_Index_Loop
	CMP	#6
	BCC	#NAME#_Earth_Index_Loop_End
	SBC	#6
	JMP	#NAME#_Earth_Index_Loop		

#NAME#_Earth_Index_Loop_End
	STA	temp01
	LDA	#VAR01#
	STA	temp18
*
*	From here goes the kernel part
*

#NAME#_Earth_Kernel_Calculate

	LDA	temp01
	ASL
	STA	temp18
	LDX	#254
*
*	For sync
*
	sleep	8

#NAME#_Earth_Kernel_Calculate_Loop
	INX
	INX
	TXA
	CLC
	ADC	temp18
	TAY	
	LDA	#BANK#_Earth_PointerTable,Y
	STA	temp02,x
	LDA	#BANK#_Earth_PointerTable+1,Y
	STA	temp03,x

	CPX	#6
	BCC	#NAME#_Earth_Kernel_Calculate_Loop

	JMP	#NAME#_Earth_Kernel

	_align	56

#NAME#_Earth_BG_Color
### &COLOR
!!!Earth_BG_Color!!!

#NAME#_Earth_Kernel
	LDX	#0
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK
	STA	COLUPF
	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STX	ENABL
	STX	NUSIZ0

	LDA 	#255
	STA	PF0
	STA	PF1

	LDA	#$01
	STA	NUSIZ0
	STA	NUSIZ1
	STA	RESP0
	STA	RESP1

	LDA	#%00000101
	STA	CTRLPF

	LDA	$20
	STA	HMP0
	LDA	$30
	STA	HMP1

	STA	WSYNC
	STA	HMOVE

	LDY	#55

	LDA	#VAR02#
!!!ShiftToRight!!!
	STA	COLUP0
	STA	COLUP1


	JMP	#NAME#_Earth_Kernel_Loop
*
*	Pointers: temp02, temp04, temp06, temp08
*
*
	_align	35

#NAME#_Earth_Kernel_Loop
	STA	WSYNC			

	LDA	#BANK#_Earth_Playfield,y ; 4
	STA	PF2			; 3 (7)
	
	LDA	#NAME#_Earth_BG_Color,y  ; 4 (11) 
	STA	COLUBK			; 3 (14)

	LDA	(temp02),y		; 5 (19)
	STA	GRP0			; 3 (24)

	LDA	(temp04),y		; 5 (29)
	STA	GRP1			; 3 (32)

	sleep	4

	LAX	(temp08),y		; 5 (37)			
	LDA	(temp06),y		; 5 (42)
	STA	GRP0
	STX	GRP1

	DEY
	BMI	#NAME#_Earth_Reset
	JMP	#NAME#_Earth_Kernel_Loop

#NAME#_Earth_Reset
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STX	PF0
	STX	PF1
	STX	PF2
	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STA	CTRLPF
