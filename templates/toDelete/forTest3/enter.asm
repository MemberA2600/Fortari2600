picIndex = $d2
picDisplayHeight = $d3
picHeight = 27

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#27
	STA	picDisplayHeight

	LDA	#0
	STA	picIndex

	
