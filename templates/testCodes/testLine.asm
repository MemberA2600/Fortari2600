*
*	Testline
*
	LDA	#0
	STA	GRP0
	STA	GRP1
	STA	PF0
	STA	PF1
	STA	PF2

	LDA	counter
	STA	WSYNC
	STA	COLUBK
	STA	WSYNC
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK
