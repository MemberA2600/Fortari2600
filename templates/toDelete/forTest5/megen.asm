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
temp15 = $91
temp16 = $92
temp17 = $93
temp18 = $94
temp19 = $95


item = $96
frameColor = $97
			
*** Playfield Elements
pf0Pointer = $98		; 16 bits
pf1Pointer = $9a		; 16 bits
pf2Pointer = $9c		; 16 bits	
pfColorPointer = $9e		; 16 bits 
bkColorPointer = $a0		; 16 bits
bkBaseColor = $a2
pfBaseColor = $a3
pfIndex = $a4

************************
SubMenu = $a5		; 0-1 : SubMenuLines
NoGameMode = $a5	; 2-4 : BankToJump
bankToJump = $a5	; 5 : FREE
SubMenuLines = $a5	; 6 : Go to SubMenu
************************  7 : No Game Mode

*** Player Settings
P0SpritePointer = $a6		; 16bit
P0ColorPointer = $a8		; 16bit
P1SpritePointer = $aa		; 16bit
P1ColorPointer = $ac		; 16bit

************
* Settings *
****************************************	
P0Settings = $ae			; Bits 0-2 are sprite settings, 
P0Mirrored = $ae			; 3 is reflection, bits 4-5 are missile settings. 
P0TurnOff  = $ae			; 6: Turn Off Sprite
P1Settings = $af			; 7: Turn off Missile
P1Mirrored = $af			; Must be in order!
P1TurnOff  = $af
****************************************
pfSettings = $b0	; Since CTRLPF 0-1 bits are fixed in the screen loop
pfEdges	= $b0		; 0-1: free
BallTurnOff = $b0	; 2: Players move behind the pf
#Has to be here because	; 3: Turn off Ball
#of the edge check	; 4-5: Ball Settings
#routine.		; 6-7: 00 - Nothing 01 - Mixed 10 - All stop 11 - All go through 		;
************************

P0Height = $b1
P1Height = $b2

****************************************
P0SpriteIndex = $b3			; low nibble is P0 sprite index
P1SpriteIndex = $b3			; high nibble is P1 sprite index
****************************************

*** Positions (Must be aligned!!)
P0Y = $b4	
P1Y = $b5	
M0Y = $b6
M1Y = $b7
BLY = $b8

P0X = $b9
P1X = $ba
M0X = $bb
M1X = $bc
BLX = $bd

*** Fake Missile Colors
M0Color = $be
M1Color = $bf

*** TileScreen
TileSetPointer = $c0	; 16 bit
TileScreenMainColor = $c2

*** Matrix 6x4
Tile1_1 = $c3
Tile1_2 = $c3
Tile1_3 = $c4
Tile1_4 = $c4
Tile1_5 = $c5
Tile1_6 = $c5

Tile2_1 = $c6
Tile2_2 = $c6
Tile2_3 = $c7
Tile2_4 = $c7
Tile2_5 = $c8
Tile2_6 = $c8

Tile3_1 = $c9
Tile3_2 = $c9
Tile3_3 = $ca
Tile3_4 = $ca
Tile3_5 = $cb
Tile3_6 = $cb

Tile4_1 = $cc
Tile4_2 = $cc
Tile4_3 = $cd
Tile4_4 = $cd
Tile4_5 = $ce
Tile4_6 = $ce

TileColorPointer = $cf 	; 16 bits

*******************
TileSelected = $d1  ; 0-4th bit: Selected Tile (5 bits)
OverlapScreen = $d1 ; 5th bit: Have some part of the other screen
GrayScale     = $d1 ; 6th bit: GrayScale overlap
OverLapIndicator = $d1
*******************

	; Constants
 
NTSC_Vblank =	169
NTSC_Overscan =	163

PAL_Vblank =	185
PAL_Overscan =	206


	; User defined variables

*Global
*---------


*Bank2
*---------


*Bank3
*---------


*Bank4
*---------


*Bank5
*---------


*Bank6
*---------


*Bank7
*---------


*Bank8
*---------


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

EnterKernel
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

	BIT	SubMenu
	BVC	StayHere	; Go to the SubMenu Kernel
	JMP 	DoSubMenuKernel	; instead.

StayHere
	LDA	frameColor	
	sta	WSYNC
	STA	COLUBK
  	ldx	#4 		; From bl -> p0

HorPosLoop		
   	lda	P0X,X	
DivideLoop
	sbc	#15
   	bcs	DivideLoop
   	sta	temp01,X
   	sta	RESP0,X	
   	sta	WSYNC
   	dex
   	bpl	HorPosLoop	

	ldx	#4		; bl
   	ldy	temp05
   	lda	FineAdjustTable256,Y
   	sta	HMP0,X		

	dex			; m1
   	ldy	temp04
   	lda	FineAdjustTable256,Y
   	sta	HMP0,X	
   
	dex			; m0
   	ldy	temp03
   	lda	FineAdjustTable256,Y
   	sta	HMP0,X	
   
	dex			; p1
   	ldy	temp02
   	lda	FineAdjustTable256,Y
   	sta	HMP0,X	

	dex			; p0
   	ldy	temp01
   	lda	FineAdjustTable256,Y
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

SettingUpP0SpriteAndMissile0

	LDA	P0Settings	;3 (59)
	STA	REFP0		;3 (62)
	AND	#%00110111	;2 (64)
	STA	NUSIZ0	; Sets P0 and M0 registers 3 (67)

	LDA	P0SpritePointer+1	; temp08 will store the sprite pointers high byte ; 3 (70)
	STA	temp07+1		; 2 (72)

	LDA	P0Y ; 3 (75)
	STA	temp09 	; temp09 stores P0 Y position. 3 (2) One line wasted.
	
SettingUpP1SpriteAndMissile1

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


FinishPreparation
	TSX			; 2 (31)
	STX	item		; Save the stack pointer 3 (34)

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
	BVC	NoP0TurnOff	; 2 (14)

	LDA	#<Zero		  ; 2
	STA	P0SpritePointer   ; 3
	LDA	#>Zero		  ; 2
	STA	P0SpritePointer+1 ; 3
	LDA	#1		; 2
	STA	P0Height	; 3

	STY	P0Y		; 3 (17)
NoP0TurnOff
	BPL	NoM0TurnOff	; 2 (19)
	STY	M0Y		; 3 (22)
NoM0TurnOff
	
	LDA	P1TurnOff	; 3 (25)
	BVC	NoP1TurnOff	; 2 (27)

	LDA	#<Zero		  ; 2
	STA	P1SpritePointer   ; 3
	LDA	#>Zero		  ; 2
	STA	P1SpritePointer+1 ; 3
	LDA	#1		; 2
	STA	P1Height	; 3	

	STY	P1Y		; 3 (30)
NoP1TurnOff
	BPL	NoM1TurnOff	; 2 (32)
	STY	M1Y		; 3 (35)
NoM1TurnOff

	LDA	BallTurnOff	; 3 (38)
	AND	#%00001000	; 2 (40)
	CMP	#%00001000	; 2 (42)
	BNE	NoBallTurnOff	; 2 (44)
	STY	BLY		; 3 (47)

NoBallTurnOff
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
	JMP	FirstLine	; 3(76)

NoP0DrawNow
	CPX	M0Y		; 3
	BNE	NoColorOverWriteM0

	LDA	M0Color		; 3
	STA	COLUP0		; 3
	LDA	#0	  	; 2

	JMP	saveP0Sprite	; 3 


NoColorOverWriteM0
	sleep 	5
	LDA	#0
	JMP	saveP0Sprite	; 3 


NoP1DrawNow
	CPX	M1Y		; 3
	BNE	NoColorOverWriteM1

	LDA	M1Color		; 3
	STA	COLUP1		; 3
	LDA	#0	  	; 2

	JMP	saveP1Sprite	; 3 


NoColorOverWriteM1
	sleep 	5
	LDA	#0
	JMP	saveP1Sprite	; 3 



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

FirstLine
	STA	WSYNC		; 3 (76)
StartWithoutWSYNC
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

MiddleLine

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
	BCC	NoP0DrawNow	; 2 
	LDY	temp09		; 3 
	LDA	(P0ColorPointer),y 	; 5 
	STA	COLUP0		; 3 
	LDA	(temp07),y 	; 5 
saveP0Sprite
	STA	temp14		; 3 
	; 29 (3)

LastLine

	LDA	temp05		; 3 (9)
	STA	PF0		; 3 (12)

	LDA 	P1Height 	; 3 
	DCP	temp12 		;  temp12 contains P0Y!  ; 5 
	BCC	NoP1DrawNow	; 2 
	LDY	temp12		; 3 
	LDA	(P1ColorPointer),y 	; 5
	STA	COLUP1	; 3 
	LDA	(temp10),y 	; 5
saveP1Sprite
	STA	temp03		; 3 
	; 29 (41)

	LDA	temp06		; 3 (44)
	STA	PF0		; 3 (47)

	LDY	temp14		; 3 (50)


	CPX	#1		; 2 (58)
	BEQ	ResetAll  	; 2 (60)

	DEX			; 2 (62)
	LDA	temp02		; 3 (65)

	DEC	temp01		; 5 (70)
	JMP	FirstLine	; 3 (73)

ResetAll
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

	LDX	item		; Retrieve the stack pointer
	TXS


JumpBackToBankScreenBottom

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
		
		
	lda	ScreenJumpTable,y
   	pha
   	lda	ScreenJumpTable+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

LoadNextData
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
	JMP	LoadedShit	; 3

DoSubMenuKernel
	TSX			; 2 
	STX	item		; 3

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
	BEQ	DoThisCrap
	JMP	NoOverLap

DoThisCrap
	LDX	#3
AddLines
	STA	WSYNC
	DEX	
	CPX	#255
	BNE	AddLines
	
DoItAgainPlease
	STA	WSYNC
	LDA	SubMenuLines
	AND	#%00000011
	TAX

	LDA	OverLapIndicator
	BMI	ItsTheBottom
	LDA	ScreenOverlapTop,x
	JMP	SaveToppp
ItsTheBottom
	LDA	ScreenOverlapBottom,x
SaveToppp
	STA	temp11
	

	LDA	#15		
	CLC			
	ADC	pfIndex		 
	STA	temp01		; Save pfIndex 
	STA	WSYNC
	LDA	OverLapIndicator
	BPL	NoTemp01Dec
	LDA	SubMenuLines
	AND	#%00000011
	TAX

	LDA	temp01
	SEC
	SBC	DecrementTemp1,x
	STA	temp01
NoTemp01Dec
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
	BNE	NotGray
	LDA	temp02
	AND	#%00001111
	STA	temp02
	LDA	temp04
	AND	#%00001111
	STA	temp04
NotGray
	STA	WSYNC

	LDA	OverLapIndicator
	BPL	NoINY
	INY
NoINY
	LDA	(pf2Pointer),y		
	STA	PF2	
	
	LDA	(pf1Pointer),y	
	STA	PF1

	LDA	(pf0Pointer),y		
	STA	PF0	
	STA	temp03
	LDA	OverLapIndicator
	BPL	NoDEY
	DEY
NoDEY

NewLineWithTemp04
	LDA	temp04
NewLine
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
	

	JSR	GetSecondPF0	

	

	LDA	(pfColorPointer),y	; 5 (55)
	CLC			; 2 (57)	
	ADC	pfBaseColor 	; 3 (60)
	STA	temp02		; 3 (63)
	DEY			
	STA	WSYNC	
	LDA	temp03		; 3
	STA	PF0		; 3 (6)
	sleep	2
	JSR	GetSecondPF0	; 6 (12) + 20

	LDA	GrayScale	; 3 
	AND	#%01000000	; 2 
	CMP	#%01000000	; 2 
	BNE	NotGray2	; 2 
	LDA	temp02		; 3 
	AND	#%00001111	; 2 
	STA	temp02		; 3 
	LDA	temp04		; 3 
	AND	#%00001111	; 2 
	STA	temp04		; 3 
NotGray2

	DEX
	CPX	#1	
	BEQ	ResetToOther


	LDA	temp04
	JMP	NewLine
ResetToOther

	
NoOverLap
*	temp01: Rows left
*	temp02: LineNum
*	temp03 - temp14: GRP0 pointers
*	temp15 - temp16: Selector Sprite Pointer
*	temp17: ColorData
*	temp18: TileY
*	temp19: SelectorData



NoResetNow
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK		; 3
	LDA	#0		
	STA	PF0		
	STA	PF1	
	STA	PF2


	LDA	OverLapIndicator
	BPL	FFFF	

	JMP	ResetAll
FFFF


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
	ADC	#<Selector-1	; 3 
	STA	temp15		; 3 
	LDA	#>Selector-1	; 3 
	STA	temp16		; 3 

	LDY	#0
	STY	NUSIZ0
	LDA	TileSelected
	AND	#%00011111

SmallerThan6
	CMP	#6
	BCC	GetP0Poz
	SEC
	SBC	#6
	INY
	JMP	SmallerThan6
GetP0Poz
	STY	temp18	; Get the Tile row number reversed
	LDY	#0
	STY	temp03

	STA	WSYNC
	TAX
	LDA	CursorXPosition,x
	LDX	temp03
CursorPozLoop
	sbc	#15
   	bcs	CursorPozLoop
   	sleep	2
	tay
   	sta	RESP0	
   	LDA	FineAdjustTable256,Y
	STA	HMP0
	INC	temp18

SetP0TilePositions
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
	BEQ	OddStart
	LDA	#$C0
	JMP	EvenStart
OddStart
	LDA	#$C0
EvenStart	
	STA	HMP1
	
	LDA	#0		
	STA	temp02

	STA	WSYNC		; 73
	STA	HMOVE		
	
	LDA	#%00000010	; 2
	STA	PF2		; 3

		
CalculatorLine
	LDX	temp02		; 3
	LDA	#0		; 2
	STA	GRP0		; 3
	STA	GRP1		; 3

	DEC 	temp18

	JMP	LoadNextData	; 3
LoadedShit
	LDY	#7
	LDA	(TileColorPointer),y	; 5 
	CLC			; 3 
	ADC	TileScreenMainColor	; 3 
	STA	COLUPF		; 3 
	STA	COLUP1		; 3 

	INY
	LDA	(temp15),y	; 5
	STA	temp19
	DEY

	STA	WSYNC
	; 2
	LDA	counter		; 3 (5)
	AND	#%00000001	; 2 (7)
	CMP	#%00000001	; 2 (9)
	BEQ	JumpOddFrame	; 2 (11)

	JMP	EvenFrame	; 3 (14)
JumpOddFrame
	JMP	OddFrame

	align	256

OddFrame
	LDA	#$00
	STA	HMP0

	
	sta	WSYNC

Loop_Odd_Line1
	STA	HMOVE		; 3
	LDA	#$00		; 2 (5)
	STA	HMP1		; 3 (8)
	
	LDA	temp18		; 3
	CMP	#0		; 2
	BEQ	SelectorDraw	; 2
	LDA	#0		; 2
	sleep	2
	JMP	NoSelectorDraw	; 3
SelectorDraw
	sleep	3
	LDA	temp19		; 3
NoSelectorDraw
	STA	GRP0		; 3

	
	LDA	(temp03),y 	; 5 (30)
	STA	GRP1		; 3 (33)

	LDA	(temp11),y 	; 5 (38)
	TAX			; 2 (40)

	LDA	(temp07),y 	; 5 (45)
	STA	GRP1		; 3 (48)
	sleep	2
	STX	GRP1		; 3 (53)
	

	sleep	8	
	LDA	(temp15),y	
	STA	temp19


	LDA	#$00
	STA	HMP0

Loop_Odd_Line2
	STA	HMOVE		; 3
	LDA	#$80		; 2 (5)
	STA 	HMP1		; 3 (8)

	LDA	(TileColorPointer),y	; 5 
	CLC			; 3 
	ADC	TileScreenMainColor	; 3 
	STA	temp17		; 3 
	sleep	3

	LDA	(temp05),y 	; 5 (30)
	STA	GRP1		; 3 (33)

	LDA	(temp13),y 	; 5 (38)
	TAX			; 2 (40)

	LDA	(temp09),y 	; 5 (45)
	STA	GRP1		; 3 (48)
	sleep 	2
	STX	GRP1		; 3 (53)

	
	sleep	10
		


	LDA	temp17		; 3
	STA	COLUPF		; 3
	STA	COLUP1		; 3 

	DEY			; 2 (74)
	BPL	Loop_Odd_Line1	; 2 (76)
	LDA	#0
	STA	GRP0
	STA	GRP1

	DEC	temp01		; 5	
	LDA	temp01		; 3
	CMP	#0		; 2
	BEQ	EndOfAll	; 2
	JMP	CalculatorLine	; 3 	

EvenFrame

	_sleep	52		; (74)
	sleep	5
	
	LDA	#$00
	STA	HMP0


Loop_Even_Line1
	STA	HMOVE		; 3
	LDA	#$80		; 2 (5)
	STA	HMP1		; 3 (8)
	
	LDA	temp18		; 3
	CMP	#0		; 2
	BEQ	SelectorDraw2	; 2
	LDA	#0		; 2
	sleep	2
	JMP	NoSelectorDraw2	; 3
SelectorDraw2
	sleep	3
	LDA	temp19		; 3
NoSelectorDraw2
	STA	GRP0		; 3
	

	LDA	(temp05),y 	; 5 (30)
	STA	GRP1		; 3 (33)

	LDA	(temp13),y 	; 5 (38)
	TAX			; 2 (40)

	LDA	(temp09),y 	; 5 (45)
	STA	GRP1		; 3 (48)
	sleep	2
	STX	GRP1		; 3 (53)


	sleep	10
	LDA	(temp15),y	; 5
	STA	temp19

	LDA	#$00
	STA	HMP0

Loop_Even_Line2
	STA	HMOVE		; 3
	LDA	#$00		; 2 (5)
	STA 	HMP1		; 3 (8)

	LDA	(TileColorPointer),y	; 5 
	CLC			; 3 
	ADC	TileScreenMainColor	; 3 
	STA	temp17		; 3 
	sleep	3

	LDA	(temp03),y 	; 5 (30)
	STA	GRP1		; 3 (33)

	sleep	2
	LDA	(temp11),y 	; 5 (38)
	TAX			; 2 (40)

	LDA	(temp07),y 	; 5 (45)
	STA	GRP1		; 3 (48)
	sleep 	3
	STX	GRP1		; 3 (53)

	LDA	#$00
	STA	HMP0

	LDA	temp17		; 3
	STA	COLUPF		; 3
	STA	COLUP1		; 3 

	DEY			; 2 (72)
	BPL	Loop_Even_Line1	; 2 (74)
	LDA	#0
	STA	GRP0
	STA	GRP1

	DEC	temp01		; 5	
	LDA	temp01		; 3
	CMP	#0		; 2
	BEQ	EndOfAll	; 2
	JMP	CalculatorLine	; 3 	

EndOfAll
	
	STA	WSYNC
	LDA	#0
	STA	GRP0
	STA	GRP1

	STA	WSYNC
	LDA	#%11111110
	STA	PF2

	STA	WSYNC
	STA	WSYNC
	STA	WSYNC


IsThereOverLap
	LDA	OverlapScreen
	AND	#%00100000
	CMP	#%00100000
	BEQ	ThereItIs
	STA	WSYNC
	JMP	ResetAll

ThereItIs
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
	LAX	ExtraWSYNC,y
DoExtraWSYNC
	CPX	#0
	BEQ	NoMoreLiiiiines
	STA	WSYNC
	DEX
	JMP	DoExtraWSYNC

NoMoreLiiiiines
	JMP	DoItAgainPlease



	align	256
FineAdjustTable256
	fill 	156

Zero
Null
None
	.BYTE	#0	; This is an empty byte for constant code usage.
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0
	.BYTE	#0

Selector
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

GetSecondPF0
	LDA	temp03		
	ASL			
	ASL			
	ASL			
	ASL			
	STA	PF0	
	RTS

ScreenOverlapTop
	byte	#16
	byte	#12
	byte	#7
	byte	#4

ScreenOverlapBottom
	byte	#16
	byte	#13
	byte	#11
	byte	#8

DecrementTemp1
	byte	#27
	byte	#30
	byte	#32
	byte	#35

ExtraWSYNC
	byte	#0
	byte	#1
	byte	#2
	byte	#0

ScreenJumpTable
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

CursorXPosition
	byte	#60	
	byte	#79	
	byte	#83	
	byte	#87
	byte	#106	
	byte	#110	


FineAdjustTable
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

UnderTheTable


*Data Section
*-------------------------------
* Contains graphics data for the
* main kernel.



	align 256

Data_Section


	saveFreeBytes
	rewind 1fd4

start_bank1 
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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

picIndex = $d2
picDisplayHeight = $d3
picHeight = 27

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#27
	STA	picDisplayHeight

	LDA	#0
	STA	picIndex

	

		
	JMP	WaitUntilOverScanTimerEndsBank2

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank2



JumpToNewScreenBank2
	LAX	temp02		; Contains the bank to jump
	
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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank2
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank2

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*


	tsx
	stx	item

pic64px_KernelStart
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)
	STA	COLUPF		; 3 (15)

	LDA	#0		; 2 (17)
	STA	PF0		; 3 (20)
	STA	PF1		; 3 (23)
	STA	PF2		; 3 (26)
	STA	GRP0		; 3 (29)
	STA	GRP1		; 3 (32)
	STA	VDELP0		; 3 (35)
	STA	VDELP1		; 3 (38)

	LDA	#$02		; 2 (40)
	STA	NUSIZ0		; 3 (43)
	STA	NUSIZ1		; 3 (46) 

	LDA	#%00000001	; mirrored pf with regular colors 2 (48)
 	STA	CTRLPF		; 3 (51)

	LDA	#picHeight	; height of the picture 3 (53)
	SEC			; 2 (55)
	SBC	picIndex	; index of scrolling 3 (58)
	STA	temp01		; starting point 3 (61)
	TAY			; 2 (63)
	SEC			; 2 (65)
	SBC 	picDisplayHeight ; 3 (68)
	STA 	temp02		; displayed height (stops if Y gets here) 3 (71)
	STA	WSYNC		; (76)	- One line wasted

	_sleep	26
	sleep 3

	STA	RESP0		; 3 (32)
	sleep	3		;   (34)	
	STA	RESP1		; 3 (37) Set the X pozition of sprites.

	LDA	counter		; 3 (6)
	AND	#%00000001	; 2 (8)
	CMP	#%00000001	; 2 (10)
	BNE	pic64px_OddFrame  ; 2 (12)
	JMP	pic64px_EvenFrame ; 3 (15)	

	align	256

pic64px_OddFrame
	_sleep	42
	sleep	5

	LDA	#0
	STA	GRP0
	STA	GRP1

	LAX	pic64px_06,y

	LDA	#$00				; 2
	STA 	HMP0				; 3 
	LDA	#$20				; 2
	STA 	HMP1				; 3 
	STA 	WSYNC				; 76

pic64px_OddFrame_Line1
	STA	HMOVE				; 3 

	LDA	pic64px_BGColor,y		; 4 (7)
	STA	COLUBK				; 3 (10)	
	LDA	pic64px_PF,y			; 4 (14)
	STA	PF2				; 3 (17)
	LDA	pic64px_PFColor,y		; 4 (21)
	STA	COLUPF				; 3 (24)
		
	LDA	pic64px_Color,y			; 4 
	STA	COLUP0				; 3 
	STA	COLUP1				; 3 
	
	LDA	pic64px_00,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_02,y			; 4
	STA	GRP1				; 3 

	LDA	pic64px_04,y			; 4
	STA	GRP0				; 3 

	STX	GRP1				; 3 

*		+13
*	sleep	49
						; (65)
	LDA	#$80				; 2 (67)
	STA 	HMP0				; 3 (70)
	STA 	HMP1				; 3 (73)

pic64px_OddFrame_Line2
	STA 	WSYNC
	STA	HMOVE				; 3 

	LDA	pic64px_01,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_03,y			; 4 
	STA	GRP1				; 3 

	DEY
	LAX	pic64px_06,y			; 4
	INY

	sleep	12

	LDA	pic64px_05,y			; 4 
	STA	GRP0				; 3 

	LDA	pic64px_07,y			; 4 
	STA	GRP1				; 3 


***	sleep	48
						; (56, but 52?!)
	LDA	#$00				; 2 (58)
	STA 	HMP0				; 3 (61)
	STA 	HMP1				; 3 (64)
	DEY					; 2 (66)
	CPY	temp02				; 3 (69)
	BEQ	pic64px_Reset			; 2 (71)	
	JMP	pic64px_OddFrame_Line1		; 3 (74)

pic64px_EvenFrame
	_sleep	30
	sleep	5

	LDA	#0
	STA	GRP0
	STA	GRP1

	LDA	pic64px_PFColor,y		
	STA	COLUPF				

	LAX	pic64px_07,y
	TXS
	LAX	pic64px_05,y

	LDA	#$80				
	STA 	HMP0				
	LDA	#$A0				
	STA 	HMP1	

pic64px_EvenFrame_Line1			
	STA 	WSYNC				; 76
	STA	HMOVE				; 3

	LDA	pic64px_BGColor,y		; 4 (7)
	STA	COLUBK				; 3 (10)	
	LDA	pic64px_PF,y			; 4 (14)
	STA	PF2				; 3 (17)
	sleep	5
		
	LDA	pic64px_Color,y			; 4 
	STA	COLUP0				; 3 
	STA	COLUP1				; 3 (34 - 31)

	LDA	pic64px_01,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_03,y			; 4 

	STA	GRP1				; 3 
	STX	GRP0				; 3 
	TSX					; 2
	STX	GRP1				; 3

	sleep	8

***	+13 (59)
***	sleep	46
						; (66)
	LDA	#$00				; 2 (68)
	STA 	HMP0				; 3 (71)
	STA 	HMP1				; 3 (74)
pic64px_EvenFrame_Line2
	STA	HMOVE				; 3 

	LDA	pic64px_00,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_02,y			; 4 
	STA	GRP1				; 3 
	
	DEY
	LAX	pic64px_07,y	
	TXS
	LAX	pic64px_05,y
	INY


	LDA	#$80				; 2 
	STA 	HMP0				; 3 
	STA 	HMP1				; 3 

	sleep	6
	
	LDA	pic64px_04,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_06,y			; 4 
	STA	GRP1				; 3 

	DEY
	LDA	pic64px_PFColor,y		
	STA	COLUPF


***	sleep	55				; (58)

***	DEY					; 2 (68)
	CPY	temp02				; 3 (71)
	BNE	pic64px_EvenFrame_Line1		; 2 (73)

pic64px_Reset
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF
	LDA	#0		
	STA	PF0
	STA	PF1		
	STA	PF2		
	STA	GRP0		
	STA	GRP1		
	STA	VDELP0		
	STA	VDELP1	
		

	JMP	TestEnded

pic64px_Data_Section

	align	256

pic64px_00
	BYTE %00000000
	BYTE %00000000
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110
	BYTE %00001110 
	BYTE %00001110
	BYTE %00001111
	BYTE %00011111
	BYTE %00011111
	BYTE %00111111
	BYTE %11111111
	BYTE %11111110
	BYTE %11111110
	BYTE %11111110
	BYTE %11111110 
	BYTE %11111110
	BYTE %11111110
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000


pic64px_01
	BYTE %00000000
	BYTE %00000000
	BYTE %00000111
	BYTE %00001111
	BYTE %00011111
	BYTE %00011110
	BYTE %00011110
	BYTE %00011110
	BYTE %00011111
	BYTE %00001111
	BYTE %00001111
	BYTE %00000111
	BYTE %00000001
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_02
	BYTE %00000000
	BYTE %00000000
	BYTE %11111000
	BYTE %11111100
	BYTE %00111110
	BYTE %00011110
	BYTE %00011110
	BYTE %00011110
	BYTE %00111110
	BYTE %11111100
	BYTE %11111100
	BYTE %11111000
	BYTE %11100000
	BYTE %11100000
	BYTE %11100000
	BYTE %11100000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_03
	BYTE %00000000
	BYTE %00000000
	BYTE %11110000
	BYTE %11110000
	BYTE %11110000
	BYTE %11110001
	BYTE %11110001
	BYTE %11110001
	BYTE %11110001
	BYTE %11111001
	BYTE %01111101
	BYTE %00111101
	BYTE %00011101
	BYTE %00000001
	BYTE %00000001
	BYTE %00000001
	BYTE %00000001
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_04
	BYTE %00000000
	BYTE %00000000
	BYTE %00111000
	BYTE %11111001
	BYTE %11110011
	BYTE %11100011
	BYTE %11100011
	BYTE %11100011
	BYTE %11100011
	BYTE %11100011
	BYTE %11111001
	BYTE %11111000
	BYTE %11111000
	BYTE %11100000
	BYTE %11100000
	BYTE %11100000
	BYTE %11100000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_05
	BYTE %00000000
	BYTE %00000000
	BYTE %11111101
	BYTE %11111111
	BYTE %11000111
	BYTE %10000011
	BYTE %10000011
	BYTE %10000011
	BYTE %11000111
	BYTE %11111111
	BYTE %11111111
	BYTE %11111110
	BYTE %01111100
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
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_06
	BYTE %00000000
	BYTE %00000000
	BYTE %11011110
	BYTE %11011110
	BYTE %11011110
	BYTE %11011110
	BYTE %11011110
	BYTE %11011110
	BYTE %10011110
	BYTE %10011111
	BYTE %00001111
	BYTE %00000111
	BYTE %00000011
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
	BYTE %11111111
	BYTE %11111111
	BYTE %11111111
	BYTE %00000000

pic64px_07
	BYTE %00000000
	BYTE %00000000
	BYTE %01111111
	BYTE %01111111
	BYTE %01111111
	BYTE %01111111
	BYTE %00111111
	BYTE %00001111
	BYTE %00000111
	BYTE %00000111
	BYTE %10000111
	BYTE %10000111
	BYTE %10000111
	BYTE %00000000
	BYTE %00000000
	BYTE %00000111
	BYTE %00000111
	BYTE %00000111
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %00000000
	BYTE %11110000
	BYTE %11111000
	BYTE %11110000
	BYTE %00000000 	; 224


pic64px_Color
	BYTE #$00
	BYTE #$02
	BYTE #$04
	BYTE #$06
	BYTE #$08
	BYTE #$0a
	BYTE #$0c
	BYTE #$0e
	BYTE #$0c
	BYTE #$0a
	BYTE #$08
	BYTE #$06
	BYTE #$08
	BYTE #$0a
	BYTE #$0a
	BYTE #$08
	BYTE #$06
	BYTE #$08
	BYTE #$0a
	BYTE #$0c
	BYTE #$0e
	BYTE #$0c
	BYTE #$0a
	BYTE #$08
	BYTE #$06
	BYTE #$04
	BYTE #$02
	BYTE #$00	; 252

	align	256

pic64px_PF
	BYTE %10000110
	BYTE %10001110
	BYTE %10011110
	BYTE %10011100
	BYTE %10011000
	BYTE %10011000
	BYTE %10011000
	BYTE %10011000
	BYTE %10011000
	BYTE %10011000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10110000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000
	BYTE %10100000


pic64px_PFColor
	BYTE #$40
	BYTE #$42
	BYTE #$44
	BYTE #$46
	BYTE #$48
	BYTE #$46
	BYTE #$48
	BYTE #$4a
	BYTE #$48
	BYTE #$4a
	BYTE #$48
	BYTE #$4a
	BYTE #$4c
	BYTE #$4a
	BYTE #$4a
	BYTE #$4c
	BYTE #$4a
	BYTE #$48
	BYTE #$4a
	BYTE #$48
	BYTE #$4a
	BYTE #$48
	BYTE #$46
	BYTE #$48
	BYTE #$46
	BYTE #$44
	BYTE #$42
	BYTE #$40

pic64px_BGColor
	BYTE #$1e
	BYTE #$1c
	BYTE #$1a
	BYTE #$18
	BYTE #$16
	BYTE #$14
	BYTE #$12
	BYTE #$10
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$00
	BYTE #$10
	BYTE #$12
	BYTE #$14
	BYTE #$16
	BYTE #$18
	BYTE #$1a
	BYTE #$1c
	BYTE #$1e

TestEnded

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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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




###End-Bank2
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

	saveFreeBytes
	rewind 	2fd4
	
start_bank2
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank3

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank3



JumpToNewScreenBank3
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank3




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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank3
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank3

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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



###End-Bank3
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*




	saveFreeBytes
	rewind 	3fd4

start_bank3
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank4

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank4



JumpToNewScreenBank4
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank4




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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank4
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank4

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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



###End-Bank4
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

	saveFreeBytes
	rewind 	4fd4
	
start_bank4
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank5

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank5



JumpToNewScreenBank5
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank5




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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank5
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank5

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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



###End-Bank5
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

	saveFreeBytes
	rewind 	5fd4
	
start_bank5
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank6

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank6



JumpToNewScreenBank6
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank6




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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank6
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank6

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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



###End-Bank6
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

	saveFreeBytes
	rewind 	6fd4
	
start_bank6
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank7

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank7



JumpToNewScreenBank7
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T


*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank7




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

	lda	#>(CalculateDuringVBLANK-1)
   	pha
   	lda	#<(CalculateDuringVBLANK-1)
   	pha
   	pha
   	pha
   	ldx	#8
   	jmp	bankSwitchJump

VBlankEndBank7
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank7

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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




###End-Bank7
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

	saveFreeBytes
	rewind 	7fd4
	
start_bank7
	ldx	#$ff
   	txs
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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


		
	JMP	WaitUntilOverScanTimerEndsBank8

*Leave Bank
*-------------------------------
*
* This section goes as you leave
* the screen. Should set where to
* go and close or save things.
*

LeaveScreenBank8



JumpToNewScreenBank8
	LAX	temp02		; Contains the bank to jump
	
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
 	LDA	#NTSC_Vblank
	STA	TIM64T

*VBLANK
*-----------------------------
* This is were you can set a piece
* of code as well, but some part may
* be used by the kernel.
*
VBLANKBank8




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

   	jmp	CalculateDuringVBLANK

VBlankEndBank8
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank8

    	LDA	#229
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*

	tsx
	stx	item



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

	lda	#>(EnterKernel-1)
   	pha
   	lda	#<(EnterKernel-1)
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



	LDA	frameColor
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




###End-Bank8
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*




	align 256

*Calculations during VBLANK
*----------------------------
*

CalculateDuringVBLANK

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
	BVC	CheckIfOutOfBorders	; Go to the SubMenu Kernel
	JMP	SubMenuVBLANK	


*CheckIfOutOfBorders
*--------------------------------------------
* This section will decide what should happen
* to the objects as they are touching the borders
* of the screen.

CheckIfOutOfBorders
	
	LDA	pfEdges
	AND	#%11000000
	STA	temp07
	CMP	#%00000000
	BEQ	CalculateIndexes	

	TSX
	STX	temp03	
	LDX	#4	; p0, p1, m0, m1, bl


NextItemThings
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
 	LDA	XTable,x

	TAX
	STA	temp04
	LDA	P0Settings,x
	AND	#%00000111
	TAX	
	LDA	XHorBorderAddSprite,x
	TSX
	CPX	#2
	BCC	NotAMissile
ItsAMissile	
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
	LDA	XHorBorderAddMissile,x
	CLC
	ADC	temp05

NotAMissile
	STA	temp05
	LDA	#160	
	SEC	
	SBC	temp05
	STA	temp01

VerticalFun
	LDX	temp04
	LDA	P0Height,x
	TSX
	CPX	#2
	BCS	ItsAMissile2
	LDA	temp04
	JMP 	NotAMissile2
ItsAMissile2
	LDA	#0
NotAMissile2
	STA	temp05
	LDA	#40
	SEC
	SBC	temp05
	STA	temp02

VerticalFun2
	LDX	temp04
	LDA	P0Height,x
	TSX
	CPX	#2
	BCS	ItsAMissile3
	CLC	
	ADC	#2
	ADC	temp04

	JMP	NotAMissile3
ItsAMissile3
	LDA	#2
NotAMissile3
	STA	temp06

	TSX
	LDA	temp07
	CMP	#%11000000
	BEQ	AppearOpposite

	LDA	temp07
	BMI	NoBLAHBLAH
	CPX	#2
	BCS	AppearOpposite

NoBLAHBLAH
	LDA	P0X,x
	CMP	#16
	BCS	NotSmallerThan
	LDA	#16
	STA	P0X,x	
	JMP	doYForNow
NotSmallerThan
	LDA	temp01
	CMP 	P0X,x
	BCS	doYForNow
	STA	P0X,x
doYForNow
	LDA	P0Y,x
	CMP	temp06
	BCS	NotLowerThan
	LDA	temp06
	STA	P0Y,x
NotLowerThan
	LDA	temp02
	CMP	P0Y,x
	BCS	PrepareForNext
	LDA	temp02
	STA	P0Y,x
PrepareForNext
	DEX	
	CPX	#255
	BNE	NextItemThings
	JMP	StackBackUp

AppearOpposite
	LDA	P0X,x
	CMP	#16
	BCS	NotSmallerThan2
	LDA	temp01
	SEC
	SBC	#1
	STA	P0X,x	
	JMP	doYForNow2
NotSmallerThan2
	LDA	temp01
	CMP 	P0X,x
	BCS	doYForNow2
	LDA	#17
	STA	P0X,x
doYForNow2
	LDA	P0Y,x
	CMP	temp06
	BCS	NotLowerThan2
	LDA	temp02
	SEC
	SBC	#1
	STA	P0Y,x
NotLowerThan2
	LDA	temp02
	CMP	P0Y,x
	BCS	PrepareForNext2
	LDA	temp06
	CLC
	ADC	#1
	STA	P0Y,x
PrepareForNext2
	DEX	
	CPX	#255
	BNE	NextItemThings

StackBackUp
	LDX	temp03
	TXS

CalculateIndexes
	LDA 	P0Height
	CLC
	ADC	#1
	STA	temp01	

	LDA	P0SpriteIndex	
	AND	#%00001111	; Get low nibble for P0 index
	TAY			; Move it to Y for calculations
	LDA	P0SpritePointer
	
CalculateP0PointerIndex
	; You can only have the maximum number of sprites 256/height that is always smaller than 16
	; (over 16 px height, you cannot use all 16 indexes because of the paging overflow that would break timing.

	CPY	#0
	BEQ	CalculateP0PointerIndexDone
	CLC	
	ADC	temp01
	DEY
	JMP	CalculateP0PointerIndex


CalculateP0PointerIndexDone
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
	
CalculateP1PointerIndex
	; You can only have the maximum number of sprites 256/height that is always smaller than 16
	; (over 16 px height, you cannot use all 16 indexes because of the paging overflow that would break timing.

	CPY	#0
	BEQ	CalculateP1PointerIndexDone
	CLC	
	ADC	temp01
	DEY
	JMP	CalculateP1PointerIndex


CalculateP1PointerIndexDone
	STA	temp10		; temp10 will store the sprite pointers low byte

JumpBackToBankScreenTop

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
		
		
	lda	VBlankJumpTable,y
   	pha
   	lda	VBlankJumpTable+1,y
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump



VBlankJumpTable
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

XTable
	byte	#0
	byte	#1
	byte	#0
	byte	#1
	byte	#2

XHorBorderAddSprite
	byte	#8
	byte	#24
	byte	#40
	byte	#40
	byte	#72
	byte	#16
	byte	#72
	byte	#32
	

XHorBorderAddMissile
	byte	#1
	byte	#2
	byte	#4
	byte	#8


SubMenuVBLANK	
	LDA	SubMenuLines
	AND	#%00000011
	CLC
	ADc	#1
	TAY
	LDA	#0
	STA	temp02
Add6ToThat
	CPY	#0
	BEQ	NoMore6
	CLC
	ADC	#6
	DEY
	JMP 	Add6ToThat
NoMore6
	STA	temp02
	
	LDA	TileSelected
	AND	#%00011111
	CMP	temp02
	BCC	NoLargerThan24
	LDA	TileSelected
	AND	#%11100000
	STA	TileSelected
NoLargerThan24

SubMenuVBLANKEnd
	JMP	JumpBackToBankScreenTop
	
	align 256
	
Start
   	sei
   	cld
   	ldy	#0
   	lda	$D0
   	cmp	#$2C		;check RAM location #1   	bne	MachineIs2600
   	lda	$D1
   	cmp	#$A9		;check RAM location #2   	bne	MachineIs2600
   	dey
MachineIs2600
	ldx	#0
  	txa
clearmem
   	inx
   	txs
   	pha
	cpx	#$00
   	bne	clearmem	; Clear the RAM.

	LDA	$F080		; Sets two values for the SC RAM 
	STA	$80		; to Random and Counter variables
	LDA	$F081
	STA	$81

	LDY	#0		
	TYA
	STA	$F029
ClearSCRAM
	STA 	$F000,Y
	INY
	BPL 	ClearSCRAM

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
   	lda	#>(Start-1)
   	pha
   	lda	#<(Start-1)
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
   	.byte 	#<Start
  	.byte 	#>Start
   	.byte 	#<Start
  	.byte 	#>Start