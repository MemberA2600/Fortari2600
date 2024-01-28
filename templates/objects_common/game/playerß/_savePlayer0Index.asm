	LDA	#TEMPVAR#	
	AND	#$0F
	STA	#TEMPVAR#

	LDA	P0SpriteIndex
	AND	#$F0
	ORA	#TEMPVAR#
	STA	P0SpriteIndex

	
