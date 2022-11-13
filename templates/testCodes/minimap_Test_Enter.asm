*
*	#VAR01#:	Current X Position on Matrix	
*	#VAR02#:	Current Y Position on Matrix
*	#VAR03#:	Foreground color (PF and sprites)
*	#VAR04#:	Background Color (Background under the minimap)
*	#VAR05#:	Ball Color (basically PF at sprite region)
*	#VAR06#:	Ball's current X
*	#VAR07#:	Ball's current Y
*

	LDA	#0
	STA	#VAR01#
	STA	#VAR02#
	STA	#VAR06#
	STA	#VAR07#

	LDA	#COLOR1#
	STA	#VAR03#

	LDA	#COLOR2#
	STA	#VAR04#

	LDA	#COLOR3#
	STA	#VAR05#

	LDA	#%10000000	; Disables game kernel, so won't run
	STA	NoGameMode 	; main kernel and vblank code.

	LDA	#COLOR4#	
	STA	frameColor
