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
P1Settings = $a8			
P1Mirrored = $a8			; Must be in order!
****************************************
pfSettings = $a9	; Since CTRLPF 0-1 bits are fixed in the screen loop
pfEdges	= $a9		; 0-1: free
			; 2: Players move behind the pf
Has to be here because	; 3: Free
of the edge check	; 4-5: Ball Settings
routine.		; 6-7: 00 - Nothing 01 - Mixed 10 - All stop 11 - All go through 
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
   	sta	HMOVE

	LDA	frameColor	; 3 
	STA 	COLUPF		; 3 

	LDA	#0	;2 
	STA 	ENAM0	;3 
	STA 	ENAM1	;3
	STA 	ENABL	; Disables missiles and ball 3 
	STA	GRP0	;3 
	STA	GRP1	; Sets player sprites to blank 3
 	STA	VDELP0	;3 
	STA	VDELP1  ;3 
	
	STA	PF1	;3 
	STA	PF2	;3 
	STA	PF0	;3 
	STA	temp03 	;3 Erase P1 sprite data
	


	LDA	pfSettings	;3 
	ORA	#%00000001	; Reflected playfield 2 
	AND	#%11111101	; Always get the original colors. 2 
	STA	CTRLPF		; 3 (54)

SettingUpP0SpriteAndMissile0

	LDA	P0Settings	;3 
	STA	REFP0		;3 
	AND	#%00110111	;2
	STA	NUSIZ0	; Sets P0 and M0 registers 3

	LDA	P0SpritePointer+1	; temp08 will store the sprite pointers high byte ; 3 (6)
	STA	temp07+1		; 2 (9)

	LDA	P0Y
	STA	temp09 	; temp09 stores P0 Y position.
	
SettingUpP1SpriteAndMissile1

	LDA	P1Settings
	STA	REFP1
	AND	#%00110111
	STA	NUSIZ1	; Sets P1 and M1 registers

	LDA	P1SpritePointer+1	; temp11 will store the sprite pointers high byte
	STA	temp10+1

	LDA	P1Y
	SEC		; Substract 1 because of the latency
	SBC	#1      ;
	STA	temp12 	; temp12 stores P1 Y position.


FinishPreparation
	TSX			;2
	STX	item		; Save the stack pointer 3 (5)

	LDA	#42	; 2 (7)
	TAX		; 2 (9)
	tay		;2 (11)
	DEY

	LDA	(pfColorPointer),y	; 5 (16)
	CLC				; 2 (18)
	ADC	pfBaseColor 		; 3 (21)
	STA	temp02		; savePFColor 3 (24)

	LDA	(bkColorPointer),y 	; 5 (29)
	CLC				; 2 (31)
	ADC	bkBaseColor 		; 3 (34)
	STA	temp04		; saveBKColor 3 (37)

	LDY 	P1Height		; 3 (40)  		
	LDA	(P1ColorPointer),y	; 5 (45)
	STA	COLUP1		; Load first color 3 (48)

	STA	WSYNC
	
	LDX  	#42		; 2
	LDA	#14		; 2(4)
	CLC			; 2(6)
	ADC	pfIndex		; 3(9)
	STA	temp01		; Save pfIndex 3(12)	
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
	LDA	M0Color		; 3
	STA	COLUP0		; 3
	LDA	#0	  	; 2
	sleep	5		; 5

	JMP	saveP0Sprite	; 3 	 

NoP1DrawNow
	LDA	M1Color		; 3
	STA	COLUP1		; 3
	LDA	#0	  	; 2
	sleep	5		; 5

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

	DEX			; 2 (58)
	LDA	temp02		; 3 (61)

	CPX	#0		; 2 (63)
	BEQ	ResetAll  	; 2 (65)
	DEC	temp01		; 5 (70)
	JMP	FirstLine	; 3 (73)

ResetAll
	LDA	frameColor	; 3 (70)
	STA 	COLUBK		; 3 (73)
	STX	WSYNC		; 3 (76)
	STA 	COLUPF

	LDX	#0
	STX	PF0
	STX	PF1
	STX	PF2
	STX 	COLUBK
	STX	ENAM0
	STX	ENAM1

	STX	VDELP0
	STX	VDELP1
	STX	VDELBL
	STX	GRP0
	STX	GRP1
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
	LDA	#43
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
!!!KERNEL_DATA!!!

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

!!!OVERSCAN_BANK2!!!


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

!!!VBLANK_BANK2!!!


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

!!!SCREENTOP_BANK2!!!


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

!!!SCREENBOTTOM_BANK2!!!

	JMP	OverScanBank2


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK2!!!
	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK2!!!

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

!!!OVERSCAN_BANK3!!!


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

!!!VBLANK_BANK3!!!


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

!!!SCREENTOP_BANK3!!!


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

!!!SCREENBOTTOM_BANK3!!!

	JMP	OverScanBank3


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK3!!!


*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK3!!!

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

!!!OVERSCAN_BANK4!!!


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

!!!VBLANK_BANK4!!!


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

!!!SCREENTOP_BANK4!!!


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

!!!SCREENBOTTOM_BANK4!!!

	JMP	OverScanBank4


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK4!!!
	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK4!!!

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

!!!OVERSCAN_BANK5!!!


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

!!!VBLANK_BANK5!!!


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

!!!SCREENTOP_BANK5!!!


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

!!!SCREENBOTTOM_BANK5!!!

	JMP	OverScanBank5


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK5!!!
	
*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK5!!!


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

!!!OVERSCAN_BANK6!!!


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

!!!VBLANK_BANK6!!!


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

!!!SCREENTOP_BANK6!!!


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

!!!SCREENBOTTOM_BANK6!!!

	JMP	OverScanBank6


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK6!!!
	

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK6!!!


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

!!!OVERSCAN_BANK7!!!


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

!!!VBLANK_BANK7!!!


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

!!!SCREENTOP_BANK7!!!


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

!!!SCREENBOTTOM_BANK7!!!

	JMP	OverScanBank7


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK7!!!
	
*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK7!!!


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

!!!OVERSCAN_BANK8!!!


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

!!!VBLANK_BANK8!!!


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

!!!SCREENTOP_BANK8!!!


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

!!!SCREENBOTTOM_BANK8!!!

	JMP	OverScanBank8


*Routine Section
*---------------------------------
* This is were the routines are
* used by the developer.
*

!!!ROUTINES_BANK8!!!

*Data Section 
*----------------------------------
* Here goes the data used by
* custom ScreenTop and ScreenBottom
* elments.
*

!!!USER_DATA_BANK8!!!

	
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