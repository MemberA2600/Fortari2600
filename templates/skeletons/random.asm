CallRandomBankX
	LDA	random
	lsr
	BCC 	*+4
	EOR	#$d4
	EOR	counter
	STA	random
	rts