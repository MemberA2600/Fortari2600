	LDA	#BANKBACK
	asl
	asl			; Rol left two bits to save bankNumber
	STA	temp01

	LDA 	bankToJump
	AND	#%11100011	; Clear previous bankNumber
	ORA	temp01		; Save the bankNumber
	STA	bankToJump

	lda	#<(CoolSong_JumpBack-1)
	sta	temp01
   	lda	#>(CoolSong_JumpBack-1)
	sta	temp02

	lda	#>(CoolSong_Driver0-1)
   	pha
   	lda	#<(CoolSong_Driver0-1)
   	pha
   	pha
   	pha
   	ldx	#BANKNEXT
   	jmp	bankSwitchJump
CoolSong_JumpBack