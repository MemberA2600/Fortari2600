Letter01 = $d2
Letter02 = $d3
Letter03 = $d4
Letter04 = $d5
Letter05 = $d6
Letter06 = $d7
Letter07 = $d8
Letter08 = $d9
Letter09 = $da
Letter10 = $db
Letter11 = $dc
Letter12 = $dd
TextColor = $de
BackColor = $df

	LDA	#0
	STA	Letter01
	LDA	#1
	STA	Letter02
	LDA	#2
	STA	Letter03
	LDA	#3
	STA	Letter04
	LDA	#4
	STA	Letter05
	LDA	#5
	STA	Letter06
	LDA	#6
	STA	Letter07
	LDA	#7
	STA	Letter08
	LDA	#8
	STA	Letter09
	LDA	#9
	STA	Letter10
	LDA	#10
	STA	Letter11
	LDA	#11
	STA	Letter12

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#$1a
	STA	TextColor
	
	LDA	#$40
	STA	BackColor	