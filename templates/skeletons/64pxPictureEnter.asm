
**************************
*Picture Data*
**************
picIndex = #VAR01#
picDisplayHeight = #VAR02#
picHeight = FULLHEIGHT
**************************

	LDA	#picHeight
	STA	picDisplayHeight

	LDA	#0
	STA	picIndex

	LDA	#90
	CMP	picDisplayHeight
	BCS	64pxPicture_NoINITDec
	STA	picDisplayHeight

64pxPicture_NoINITDec
