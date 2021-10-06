picIndex = $d2
picDisplayHeight = $d3
picHeight = FULLHEIGHT

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#DSPHEIGHT
	STA	picDisplayHeight

	LDA	#DSPINDEX
	STA	picIndex