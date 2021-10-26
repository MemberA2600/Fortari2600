picIndex = $d2
picDisplayHeight = $d3
picHeight = FULLHEIGHT

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#DSPHEIGHT
	STA	picDisplayHeight

	LDA	#DSPINDEX
	STA	picIndex

	LDA	#90
	CMP	picDisplayHeight
	BCS	64pxPicture_NoINITDec
	STA	picDisplayHeight

64pxPicture_NoINITDec