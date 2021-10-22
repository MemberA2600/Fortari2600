picIndex = $d2
picDisplayHeight = $d3
picHeight = FULLHEIGHT

Letter01 = $d4
Letter02 = $d5
Letter03 = $d6
Letter04 = $d7
Letter05 = $d8
Letter06 = $d9
Letter07 = $da
Letter08 = $db
Letter09 = $dc
Letter10 = $dd
Letter11 = $de
Letter12 = $df
TextColor = $e0
TextBackColor = $e1

TextEnd = TEST_TEXT_END
TextPoz = $ec
TextDir = $ed


	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#TEST_TEXT_COLOR
	STA	TextColor
	
	LDA	#$TEST_BACK_COLOR
	STA	TextBackColor	

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#DSPHEIGHT
	STA	picDisplayHeight

	LDA	#DSPINDEX
	STA	picIndex

	LDA	#INITLETTER01
	STA	Letter01

	LDA	#INITLETTER02
	STA	Letter02

	LDA	#INITLETTER03
	STA	Letter03

	LDA	#INITLETTER04
	STA	Letter04

	LDA	#INITLETTER05
	STA	Letter05

	LDA	#INITLETTER06
	STA	Letter06

	LDA	#INITLETTER07
	STA	Letter07

	LDA	#INITLETTER08
	STA	Letter08

	LDA	#INITLETTER09
	STA	Letter09

	LDA	#INITLETTER10
	STA	Letter10

	LDA	#INITLETTER11
	STA	Letter11

	LDA	#INITLETTER12
	STA	Letter12

	LDA	#FRAME_COLOR
	STA	frameColor