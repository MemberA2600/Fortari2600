*
*	Should be able to do:
*	-Left / Right scrolls the picture
*	-Up / Down changes the display height
*	-Select changes speed of animation
*	-Fire adds 1 to animation frame manually 
*

	BIT	SWCHA
	BVS	NoLeftPressed
	DEC	#INDEX#
	
	JMP	NoRightPressed
NoLeftPressed
	BMI	NoRightPressed
	INC	#INDEX#
NoRightPressed

	LDX	#$FF
	STX	$F0

	LDA	#$10
	BIT	SWCHA
	BNE	NoUpPressed
	DEC	#DSPHEIGHT#

	JMP	NoDownPressed
NoUpPressed
	LDA	#$20
	BIT	SWCHA
	BNE	NoDownPressed
	INC	#DSPHEIGHT#	

NoDownPressed
