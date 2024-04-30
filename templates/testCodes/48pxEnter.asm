#DSPHEIGHT# = $d2
#SETTERS# = $d3
#INDEX# = $d4
stopBits = $d5
*
*	Setters:
*	0-3: frameIndex
*	4-5: speed	
*

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#0
	STA	#INDEX#

	LDA	#NAME#_LineNum_Number_Of_Lines
	CMP	#70
	BCC	THANKGOD_SMALLER
	LDA	#70
THANKGOD_SMALLER
	CMP 	##NAME#_LineNum_Number_Of_Lines
	BCS	THANKGOD_SMALLER2
	LDA	##NAME#_LineNum_Number_Of_Lines
THANKGOD_SMALLER2
	STA	#DSPHEIGHT#	

	LDA	##SPEED#
	ASL
	ASL
	ASL
	ASL
	AND 	#%01110000
	STA	#SETTERS#

	LDA	##BACKGROUND#
	STA	frameColor

