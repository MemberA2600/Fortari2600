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

pfIndex = $9b

************************
pfLines = $9c		; use only the low two bits  of $98 ???
NoGameMode = $9c	; if 7th bit set, don't draw the game section
bankToJump = $9c	;	; use only bites 2-4 of $98
			; 5-6 : FREE
************************

*** Player Settings
P1SpritePointer = $9d		; 16bit
P1ColorPointer = $9f		; 16bit

************
* Settings *
****************************************	
M0Settings = $a0			; Bits 0-2 are sprite settings, 
M0TurnOff  = $a0			; 3 is reflection, bits 4-5 are missile settings. 
					; 6: Turn Off Sprite
P1Settings = $a1			; 7: Turn off Missile
P1Mirrored = $a1			; Must be in order!
P1TurnOff  = $a1
****************************************

P1SpriteIndex = $a0			; Part of M0Settings, using the LO nibble.

************************
pfSettings = $a2	; Since CTRLPF 0-1 bits are fixed in the screen loop
pfEdges	= $a2		; 0-1: free
BallTurnOff = $a2	; 2: Players move behind the pf
#Has to be here because	; 3: Turn off Ball
#of the edge check	; 4-5: Ball Settings
#routine.		; 6-7: 00 - Nothing 01 - Mixed 10 - All stop 11 - All go through 
************************

P1Height = $a3

*** Positions (Must be aligned!!)	
P1Y = $a4	
M0Y = $a5
M1Y = $a6
BLY = $a7

P1X = $a8
M0X = $a9
M1X = $aa
BLX = $ab

*** Fake Missile Colors
M0Color = $ac
M1Color = $ad

*** MultiSprite Kernel Related Stuff
P0_1SpritePointerLO = $ae	 
P0_2SpritePointerLO = $af	
P0_3SpritePointerLO = $b0	
P0_4SpritePointerLO = $b1	

P0_1SpritePointerHI = $b2	 
P0_2SpritePointerHI = $b3	
P0_3SpritePointerHI = $b4	
P0_4SpritePointerHI = $b5	

******************
P0_1Settings = $b6	; 0-3: Sprite settings
P0_2Settings = $b7 	; 4: Reflection
P0_3Settings = $b8 	; 5-6: Free
P0_4Settings = $b9 	; 7: Disabled?
******************
P0_1X = $ba		
P0_2X = $bb		
P0_3X = $bc		
P0_4X = $bd
************
P0_1Y = $be	
P0_2Y = $bf		
P0_3Y = $c0		
P0_4Y = $c1		
****************
P0_1Color = $c2		
P0_2Color = $c3		
P0_3Color = $c4		
P0_4Color = $c5		
****************
P0_1Height = $c6		
P0_2Height = $c7
P0_3Height = $c8
P0_4Height = $c9
****************
P0_1Index = $ca
P0_2Index = $ca		
P0_3Index = $cb		
P0_4Index = $cb

*
* P0 Data Array
*---------------
*

P0_Data01 = $cc
P0_Data02 = $cd
P0_Data03 = $ce
P0_Data04 = $cf
P0_Data05 = $d0
P0_Data06 = $d1
P0_Data07 = $d2
P0_Data08 = $d3
P0_Data09 = $d4
P0_Data10 = $d5
P0_Data11 = $d6
P0_Data12 = $d7
P0_Data13 = $d8
P0_Data14 = $d9
P0_Data15 = $da
P0_Data16 = $db
P0_Data17 = $dc
P0_Data18 = $dd
P0_Data19 = $de
P0_Data20 = $df
P0_Data21 = $e0
P0_Data22 = $e1
P0_Data23 = $e2
P0_Data24 = $e3
P0_Data25 = $e4
P0_Data26 = $e5
P0_Data27 = $e6
P0_Data28 = $e7
P0_Data29 = $e8
P0_Data30 = $e9
P0_Data31 = $ea
P0_Data32 = $eb
P0_Data33 = $ec
P0_Data34 = $ed
P0_Data35 = $ee
P0_Data36 = $ef
P0_Data37 = $f0
P0_Data38 = $f1
P0_Data39 = $f2
P0_Data40 = $f3
P0_Data41 = $f4
P0_Data42 = $f5


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
   	lda	P1X,X	
DivideLoop
	sbc	#15
   	bcs	DivideLoop
   	sta	temp01,X
   	sta	RESP0,X	
   	sta	WSYNC
   	dex
	CPX	#1
   	BNE	HorPosLoop	

	ldx	#4		; bl
   	ldy	temp05
   	lda	FineAdjustTable256,Y
   	sta	HMP1,X		

	dex			; m1
   	ldy	temp04
   	lda	FineAdjustTable256,Y
   	sta	HMP1,X	
   
	dex			; m0
   	ldy	temp03
   	lda	FineAdjustTable256,Y
   	sta	HMP1,X	
   
	dex			; p1
   	ldy	temp02
   	lda	FineAdjustTable256,Y
   	sta	HMP1,X

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

SettingUpMissile0

	LDA	M0Settings	;3 (59)
	AND	#%00110000	;2 (61)
	STA	NUSIZ0	; Sets M0 registers 3 (64)
	
SettingUpP1SpriteAndMissile1

	LDA	P1Settings 	; 3 (67)
	STA	REFP1		; 3 (70)
	AND	#%00110111	; 2 (72)
	STA	NUSIZ1		; 3 (75) Sets P1 and M1 registers

	LDA	P1SpritePointer+1	; 3 (78) temp07 will store the sprite pointers high byte
	STA	temp06+1		; 3 (2) - One line wasted.

	LDA	P1Y	; 3 (5)
	SEC		; 2 (7) Substract 1 because of the latency
	SBC	#1      ; 2 (9)
	STA	temp08 	; 3 (12) temp08 stores P1 Y position.


FinishPreparation
	TSX			; 2 (14)
	STX	item		; Save the stack pointer 3 (17)

	LDX	#42		; 2 (19)
	LDA	#14		; 2 (21)
	CLC			; 2 (23)
	ADC	pfIndex		; 3 (26)
	STA	temp01		; Save pfIndex 3 (29)	
	TAY			; 2 (31)

	LDA	(bkColorPointer),y 	; 5 (36)
	STA	temp02			; saveBKColor 3 (39)

	LDY 	P1Height		; 3 (42)		
	LDA	(P1ColorPointer),y	; 5 (47)
	STA	COLUP1		; Load first color 3 (50)

	LDY	#200		; 2 (52)
	LDA	M0TurnOff	; 3 (55)
	BPL	NoM0TurnOff	; 2 (57)
	STY	M0Y		; 3 (60)
NoM0TurnOff
	
	LDA	P1TurnOff	; 3 (63)
	BVC	NoP1TurnOff	; 2 (65)
	STY	P1Y		; 3 (70)
NoP1TurnOff
	STA	WSYNC		; 76 - Has to waste.

	BPL	NoM1TurnOff	; 2 
	STY	M1Y		; 3 (5)
	JMP	GoForBall	; 3 (8)
NoM1TurnOff
	sleep 	6
GoForBall
	LDA	BallTurnOff	; 3 (11)
	AND	#%00001000	; 2 (13)
	CMP	#%00001000	; 2 (15)
	BNE	NoBallTurnOff	; 2 (17)
	STY	BLY		; 3 (20)
	JMP	WoWAllDone	; 3 (23)
NoBallTurnOff
	sleep	6
WoWAllDone

	LDA	temp01		; pfIndex 3 (26)	
	TAY			; 2 (28)
	LDA	#0		; 2 (30)
	STA	temp04		; 3 (33) - Set the first sprite's number
	STX	temp05		; 3 (36) - Shoud calculate on first line!

	LDX	#42		; 2 (38)
	STX	temp09		; 3 (41)


	sleep	29
	LDA	temp02			; 3 (73)	
	JMP	StartWithoutWSYNC	; 3 (76)


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


AskFOrNewP0 
	LDY	#0		; 2 
	INC	temp04		; 5
	LDX	temp04		; 3
	JMP	JumpHereAsking	; 3 

DrawingTheScreen
	; temp01 = pfIndex
	; temp02 = bgColor
	; temp03 = P1 Sprite data
	; temp04 = P0 SpriteNum
	; temp05 = NextCalcY
	; temp06, temp07 = P1 sprite pointers
	; temp08 = p1height
	; temp09 = lineNum
	; temp10, temp11, temp12, temp13 = CalcH

FirstLine
	STA	WSYNC		; 3 (76)
StartWithoutWSYNC
	STA	COLUBK		; 3 We have coluBK in temp02

	LDA	(pfColorPointer),y	; 5 (8)
	STA	COLUPF		; 3 (11)

	LDA	(pf0Pointer),y	; 5 (16)
	STA	PF0		; 3 (19)

	LDA	(pf1Pointer),y	; 5 (24)
	STA 	PF1		; 3 (27)

	LDA	(pf2Pointer),y	; 5 (32)
	STA 	PF2		; 3 (35)

****Job with P0 starts here.	
	LDX	temp09		; 3 (38)
	CPX	temp05		; 3 (41)
	BEQ	AskFOrNewP0	; 2 (43)

	LDX	temp04		; 3 (46)
	
	LDA	P0_Data01,x	; 4 (50)	
	TAY			; 2 (52)
	CMP	#0		; 2 (54)
	BNE	HasOwnColor	; 2 (56)
	LDA	M0Color		; 3 (59)
	JMP	SetToMissileColor ; 3 (62)
HasOwnColor	
	LDA	P0_1Color,x     ; 4  
	sleep	2;
SetToMissileColor
	STA	COLUP0		; 3 (65)
	LDA	temp03		; 3 (68)
	STA	GRP1		; 3 (71)
	STY	GRP0		; 3 (74)

SecondLine_NONewP0

*** Set NUSIZ0
	LDA	P0_1Settings,x	; 4 (2)
	TAY			; 2 (4)
	AND	#%00001111	; 2 (6)
	STA	temp06		; 3 (9)
	LDA	M0Settings	; 3 (12)
	AND	#%11110000	; 3 (15)
	STA	NUSIZ0		; 3 (18)	
	STA	REFP0		; 3 (21)

*** Calculate NextHor Borders

	TYA			; 2 (23)
	AND	#%00000111	; 2 (25)
	TAX			; 2 (27)
	LDA	XHorBorderAddSprite,x ; 4 (31)
	STA	temp06		; 3 (34) - maxX

	LDA	P0_1X,x		; 4 (38)
	CMP	#16		; 2 (40)
	BCS	NotSmallerThan16 ; 2 (42)
	LDA	#16		; 2 (44)
	sleep	3		; 3 (47)
	JMP	SaveHorX	; 3 (50)
NotSmallerThan16
	CMP	temp06		; 3 
	BCC	NoChangeHorX	; 2 
	LDA	temp06		; 3 
SaveHorX
	STA	P0_1X,x		; 4 (54)
ISaidNoChange

	LDY	temp01		; 3 (57)
	DEX			; 2 (59)
	DEY			; 2 (61)
	cpx	BLY		; 3 (64)
	php			; 3 (67)
	cpx	M1Y		; 3 (70)
	php			; 3 (73)
	cpx	M0Y		; 3 (76) 
	php			; 3 

	sleep	6		; 6 (9)	
	JMP	JoinKernel	; 3 (12)
**************************************************
NoChangeHorX
	sleep	4		; 4 (51)
	JMP	ISaidNoChange	3 (54)

JumpHereAsking

	LDA	temp10,x	; 4 (60)
	STA	temp05		; 3 (63)

	LDA	M0Color		; 3 (66)
	sta	COLUP0		; 3 (69)
	sty	GRP0		; 3 (72)
	STA	WSYNC		; 76
		

SecondLine_WithNewP0

	LDA	temp03		; 3 
	sta	GRP1		; 3 (6)
	LDA	P0_1X,x		; 4 (10)
DivideLoop_MultiP0
	sbc	#15
   	bcs	DivideLoop_MultiP0
   	sta	RESP0
	TAX

   	lda	FineAdjustTable256,X
   	sta	HMP0
	
	STA	WSYNC

LastLine
	STA	HMOVE		; 3	
	INC	temp04		; 5 (8)
	sleep	4
				
JoinKernel
	LDX	temp09		; 3 (15)

	LDA 	P1Height 	; 3 (18)
	DCP	temp08 		;  temp08 contains P0Y!  ; 5 (23)
	BCC	NoP1DrawNow	; 2 (25)
	LDY	temp08		; 3 (28)
	LDA	(P1ColorPointer),y 	; 5 (33)
	STA	COLUP1	; 3 (36)
	LDA	(temp06),y 	; 5 (38)
saveP1Sprite
	STA	temp03		; 3 (41) 

	DEC	temp01		; 5 (46)
	LDY	temp01		; 3 (49)

	LDA	(bkColorPointer),y	; 5 (54)
	STA	temp02		; 3 (57)
	
	CPX	#0		; 2 (59)
	BEQ	ResetAll  	; 2 (61)

	DEX			; 2 (63)
	STX	temp09		; 3 (66)  Saves the lineNum
	ldx 	#$1f		; 2 (68)  Address of ENABL 
	txs			; 2 (70)

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

Init_P0Data

*	temp01 - StartPoz	
*	temp02 - Counter
*	temp03, temp04 - SpritePointer
*	temp05 - LoPointerIndexed
*	temp06 - TempHeight
*	temp07 - stack

	TSX
	STX	temp07

	LDX	#41
	LDA	#0
	STA	temp02
DoItAgainPlease
	STA	P0_Data01,x
	DEX
	BPL	DoItAgainPlease

	LDX	#0
NextSprite
	TXA

	LDA 	P0_1Height,x
	CLC
	ADC	#1
	STA	temp06

	TXA
	TAY
	AND	#%00000001
	CMP	#0
	BNE	HasToLSR	; Only nibbles are used.

	TYA
	LSR
	TAX
	
	LDA	P0_1Index,x
	AND	#%00001111	
	
	JMP	ContinueWithThings
HasToLSR
	TYA
	LSR
	TAX

	LDA	P0_1Index,x
	AND	#%11110000
	LSR
	LSR
	LSR
	LSR



ContinueWithThings

	TAX
	TXS
	TYA
	TAX
	LDA	P0_1SpritePointerLO,x
	TSX

	CPX	#0
	BEQ	CalculatePointerDone
	CLC	
	ADC	temp06
	DEX
	JMP	ContinueWithThings

CalculatePointerDone
	STA	temp03		; temp06 will store the sprite pointers low byte

	TYA
	TAX

	LDA	P0_1SpritePointerHI,x
	STA	temp04	

	LDA	P0_1Y,x
	STA	temp01
	CLC
	ADC	P0_1Height,x
	CMP	#42
	BCC	NotGoingOver
	LDA	#42
NotGoingOver
	STA	temp10,x

	TAX			; Got the highest point
	SEC
	SBC	temp01		
	TAY			; Got the sprite line-number			 
	
				; Set temporal pointers
CopyBytes
	LDA 	(temp03),y
	STA	P0_Data01,x	
	DEX
	DEY
	BPL	CopyBytes
	INC	temp02
	LDX	temp02
	CPX	#4
	BNE	NextSprite

CalculateP1Index

	LDA 	P1Height
	CLC
	ADC	#1
	STA	temp01	

	LDA	P1SpriteIndex	
	AND	#%00001111	; Get low nibble for P1 index
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
	STA	temp06		; temp06 will store the sprite pointers low byte

	LDX	temp07
	TXS

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


	LDA	#$00
	sta 	frameColor

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




###End-Bank2
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




###End-Bank3
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



###End-Bank4
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



###End-Bank5
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


###End-Bank6

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



###End-Bank7
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



###End-Bank8	
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