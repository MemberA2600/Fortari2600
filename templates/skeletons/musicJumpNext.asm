	lda	#>(CoolSong_Driver1-1)
   	pha
   	lda	#<(CoolSong_Driver1-1)
   	pha
   	pha
   	pha
   	ldx	#BANKNEXT
   	jmp	bankSwitchJump