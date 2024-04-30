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

	BIT	INPT4
	BMI	NoFirePressed	

	BIT	stopBits
	BMI	NoClearBit7

	LDA	#SETTERS#
	AND	#$F0
	STA	temp01
	LDA	#SETTERS#
	AND	#$0F
	CLC
	ADC	#1
	AND	#$0F
	STA	temp02

	LDA	##NAME#_Frames_Max_Index
	CMP	temp02
	BCS 	DoNotZeroIndex
	LDA	#0
	STA	temp02
DoNotZeroIndex
	LDA	temp02
	ORA	temp01
	STA	#SETTERS#

	LDA	stopBits
	ORA	#%10000000
	STA	stopBits

	JMP	NoClearBit7
NoFirePressed
	LDA	stopBits
	AND	#%01111111
	STA	stopBits

NoClearBit7
	LDA	#$02
	BIT	SWCHB
	BNE	NoSelectPressed

	BIT	stopBits
	BVS	NoClearBit6

	LDA	#SETTERS#
	AND	#$0F
	STA	temp01
	LDA	#SETTERS#
	LSR
	LSR
	LSR
	LSR
	AND	#%00000111

	CLC
	ADC	#1
	AND	#%00000111
	STA	temp02

	LDA	#7
	CMP	temp02
	BCS 	DoNotZeroIndex2
	LDA	#0
	STA	temp02
DoNotZeroIndex2
	LDA	temp02
	ASL
	ASL
	ASL
	ASL
	ORA	temp01
	STA	#SETTERS#

	LDA	stopBits
	ORA	#%01000000
	STA	stopBits

	JMP	NoClearBit6

NoSelectPressed
	LDA	stopBits
	AND	#%10111111
	STA	stopBits

NoClearBit6
