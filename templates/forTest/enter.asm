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

	LDA	#0
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

MissileDir = $f0
NUSIZ = $f1
Sound = $f2


	LDA	#0
	STA	NUSIZ
	STA	Sound
	STA	MissileDir


maxFrames=3

	LDA	SubMenuLines
	AND	#%11111100
	ORA	#%00000011
	STA	SubMenuLines	; Set to 5 lines.

	LDA	#<Symbols
	STA 	TileSetPointer 
	LDA	#>Symbols
	STA 	TileSetPointer+1

	LDA	#<SubMenuGradient
	STA 	TileColorPointer 
	LDA	#>SubMenuGradient
	STA 	TileColorPointer+1


	LDA	#$14
	STA	TileScreenMainColor

*	LDA	#%11111110
*
*	LDX	#0
FillTiles
*	CLC
*	ADC	#%0010010
*	STA	Tile1_1,x
*	INX
*	CPX	#12
*	BNE	FillTiles	
*

	LDX	#0
	LDA	#%00000001
	STA	Tile1_1,x	; 0, 1

	LDX	#1
	LDA	#%00100011
	STA	Tile1_1,x	; 2, 3

	LDX	#2
	LDA	#%01000101
	STA	Tile1_1,x	; 4, 5

	LDX	#3
	LDA	#%01100111
	STA	Tile1_1,x	; 6, 7

	LDX	#4
	LDA	#%10001001
	STA	Tile1_1,x	; 8, 9

	LDX	#5
	LDA	#%10101011
	STA	Tile1_1,x	; 10, 11

	LDX	#6
	LDA	#%11001101
	STA	Tile1_1,x	; 12, 13

	LDX	#7
	LDA	#%11101111
	STA	Tile1_1,x	; 14, 15

	LDX	#8
	LDA	#%00000001
	STA	Tile1_1,x	; 0, 1

	LDX	#9
	LDA	#%00100011
	STA	Tile1_1,x	; 2, 3

	LDX	#10
	LDA	#%01000101
	STA	Tile1_1,x	; 4, 5

	LDX	#11
	LDA	#%01100111
	STA	Tile1_1,x	; 6, 7


	LDA	SubMenu
	ORA	#%01000000
	STA	SubMenu		; Switch to SubMenu Mode	
	

	LDA	#0
	STA	Selected
