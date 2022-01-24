	bit	INPT5	
	BPL	PlaySoundXX_JumpToTheSound
	bit	INPT4	
	BMI	PlaySoundXX_Return
PlaySoundXX_JumpToTheSound
	LDA	#2
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#>(PlaySoundXX_Initialize-1)
   	pha
   	lda	#<(PlaySoundXX_Initialize-1)
   	pha
   	pha
   	pha
   	ldx	#3
   	jmp	bankSwitchJump

PlaySoundXX_Return