*
* How to branch!
* I always forget these!!
*
* X < Y
* LDA	X	
* CMP	Y
* BCS   else 	 
*
* X <= Y
*
* LDA	Y
* CMP	X
* BCC	else
*
* X > Y 
*
* LDA	Y
* CMP	X
* BCS	else
*
* X >= Y
*
* LDA	X
* CMP	Y
* BCC 	else
*



*Init Section
*---------------------------
* This is were variables and
* constants are asigned.
*
* This does not count into the
* ROM space.
*

random = $80
counter = $81
stack = $82
temp01 = $83
temp02 = $84
temp03 = $85
temp04 = $86
temp05 = $87
temp06 = $88
temp07 = $89
temp08 = $8a
temp09 = $8b
temp10 = $8c
temp11 = $8d
temp12 = $8e
temp13 = $8f
temp14 = $90
temp15 = $91
temp16 = $92
temp17 = $93
temp18 = $94
temp19 = $95

************************
*
* Constants
*-----------------------

NTSC_Vblank   =	169
NTSC_Overscan =	163
NTSC_Display  = 229

PAL_Vblank   =	169
PAL_Overscan =	206
PAL_Display  =  244


***************************
********* Start of 1st bank
***************************

	fill 256	; We have to prevent writing on addresses taken by the SuperChip RAM.

###Start-Bank1

*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank1

*
* Bank1 contains the main kernel and basically the game itself.
* This section is read as you start a new game.
*
*
		
	JMP	WaitUntilOverScanTimerEndsBank1

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank1


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank1

	CLC
        LDA	INTIM 
        BNE 	OverScanBank1

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#NTSC_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*








*VSYNC
*----------------------------7
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank1
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank1

* Sync the Screen
*

	LDA 	#2
	STA 	WSYNC  ; one line with VSYNC
	STA 	VSYNC	; enable VSYNC
	STA 	WSYNC 	; one line with VSYNC
	STA 	WSYNC 	; one line with VSYNC
	LDA 	#0
	STA 	WSYNC 	; one line with VSYNC
	STA 	VSYNC 	; turn off VSYNC

* Set the timer for VBlank
*
	STA	VBLANK
	STA 	WSYNC

	CLC
 	LDA	#NTSC_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank1



*SkipIfNoGameSet - VBLANK
*---------------------------------
*


VBlankEndBank1
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank1

    	LDA	#NTSC_Display
    	STA	TIM64T


*Screen
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	stack


	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	
*
*
*
*


	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	stack
	txs

	JMP	OverScanBank1

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

*Routines Section 
*----------------------------------
* Reusable code
*

###End-Bank1

	align	256

	saveFreeBytes
	rewind 1fd4

start_bank1 
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address   
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 1ffc
   	.byte 	#<start_bank1
   	.byte 	#>start_bank1
   	.byte 	#<start_bank1
   	.byte 	#>start_bank1

***************************
********* Start of 2nd bank
***************************
	Bank 2

	fill	256
###Start-Bank2
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*


EnterScreenBank2

*
* This is the very first screen you witness as
* you startup the game. Contains the menu.
*
*

	LDA	#0
	STA	AUDV0
	STA	AUDV1
*
*	Mute any sound.
*
	STA	ENAM0
	STA	ENAM1
	STA	ENABL

*
*	Disable missiles and ball.
*
*
* 	The columns are 8 lines tall.
*
ScrollingColumn1 = $96
ScrollingColumn2 = $9E
ScrollingColumn3 = $A6
ScrollingColumn4 = $AE
*
*	Next free one: $B7
*
WaitCounter = $B7

PressedDelay = $B8
*	7th bit   : ON / OFF
*	6th bit   : Checks if fire was hold at the beginning.
*	All others: 6bit counter


	LDX	#8
Bank2InitScrollingColumns	
	STA	ScrollingColumn1,x
	STA	ScrollingColumn2,x
	STA	ScrollingColumn3,x
	STA	ScrollingColumn4,x
	DEX
	BPL	Bank2InitScrollingColumns

	STA	PressedDelay

	LDA	#255
	STA	WaitCounter

*
*	Superchip RAM $F0000 - F0015 is reserved for long time storage!
* 	Never use those!
*

	LDA	#0
	BIT 	INPT4
	BMI	Bank2_No_Joy0_Fire_Was_Pressed_At_Enter
	LDA	#%01000000
Bank2_No_Joy0_Fire_Was_Pressed_At_Enter
	STA	PressedDelay

	JMP	WaitUntilOverScanTimerEndsBank2

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank2


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank2

	CLC
        LDA	INTIM 
        BNE 	OverScanBank2

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#NTSC_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*


*
*	Fill the SARA with JinJang PF data!
*

JinJang_Col_01W = $F016
JinJang_Col_01R = $F096

JinJang_Col_02W = $F036
JinJang_Col_02R = $F0B6

JinJang_ColorW = $F056
JinJang_ColorR = $F0D6

	LDA	counter
	LSR
	LSR
	AND	#%00000111
	TAY
	LSR
***	LSR
	AND	#%00000011
	TAX
	LDA	JingJang_Color_Adder,y
	STA	temp05
*
*	temp01: The low  nibble for JJ Left
*	temp02: The high nibble for JJ Left
*	temp03: The low  nibble for JJ Right
*	temp04: The high nibble for JJ Right
*       temp05: Amplitude
*

	LDA	JingJang_00_LookUp,x	
	STA	temp01			

	LDA	#>JinJang_1_00		
	STA	temp02			

	LDA	JingJang_01_LookUp,x	
	STA	temp03			

	LDA	#>JinJang_1_01		
	STA	temp04			

	LDY	#15
	LDX	#31

JinJang_Fill_SARA
	LDA	(temp01),y		
	STA	JinJang_Col_01W,x

	LDA	(temp03),y		
	STA	JinJang_Col_02W,x

	LDA	temp05
	BPL	JinJang_Fill_SARA_HasColor_1
	LDA	#0
	JMP	JinJang_Fill_SARA_Nope_1
JinJang_Fill_SARA_HasColor_1
	LDA	JinJang_Colors_32,x
	CLC
	ADC	temp05
JinJang_Fill_SARA_Nope_1
	STA	JinJang_ColorW,x

	DEX
	LDA	(temp01),y		
	STA	JinJang_Col_01W,x

	LDA	(temp03),y		
	STA	JinJang_Col_02W,x

	LDA	temp05
	BPL	JinJang_Fill_SARA_HasColor_2
	LDA	#0
	JMP	JinJang_Fill_SARA_Nope_2
JinJang_Fill_SARA_HasColor_2
	LDA	JinJang_Colors_32,x
	CLC
	ADC	temp05
JinJang_Fill_SARA_Nope_2
	STA	JinJang_ColorW,x

	DEY
	DEX
	BPL	JinJang_Fill_SARA

*
*	Text is based on mirrored playfield.
*	So shifting bits to the left goes like this.
*	Non-mirrored PF1 << Mirrored PF2 << Non-Mirrored PF2 << Mirrored PF1 << Buffer
*	temp 19 is tud buffer.	
*
*	

Bank2FirstNum = 180
Bank2SecondNum = 150

	LDA	counter
	AND	#%0000011
	CMP	#%0000011
	BNE	Bank2WaitCounterNoChange

	INC	WaitCounter
	LDA	WaitCounter
	CMP	#Bank2FirstNum
	BCC	Bank2WaitCounterNotLargerThan1

	LDA	#0
	STA	WaitCounter
	JMP	Bank2WaitCounterNoMoreThings
Bank2WaitCounterNotLargerThan1
	CMP	#Bank2SecondNum
	BCC	Bank2WaitCounterNotLargerThan2

	LDA	#0
	JMP	Bank2WaitCounterNoMoreThings
Bank2WaitCounterNotLargerThan2
	TAX

	LDA	Impure_Soul_Eclipse,x
Bank2WaitCounterNoMoreThings
	STA	temp19

	LDX	#7
Bank2ShiftingLoop
	LSR	temp19
	ROR	ScrollingColumn4,x
	ROL	ScrollingColumn3,x
	ROR	ScrollingColumn2,x
	ROL	ScrollingColumn1,x
	DEX
	BPL	Bank2ShiftingLoop

Bank2WaitCounterNoChange

	BIT 	INPT4
	BPL	Bank2_No_Joy0_Fire_Was_Released_At_Overscan
	LDA	PressedDelay
	AND	#%10111111
	STA	PressedDelay
Bank2_No_Joy0_Fire_Was_Released_At_Overscan


*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank2
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank2

* Sync the Screen
*

	LDA 	#2
	STA 	WSYNC  ; one line with VSYNC
	STA 	VSYNC	; enable VSYNC
	STA 	WSYNC 	; one line with VSYNC
	STA 	WSYNC 	; one line with VSYNC
	LDA 	#0
	STA 	WSYNC 	; one line with VSYNC
	STA 	VSYNC 	; turn off VSYNC

* Set the timer for VBlank
*
	STA	VBLANK
	STA 	WSYNC

	CLC
 	LDA	#NTSC_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank2



*SkipIfNoGameSet - VBLANK
*---------------------------------
*


VBlankEndBank2
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank2

    	LDA	#NTSC_Display
    	STA	TIM64T


*Screen
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	stack

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUPF		; 3 
	STA	COLUP0		; 3 (6)
	STA	COLUP1		; 3 (9)
	STA	COLUBK		; 3 (12)	

*
* The Touhou logo has two seperated parts.
* First, a spinning jinjang ball in the background.	
* The other part is the Touhou 2600 text.
*

Bank2_DrawLogo
	STA	PF0		; 3 (15)
	STA	PF1		; 3 (18)
	STA	NUSIZ1		; 3 (21)
*
*	CTRLPF bits:
*	0  : Mirrored
*	1  : Two Colors
*	2  : Players move behind playfield
*	4-5: Ball Size
* 
	LDA	#%0000001	; 2 (20)
	STA	CTRLPF		; 3 (23)
*
*	Mirrored playfield.
*
	
	LDA	counter		; 3 (26)
	LSR
	LSR		
	LSR			; 6 (32)

	AND	#%00000011	; 2 (34)
	STA	RESP0
	TAX			; 2 (36)
	STA	RESP1

	LDA	#$02			; 2 
	STA	NUSIZ0			; 3
*
*	P0 spites set to 2 instances with medium gaps.
*

	LDA	counter
	AND	#$0F
	TAX
	LDA	Touhou_Title_Color,x
	STA	COLUP0
	STA	COLUP1

	LDA	#$10
	STA	HMP0
	LDA	#$00
	STA	HMP1
	
	STA	WSYNC
	STA	HMOVE

	LDX	#4
Bank2_Blank_Lines1
	STA	WSYNC
	DEX
	BPL	Bank2_Blank_Lines1

	LDA	counter
	AND	#1
	TAX	
	LDA	JingJang_First_HMOVE,x
	STA	HMP0
	STA	HMP1
	STA	WSYNC
	STA	HMOVE

Bank2_DrawLogo_Loop_Text

	LDA	#0
	STA	PF2
	STA	GRP0
	STA	GRP1
*
*	temp01: Pointer to touhou text column 1
*	temp03: Pointer to touhou text column 2	
*	temp05: Pointer to touhou text column 3
*	temp07: Pointer to touhou text column 4
*	temp09: Pointer to touhou text column 5
*	temp11: Pointer to touhou text column 6
*
*	temp13: Adder to Col6
*	temp14: Adder to Col5
*	temp15: Adder to Col4
*	temp16: Adder to Col3
*	temp17: Adder to Col2
*	temp18: Adder to Col1
*
	LDX	#6
Bank2_Set_Adders
	TXA
	ASL
	ASL
	ASL
	ASL
	CLC
	ADC	counter
	BMI	Bank2_NotThatEasy

	sleep	9
	LDA	#8
	JMP	Bank2_NextAdder
Bank2_NotThatEasy
	AND	#%01111111
	LSR
	LSR
	LSR
	TAY
	LDA	Touhou_Letter_Adder,y	
Bank2_NextAdder
	STA	temp13,x
	DEX
	BPL	Bank2_Set_Adders
	

	LDA	#<Touhou_Title__E00
	CLC	
	ADC	temp18	
	STA	temp01

	LDA	#<Touhou_Title__E01
	CLC	
	ADC	temp17	
	STA	temp03

	LDA	#<Touhou_Title__E02
	CLC	
	ADC	temp16	
	STA	temp05

	LDA	#<Touhou_Title__E03
	CLC	
	ADC	temp15	
	STA	temp07

	LDA	#<Touhou_Title__E04
	CLC	
	ADC	temp14	
	STA	temp09

	LDA	#<Touhou_Title__E05
	CLC	
	ADC	temp13	
	STA	temp11

	LDA	#>Touhou_Title__E00
	STA	temp02
	STA	temp04
	STA	temp06
	STA	temp08
	STA	temp10
	STA	temp12

	LDY	#31

	LDA	counter
	AND	#1
	TAX
	CPX	#1
	BNE	Bank2_DrawLogo_Loop_Text_Odd_Start		
	JMP	Bank2_DrawLogo_Loop_Text_Even_Start

	_align	100
Bank2_DrawLogo_Loop_Text_Even_Start
	LDA	#$80			; 2 
	STA	HMP0			; 3 
	STA	HMP1			; 3 

Bank2_DrawLogo_Loop_Text_Even_Loop		
	STA	WSYNC			; 3
	STA	HMOVE			; 3 (6)

***	sleep 	64
	LDA	JinJang_Col_01R,y	; 4 
	STA	PF2			; 3 (13)

	LDA	JinJang_ColorR,y	; 4
	STA	COLUPF			; 3 (20)

	LDA	(temp03),y		
	STA	GRP0			; 8 (28)
	
	LDA	(temp07),y		
	STA	GRP1			; 8 (36)

	sleep	2
	LDA	JinJang_Col_02R,y	; 4 (42)

******	sleep	23
	sleep	3
	STA	PF2			; 3 (48)
	LDA	(temp11),y		; 5 (53)

	STA	GRP0			; 3 (56)

	sleep	10

	LDA	#$00			; 2 (68)
	STA	HMP0			; 3 
	STA	HMP1			; 3 (76)

Bank2_DrawLogo_Loop_Text_Even_SecondLine
	STA	HMOVE			; 3 (2)

	LDA	JinJang_Col_01R,y	; 4 
	STA	PF2			; 3 (9)

	LDA	(temp01),y		
	STA	GRP0			; 8 (15)

	LDA	(temp05),y		
	STA	GRP1			; 8 (23)

	LAX	JinJang_Col_02R,y	; 4 (27)

	sleep	13

	LDA	(temp09),y		; 5 (45)
	STX	PF2			; 3 (48)
	STA	GRP0			; 3 (51)

	LDA	#$80			; 2 (53)
	STA	HMP0			; 3 
	STA	HMP1			; 3 (59)
	
	DEY				; 2 (61)
	BPL	Bank2_DrawLogo_Loop_Text_Even_Loop	; 2
	JMP	Bank2_DrawLogo_Loop_Text_Ended

	_align	120
Bank2_DrawLogo_Loop_Text_Odd_Start
*
*	Currently at cycle 18
*	
	LDA	#$00
	STA	HMP0 
	STA	HMP1	; 7

	_sleep 	46
	sleep	2

Bank2_DrawLogo_Loop_Text_Odd_Loop
	STA	HMOVE			; 3 (2)

	LDA	JinJang_Col_01R,y	; 4 
	STA	PF2			; 3 (9)

	LDA	JinJang_ColorR,y	; 4
	STA	COLUPF			; 3 (16)

	LDA	(temp01),y		
	STA	GRP0			; 8 (24)

	LDA	(temp05),y		
	STA	GRP1			; 8 (32)

	sleep	6

	LAX	JinJang_Col_02R,y	; 4 (42)
	LDA	(temp09),y		; 4 (46)

	STX	PF2			; 3 (49)
	STA	GRP0			; 8 (55)


	LDA	#$80			; 2
	STA	HMP0			; 3
	STA	HMP1			; 3 (63)
Bank2_DrawLogo_Loop_Text_Odd_SecondLine
	STA	WSYNC			; 3 (76)
	STA	HMOVE			; 6 

	LDA	JinJang_Col_01R,y	; 4 
	STA	PF2			; 3 (13)

***	sleep	57

	LDA	(temp03),y		
	STA	GRP0			; 8 (21)
	
	LDA	(temp07),y		
	STA	GRP1			; 8 (29)

	LDA	JinJang_Col_02R,y	; 4 (33)
	sleep	12
	STA	PF2			; 3 (48)
	LDA	(temp11),y		; 5 (53)

	STA	GRP0			; 8 (61)

	sleep	2


	LDA	#$00			
	STA	HMP0			
	STA	HMP1			; 7 (70)

	DEY						; 2 (72)
	BPL	Bank2_DrawLogo_Loop_Text_Odd_Loop	; 2 (74)

Bank2_DrawLogo_Loop_Text_Ended

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	
	STA	HMCLR
	STA	PF2
	STA	GRP0
	STA	GRP1

	ldx	stack
	txs

	LDX	#4
Bank2_Blank_Lines2
	STA	WSYNC
	DEX
	BPL	Bank2_Blank_Lines2

	JSR	Bank2_Decrementing_RainbowLine

Bank2_Press_Start_Text
*
*	temp01: P0-1 pointer	
*	temp03: P1   pointer
*	temp05: P0-2 pointer
*	temp07: FG   pointer
*	temp09: BG   pointer
*
*




Bank2_Draw_ScrollingText
*
*	For testing, flat colors.
*

	LDX	#7
Bank2_Draw_ScrollingText_Loop2
	LDY	#1
Bank2_Draw_ScrollingText_Loop
	STA	WSYNC			; 76
	LDA	ScrollingColumn1,x	; 4
	STA	PF1			; 3 (7)
	LDA	ScrollingColumn2,x	; 4 (11)
	STA	PF2			; 3 (14)

	LDA	JingJang_Color_Adder,x  ; 4 (18)
	CLC				; 2 (20)
	ADC	counter			; 3 (23)
	STA	COLUPF			; 3 (26)

	sleep	15
	LDA	ScrollingColumn3,x	; 4 (46)
	STA	PF2			; 3 (49)
	LDA	ScrollingColumn4,x	; 4 (55)
	STA	PF1			; 3 (58)
	DEY
	BPL	Bank2_Draw_ScrollingText_Loop
	DEX
	BPL	Bank2_Draw_ScrollingText_Loop2

Bank2_Draw_ScrollingText_Ended
	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUPF	
	STA	PF1
	STA	PF2

	JSR	Bank2_Incrementing_RainbowLine

	JMP	OverScanBank2

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	_align 16
Touhou_Letter_Adder
	BYTE	#8
	BYTE	#7
	BYTE	#6
	BYTE	#5
	BYTE	#4
	BYTE	#5
	BYTE	#6
	BYTE	#7
	BYTE	#8
	BYTE	#9
	BYTE	#10
	BYTE	#11
	BYTE	#12
	BYTE	#11
	BYTE	#10
	BYTE	#9

	_align 8
JingJang_Color_Adder
	BYTE	#$00
	BYTE	#$02
	BYTE	#$04
	BYTE	#$06
	BYTE	#$06
	BYTE	#$04
	BYTE	#$02
	BYTE	#$00

	_align	2
JingJang_First_HMOVE
	BYTE	#$00
	BYTE	#$00

	_align	4
JingJang_00_LookUp
	BYTE #<JinJang_1_00
	BYTE #<JinJang_2_00
	BYTE #<JinJang_3_00
	BYTE #<JinJang_4_00

	_align	4
JingJang_01_LookUp
	BYTE #<JinJang_1_01
	BYTE #<JinJang_2_01
	BYTE #<JinJang_3_01
	BYTE #<JinJang_4_01

	_align	32

JinJang_Colors_32
	BYTE $02
	BYTE $04
	BYTE $06
	BYTE $06
	BYTE $04
	BYTE $02
	BYTE $02
	BYTE $04
	BYTE $06
	BYTE $06
	BYTE $04
	BYTE $04
	BYTE $02
	BYTE $02
	BYTE $04
	BYTE $06
	BYTE $06
	BYTE $04
	BYTE $02
	BYTE $02
	BYTE $04
	BYTE $06
	BYTE $06
	BYTE $04
	BYTE $04
	BYTE $02
	BYTE $02
	BYTE $04
	BYTE $06
	BYTE $06
	BYTE $04
	BYTE $02

	_align	64

JinJang_1_00
	BYTE %11100000
	BYTE %00011000
	BYTE %11110100
	BYTE %01111010
	BYTE %01111010
	BYTE %11111101
	BYTE %11111101
	BYTE %11111101
	BYTE %00111101
	BYTE %00011101
	BYTE %00001101
	BYTE %10001010
	BYTE %10001010
	BYTE %00000100
	BYTE %00011000
	BYTE %11100000
JinJang_2_00
	BYTE %11100000
	BYTE %00011000
	BYTE %11100100
	BYTE %11111010
	BYTE %11000010
	BYTE %10000001
	BYTE %00000001
	BYTE %00011001
	BYTE %00011001
	BYTE %00000001
	BYTE %00000001
	BYTE %00000010
	BYTE %00000010
	BYTE %00000100
	BYTE %00011000
	BYTE %11100000
JinJang_3_00
	BYTE %11100000
	BYTE %00011000
	BYTE %00000100
	BYTE %10000010
	BYTE %10000010
	BYTE %00000001
	BYTE %00000001
	BYTE %00000001
	BYTE %11000001
	BYTE %11100001
	BYTE %11110001
	BYTE %01110010
	BYTE %01110010
	BYTE %11100100
	BYTE %00011000
	BYTE %11100000
JinJang_4_00
	BYTE %11100000
	BYTE %00011000
	BYTE %00000100
	BYTE %00000010
	BYTE %00111010
	BYTE %01111101
	BYTE %11111101
	BYTE %11100101
	BYTE %11100101
	BYTE %11111101
	BYTE %11111101
	BYTE %11111110
	BYTE %11111010
	BYTE %11100100
	BYTE %00011000
	BYTE %11100000

	_align	64

JinJang_1_01
	BYTE %11100000
	BYTE %00011000
	BYTE %11100100
	BYTE %01110010
	BYTE %01110010
	BYTE %11110001
	BYTE %11100001
	BYTE %11000001
	BYTE %00000001
	BYTE %00000001
	BYTE %00000001
	BYTE %10000010
	BYTE %10000010
	BYTE %00000100
	BYTE %00011000
	BYTE %11100000
JinJang_2_01
	BYTE %11100000
	BYTE %00011000
	BYTE %11100100
	BYTE %11111010
	BYTE %11111110
	BYTE %11111101
	BYTE %11111101
	BYTE %11100101
	BYTE %11100101
	BYTE %11111101
	BYTE %01111101
	BYTE %00111010
	BYTE %00000010
	BYTE %00000100
	BYTE %00011000
	BYTE %11100000
JinJang_3_01
	BYTE %11100000
	BYTE %00011000
	BYTE %00000100
	BYTE %10001010
	BYTE %10001010
	BYTE %00001101
	BYTE %00011101
	BYTE %00111101
	BYTE %11111101
	BYTE %11111101
	BYTE %11111101
	BYTE %01111010
	BYTE %01111010
	BYTE %11110100
	BYTE %00011000
	BYTE %11100000
JinJang_4_01
	BYTE %11100000
	BYTE %00011000
	BYTE %00000100
	BYTE %00000010
	BYTE %00000010
	BYTE %00000001
	BYTE %00000001
	BYTE %00011001
	BYTE %00011001
	BYTE %00000001
	BYTE %10000001
	BYTE %11000010
	BYTE %11111010
	BYTE %11100100
	BYTE %00011000
	BYTE %11100000

*
*	Extra blanks added so the title can move up and down by 16.
*

	_align 16
Touhou_Title_Color
	BYTE	#$12
	BYTE	#$14
	BYTE	#$16
	BYTE	#$18
	BYTE	#$1A
	BYTE	#$1C
	BYTE	#$1E
	BYTE	#$0E
	BYTE	#$1E
	BYTE	#$1C
	BYTE	#$1A
	BYTE	#$18
	BYTE	#$16
	BYTE	#$14
	BYTE	#$12

	_align	208

Touhou_Title__E00
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__00
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00111000
	BYTE %00010000
	BYTE %00111000
	BYTE %00010000
	BYTE %00010000
	BYTE %10010010
	BYTE %11111110

Touhou_Title__E01
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__01
	BYTE %11111110
	BYTE %01000010
	BYTE %00110000
	BYTE %00011000
	BYTE %00000100
	BYTE %10000010
	BYTE %01000100
	BYTE %00111000
	BYTE %00000000
	BYTE %00111000
	BYTE %01000100
	BYTE %10000110
	BYTE %10111010
	BYTE %11000010
	BYTE %01000100
	BYTE %00111000

Touhou_Title__E02
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__02
	BYTE %00111000
	BYTE %01000100
	BYTE %11000010
	BYTE %11100010
	BYTE %10111100
	BYTE %10000000
	BYTE %01000010
	BYTE %00111100
	BYTE %00000000
	BYTE %01111100
	BYTE %11000110
	BYTE %10000010
	BYTE %11000010
	BYTE %10000010
	BYTE %10000110
	BYTE %10000010

Touhou_Title__E03
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__03
	BYTE %00111100
	BYTE %11000110
	BYTE %10000010
	BYTE %10000010
	BYTE %10000010
	BYTE %10000010
	BYTE %11000110
	BYTE %01111000
	BYTE %00000000
	BYTE %11000110
	BYTE %10000010
	BYTE %10000010
	BYTE %11111110
	BYTE %10000010
	BYTE %10000010
	BYTE %11000110

Touhou_Title__E04
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__04
	BYTE %00111100
	BYTE %11000110
	BYTE %10000010
	BYTE %10000010
	BYTE %10000010
	BYTE %10000010
	BYTE %11000110
	BYTE %01111000
	BYTE %00000000
	BYTE %00111000
	BYTE %01000100
	BYTE %10000110
	BYTE %10111010
	BYTE %11000010
	BYTE %01000100
	BYTE %00111000

Touhou_Title__E05
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

Touhou_Title__05
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %01111100
	BYTE %11000110
	BYTE %10000010
	BYTE %11000010
	BYTE %10000010
	BYTE %10000110
	BYTE %10000010

Touhou_Title__E06
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000

	_align	150
Impure_Soul_Eclipse
	BYTE %10000001
	BYTE %10100001
	BYTE %11111111
	BYTE %10010001
	BYTE %10000001
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %00100001	
	BYTE %00000010	; 10
	BYTE %00001100
	BYTE %00000010
	BYTE %00010001
	BYTE %11111111
	BYTE %00000000
	BYTE %11111111
	BYTE %00010001
	BYTE %00011001
	BYTE %00010011
	BYTE %00010001	; 20
	BYTE %00001010
	BYTE %00000100
	BYTE %00000000
	BYTE %01111111
	BYTE %10100000
	BYTE %10100000
	BYTE %10000000
	BYTE %10001000
	BYTE %10001000
	BYTE %01111111	; 30
	BYTE %00000000
	BYTE %11111111
	BYTE %00010001
	BYTE %00011001
	BYTE %01110011
	BYTE %11010001
	BYTE %10001010
	BYTE %00000100
	BYTE %00000000
	BYTE %11111111	; 40
	BYTE %10001001
	BYTE %10011001
	BYTE %10001101
	BYTE %10000001
	BYTE %11000011
	BYTE %10000001
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000	; 50
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %01100110
	BYTE %10001001
	BYTE %10001001
	BYTE %10011101
	BYTE %10110001	; 60
	BYTE %10010001
	BYTE %01100110
	BYTE %00000000
	BYTE %00111100
	BYTE %01010010
	BYTE %10010001
	BYTE %10011001
	BYTE %10001001
	BYTE %01001010
	BYTE %00111100	; 70
	BYTE %00000000
	BYTE %01111111
	BYTE %10100000
	BYTE %10100000
	BYTE %10000000
	BYTE %10001000
	BYTE %10001000
	BYTE %01111111
	BYTE %00000000
	BYTE %11111111	; 80
	BYTE %10000100
	BYTE %10000000
	BYTE %10000000
	BYTE %11000000
	BYTE %10000000
	BYTE %10000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000	; 90
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %10001001
	BYTE %10011001
	BYTE %10001101
	BYTE %10000001	; 100
	BYTE %11000011
	BYTE %10000001
	BYTE %00000000
	BYTE %00111100
	BYTE %01010010
	BYTE %10010001
	BYTE %10000001
	BYTE %10000001
	BYTE %10000001
	BYTE %01000010	; 110
	BYTE %00000000
	BYTE %11111111
	BYTE %10000100
	BYTE %10000000
	BYTE %10000000
	BYTE %11000000
	BYTE %10000000
	BYTE %10000000
	BYTE %00000000
	BYTE %00000000	; 120
	BYTE %10000001
	BYTE %10100001
	BYTE %11111111
	BYTE %10010001
	BYTE %10000001
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %00010001
	BYTE %00011001	; 130
	BYTE %00010011
	BYTE %00010001
	BYTE %00001010
	BYTE %00000100
	BYTE %00000000
	BYTE %01100110
	BYTE %10001001
	BYTE %10001001
	BYTE %10011101
	BYTE %10110001	; 140
	BYTE %10010001
	BYTE %01100110
	BYTE %00000000
	BYTE %11111111
	BYTE %10001001
	BYTE %10011001
	BYTE %10001101
	BYTE %10000001
	BYTE %11000011
	BYTE %10000001	; 150

	_align 5

Bank2_Press_Fire_01
	BYTE	%10101000
	BYTE	%00001000
	BYTE	%10101100
	BYTE	%10101010
	BYTE	%10101100

	_align 5

Bank2_Press_Fire_02
	BYTE	%10101110
	BYTE	%10101000
	BYTE	%11001100
	BYTE	%10101000
	BYTE	%11001110

	_align 5

Bank2_Press_Fire_03
	BYTE	%11001100
	BYTE	%00100010
	BYTE	%01000100
	BYTE	%10001000
	BYTE	%01100110

	_align 5

Bank2_Press_Fire_04
	BYTE	%00000100
	BYTE	%00000100
	BYTE	%11110110
	BYTE	%00000100
	BYTE	%00000111

	_align 5

Bank2_Press_Fire_04
	BYTE	%01110101
	BYTE	%00100101
	BYTE	%00100110
	BYTE	%00100101
	BYTE	%01110110

	_align 5

Bank2_Press_Fire_05
	BYTE	%01110101
	BYTE	%01000000
	BYTE	%01100101
	BYTE	%01000101
	BYTE	%01110101

	_align 5

Bank2_Press_Fire_Colors_BG_Normal
	BYTE	$00
	BYTE	$00
	BYTE	$00
	BYTE	$00
	BYTE	$00

	_align 5

Bank2_Press_Fire_Colors_BG_Selected
	BYTE	$44
	BYTE	$48
	BYTE	$4C
	BYTE	$48
	BYTE	$44

	_align 5

Bank2_Press_Fire_Colors_FG_Normal
	BYTE	$0A
	BYTE	$0C
	BYTE	$0E
	BYTE	$0C
	BYTE	$0A

	_align 5

Bank2_Press_Fire_Colors_FG_Selected
	BYTE	$1A
	BYTE	$1C
	BYTE	$1E
	BYTE	$1C
	BYTE	$1A

*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

Bank2_Decrementing_RainbowLine
	LDX	#1
Bank2_Decrementing_RainbowLine_Loop
	LDY	counter
	STA	WSYNC
	STY	COLUBK
	LDA	#255
	STA	PF0	

	sleep	6

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	DEY
	DEY 	
	STY	COLUBK

	LDA	#0
	sleep	3
	STA	COLUBK
	DEX
	BPL 	Bank2_Decrementing_RainbowLine_Loop
	STA	PF0
	

	RTS

Bank2_Incrementing_RainbowLine
	LDX	#1
Bank2_Incrementing_RainbowLine_Loop
	LDY	counter
	STA	WSYNC
	STY	COLUBK
	LDA	#255
	STA	PF0	

	sleep	6

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	INY
	INY 	
	STY	COLUBK

	LDA	#0
	sleep	3
	STA	COLUBK
	DEX
	BPL 	Bank2_Incrementing_RainbowLine_Loop
	STA	PF0
	

	RTS

###End-Bank2
	saveFreeBytes
	rewind 	2fd4
	
start_bank2
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address  
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 2ffc
   	.byte 	#<start_bank2
   	.byte 	#>start_bank2
   	.byte 	#<start_bank2
   	.byte 	#>start_bank2

***************************
********* Start of 3rd bank
***************************
	Bank 3
	fill	256
###Start-Bank3
	


###End-Bank3

	saveFreeBytes
	rewind 	3fd4

start_bank3
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address 
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 3ffc
   	.byte 	#<start_bank3
   	.byte 	#>start_bank3
   	.byte 	#<start_bank3
   	.byte 	#>start_bank3

***************************
********* Start of 4th bank
***************************
	Bank 4
	fill	256
###Start-Bank4

###End-Bank4

	saveFreeBytes
	rewind 	4fd4
	
start_bank4
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address  
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 4ffc
   	.byte 	#<start_bank4
   	.byte 	#>start_bank4
   	.byte 	#<start_bank4
   	.byte 	#>start_bank4


***************************
********* Start of 5th bank
***************************
	Bank 5
	fill	256
###Start-Bank5
	

###End-Bank5

	saveFreeBytes
	rewind 	5fd4
	
start_bank5
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address   
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 5ffc
   	.byte 	#<start_bank5
   	.byte 	#>start_bank5
   	.byte 	#<start_bank5
   	.byte 	#>start_bank5

***************************
********* Start of 6th bank
***************************
	Bank 6
	fill	256
###Start-Bank6
	

###End-Bank6


	saveFreeBytes
	rewind 	6fd4
	
start_bank6
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address   	
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 6ffc
   	.byte 	#<start_bank6
   	.byte 	#>start_bank6
   	.byte 	#<start_bank6
   	.byte 	#>start_bank6

***************************
********* Start of 7th bank
***************************
	Bank 7
	fill	256
###Start-Bank7
	

###End-Bank7
*Routine Section
	

	saveFreeBytes
	rewind 	7fd4
	
start_bank7
	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
   	pha
   	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address   	
   	rol
   	rol
   	rol
	rol
   	and	#7	 
	tax
   	inx
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 7ffc
   	.byte 	#<start_bank7
   	.byte 	#>start_bank7
   	.byte 	#<start_bank7
   	.byte 	#>start_bank7

***************************
********* Start of 8th bank
***************************
	Bank 8
	fill	256
###Start-Bank8
	

###End-Bank8

*****	align 256
	
bank8_Start
   	sei
   	cld
   	ldy	#0
   	lda	$D0
   	cmp	#$2C		;check RAM location #1   	
	bne	bank8_MachineIs2600
   	lda	$D1
   	cmp	#$A9		;check RAM location #2   	
	bne	bank8_MachineIs2600
   	dey
bank8_MachineIs2600
	ldx	#0
  	txa
bank8_clearmem
   	inx
   	txs
   	pha
	cpx	#$00
   	bne	bank8_clearmem	; Clear the RAM.

	LDA	$F080		; Sets two values of the SC RAM 
	STA	$80		; to Random and Counter variables
	LDA	$F081
	STA	$81

	LDY	#0		
	TYA
****	STA	$F029
bank8_ClearSCRAM
	STA 	$F000,Y
	INY
	BPL 	bank8_ClearSCRAM

	lda	#>(EnterScreenBank2-1)
   	pha
   	lda	#<(EnterScreenBank2-1)
   	pha
   	pha
   	pha
   	ldx	#2
   	jmp	bankSwitchJump

	saveFreeBytes
	rewind 	8fd4

bankSwitchCode
 	ldx	#$ff
   	txs
   	lda	#>(bank8_Start-1)
   	pha
   	lda	#<(bank8_Start-1)
   	pha
bankSwitchReturn
	pha
	txa
   	pha
   	tsx
   	lda	4,x	; get high byte of return address	
	rol
   	rol
   	rol
   	rol
   	and	#7	
	tax
   	inx
bankSwitchJump
   	lda	$1FF4-1,x
   	pla
   	tax
   	pla
   	rts
	rewind 8ffc	   
   	.byte 	#<bank8_Start
  	.byte 	#>bank8_Start
   	.byte 	#<bank8_Start
  	.byte 	#>bank8_Start