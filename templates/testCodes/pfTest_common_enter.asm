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

	LDA	#50
	STA	P0Y
	STA	P1Y	
	STA	M0Y
	STA	M1Y
	STA	BLY

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