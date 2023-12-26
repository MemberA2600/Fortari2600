!!!BCDon!!!
!!!CALCADD!!!
!!!CALCAND!!!
	LDA	random
	lsr
	BCC 	*+4
	EOR	#$d4
******	EOR	counter
!!!ADD!!!
!!!AND!!!
	STA	random
!!!from8bit!!!
	STA	#VAR01#
!!!BCDoff!!!