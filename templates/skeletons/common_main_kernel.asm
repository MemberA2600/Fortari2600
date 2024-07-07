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
temp01 = $82
temp02 = $83
temp03 = $84
temp04 = $85
temp05 = $86
temp06 = $87
temp07 = $88
temp08 = $89
temp09 = $8a
temp10 = $8b
temp11 = $8c
temp12 = $8d
temp13 = $8e
temp14 = $8f
temp15 = $90
temp16 = $91
temp17 = $92
temp18 = $93
temp19 = $94
item = $95

!!!MAINVARS!!!
!!!MUSICVARS!!!
!!!COLLISIONVARS!!!

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

*
* User defined variables
*------------------------

*Global
*---------
!!!GLOBAL_VARIABLES!!!

*Bank2
*---------
!!!BANK2_VARIABLES!!!

*Bank3
*---------
!!!BANK3_VARIABLES!!!

*Bank4
*---------
!!!BANK4_VARIABLES!!!

*Bank5
*---------
!!!BANK5_VARIABLES!!!

*Bank6
*---------
!!!BANK6_VARIABLES!!!

*Bank7
*---------
!!!BANK7_VARIABLES!!!

*Bank8
*---------
!!!BANK8_VARIABLES!!!

***************************
********* Start of 1st bank
***************************

*Enter Bank
*--------------------------
* Bank1 contains the main
* kernel and most game
* data
*

	fill 256	; We have to prevent writing on addresses taken by the SuperChip RAM.

bank1_EnterKernel
	LDA	#0		
	STA	PF0		 
	STA	PF1		
	STA	PF2		 
	STA	GRP0		 
	STA	GRP1		  
	STA	VDELP0		 
	STA	VDELP1		
	STA	ENAM0		
	STA	ENAM1		 
	STA	ENABL
	STA	CXCLR
	
	TSX
	STX	item
###Start-Main-Kernel
	BIT	SubMenu
	BVC	bank1_StayHere	; Go to the SubMenu Kernel
	JMP 	bank1_DoSubMenuKernel	; instead.

bank1_StayHere

	LDA	frameColor	
	sta	WSYNC
	STA	COLUBK
  	ldx	#4 		; From bl -> p0

bank1_HorPosLoop		
   	lda	P0X,X	
bank1_DivideLoop
	sbc	#15
   	bcs	bank1_DivideLoop
   	sta	temp01,X
   	sta	RESP0,X	
   	sta	WSYNC
   	dex
   	bpl	bank1_HorPosLoop	

	ldx	#4		; bl
   	ldy	temp05
   	lda	bank1_FineAdjustTable256,Y
   	sta	HMP0,X		

	dex			; m1
   	ldy	temp04
   	lda	bank1_FineAdjustTable256,Y
   	sta	HMP0,X	
   
	dex			; m0
   	ldy	temp03
   	lda	bank1_FineAdjustTable256,Y
   	sta	HMP0,X	
   
	dex			; p1
   	ldy	temp02
   	lda	bank1_FineAdjustTable256,Y
   	sta	HMP0,X	

	dex			; p0
   	ldy	temp01
   	lda	bank1_FineAdjustTable256,Y
   	sta	HMP0,X	

   	sta	WSYNC
   	sta	HMOVE		; 3

	LDA	frameColor	; 3 (6)
	STA 	COLUPF		; 3 (9)

	LDA	#0	;2 (11)
	STA	temp03 	;3 (46) Erase P1 sprite data
	STA	temp14	;3

	LDA	pfSettings	; 3 (49)
	ORA	#%00000001	; 2 (51) Reflected playfield
	AND	#%11111101	; 2 (53) Always get the original colors.
	STA	CTRLPF		; 3 (56)

bank1_SettingUpP0SpriteAndMissile0

	LDA	P0Settings	;3 (59)
	STA	REFP0		;3 (62)
	AND	#%00110111	;2 (64)
	STA	NUSIZ0	; Sets P0 and M0 registers 3 (67)

	LDA	P0SpritePointer+1	; temp08 will store the sprite pointers high byte ; 3 (70)
	STA	temp07+1		; 2 (72)

	LDA	P0Y ; 3 (75)
	STA	temp09 	; temp09 stores P0 Y position. 3 (2) One line wasted.
	
bank1_SettingUpP1SpriteAndMissile1

	LDA	P1Settings 	; 3 (5)
	STA	REFP1		; 3 (8)
	AND	#%00110111	; 2 (10)
	STA	NUSIZ1		; 3 (13) Sets P1 and M1 registers

	LDA	P1SpritePointer+1	; 3 (16) temp11 will store the sprite pointers high byte
	STA	temp10+1		; 3 (19)

	LDA	P1Y	; 3 (22)
	SEC		; 2 (24) Substract 1 because of the latency
	SBC	#1      ; 2 (26)
	STA	temp12 	; 3 (29) temp12 stores P1 Y position.


bank1_FinishPreparation
**	TSX			; 2 (31)
**	STX	item		; Save the stack pointer 3 (34)

	LDX	#42
	LDA	#15		; 2 (36)
	CLC			; 2 (38)
	ADC	pfIndex		; 3 (41)
	STA	temp01		; Save pfIndex 3 (44)	
	TAY			; 2 (46)

	LDA	(pfColorPointer),y	; 5 (51)
	CLC				; 2 (53)
	ADC	pfBaseColor 		; 3 (56)
	STA	temp02		; savePFColor 3 (59)

	LDA	(bkColorPointer),y 	; 5 (64)
	CLC				; 2 (66)
	ADC	bkBaseColor 		; 3 (69)
	STA	temp04		; saveBKColor 3 (72)

	LDY 	P1Height		; 3 (75) - Wow, another line done!  		
	LDA	(P1ColorPointer),y	; 5 (4)
	STA	COLUP1		; Load first color 3 (7)

	LDY	#225		; 2 (9)
	LDA	P0TurnOff	; 3 (12)
	BVC	bank1_NoP0TurnOff	; 2 (14)

	LDA	#<bank1_Zero	  ; 2
	STA	P0SpritePointer   ; 3
	LDA	#>bank1_Zero	  ; 2
	STA	P0SpritePointer+1 ; 3
	LDA	#1		; 2
	STA	P0Height	; 3

	STY	P0Y		; 3 (17)
bank1_NoP0TurnOff
	BPL	bank1_NoM0TurnOff ; 2 (19)
	STY	M0Y		; 3 (22)
bank1_NoM0TurnOff
	
	LDA	P1TurnOff	; 3 (25)
	BVC	bank1_NoP1TurnOff ; 2 (27)

	LDA	#<bank1_Zero	  ; 2
	STA	P1SpritePointer   ; 3
	LDA	#>bank1_Zero	  ; 2
	STA	P1SpritePointer+1 ; 3
	LDA	#1		; 2
	STA	P1Height	; 3	

	STY	P1Y		; 3 (30)
bank1_NoP1TurnOff
	BPL	bank1_NoM1TurnOff ; 2 (32)
	STY	M1Y		; 3 (35)
bank1_NoM1TurnOff

	LDA	BallTurnOff	; 3 (38)
	AND	#%00001000	; 2 (40)
	CMP	#%00001000	; 2 (42)
	BNE	bank1_NoBallTurnOff ; 2 (44)
	STY	BLY		; 3 (47)

bank1_NoBallTurnOff
* _sleep numbers:	14, 18, 22, 26,
*  		 	30, 34, 38, 42, etc. 
*			(n-2) % 4 = 0

	STA	WSYNC
	
	LDA	temp01		; pfIndex 3 (12)	
	TAY			; 2(14)

	LDA	(pf0Pointer),y	; 5(19)
	STA	PF0		; 3(22)	
	STA	temp05		; 3(25)
	asl			; 2(27)
	asl			; 2(29)
	asl			; 2(31)
	asl			; 2(33)
	STA	temp06		; 3(36)


	LDA	(pf2Pointer),y	; 5(45)
	STA	PF2		; 3(50)

	LDA	(pf1Pointer),y	; 5(55)
	STA	PF1		; 3(58)
	
	LDA	temp02			; 3(73)	
	LDY	#0
	JMP	bank1_FirstLine	; 3(76)

bank1_NoP0DrawNow
	CPX	M0Y		; 3
	BNE	bank1_NoColorOverWriteM0 ; 2

	LDA	M0Color		; 3
	STA	COLUP0		; 3
	LDA	#0	  	; 2

	JMP	bank1_saveP0Sprite ; 3 

bank1_NoColorOverWriteM0
	sleep 	5
	LDA	#0
	JMP	bank1_saveP0Sprite ; 3 

bank1_NoP1DrawNow
	CPX	M1Y		; 3
	BNE	bank1_NoColorOverWriteM1

	LDA	M1Color		; 3
	STA	COLUP1		; 3
	LDA	#0	  	; 2

	JMP	bank1_saveP1Sprite	; 3 

bank1_NoColorOverWriteM1
	sleep 	5
	LDA	#0
	JMP	bank1_saveP1Sprite	; 3 

DrawingTheScreen
	; temp01 = pfIndex
	; temp02 = pfColor
	; temp03 = P1 Sprite data
	; temp04 = bkColor
	; temp05 = P0 / 1
	; temp06 = P0 / 2
	; temp07, temp08 = P0 sprite pointers
	; temp09 = p0 Y
	; temp10, temp11 = P1 sprite pointers
	; temp12 = p1height
	; temp13 = lineNum
	; temp14 = P0 Sprite Data

bank1_FirstLine
	STA	WSYNC		; 3 (76)
bank1_StartWithoutWSYNC
	STA	COLUPF		; 3 (3)
	LDA	temp04		; 3 (6)
	STA	COLUBK		; 3 (9)

	LDA	temp05		; 3 (12)
	STA	PF0		; 3 (15)

	LDA	temp03		; 3 (18)
	STY	GRP0		; 3 (21)
	STA	GRP1		; 3 (24)


	STX	temp13		; 3 (27) Saves the lineNum
	ldx 	#$1f		; Address of ENABL 2 (29) 
	txs			; 2 (31) 
	LDX	temp13		; 3 (34) Retrive the lineNum

	LDA	temp06		; 3 (36)	
	STA	PF0		; 3 (39)

	LDY	temp01		; 3 (42)

	LDA	(pfColorPointer),y	; 5 (47)
	ADC	pfBaseColor		; 3 (50)
	STA	temp02		; 3 (53)

	LDA	(bkColorPointer),y ;5 (58)
	ADC	bkBaseColor	; 3 (61)	
	STA	temp04		; 3 (64)

	cpx	BLY		; 3
	php			; 3
	cpx	M1Y		; 3
	php			; 3
	cpx	M0Y		; 3
	php			; 18 (6)

bank1_MiddleLine

	LDA	(pf0Pointer),y	; 5 (11)
	STA	PF0		; 3 (14)
	STA	temp05		; 3 (17)

	LDA	(pf1Pointer),y	; 5 (22)
	STA 	PF1		; 3 (25)

	LDA	(pf2Pointer),y	; 5 (30)
	STA 	PF2		; 3 (33)
	LDA	temp05		; 3 (36)
	asl			; 2 
	asl			; 2 
	asl			; 2 
	asl			; 8 (44)
	STA	PF0		; 3 (47)
	STA	temp06		; 3 (50)


	LDA 	P0Height 	; 3 
	DCP	temp09 		;  temp09 contains P0Y!  ; 5 
	BCC	bank1_NoP0DrawNow	; 2 
	LDY	temp09		; 3 
	LDA	(P0ColorPointer),y 	; 5 
	STA	COLUP0		; 3 
	LDA	(temp07),y 	; 5 
bank1_saveP0Sprite
	STA	temp14		; 3 
	; 29 (3)

bank1_LastLine
	LDA	temp05		; 3 (9)
	STA	PF0		; 3 (12)

	LDA 	P1Height 	; 3 
	DCP	temp12 		;  temp12 contains P0Y!  ; 5 
	BCC	bank1_NoP1DrawNow	; 2 
	LDY	temp12		; 3 
	LDA	(P1ColorPointer),y 	; 5
	STA	COLUP1	; 3 
	LDA	(temp10),y 	; 5
bank1_saveP1Sprite
	STA	temp03		; 3 
	; 29 (41)

	LDA	temp06		; 3 (44)
	STA	PF0		; 3 (47)

	LDY	temp14		; 3 (50)

	CPX	#1		; 2 (58)
	BEQ	bank1_ResetAll 	; 2 (60)

	DEX			; 2 (62)
	LDA	temp02		; 3 (65)

	DEC	temp01		; 5 (70)
	JMP	bank1_FirstLine	; 3 (73)

###End-Main-Kernel

bank1_ResetAll
	LDX	#0		; 2 (62)
	STX	HMCLR		; 3 (65)
	LDA	frameColor	; 3 (68)
	STX	PF2		; 3 (71)

	STX	WSYNC		

	STA 	COLUBK		 
	STA 	COLUPF		

	STX	PF0
	STX	PF1

	STX	ENAM0
	STX	ENAM1
	STX	ENABL
	STX	GRP0
	STX	GRP1

	STX	VDELP0
	STX	VDELP1
	STX	VDELBL
	STX	REFP0
	STX	REFP1

	LDX	item		; Retrieve the stack pointer
	TXS

!!!COLLISIONS_CODE!!!

bank1_JumpBackToBankScreenBottom

	lda	bankToJump
	lsr
	lsr
	AND	#%00000111	; Get the bank number to return
	tax
	
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table
		
		
	lda	bank1_ScreenJumpTable,y
   	pha
   	lda	bank1_ScreenJumpTable+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

###Start-Main-Kernel-Sub

bank1_LoadNextData
	LDA	Tile1_1,x	; 4	
	AND	#%00001111	; 2 Get low nibble
	ASL			; 2 and multiply
	ASL			; 2 by 8
	ASL			; 2
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp03		; 3


	LDA	Tile1_1,x	; 4 Get high nibble
	AND	#%11110000	; 2 and divide by 2
	LSR			; 2 
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp05		; 3

	INX			; 2

	LDA	Tile1_1,x	; 4	
	AND	#%00001111	; 2 Get low nibble
	ASL			; 2 and multiply
	ASL			; 2 by 8
	ASL			; 2 
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp07		; 3


	LDA	Tile1_1,x	; 4 Get high nibble
	AND	#%11110000	; 2 and divide by 2
	LSR			; 2 
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp09		; 3

	INX			; 2

	LDA	Tile1_1,x	; 4	
	AND	#%00001111	; 2 Get low nibble
	ASL			; 2 and multiply
	ASL			; 2 by 8
	ASL			; 2 
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp11		; 3


	LDA	Tile1_1,x	; 4 Get high nibble
	AND	#%11110000	; 2 and divide by 2
	LSR			; 2 
	CLC			; 2
	ADC	TileSetPointer	; 3
	STA	temp13		; 3

	INX			; 2

	STX	temp02		; 3
	JMP	bank1_LoadedShit	; 3

bank1_DoSubMenuKernel
**	TSX			; 2 
**	STX	item		; 3

	LDA	frameColor
	STA	WSYNC
	STA	COLUBK	
	STA	COLUPF

	LDA	pfSettings	; 
	ORA	#%00000101	; Reflected playfield and
				; players go behind.
	AND	#%11111101	; Always get the original colors.
	STA	CTRLPF		; 

	LDA	#$03		;
	STA	NUSIZ1		; Fixed 3 with large gaps.	 

	LDA	OverLapIndicator
	AND	#%01111111
	STA	OverLapIndicator

	LDA	OverlapScreen
	AND	#%00100000
	CMP	#%00100000
	BEQ	bank1_DoThisCrap
	JMP	bank1_NoOverLap

bank1_DoThisCrap
	LDX	#3
bank1_AddLines
	STA	WSYNC
	DEX	
	CPX	#255
	BNE	bank1_AddLines
	
bank1_DoItAgainPlease
	STA	WSYNC
	LDA	SubMenuLines
	AND	#%00000011
	TAX

	LDA	OverLapIndicator
	BMI	bank1_ItsTheBottom
	LDA	bank1_ScreenOverlapTop,x
	JMP	bank1_SaveToppp
bank1_ItsTheBottom
	LDA	bank1_ScreenOverlapBottom,x
bank1_SaveToppp
	STA	temp11
	
	LDA	#15		
	CLC			
	ADC	pfIndex		 
	STA	temp01		; Save pfIndex 
	STA	WSYNC
	LDA	OverLapIndicator
	BPL	bank1_NoTemp01Dec
	LDA	SubMenuLines
	AND	#%00000011
	TAX

	LDA	temp01
	SEC
	SBC	bank1_DecrementTemp1,x
	STA	temp01
bank1_NoTemp01Dec
	LDX	temp11

	LDY	temp01			

	STA	WSYNC
	
	LDA	(pfColorPointer),y	
	CLC				
	ADC	pfBaseColor 	
	STA	temp02		; savePFColor 

	LDA	(bkColorPointer),y 	
	CLC				
	ADC	bkBaseColor 	
	STA	temp04		; saveBKColor 	

	STA	WSYNC
	LDA	GrayScale
	AND	#%01000000
	CMP	#%01000000
	BNE	bank1_NotGray
	LDA	temp02
	AND	#%00001111
	STA	temp02
	LDA	temp04
	AND	#%00001111
	STA	temp04
bank1_NotGray
	STA	WSYNC

	LDA	OverLapIndicator
	BPL	bank1_NoINY
	INY
bank1_NoINY
	LDA	(pf2Pointer),y		
	STA	PF2	
	
	LDA	(pf1Pointer),y	
	STA	PF1

	LDA	(pf0Pointer),y		
	STA	PF0	
	STA	temp03
	LDA	OverLapIndicator
	BPL	bank1_NoDEY
	DEY
bank1_NoDEY

bank1_NewLineWithTemp04
	LDA	temp04
bank1_NewLine
	STA	WSYNC
	STA	COLUBK		; 3
	LDA	temp02		; 3 (6)
	STA	COLUPF		; 3 (9)

	LDA	temp03		
	STA	PF0

	
	LDA	(bkColorPointer),y ; 3	
	CLC			; 2 	
	ADC	bkBaseColor 	; 3 
	STA	temp04		; 3 
	
	sleep	8

	LDA	temp03
	ASL			; 2 (34)
	ASL			; 2 (36)
	ASL			; 2 (38)
	ASL			; 2 (40)
	STA	PF0		; 3 (43)

	STA	WSYNC	
	LDA	(pf0Pointer),y	; 5
	STA	PF0		; 3 (8)	
	STA	temp03		; 3 (12)
	LDA	(pf1Pointer),y	; 5 (15)	
	STA	PF1		; 3 (18)
	LDA	(pf2Pointer),y	; 5 (23)	
	STA	PF2		; 3 (28)
	
	JSR	bank1_GetSecondPF0	

	LDA	(pfColorPointer),y	; 5 (55)
	CLC			; 2 (57)	
	ADC	pfBaseColor 	; 3 (60)
	STA	temp02		; 3 (63)
	DEY			
	STA	WSYNC	
	LDA	temp03		; 3
	STA	PF0		; 3 (6)
	sleep	2
	JSR	bank1_GetSecondPF0 ; 6 (12) + 20

	LDA	GrayScale	; 3 
	AND	#%01000000	; 2 
	CMP	#%01000000	; 2 
	BNE	bank1_NotGray2	; 2 
	LDA	temp02		; 3 
	AND	#%00001111	; 2 
	STA	temp02		; 3 
	LDA	temp04		; 3 
	AND	#%00001111	; 2 
	STA	temp04		; 3 
bank1_NotGray2

	DEX
	CPX	#1	
	BEQ	bank1_ResetToOther


	LDA	temp04
	JMP	bank1_NewLine
bank1_ResetToOther
	
bank1_NoOverLap
*	temp01: Rows left
*	temp02: LineNum
*	temp03 - temp14: GRP0 pointers
*	temp15 - temp16: Selector Sprite Pointer
*	temp17: ColorData
*	temp18: TileY

bank1_NoResetNow
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK		; 3
	LDA	#0		
	STA	PF0		
	STA	PF1	
	STA	PF2


	LDA	OverLapIndicator
	BPL	bank1_FFFF	

	JMP	bank1_ResetAll
bank1_FFFF


	LDA	#%11111110	; 2 (15)			
	STA	PF2		; 3 (18)	

	LDY	#7
	LDA	(TileColorPointer),y	; 5 (57)
	CLC			; 3 (60)
	ADC	TileScreenMainColor	; 3 (63)
	STA	COLUPF		; 3 (66)
	STA	COLUP1		; 3 (69)

	LDA	SubMenuLines	; 3 (72)
	AND	#%00000011	; 2 (74)
	CLC			; 2 (76)
	ADC	#1		; 2 
	STA	temp01		; 3 (5) Saving the lineNum	

	LDA	counter		; 3 (8)
	STA	COLUP0		; 3 (11)
	AND	#%00001100	; 2 (13) 
	ASL

	CLC			; 2 
	ADC	#<bank1_Selector ; 3 
	STA	temp15		; 3 
	LDA	#>bank1_Selector ; 3 
	STA	temp16		; 3 

	LDY	#0
	STY	NUSIZ0
	LDA	TileSelected
	AND	#%00011111

bank1_SmallerThan6
	CMP	#6
	BCC	bank1_GetP0Poz
	SEC
	SBC	#6
	INY
	JMP	bank1_SmallerThan6
bank1_GetP0Poz
	STY	temp18	; Get the Tile row number reversed
	LDY	#0
	STY	temp03

	STA	WSYNC
	TAX
	LDA	bank1_CursorXPosition,x
	LDX	temp03
bank1_CursorPozLoop
	sbc	#15
   	bcs	bank1_CursorPozLoop
   	sleep	2
	tay
   	sta	RESP0	
   	LDA	bank1_FineAdjustTable256,Y
	STA	HMP0
	INC	temp18

bank1_SetP0TilePositions
	STA	WSYNC
	STA	HMOVE
	LDA	TileSetPointer+1  ; 5
	STA	temp04		; 3	High nibble of pointer
	STA	temp06		; 3	High nibble of pointer
	STA	temp08		; 3	High nibble of pointer
	STA	temp10		; 3	High nibble of pointer
	STA	temp12		; 3	High nibble of pointer
	STA	temp14		; 3	High nibble of pointer


	_sleep	14
	sleep	3		
	STA	RESP1		; (41) X pos
	

	LDA	counter		; 3 
	AND	#%00000001	; 2 
	CMP	#%00000001	; 2 	
	BEQ	bank1_OddStart
	LDA	#$C0
	JMP	bank1_EvenStart

bank1_OddStart
	LDA	#$C0
bank1_EvenStart	
	STA	HMP1
	
	LDA	#0		
	STA	temp02

	STA	WSYNC		; 73
	STA	HMOVE		
	
	LDA	#%00000010	; 2
	STA	PF2		; 3
		
bank1_CalculatorLine
	LDX	temp02		; 3
	LDA	#0		; 2
	STA	GRP0		; 3
	STA	GRP1		; 3

	DEC 	temp18

	JMP	bank1_LoadNextData	; 3
bank1_LoadedShit
	LDY	#7
	LDA	(TileColorPointer),y	; 5 
	CLC			; 3 
	ADC	TileScreenMainColor	; 3 
	STA	COLUPF		; 3 
	STA	COLUP1		; 3 

	LDA	(temp15),y	; 5
	STA	temp19

	STA	WSYNC
	; 2
	LDA	counter		; 3 (5)
	AND	#%00000001	; 2 (7)
	CMP	#%00000001	; 2 (9)
	BEQ	bank1_JumpOddFrame	; 2 (11)

	JMP	bank1_EvenFrame ; 3 (14)
bank1_JumpOddFrame
	JMP	bank1_OddFrame  ; 3 

	align	256

bank1_OddFrame
	LDA	#$00
	STA	HMP0

bank1_Loop_Odd_Line1
	STA	WSYNC		; 3 (76)
	STA	HMOVE		; 3

	LDA	#0		; 2 (5)
	STA	HMP1		; 3 (8)

***	sleep	67

	CMP	temp18		; 3 (11)
	BEQ	bank1_Loop_Odd_IsSelector	; 2 (13)
	NOP			; 2 (15)		
	JMP	bank1_Loop_Odd_NoSelector 	; 3 (18)		

bank1_Loop_Odd_IsSelector
	LDA	(temp15),y	; 5 (18)
bank1_Loop_Odd_NoSelector
	STA	GRP0		; 3 (21)

	LDA	(temp03),y 	; 5 (26)
	STA	GRP1		; 3 (29)
	
***	sleep	45
	sleep	6

	LAX	(temp11),y 	; 5 (40)

	LDA	(temp07),y 	; 5 (45)
	STA	GRP1		; 3 (48)

	sleep	2
	STX	GRP1		; 3 (53)

	LAX	(temp13),y 	; 5 (58)
	TXS			; 2 (60)
	LAX	(temp09),y 	; 5 (65)
	
	LDA	(temp05),y 	; 5 (70)
***	STA	GRP1	
	BYTE	#$8D
	BYTE	#GRP1
	BYTE	$00		; 4 (74)

bank1_Loop_Odd_Line2
	STA	HMOVE		; 2

	LDA	#$80		; 2 (4)
	STA	HMP1		; 3 (7)

	DEY			; 2 (9)

	LDA	(TileColorPointer),y ; 5 (14)
	CLC			     ; 2 (16)
	ADC	TileScreenMainColor  ; 3 (19)
	STA	temp17		     ; 3 (22)

	sleep	20

	STX	GRP1
	TSX
	STX	GRP1
	
	sleep	5
	LDA	temp17
	STA	COLUP1
	STA	COLUPF

	CPY	#255
	BEQ	bank1_Loop_Odd_LineEnd	; 2 (72)
	JMP	bank1_Loop_Odd_Line1
bank1_Loop_Odd_LineEnd
	JMP	bank1_Loop_LineEnd

	align	256

bank1_EvenFrame
	_sleep	46		; (74)
	sleep	4
	
	LDA	#$00
	STA	HMP0

bank1_Loop_Even_Line1
	STA	HMOVE		; 74

	LDA	#$80		; 2
	STA	HMP1		; 3

	LDA	#0		; 2 (5)
	CMP	temp18		; 3 (8)
	BEQ	bank1_Loop_Even_IsSelector	; 2 (10)
	NOP			; 2 (12)		
	JMP	bank1_Loop_Even_NoSelector 	; 3 (15)		

bank1_Loop_Even_IsSelector
	LDA	(temp15),y	; 5 (15)
bank1_Loop_Even_NoSelector
	STA	GRP0		; 3 (18)

	LDA	(temp05),y 	; 5 (23)
	STA	GRP1		; 3 (26)

	sleep	4

	LAX	(temp13),y 	; 5 (35)

	LDA	(temp09),y 	; 5 (40)
	STA	GRP1		; 3 (43)
	sleep	2	
	STX	GRP1		; 3 (48)

	LAX	(temp11),y 	; 5 (54)
	TXS			; 2 (56)

	LAX	(temp07),y 	; 5 (61)
	LDA	(temp03),y 	; 5 (66)
	STA	GRP1		; 3 (69)
	DEY			; 2 (71)

bank1_Loop_Even_Line2
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	#0		; 2 (5)
	STA	HMP1		; 3 (8)

***	sleep	58

	LDA	(TileColorPointer),y ; 5 (13)
	CLC			     ; 2 (15)
	ADC	TileScreenMainColor  ; 3 (18)
	STA	temp17		     ; 3 (21)
	
***	sleep	45

	sleep	24		    ; 45

	STX	GRP1		    ; 3 (48)
	TSX			    ; 2 (50)
	STX	GRP1		    ; 3 (53)
	
	LDA	temp17		    ; 3 (56)
	STA	COLUP1		    ; 3 (59)
	STA	COLUPF		    ; 3 (62)

	sleep	4

	CPY	#255			; 2 (66)
	BEQ	bank1_Loop_LineEnd	; 2 (68)
	JMP	bank1_Loop_Even_Line1   ; 3 (71)
bank1_Loop_LineEnd
	LDA	#0
	STA	GRP0
	STA	GRP1

	DEC	temp01		; 5	
	LDA	temp01		; 3
	CMP	#0		; 2
	BEQ	bank1_EndOfAll	; 2
	JMP	bank1_CalculatorLine	; 3 

bank1_EndOfAll
	
	STA	WSYNC
***	LDA	#0
***	STA	GRP0
***	STA	GRP1
	LDX	item
	TXS

	STA	WSYNC
	LDA	#%11111110
	STA	PF2

	STA	WSYNC
	STA	WSYNC
	STA	WSYNC

bank1_IsThereOverLap
	LDA	OverlapScreen
	AND	#%00100000
	CMP	#%00100000
	BEQ	bank1_ThereItIs
	STA	WSYNC
	JMP	bank1_ResetAll

bank1_ThereItIs
	LDA	OverLapIndicator
	ORA	#%10000000
	STA	OverLapIndicator
	LDA	#0
	STA	WSYNC
	STA	PF2
	LDA	frameColor
	STA	COLUPF
	STA	COLUBK

	LDA	SubMenuLines
	AND	#%00000011
	TAY
	LAX	bank1_ExtraWSYNC,y
bank1_DoExtraWSYNC
	CPX	#0
	BEQ	bank1_NoMoreLiiiiines
	STA	WSYNC
	DEX
	JMP	bank1_DoExtraWSYNC

bank1_NoMoreLiiiiines
	JMP	bank1_DoItAgainPlease

!!!191bytesOfUserData!!!

###End-Main-Kernel-Sub

	align	256
bank1_FineAdjustTable256
	fill 	156

bank1_Zero
bank1_Null
bank1_None
	.BYTE	#0	; This is an empty byte for constant code usage.
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0

bank1_Selector
	byte	#%01100110	; (0)
	byte	#%00000000
	byte	#%10000001
	byte	#%10000001
	byte	#%00000000
	byte	#%00000000
	byte	#%10000001
	byte	#%10011001
	byte	#%11001100	; (1)
	byte	#%00000001
	byte	#%00000001
	byte	#%10000000
	byte	#%10000000
	byte	#%00000001
	byte	#%00000001
	byte	#%11001100
	byte	#%10011001	; (2)
	byte	#%10000001
	byte	#%00000000
	byte	#%00000000
	byte	#%10000001
	byte	#%10000001
	byte	#%00000000
	byte	#%01100110
	byte	#%00110011	; (3)
	byte	#%10000000
	byte	#%10000000
	byte	#%00000001
	byte	#%00000001
	byte	#%10000000
	byte	#%10000000
	byte	#%00110011

bank1_GetSecondPF0
	LDA	temp03		
	ASL			
	ASL			
	ASL			
	ASL			
	STA	PF0	
	RTS

bank1_ScreenOverlapTop
	byte	#16
	byte	#12
	byte	#7
	byte	#4

bank1_ScreenOverlapBottom
	byte	#16
	byte	#13
	byte	#11
	byte	#8

bank1_DecrementTemp1
	byte	#27
	byte	#30
	byte	#32
	byte	#35

bank1_ExtraWSYNC
	byte	#0
	byte	#1
	byte	#2
	byte	#0

bank1_ScreenJumpTable
	.byte	#>ScreenBottomBank2-1
	.byte	#<ScreenBottomBank2-1
	.byte	#>ScreenBottomBank3-1
	.byte	#<ScreenBottomBank3-1
	.byte	#>ScreenBottomBank4-1
	.byte	#<ScreenBottomBank4-1
	.byte	#>ScreenBottomBank5-1
	.byte	#<ScreenBottomBank5-1
	.byte	#>ScreenBottomBank6-1
	.byte	#<ScreenBottomBank6-1
	.byte	#>ScreenBottomBank7-1
	.byte	#<ScreenBottomBank7-1
	.byte	#>ScreenBottomBank8-1
	.byte	#<ScreenBottomBank8-1

bank1_CursorXPosition
	byte	#60	
	byte	#79	
	byte	#83	
	byte	#87
	byte	#106	
	byte	#110	

bank1_FineAdjustTable
	byte	#$80
	byte	#$70
	byte	#$60
	byte	#$50
	byte	#$40
	byte	#$30
	byte	#$20
	byte	#$10
	byte	#$00
	byte	#$f0
	byte	#$e0
	byte	#$d0
	byte	#$c0
	byte	#$b0
	byte	#$a0
	byte	#$90

bank1_UnderTheTable

*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK1!!!

*Data Section
*-------------------------------
* Contains graphics data for the
* main kernel.



	align 256

Data_Section
!!!KERNEL_DATA!!!

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

!!!ENTER_BANK2!!!
		
	JMP	WaitUntilOverScanTimerEndsBank2

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank2

!!!LEAVE_BANK2!!!

JumpToNewScreenBank2
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX2
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank2,y
   	pha
   	lda	LeaveJumpTableBank2+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank2
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1


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

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK2!!!
!!!OVERSCAN_BANK2!!!
!!!SOUNDBANK_BANK2!!!

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank2

!!!VBLANK_BANK2!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank2		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#2
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank2
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank2

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*


	tsx
	stx	item

!!!SCREENTOP_BANK2!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank2	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank2


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank2

	LDA	#2
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank2

	tsx
	stx	item

!!!SCREENBOTTOM_BANK2!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank2

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK2!!!


###End-Bank2
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK2!!!
	

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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank3

!!!ENTER_BANK3!!!
		
	JMP	WaitUntilOverScanTimerEndsBank3

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank3

!!!LEAVE_BANK3!!!

JumpToNewScreenBank3
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX3	
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank3,y
   	pha
   	lda	LeaveJumpTableBank3+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank3
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank3
	CLC
        LDA	INTIM 
        BNE 	OverScanBank3

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK3!!!
!!!OVERSCAN_BANK3!!!
!!!SOUNDBANK_BANK3!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank3
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank3

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank3

!!!VBLANK_BANK3!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank3		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#3
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank3
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank3

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK3!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank3	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank3


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank3

	LDA	#3
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank3

	tsx
	stx	item

!!!SCREENBOTTOM_BANK3!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank3

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK3!!!

###End-Bank3
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK3!!!


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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank4

!!!ENTER_BANK4!!!
		
	JMP	WaitUntilOverScanTimerEndsBank4

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank4

!!!LEAVE_BANK4!!!

JumpToNewScreenBank4
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX4
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank4,y
   	pha
   	lda	LeaveJumpTableBank4+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank4
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank4
	CLC
        LDA	INTIM 
        BNE 	OverScanBank4

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK4!!!
!!!OVERSCAN_BANK4!!!
!!!SOUNDBANK_BANK4!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank4
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank4

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank4

!!!VBLANK_BANK4!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank4		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#4
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank4
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank4

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK4!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank4	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank4


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank4

	LDA	#4
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank4

	tsx
	stx	item

!!!SCREENBOTTOM_BANK4!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank4

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK4!!!

###End-Bank4
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK4!!!
	

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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank5

!!!ENTER_BANK5!!!
		
	JMP	WaitUntilOverScanTimerEndsBank5

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank5

!!!LEAVE_BANK5!!!

JumpToNewScreenBank5
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX5
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank5,y
   	pha
   	lda	LeaveJumpTableBank5+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank5
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank5
	CLC
        LDA	INTIM 
        BNE 	OverScanBank5

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK5!!!
!!!OVERSCAN_BANK5!!!
!!!SOUNDBANK_BANK5!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank5
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank5

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank5

!!!VBLANK_BANK5!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank5		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#5
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank5
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank5

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK5!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank5	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank5


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank5

	LDA	#5
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank5

	tsx
	stx	item

!!!SCREENBOTTOM_BANK5!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank5

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK5!!!

###End-Bank5
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK5!!!
	

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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank6

!!!ENTER_BANK6!!!
		
	JMP	WaitUntilOverScanTimerEndsBank6

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank6

!!!LEAVE_BANK6!!!

JumpToNewScreenBank6
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX6
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank6,y
   	pha
   	lda	LeaveJumpTableBank6+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank6
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1


*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank6
	CLC
        LDA	INTIM 
        BNE 	OverScanBank6

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK6!!!
!!!OVERSCAN_BANK6!!!
!!!SOUNDBANK_BANK6!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank6
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank6

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank6

!!!VBLANK_BANK6!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank6		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#6
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank6
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank6

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK6!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank6	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank6


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank6

	LDA	#6
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank6

	tsx
	stx	item

!!!SCREENBOTTOM_BANK6!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank6


*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK6!!!

###End-Bank6
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK6!!!
	

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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank7

!!!ENTER_BANK7!!!
		
	JMP	WaitUntilOverScanTimerEndsBank7

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank7

!!!LEAVE_BANK7!!!

JumpToNewScreenBank7
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX7
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank7,y
   	pha
   	lda	LeaveJumpTableBank7+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank7
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1

*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank7
	CLC
        LDA	INTIM 
        BNE 	OverScanBank7

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK7!!!
!!!OVERSCAN_BANK7!!!
!!!SOUNDBANK_BANK7!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank7
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank7

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank7

!!!VBLANK_BANK7!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank7		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#7
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank8_CalculateDuringVBLANK-1)
   	pha
   	lda	#<(bank8_CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank7
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank7

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK7!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank7	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank7


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank7

	LDA	#7
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank7

	tsx
	stx	item

!!!SCREENBOTTOM_BANK7!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank7

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK7!!!


###End-Bank7
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK7!!!
	

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
	
*Enter Bank
*-----------------------------
*
* This is the section that happens
* everytime you go to a new screen.
* Should set the screen initialization
* here.
*

EnterScreenBank8

!!!ENTER_BANK8!!!
		
	JMP	WaitUntilOverScanTimerEndsBank8

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank8

!!!LEAVE_BANK8!!!

JumpToNewScreenBank8
	LAX	temp02		; Contains the bank to jump
JumpToNewScreenBank_NoLAX8
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table	
		
	lda	LeaveJumpTableBank8,y
   	pha
   	lda	LeaveJumpTableBank8+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LeaveJumpTableBank8
	byte	#>EnterScreenBank2-1
	byte	#<EnterScreenBank2-1
	byte	#>EnterScreenBank3-1
	byte	#<EnterScreenBank3-1
	byte	#>EnterScreenBank4-1
	byte	#<EnterScreenBank4-1
	byte	#>EnterScreenBank5-1
	byte	#<EnterScreenBank5-1
	byte	#>EnterScreenBank6-1
	byte	#<EnterScreenBank6-1
	byte	#>EnterScreenBank7-1
	byte	#<EnterScreenBank7-1
	byte	#>EnterScreenBank8-1
	byte	#<EnterScreenBank8-1

*Overscan
*-----------------------------
*
* This is the place of the main
* code of this screen.
*

OverScanBank8
	CLC
        LDA	INTIM 
        BNE 	OverScanBank8

	STA	WSYNC
	LDA	#%11000010
	STA	VBLANK
	STA	WSYNC

    	LDA	#!!!TV!!!_Overscan
    	STA	TIM64T
	INC	counter

*Overscan Code
*-----------------------------
*
* This is where the game code
* begins.
*

!!!JUKEBOX_BANK8!!!
!!!OVERSCAN_BANK8!!!
!!!SOUNDBANK_BANK8!!!

*VSYNC
*----------------------------
* This is a fixed section in
* every bank. Don't need to be
* at the same space, of course.

WaitUntilOverScanTimerEndsBank8
	CLC
	LDA 	INTIM
	BMI 	WaitUntilOverScanTimerEndsBank8

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
 	LDA	#!!!TV!!!_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank8

!!!VBLANK_BANK8!!!


*SkipIfNoGameSet - VBLANK
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BMI	VBlankEndBank8		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	#%00011100	; Save the bankNumber
	STA	bankToJump

   	jmp	bank8_CalculateDuringVBLANK

VBlankEndBank8
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank8

    	LDA	#!!!TV!!!_Display
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item

!!!SCREENTOP_BANK8!!!

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs


*SkipIfNoGameSet
*---------------------------------
*

	BIT	NoGameMode 		; NoGameMode
	BPL	JumpToMainKernelBank8	; if 7th bit set (for a title or game over screen), the main game section is skipped.	
	LDX	#0	
	JMP	ScreenBottomBank8


*JumpToMainKernel
*---------------------------------
* For this, the program go to main
* kernel in bank1.

JumpToMainKernelBank8

	LDA	#8
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(bank1_EnterKernel-1)
   	pha
   	lda	#<(bank1_EnterKernel-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

*ScreenBottom
*--------------------------------  
* This is the section for the
* bottom part of the screen.
*

ScreenBottomBank8

	tsx
	stx	item

!!!SCREENBOTTOM_BANK8!!!

	LDA	#0
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF	

	ldx	item
	txs

	JMP	OverScanBank8

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

	align	256

!!!USER_DATA_BANK8!!!


###End-Bank8
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK8!!!


	align 256

*Calculations during VBLANK
*----------------------------
*

###START-MAIN-VBLANK

bank8_CalculateDuringVBLANK

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
	BIT	SubMenu
	BVC	bank8_CheckIfOutOfBorders	; Go to the SubMenu Kernel
	JMP	bank8_SubMenuVBLANK	


*CheckIfOutOfBorders
*--------------------------------------------
* This section will decide what should happen
* to the objects as they are touching the borders
* of the screen.

bank8_CheckIfOutOfBorders
	
	LDA	pfEdges
	AND	#%11000000
	STA	temp07
	CMP	#%00000000
	BEQ	bank8_CalculateIndexes	

	TSX
	STX	temp03	
	LDX	#4	; p0, p1, m0, m1, bl


bank8_NextItemThings
*	
* temp01 - Largest X allowed
* temp02 - Largest Y allowed	
* temp03 - Stack pointer saved
* temp04 - Even Or Odd or Ball
* temp05, temp08 - Temporal Storage
* temp06 - Smallest Y allowed
* temp07 - Mode
*
	TXA	
	TXS	
 	LDA	bank8_XTable,x

	TAX
	STA	temp04
	LDA	P0Settings,x
	AND	#%00000111
	TAX	
	LDA	bank8_XHorBorderAddSprite,x
	TSX
	CPX	#2
	BCC	bank8_NotAMissile
bank8_ItsAMissile	
	SEC
	SBC	#7
	sta	temp05
	LDX	temp04
	TAX
	LDA	P0Settings,x
	AND	#%00110000		
	lsr
	lsr
	lsr
	lsr
	TAX
	LDA	bank8_XHorBorderAddMissile,x
	CLC
	ADC	temp05

bank8_NotAMissile
	STA	temp05
	LDA	#160	
	SEC	
	SBC	temp05
	STA	temp01

bank8_VerticalFun
	LDX	temp04
	LDA	P0Height,x
	TSX
	CPX	#2
	BCS	bank8_ItsAMissile2
	LDA	temp04
	JMP 	bank8_NotAMissile2
bank8_ItsAMissile2
	LDA	#0
bank8_NotAMissile2
	STA	temp05
	LDA	#40
	SEC
	SBC	temp05
	STA	temp02

bank8_VerticalFun2
	LDX	temp04
	LDA	P0Height,x
	TSX
	CPX	#2
	BCS	bank8_ItsAMissile3
	CLC	
	ADC	#2
	ADC	temp04

	JMP	bank8_NotAMissile3
bank8_ItsAMissile3
	LDA	#2
bank8_NotAMissile3
	STA	temp06

	TSX
	LDA	temp07
	CMP	#%11000000
	BEQ	bank8_AppearOpposite

	LDA	temp07
	BMI	bank8_NoBLAHBLAH
	CPX	#2
	BCS	bank8_AppearOpposite

bank8_NoBLAHBLAH
	LDA	P0X,x
	CMP	#16
	BCS	bank8_NotSmallerThan
	LDA	#16
	STA	P0X,x	
	JMP	bank8_doYForNow
bank8_NotSmallerThan
	LDA	temp01
	CMP 	P0X,x
	BCS	bank8_doYForNow
	STA	P0X,x
bank8_doYForNow
	LDA	P0Y,x
	CMP	temp06
	BCS	bank8_NotLowerThan
	LDA	temp06
	STA	P0Y,x
bank8_NotLowerThan
	LDA	temp02
	CMP	P0Y,x
	BCS	bank8_PrepareForNext
	LDA	temp02
	STA	P0Y,x
bank8_PrepareForNext
	DEX	
	CPX	#255
	BNE	bank8_NextItemThings
	JMP	bank8_StackBackUp

bank8_AppearOpposite
	LDA	P0X,x
	CMP	#16
	BCS	bank8_NotSmallerThan2
	LDA	temp01
	SEC
	SBC	#1
	STA	P0X,x	
	JMP	bank8_doYForNow2
bank8_NotSmallerThan2
	LDA	temp01
	CMP 	P0X,x
	BCS	bank8_doYForNow2
	LDA	#17
	STA	P0X,x
bank8_doYForNow2
	LDA	P0Y,x
	CMP	temp06
	BCS	bank8_NotLowerThan2
	LDA	temp02
	SEC
	SBC	#1
	STA	P0Y,x
bank8_NotLowerThan2
	LDA	temp02
	CMP	P0Y,x
	BCS	bank8_PrepareForNext2
	LDA	temp06
	CLC
	ADC	#1
	STA	P0Y,x
bank8_PrepareForNext2
	DEX	
	CPX	#255
	BNE	bank8_NextItemThings

bank8_StackBackUp
	LDX	temp03
	TXS

bank8_CalculateIndexes
	LDA 	P0Height
	CLC
	ADC	#1
	STA	temp01	

	LDA	P0SpriteIndex	
	AND	#%00001111	; Get low nibble for P0 index
	TAY			; Move it to Y for calculations
	LDA	P0SpritePointer
	
bank8_CalculateP0PointerIndex
	; You can only have the maximum number of sprites 256/height that is always smaller than 16
	; (over 16 px height, you cannot use all 16 indexes because of the paging overflow that would break timing.

	CPY	#0
	BEQ	bank8_CalculateP0PointerIndexDone
	CLC	
	ADC	temp01
	DEY
	JMP	bank8_CalculateP0PointerIndex


bank8_CalculateP0PointerIndexDone
	STA	temp07		; temp10 will store the sprite pointers low byte
 
	LDA 	P1Height
	CLC
	ADC	#1
	STA	temp01	

	LDA	P1SpriteIndex	
	AND	#%11110000	; Get high nibble for P1 index
	lsr
	lsr
	lsr
	lsr
	TAY			; Move it to Y for calculations
	LDA	P1SpritePointer
	
bank8_CalculateP1PointerIndex
	; You can only have the maximum number of sprites 256/height that is always smaller than 16
	; (over 16 px height, you cannot use all 16 indexes because of the paging overflow that would break timing.

	CPY	#0
	BEQ	bank8_CalculateP1PointerIndexDone
	CLC	
	ADC	temp01
	DEY
	JMP	bank8_CalculateP1PointerIndex


bank8_CalculateP1PointerIndexDone
	STA	temp10		; temp10 will store the sprite pointers low byte

###END-MAIN-VBLANK

bank8_JumpBackToBankScreenTop

	lda	bankToJump
	lsr
	lsr
	AND	#%00000111	; Get the bank number to return
	tax
	
	SEC
	SBC	#2
	STA	temp01		
	CLC
	ADC	temp01		; ([bankNum - 2] * 2 )
	TAY			; Get the location of address from the table
		
		
	lda	bank8_VBlankJumpTable,y
   	pha
   	lda	bank8_VBlankJumpTable+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

bank8_VBlankJumpTable
	byte	#>VBlankEndBank2-1
	byte	#<VBlankEndBank2-1
	byte	#>VBlankEndBank3-1
	byte	#<VBlankEndBank3-1
	byte	#>VBlankEndBank4-1
	byte	#<VBlankEndBank4-1
	byte	#>VBlankEndBank5-1
	byte	#<VBlankEndBank5-1
	byte	#>VBlankEndBank6-1
	byte	#<VBlankEndBank6-1
	byte	#>VBlankEndBank7-1
	byte	#<VBlankEndBank7-1
	byte	#>VBlankEndBank8-1
	byte	#<VBlankEndBank8-1

bank8_XTable
	byte	#0
	byte	#1
	byte	#0
	byte	#1
	byte	#2

bank8_XHorBorderAddSprite
	byte	#8
	byte	#24
	byte	#40
	byte	#40
	byte	#72
	byte	#16
	byte	#72
	byte	#32
	

bank8_XHorBorderAddMissile
	byte	#1
	byte	#2
	byte	#4
	byte	#8

bank8_SubMenuVBLANK	
	LDA	SubMenuLines
	AND	#%00000011
	CLC
	ADc	#1
	TAY
	LDA	#0
	STA	temp02
bank8_Add6ToThat
	CPY	#0
	BEQ	bank8_NoMore6
	CLC
	ADC	#6
	DEY
	JMP 	bank8_Add6ToThat
bank8_NoMore6
	STA	temp02
	
	LDA	TileSelected
	AND	#%00011111
	CMP	temp02
	BCC	bank8_NoLargerThan24
	LDA	TileSelected
	AND	#%11100000
	STA	TileSelected
bank8_NoLargerThan24

bank8_SubMenuVBLANKEnd
	JMP	bank8_JumpBackToBankScreenTop

	align 256
	
bank8_Start
   	sei
   	cld
   	ldy	#0
   	lda	$D0
   	cmp	#$2C		;check RAM location #1   	bne	MachineIs2600
   	lda	$D1
   	cmp	#$A9		;check RAM location #2   	bne	MachineIs2600
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

	LDA	$F080		; Sets two values for the SC RAM 
	STA	$80		; to Random and Counter variables
	LDA	$F081
	STA	$81

	LDY	#0		
	TYA
	STA	$F029
bank8_ClearSCRAM
	STA 	$F000,Y
	INY
	BPL 	bank8_ClearSCRAM

bank8_DisableMusicWaveOnStartUp
	LDA	#%00111111
	STA	JukeBox_Controller

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