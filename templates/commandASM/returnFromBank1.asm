	lda	bankToJump
	lsr
	lsr
	AND	#%00000111	; Get the bank number to return
	tax

	lda	temp18
   	pha
   	lda	temp19
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump