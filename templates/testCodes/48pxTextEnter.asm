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
Letter12 = $de
TextColor = $df
TextBackColor = $e0

	LDA	#0
	STA	Letter01
	STA	Letter02
	STA	Letter03
	STA	Letter04
	STA	Letter05
	STA	Letter06
	STA	Letter07
	STA	Letter08
	STA	Letter09
	STA	Letter10
	STA	Letter11
	STA	Letter12

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#$1a
	STA	TextColor
	
	LDA	#$40
	STA	TextBackColor	