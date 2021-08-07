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
