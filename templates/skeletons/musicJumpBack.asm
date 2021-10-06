	lda	bankToJump
	lsr
	lsr
	AND	#%00000111
	tax

	lda	temp02
   	pha
   	lda	temp01
   	pha
   	pha
   	pha
	jmp	bankSwitchJump