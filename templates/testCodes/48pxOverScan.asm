*
*	Should be able to do:
*	-Left / Right scrolls the picture
*	-Up / Down changes the display height
*	-Select changes speed of animation
*	-Fire adds 1 to animation frame manually 
*

	LDA	#$10
	BIT	SWCHA
	BNE	NoUpPressed
	
	LDA	#DSPHEIGHT#
	CMP	#1
	BEQ	NoDownPressed

	DEC	#DSPHEIGHT#

	JMP	NoDownPressed
NoUpPressed
	LDA	#$20
	BIT	SWCHA
	BNE	NoDownPressed
	INC	#DSPHEIGHT#	

NoDownPressed

	BIT	SWCHA
	BVS	NoLeftPressed

	LDA	#INDEX#
	CMP	#0
	BEQ	NoRightPressed
	DEC	#INDEX#	
	JMP	NoRightPressed
NoLeftPressed
	BMI	NoRightPressed
	
	INC	#INDEX#

NoRightPressed