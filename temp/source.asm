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

item = $8f
frameColor = $90
			
*** Playfield Elements
pf0Pointer = $91		; 16 bits
pf1Pointer = $93		; 16 bits
pf2Pointer = $95		; 16 bits	
pfColorPointer = $97		; 16 bits 
bkColorPointer = $99		; 16 bits
bkBaseColor = $9b
pfBaseColor = $9c
pfIndex = $9d

************************
pfLines = $9e		; use only the low two bits  of $98 ???
NoGameMode = $9e	; if 7th bit set, don't draw the game section
bankToJump = $9e	;	; use only bites 2-4 of $98
			; 5-6 : FREE
************************

*** Player Settings
P0SpritePointer = $9f		; 16bit
P0ColorPointer = $a1		; 16bit
P1SpritePointer = $a3		; 16bit
P1ColorPointer = $a5		; 16bit

************
* Settings *
****************************************	
P0Settings = $a7			; Bits 0-2 are sprite settings, 
P0Mirrored = $a7			; 3 is reflection, bits 4-5 are missile settings. 
P0TurnOff  = $a7			; 6: Turn Off Sprite
P1Settings = $a8			; 7: Turn off Missile
P1Mirrored = $a8			; Must be in order!
P1TurnOff  = $a8
****************************************
pfSettings = $a9	; Since CTRLPF 0-1 bits are fixed in the screen loop
pfEdges	= $a9		; 0-1: free
BallTurnOff = $a9	; 2: Players move behind the pf
#Has to be here because	; 3: Turn off Ball
#of the edge check	; 4-5: Ball Settings
#routine.		; 6-7: 00 - Nothing 01 - Mixed 10 - All stop 11 - All go through 
************************

P0Height = $aa
P1Height = $ab

****************************************
P0SpriteIndex = $ac			; low nibble is P0 sprite index
P1SpriteIndex = $ac			; high nibble is P1 sprite index
****************************************

*** Positions (Must be aligned!!)
P0Y = $ad	
P1Y = $ae	
M0Y = $af
M1Y = $b0
BLY = $b1

P0X = $b2
P1X = $b3
M0X = $b4
M1X = $b5
BLX = $b6

*** Fake Missile Colors
M0Color = $b7
M1Color = $b8


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
	STA 	ENAM0	;3 (14)
	STA 	ENAM1	;3 (17)
	STA 	ENABL	;3 (20) Disables missiles and ball  
	STA	GRP0	;3 (23)
	STA	GRP1	;2 (25) Sets player sprites to blank 
 	STA	VDELP0	;3 (28)
	STA	VDELP1  ;3 (31)
	STA	VDELBL	;3 (34)
	
	STA	PF1	;3 (37)
	STA	PF2	;3 (40)
	STA	PF0	;3 (43)
	STA	temp03 	;3 (46) Erase P1 sprite data
	


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
	LDA	#14		; 2 (36)
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

	LDY	#200		; 2 (9)
	LDA	P0TurnOff	; 3 (12)
	BVC	NoP0TurnOff	; 2 (14)
	STY	P0Y		; 3 (17)
NoP0TurnOff
	BPL	NoM0TurnOff	; 2 (19)
	STY	M0Y		; 3 (22)
NoM0TurnOff
	
	LDA	P1TurnOff	; 3 (25)
	BVC	NoP1TurnOff	; 2 (27)
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

	STA	WSYNC
	
	sleep	9
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


	sleep	9

	LDA	(pf2Pointer),y	; 5(45)
	STA	PF2		; 3(50)

	LDA	(pf1Pointer),y	; 5(55)
	STA	PF1		; 3(58)

	sleep	12
	
	LDA	temp02			; 3(73)	
	JMP	StartWithoutWSYNC	; 3(76)

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

FirstLine
	STA	WSYNC		; 3 (76)
StartWithoutWSYNC
	STA	COLUPF		; 3 (3)
	LDA	temp04		; 3 (6)
	STA	COLUBK		; 3 (9)


	LDA	temp05		; 3 (12)
	STA	PF0		; 3 (15)


	LDA 	P0Height 	; 3 (18)
	DCP	temp09 		;  temp09 contains P0Y!  ; 5 (23)
	BCC	NoP0DrawNow	; 2 (25)
	LDY	temp09		; 3 (28)
	LDA	(P0ColorPointer),y 	; 5 (33)
	STA	COLUP0		; 3 (36)
	LDA	(temp07),y 	; 5 (41)
saveP0Sprite
	TAY			;2 (43)
	; 28

	LDA	temp06		; 3 (46)	
	STA	PF0		; 3 (49)


	STX	temp13		; 3 (52) Saves the lineNum
	ldx 	#$1f		; Address of ENABL 2 (51) 
	txs			; 2 (53) 
	LDX	temp13		; 3 (55) Retrive the lineNum
	sleep	2
	

	LDA	temp03		; 3 (67)
	STY	GRP0		; 2 (70)
	STA	GRP1		; 3 (73)
MiddleLine

	LDY	temp01		; 3 (76)

	LDA	(pf0Pointer),y	; 5 (5)
	STA	PF0		; 3 (8)
	STA	temp05		; 3 (11)

	LDA	(pf1Pointer),y	; 5 (16)
	STA 	PF1		; 3 (19)

	LDA	(pf2Pointer),y	; 5 (24)
	STA 	PF2		; 3 (27)
	LDA	temp05		; 3 (30)
	asl			; 2 (32)
	asl			; 2 (34)
	asl			; 2 (36)
	asl			; 2 (38)
	STA	PF0		; 3 (41)
	STA	temp06		; 3 (44)

	DEY			; 2
	cpx	BLY		; 3
	php			; 3
	cpx	M1Y		; 3
	php			; 3
	cpx	M0Y		; 3
	php			; 3 (12)

	LDA	(pfColorPointer),y	; 6 (73)
	ADC	pfBaseColor
LastLine
	STA	temp02		; 3 (-3)
	LDA	temp05		; 3 (3)
	STA	PF0		; 3 (6)

	LDA	(bkColorPointer),y ;5 (11)
	CLC	 		; 2 (13)
	ADC	bkBaseColor	; 3 (16)	
	STA	temp04		; 3 (19)
	

	LDA 	P1Height 	; 3 (21)
	DCP	temp12 		;  temp12 contains P0Y!  ; 5 (26)
	BCC	NoP1DrawNow	; 2 (28)
	LDY	temp12		; 3 (31)
	LDA	(P1ColorPointer),y 	; 5 (36)
	STA	COLUP1	; 3 (39)
	LDA	(temp10),y 	; 5 (44)
saveP1Sprite
	STA	temp03		; 3 (47) ;
	; 29

	LDA	temp06		; 3 (53)
	STA	PF0		; 3 (56)


	CPX	#0		; 2 (58)
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
	LDA	#165	
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
	LDA	#1
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



FineAdjustTable256
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

	fill 	209

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

Zero
Null
None
	.BYTE	#0	; This is an empty byte for constant code usage.



	align 256

Data_Section
TestPlayfield_00
	byte	#%01010000
	byte	#%10100100
	byte	#%01000010
	byte	#%00001100
	byte	#%00000011
	byte	#%11111111
	byte	#%00000011
	byte	#%00001100
	byte	#%00000000
	byte	#%10000011
	byte	#%01111100
	byte	#%00000000
	byte	#%11000000
	byte	#%00110000
	byte	#%00000000
	byte	#%10011001
	byte	#%10011001
	byte	#%10011001
	byte	#%11011101
	byte	#%11111111
	byte	#%11110111
	byte	#%10010011
	byte	#%11110011
	byte	#%10010111
	byte	#%11111110
	byte	#%11111110
	byte	#%11111010
	byte	#%01100010
	byte	#%01100010
	byte	#%01100010
	byte	#%01100010
	byte	#%11110010
	byte	#%11110111
	byte	#%01100010
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000

TestPlayfield_01
	byte	#%00001000
	byte	#%01010001
	byte	#%10100001
	byte	#%00000000
	byte	#%00000000
	byte	#%11110000
	byte	#%00001000
	byte	#%00000100
	byte	#%11111110
	byte	#%00000001
	byte	#%00000000
	byte	#%11111111
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11111111
	byte	#%11010110
	byte	#%11010110
	byte	#%11010111
	byte	#%11010110
	byte	#%11010110
	byte	#%11111111
	byte	#%11010110
	byte	#%11010110
	byte	#%11101111
	byte	#%11111111
	byte	#%11111101
	byte	#%11111011
	byte	#%11001111
	byte	#%11001110
	byte	#%11111100
	byte	#%11111000
	byte	#%11111000
	byte	#%11111000
	byte	#%01110000
	byte	#%01010000
	byte	#%01110000
	byte	#%01010000
	byte	#%11111000
	byte	#%11111000
	byte	#%10101000
	byte	#%00000000

TestPlayfield_02
	byte	#%00000000
	byte	#%11111111
	byte	#%00111101
	byte	#%10111101
	byte	#%00111110
	byte	#%10011100
	byte	#%01101100
	byte	#%00101100
	byte	#%00001100
	byte	#%00111100
	byte	#%11111001
	byte	#%11100011
	byte	#%00000100
	byte	#%11111110
	byte	#%10101010
	byte	#%10101011
	byte	#%10101011
	byte	#%11111011
	byte	#%10101011
	byte	#%10101011
	byte	#%11111011
	byte	#%10101011
	byte	#%10110111
	byte	#%10101111
	byte	#%11011111
	byte	#%10111101
	byte	#%11111011
	byte	#%11101111
	byte	#%10011111
	byte	#%10111100
	byte	#%11111000
	byte	#%11110000
	byte	#%00010000
	byte	#%11110000
	byte	#%00010000
	byte	#%11111000
	byte	#%01111100
	byte	#%01001100
	byte	#%11011000
	byte	#%01110000
	byte	#%11111000
	byte	#%10101000

TestPlayfield_FG
	byte	#$1E
	byte	#$1C
	byte	#$18
	byte	#$1A
	byte	#$1C
	byte	#$1E
	byte	#$1C
	byte	#$1A
	byte	#$18
	byte	#$1A
	byte	#$18
	byte	#$14
	byte	#$08
	byte	#$06
	byte	#$04
	byte	#$06
	byte	#$04
	byte	#$06
	byte	#$08
	byte	#$0A
	byte	#$0C
	byte	#$0C
	byte	#$0A
	byte	#$08
	byte	#$06
	byte	#$04
	byte	#$06
	byte	#$08
	byte	#$06
	byte	#$08
	byte	#$08
	byte	#$06
	byte	#$04
	byte	#$06
	byte	#$08
	byte	#$06
	byte	#$04
	byte	#$02
	byte	#$06
	byte	#$08
	byte	#$06
	byte	#$04

TestPlayfield_BG
	byte	#$C4
	byte	#$C2
	byte	#$C4
	byte	#$C2
	byte	#$C0
	byte	#$C2
	byte	#$C4
	byte	#$C6
	byte	#$C4
	byte	#$C6
	byte	#$C4
	byte	#$C2
	byte	#$B2
	byte	#$B2
	byte	#$B0
	byte	#$06
	byte	#$04
	byte	#$02
	byte	#$04
	byte	#$62
	byte	#$64
	byte	#$66
	byte	#$64
	byte	#$62
	byte	#$04
	byte	#$02
	byte	#$04
	byte	#$06
	byte	#$04
	byte	#$06
	byte	#$64
	byte	#$62
	byte	#$60
	byte	#$62
	byte	#$64
	byte	#$62
	byte	#$60
	byte	#$04
	byte	#$02
	byte	#$04
	byte	#$02
	byte	#$00



TestSprite_Sprite
	byte	#%01100000	; (0)
	byte	#%00010000
	byte	#%00011000
	byte	#%00011000
	byte	#%00011000
	byte	#%00111100
	byte	#%01111110
	byte	#%11011011
	byte	#%11010101
	byte	#%10111110
	byte	#%00101010
	byte	#%00011100
	byte	#%00110000	; (1)
	byte	#%01100000
	byte	#%00110000
	byte	#%00011000
	byte	#%00011000
	byte	#%00001100
	byte	#%00011100
	byte	#%00110110
	byte	#%01110110
	byte	#%11101011
	byte	#%11011101
	byte	#%10000001
	byte	#%00000000	; (2)
	byte	#%00111100
	byte	#%01110010
	byte	#%01110000
	byte	#%00111000
	byte	#%00110100
	byte	#%00110110
	byte	#%11110111
	byte	#%11111111
	byte	#%11101011
	byte	#%10101011
	byte	#%00011100
	byte	#%01111000	; (3)
	byte	#%00111010
	byte	#%01011011
	byte	#%11011101
	byte	#%11011101
	byte	#%10011101
	byte	#%11111111
	byte	#%11100011
	byte	#%01111111
	byte	#%00101010
	byte	#%00111110
	byte	#%00011100

TestSprite_SpriteColor
	byte	#$0A
	byte	#$0C
	byte	#$0E
	byte	#$0E
	byte	#$0E
	byte	#$0C
	byte	#$0A
	byte	#$0C
	byte	#$0E
	byte	#$0E
	byte	#$0C
	byte	#$0A

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

	LDA	#0
	sta 	frameColor
	STA	P0SpriteIndex ; 	Sets both indexes to 0;
	STA	pfBaseColor
	STA	bkBaseColor

	LDA	#26
	STA	pfIndex

	LDA	#<TestPlayfield_00
	STA 	pf0Pointer 
	LDA	#>TestPlayfield_00
	STA 	pf0Pointer+1

	LDA	#<TestPlayfield_01
	STA 	pf1Pointer 
	LDA	#>TestPlayfield_01
	STA 	pf1Pointer+1

	LDA	#<TestPlayfield_02
	STA 	pf2Pointer 
	LDA	#>TestPlayfield_02
	STA 	pf2Pointer+1

	LDA	#<TestPlayfield_FG
	STA 	pfColorPointer 
	LDA	#>TestPlayfield_FG
	STA 	pfColorPointer+1

	LDA	#<TestPlayfield_BG
	STA	bkColorPointer 
	LDA	#>TestPlayfield_BG
	STA	bkColorPointer+1

	LDA	#<TestSprite_Sprite
	STA	P0SpritePointer
	LDA	#>TestSprite_Sprite
	STA	P0SpritePointer+1

	LDA	#<TestSprite_SpriteColor
	STA	P0ColorPointer
	LDA	#>TestSprite_SpriteColor
	STA	P0ColorPointer+1

	LDA	#<Zero
	STA	P1SpritePointer
	LDA	#>Zero
	STA	P1SpritePointer+1

	LDA	#1
	STA	P1Height

	LDA	#200
	STA	P1Y	
	STA	M0Y
	STA	M1Y
	STA	BLY

	LDA	#82
	STA	P0X
	STA	P1X
	STA	M0X
	STA	M1X
	STA	BLX

	LDA	#20
	STA	P0Y

	LDA	#11
	STA	P0Height

	LDA	#0
	STA	P0SpriteIndex ; 	Sets both indexes to 0;

	LDA	pfEdges		; Sprites stop, bullets go through
	AND	#%00111111
	STA	temp01
	LDA	#%01000000
	ORA	temp01
	STA	pfEdges

	LDA	P0TurnOff
	AND	#%00111111
	ORA	#%10000000
	STA	P0TurnOff	; Turn M0

	LDA	P1TurnOff
	AND	#%00111111
	ORA	#%11000000
	STA	P1TurnOff	; Turn Off P1 and M1

	LDA	BallTurnOff
	ORA	#%00001000
	STA	BallTurnOff	; Turn off Ball

MissileDir = $b9
NUSIZ = $ba
Sound = $bb


	LDA	#0
	STA	NUSIZ
	STA	Sound
	STA	MissileDir


maxFrames=3

		
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

	LDA	#$08
	BIT 	SWCHB
	BNE	ChangeColor

	LDA	#$20
	BIT	SWCHA
	BNE	NoScrollDown
	DEC	pfIndex
	JMP	DebugIndex
NoScrollDown
	LDA	#$10
	BIT	SWCHA
	BNE	ChangeColor
	INC	pfIndex
DebugIndex
	LDA	#26
	CMP	#255
	BEQ	ChangeColor
	CMP	pfIndex
	BCS	SmallerThan
	LDA	#26
	STA	pfIndex
SmallerThan
	LDA	pfIndex
	CMP	#26
	BCS	ChangeColor
	LDA	#26
	STA	pfIndex

ChangeColor
	LDA	#$01
	BIT	SWCHB
	BNE	NoOneUp
	INC	pfBaseColor
NoOneUp
	LDA	#$02
	BIT	SWCHB
	BNE 	AllDone
	INC	bkBaseColor
AllDone
	LDA	#$08
	BIT 	SWCHB
	BEQ 	MissileDone
GoWithSprite

	bit 	SWCHA
	BVS	NoLeftMove
	DEC	P0X
	LDA	P0Mirrored 
	ORA	#%00001000
	STA	P0Mirrored

	JMP	VerticalMovementCheck
NoLeftMove
	BMI 	VerticalMovementCheck
	INC	P0X
	LDA	P0Mirrored 
	AND	#%11110111
	STA	P0Mirrored	

VerticalMovementCheck	
	LDA	#$10
	bit 	SWCHA
	BNE	NoDownMove
	DEC	P0Y
	JMP	SpriteEnded
NoDownMove
	LDA	#$20
	bit 	SWCHA
	BNE	SpriteEnded
	INC	P0Y
SpriteEnded

	LDA	counter
	STA	M0Color
	AND	#%00000111
	CMP	#%00000111
	BNE	NoINC

	LDA	P0SpriteIndex
	AND	#%00001111
	TAY
	STA	temp01
	CMP	#maxFrames
	BCC	NoSetZero
SetZero
	LDA	P0SpriteIndex
	AND	#%11110000
	JMP	SaveSpriteIndex
NoSetZero
	LDA	Sound
	CMP	#0
	BNE 	GoForSure

	LDA	SWCHA
	AND	#%11110000
	CMP	#%11110000
	BEQ	SetZero
GoForSure
	LDA	temp01
	CLC
	ADC	#1
	STA	temp01
	LDA	P0SpriteIndex	
	AND	#%11110000
	ORA	temp01
SaveSpriteIndex
	STA	P0SpriteIndex
NoINC	
	
	LDA	Sound
	CMP	#0
	BNE	PlaySoundMoveMis

	bit	INPT4	
	BMI	RemoveMissile

	LDA	P0TurnOff
	AND	#%01111111	
	STA	P0TurnOff

	LDA	#12
	STA	Sound
	LDA	P0Mirrored
	AND	#%00001000
	STA	MissileDir
	CMP	#0
	BEQ 	ItsMirrored
	LDA	P0X
	CLC
	ADC	#3
	JMP	M0XDone
ItsMirrored
	LDA	P0X
	CLC
	ADC	#5
	LDY	NUSIZ
	CPY	#5
	BNE	Not5
	ADC	#9
	JMP	M0XDone
Not5	
	CPY	#7
	BNE	M0XDone
	ADC	#24

M0XDone
	STA	M0X

	LDA	P0Height
	LSR
	STA	temp02

	LDA	#42
	SEC
	SBC	P0Y
	CLC
	ADC	P0Height
	SEC
	SBC	temp02
	STA	M0Y

PlaySoundMoveMis
	LDA	MissileDir
	AND	#%00001000
	CMP	#0
	BNE 	MissileLeft
	INC	M0X
	INC	M0X
	JMP 	ToSound
MissileLeft	
	DEC	M0X
	DEC	M0X

ToSound
	LDA	Sound
	STA	AUDV0
	LDA	#8
	STA	AUDC0	
	SEC
	SBC	Sound
	STA	AUDF0
	DEC	Sound
	JMP	MissileDone
RemoveMissile
	LDA	P0TurnOff
	ORA	#%10000000	
	STA	P0TurnOff
	LDA	#0
	STA	AUDV0
MissileDone
	LDA	pfSettings
	BIT	SWCHB
	BVC	MoveBehind
	ORA	#%00000100
	JMP	MoveBefore
MoveBehind
	AND	#%11111011	
MoveBefore	
	STA	pfSettings	; Changes behaiour on P0 diff switch.	

	
	LDA	counter
	AND	#%011111111
	CMP	#%011111111
	BNE	NoNUSIZChange
	BIT	SWCHB
	BPL	NoNUSIZChange
	INC 	NUSIZ
	LDA	#7
	CMP	NUSIZ
	BCS	NoZeroNusiz
	LDA	#0
	STA	NUSIZ
NoZeroNusiz
	LDA	P0Settings
	AND	#%11001000
	ORA	NUSIZ
	STA	P0Settings

	LDA	NUSIZ
	CMP	#5
	BNE	Not5Again
	LDA	P0Settings
	AND	#%11001111
	ORA	#%00010000	
	JMP	SSSSAVE
Not5Again
	CMP	#7
	BNE	NoNUSIZChange
	LDA	P0Settings
	AND	#%11001111
	ORA	#%00110000
SSSSAVE	
	STA	P0Settings
NoNUSIZChange


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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank2
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank2

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank2

###End-Bank2
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank3
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank3

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank3

###End-Bank3
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*




*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank4
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank4

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank4

###End-Bank4
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank5
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank5

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank5

###End-Bank5
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	
*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank6
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank6

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank6

###End-Bank6
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank7
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank7

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank7

###End-Bank7
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*


	
*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
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

	BIT	pfLines 		; NoGameMode
	BMI	VBlankEndBank8		; if 7th bit set (for a title or game over screen), the calculation part is skipped.		

*Costful Calculations in VBLANK
*--------------------------------------------------------
* There are some really costful calculations those would
* require a lot of WSYNCS during the draw section, to avoid
* that, we do them in VBLANK.
*

	LDA	#8
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
   	ldx	#1
   	jmp	bankSwitchJump

VBlankEndBank8
	CLC
	LDA 	INTIM
	BMI 	VBlankEndBank8

    	LDA	#230
    	STA	TIM64T


*ScreenTop
*--------------------------------  
* This is the section for the
* top part of the screen.
*




*SkipIfNoGameSet
*---------------------------------
*

	BIT	pfLines 		; NoGameMode
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



	JMP	OverScanBank8

###End-Bank8
*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*



*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*


	
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