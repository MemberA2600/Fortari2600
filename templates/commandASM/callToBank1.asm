	LDA	##BANKNUM#
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump
*
*	For global routines, these two are excluded of usage.
*
	LDA	#>(#BACK#-1)
	STA	temp18
	LDA	#>(#BACK#-1)
	STA	temp19

	lda	#>(#LABEL#-1)
   	pha
   	lda	#<(#LABEL#-1)
   	pha
   	pha
   	pha
   	ldx	#1
   	jmp	bankSwitchJump

#BACK#
!!!SAVE!!!
