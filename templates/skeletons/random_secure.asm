*
* This is a more secure version, using the temp01/temp02
* pair for jumpback. Accumulator has the result!
*

#BANK#_Randum_Number
	LDA	random
	lsr
	BCC 	*+4
	EOR	#$d4
	EOR	counter
	STA	random

	JMP	(temp01)