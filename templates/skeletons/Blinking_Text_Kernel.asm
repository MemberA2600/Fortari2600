#NAME#_Blinking_Text

*
* Main Controller
*	  7: Text Ready
*	  6: Back Ready 
*         5: Corrector Indicator (just a pathetic hardcoded thing)	
*	  3-4: Blinking	(Slow - Fast)
*	  0-2: Background counter	
* temp01-temp08: Background Lines
* temp09-temp16: Text Colors	
* temp18: 	 IsItJustThru
*
* MainC: #VAR01#
* LineC: #VAR02#
* TextC: #VAR03#
* BackC: #VAR04#
*

#NAME#_Blinking_Text_Speed = #CON01#

	JMP	#NAME#_Blinking_Text_FirstJump
	_align	215


#NAME#_Blinking_Text_FirstJump
	STA	WSYNC			; 76
	
	LDA	#0
	STA	temp18

	LDA	#VAR01#
	AND	#%00011000
	STA	temp17

	LDA	#VAR01#
	AND	#%11100111
	STA	#VAR01#

	LDA	counter			; 3
	AND	##NAME#_Blinking_Text_Speed		; 2 (5)
	CMP	##NAME#_Blinking_Text_Speed		; 2 (7)
	BNE	#NAME#_Blinking_Text_SetupBackLines	; 2 (9)

	LDA	#%10000000
	STA	temp18

	BIT 	#VAR01#			; 3 
	BVS	#NAME#_Blinking_Text_SetupBackLines	; 2
	BMI	#NAME#_Blinking_Text_BackGround_Change	; 2 (23)
	
	LDA	counter
	LDX	##NAME#_Blinking_Text_Speed
#NAME#_Blinking_Text_Speed_Loop
	CPX	#0
	BEQ	#NAME#_Blinking_Text_Speed_Loop_End
	LSR
	DEX
	JMP	#NAME#_Blinking_Text_Speed_Loop	
#NAME#_Blinking_Text_Speed_Loop_End
	EOR	random
	AND	#%00000111
	TAX

	LDA	#VAR02#			; 3 (35)
	ORA	#NAME#_Blinking_Text_BitMask1,x	; 4 (39)
	STA	#VAR02#			; 3 (42)

	CMP	#255			; 2 (44)
	BNE	#NAME#_Blinking_Text_DontSetReady ; 2 (46)

	LDA	#VAR01#			; 3 (49)
	ORA	#%10000000		; 2 (51)
	STA	#VAR01#			; 3 (54)
#NAME#_Blinking_Text_DontSetReady
	LDA	frameColor		; 3 
	LDX	#8
#NAME#_Blinking_Text_BlankLoop
	STA	temp01,x		; 3 	
	DEX				; 2
	BPL	#NAME#_Blinking_Text_BlankLoop	; 2

	JMP	#NAME#_Blinking_Text_PrepareDone	; 3 (8)

#NAME#_Blinking_Text_BackGround_Change
	LDA	#VAR01#					; 3 (21)
	EOR	#255					; 2
	AND	#%00000111				; 2
	STA	temp19					; 3 (32)

	sleep	7

	LDX	#7					; 2 (42)
	CLC						; 2 (44)
	LDY	frameColor				; 3 (47)

*
#NAME#_Blinking_Text_BackGround_Change_Loop
*
*	One loop: 22
*	x8 : 88
*
	LDA	#NAME#_Blinking_Text_Back_Gradient,x	; 4 
	CMP	temp19					; 3 
	BCS	#NAME#_Blinking_Text_BackGround_Change_Loop_NoZero  ; 2 

	TYA							    ; 2	
	JMP	#NAME#_Blinking_Text_BackGround_Change_Loop_WasZero  ; 3 
#NAME#_Blinking_Text_BackGround_Change_Loop_NoZero
	CLC							; 2
	ADC	#VAR04#						; 3
#NAME#_Blinking_Text_BackGround_Change_Loop_WasZero
*******	STA	temp01,x					; 4
#STA02#
	DEX							; 2
	BPL	#NAME#_Blinking_Text_BackGround_Change_Loop	; 2

	BIT	temp18
	BMI	#NAME#_Blinking_Text_BackGround_Change_Loop_Progess
	JMP	#NAME#_Blinking_Text_SecondJump
#NAME#_Blinking_Text_BackGround_Change_Loop_Progess

	LDA	#%1100000
	STA	temp18

	INC	#VAR01#
	LDA	#VAR01#

	CMP	#%10000111
	BNE	#NAME#_Blinking_Text_BackGround_Change_NotSetDone
	ORA	#%01000000
	STA	#VAR01#
#NAME#_Blinking_Text_BackGround_Change_NotSetDone

	JMP	#NAME#_Blinking_Text_PrepareDone

#NAME#_Blinking_Text_SetupBackLines

	BIT	#VAR01#
	BMI 	#NAME#_Blinking_Text_SetupBackLines_NoJumPBack
	JMP	#NAME#_Blinking_Text_DontSetReady

#NAME#_Blinking_Text_SetupBackLines_NoJumPBack
	BVS	#NAME#_Blinking_Text_SetupBackLines_NoJumPBack2
	JMP	#NAME#_Blinking_Text_BackGround_Change

#NAME#_Blinking_Text_SetupBackLines_NoJumPBack2

	sleep	7
				
	LDX	#7
	CLC

#NAME#_Blinking_Text_SetupBackLines_Loop
	LDA	#NAME#_Blinking_Text_Back_Gradient,x
	ADC	#VAR04#	
	STA	temp01,x
	DEX
	BPL	#NAME#_Blinking_Text_SetupBackLines_Loop

#NAME#_Blinking_Text_PrepareDone

	LDX	#7
	LDY	#VAR02#
	CLC
#NAME#_Blinking_Text_AddColorToText
	TYA
	BMI	#NAME#_Blinking_Text_LoadColor

	BYTE	#$AD
	BYTE	#frameColor
	BYTE	#0

	JMP	#NAME#_Blinking_Text_LoadColorLoaded
#NAME#_Blinking_Text_LoadColor

	LDA	#VAR03#
	ADC	#NAME#_Blinking_Text_Text_Gradient,x
#NAME#_Blinking_Text_LoadColorLoaded
******	STA	temp09,x
#STA01#

	TYA
	ASL	
	TAY		

	DEX
	BPL	#NAME#_Blinking_Text_AddColorToText

	JMP	#NAME#_Blinking_Text_SecondJump
	_align	175

#NAME#_Blinking_Text_SecondJump
	BIT	temp18
	BMI	#NAME#_Blinking_Text_NoCorrect1
	BIT	#VAR01#
	BVS	#NAME#_Blinking_Text_NoCorrect1
	STA	WSYNC
	BPL	#NAME#_Blinking_Text_NoCorrect1
	STA	WSYNC
#NAME#_Blinking_Text_NoCorrect1
	BIT	temp18
	BVS	#NAME#_Blinking_Text_NoCorrect2

	STA	WSYNC
	STA	WSYNC
	STA	WSYNC
#NAME#_Blinking_Text_NoCorrect2

	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	#NAME#_Blinking_Text_NoCorrect3
	LDA	#VAR01#
	CMP	#%11000111
	BNE	#NAME#_Blinking_Text_NoCorrect3	
	LDA	#%11100111
	STA	#VAR01#
	STA	WSYNC
#NAME#_Blinking_Text_NoCorrect3
	LDA	frameColor
	LDX	#0
	STA 	WSYNC		; 76
	STA	COLUBK	
	STX	PF0
	STX	PF1
	STX	PF2
	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1		; 33

	STA	RESP0		
	sleep 	3		
	STA	RESP1		; 9 (42)

	LDA	#$02		; 2 (44)
	STA	NUSIZ0		; 3 (47)
	STA	NUSIZ1		; 3 (50)

	LDA	#$E0		; 2 (52)
	STA	HMP0		; 3 (55)
	LDA	#$00		; 2 (57)
	STA	HMP1		; 3 (60)

	LDX	#7		; 2 (62)

	LDA	#VAR01#		
	ORA	temp17
	STA	#VAR01#		; 8 (70)

	STA	WSYNC
	BIT 	#VAR01#		
	BPL	#NAME#_Blinking_Text_NoBlinking
	BVC	#NAME#_Blinking_Text_NoBlinking

	LDA	temp17
	LSR
	LSR
	LSR
	TAY
	LDA	#NAME#_Blinking_Text_BlinkingMasks,y
	CMP	#0
	BEQ	#NAME#_Blinking_Text_NoBlinking

	STA	temp17 

	LDA	counter
	AND	temp17
	CMP	temp17
	BNE	#NAME#_Blinking_Text_NoBlinking

#NAME#_Blinking_Text_BlinkColorLoop
	LDA	temp01,x
	STA	temp09,x
	DEX
	BPL	#NAME#_Blinking_Text_BlinkColorLoop
	LDX	#7
	JMP	#NAME#_Blinking_Text_Blinked

#NAME#_Blinking_Text_BitMask1
	BYTE	#%00000001
	BYTE	#%00000010
	BYTE	#%00000100
	BYTE	#%00001000
	BYTE	#%00010000
	BYTE	#%00100000
	BYTE	#%01000000
	BYTE	#%10000000

#NAME#_Blinking_Text_NoBlinking
	STA	WSYNC
#NAME#_Blinking_Text_Blinked
	STA	WSYNC
	STA	HMOVE		; 3
	
	LDA	counter		; 3 (6)
	AND	#%00000001	; 2 (8) 
	CMP	#%00000001  	; 2 (10)
	BEQ	#NAME#_Blinking_Text_Odd_Frame   ; 2 (12)
	JMP	#NAME#_Blinking_Text_Even_Frame  ; 3 (15)

#NAME#_Blinking_Text_BlinkingMasks
	BYTE	#0
	BYTE	#%01000000
	BYTE	#%00100000
	BYTE	#%00010000

	_align 	220

#NAME#_Blinking_Text_Even_Frame
	LDA	#$80
	STA	HMP0
	STA	HMP1
#NAME#_Blinking_Text_Even_Frame_Loop	
	STA	WSYNC		; 76
	STA	HMOVE		; 3
	
	LDA	temp01,x
	STA	COLUBK

	LDA	#NAME#_Blinking_Text_Letter1,x	; 5 (8)
	STA	GRP0				; 3 (11)

	LDA	#NAME#_Blinking_Text_Letter3,x	; 5 (16)
	STA	GRP1				; 3 (19)

	LDA	temp09,x
	STA	COLUP0
	STA	COLUP1		; 10

	sleep	6

	LDA	#NAME#_Blinking_Text_Letter5,x	; 5 
	STA	GRP0				; 3

	LDA	#NAME#_Blinking_Text_Letter7,x	; 5
	STA	GRP1				; 3

	LDA	#$00		; 2 
	STA	HMP0		; 3 
	STA	HMP1		; 3 

	sleep	8

	STA	HMOVE				; Early 74

	LDA	#NAME#_Blinking_Text_Letter0,x	; 5 (3)
	STA	GRP0				; 3 (6)

	LDA	#NAME#_Blinking_Text_Letter2,x	; 5 (11)
	STA	GRP1				; 3 (14)

	LDA	#$80
	STA	HMP0
	STA	HMP1

	sleep	15

	LDA	#NAME#_Blinking_Text_Letter4,x	; 5 
	STA	GRP0				; 3

	LDA	#NAME#_Blinking_Text_Letter6,x	; 5
	STA	GRP1				; 3

	DEX	
	BPL	#NAME#_Blinking_Text_Even_Frame_Loop
	JMP	#NAME#_Blinking_Text_End

#NAME#_Blinking_Text_Odd_Frame

	sleep	3
#NAME#_Blinking_Text_Odd_Frame_Jump2
	LDA	#$80
	STA	HMP0
	STA	HMP1	; 8 (23)
	
	_sleep	32
	LDA	temp01,x
	TAY
#NAME#_Blinking_Text_Odd_Frame_Loop
	sleep	6
	STA	HMOVE   ; Early 74
	STY	COLUBK
	LDA	#NAME#_Blinking_Text_Letter0,x	; 5 (3)
	STA	GRP0				; 3 (6)

	LDA	#NAME#_Blinking_Text_Letter2,x	; 5 (11)
	STA	GRP1				; 3 (14)

	LDA	temp09,x
	STA	COLUP0
	STA	COLUP1		; 10

	LDA	#$80
	STA	HMP0
	STA	HMP1

	sleep	2

	LDA	#NAME#_Blinking_Text_Letter4,x	; 5 
	STA	GRP0				; 3

	LDA	#NAME#_Blinking_Text_Letter6,x	; 5
	STA	GRP1				; 3

	STA	WSYNC	
	STA	HMOVE	; 3

	LDA	#NAME#_Blinking_Text_Letter1,x	; 5 (8)
	STA	GRP0				; 3 (11)

	LDA	#NAME#_Blinking_Text_Letter3,x	; 5 (16)
	STA	GRP1				; 3 (19)

	LDA	#$00	; 2 (21)
	STA	HMP0	; 3 (24)
	STA	HMP1 	; 3 (27)

	DEX			; 2
	LDA	temp01,x	; 4
	TAY			; 2
	INX			; 2
	sleep	5	; 42

	LDA	#NAME#_Blinking_Text_Letter5,x	; 5 (47)
	STA	GRP0				; 3 (50)

	LDA	#NAME#_Blinking_Text_Letter7,x	; 5 (55)
	STA	GRP1				; 3 (58)


	sleep	4

	DEX		; 2 (69)
	BPL	#NAME#_Blinking_Text_Odd_Frame_Loop	; 2 (71)
	

#NAME#_Blinking_Text_End

	LDX	#0
	LDA	frameColor
	STA	WSYNC		; 76
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1
	STX	GRP0
	STX	GRP1
	STA	HMCLR
