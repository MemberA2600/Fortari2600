	LDA	#0
	sta 	frameColor
	STA	P0SpriteIndex ; 	Sets both indexes to 0;
	STA	pfBaseColor
	STA	bkBaseColor

	LDA	#!!!Min!!!
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
	STA	P1SpritePointer
	LDA	#>TestSprite_Sprite
	STA	P1SpritePointer+1

	LDA	#<TestSprite_SpriteColor
	STA	P1ColorPointer
	LDA	#>TestSprite_SpriteColor
	STA	P1ColorPointer+1

	LDA	#<Zero
	STA	P0SpritePointer
	LDA	#>Zero
	STA	P0SpritePointer+1

	LDA	#1
	STA	P0Height

	LDA	#110
	STA	P0X
	STA	P1X
	STA	M0X
	STA	M1X
	STA	BLX

	LDA	#!!!StartY!!!
	STA	P1Y

	LDA	#!!!Height!!!
	STA	P1Height

	LDA	#0
	STA	P1SpriteIndex ; 	Sets both indexes to 0;

	LDA	pfEdges		; Sprites stop, bullets go through
	AND	#%00111111
	STA	temp01
	LDA	#%01000000
	ORA	temp01
	STA	pfEdges

	LDA	P1TurnOff
	AND	#%00111111
	ORA	#%10000000
	STA	P1TurnOff	; Turn off M1

	LDA	P0TurnOff
	AND	#%00111111
	ORA	#%11000000
	STA	P0TurnOff	; Turn Off P0 and M0

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


maxFrames=!!!MaxFrames!!!

