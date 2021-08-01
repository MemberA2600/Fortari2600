	LDA	#0
	sta 	frameColor
	STA	P0SpriteIndex ; 	Sets both indexes to 0;
	STA	P0X
	STA	P1X
	STA	pfBaseColor
	STA	bkBaseColor
	STA	M0X
	STA	M1X
	STA	BLX

	LDA	P0TurnOff
	AND	#%00111111
	ORA	#%11000000
	STA	P0TurnOff	; Turn Off P0 and M0

	LDA	P1TurnOff
	AND	#%00111111
	ORA	#%11000000
	STA	P1TurnOff	; Turn Off P1 and M1

	LDA	BallTurnOff
	ORA	#%00001000
	STA	BallTurnOff	; Turn off Ball

	
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