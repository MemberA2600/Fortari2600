	LDA	random
	lsr
	BCC 	*+4
	EOR	#$d4
	EOR	counter
	STA	random
	STA	frameColor
