*
*	#VAR01#:	Current X Position on Matrix	
*	#VAR02#:	Current Y Position on Matrix
*	#VAR03#:	Foreground color (PF and sprites)
*	#VAR04#:	Background Color (Background under the minimap)
*	#VAR05#:	Ball Color (basically PF at sprite region)
*	#VAR06#:	Ball's current X
*	#VAR07#:	Ball's current Y
*

	LDA	counter
	AND	#1
	CMP	#1
	BEQ	#NAME#_DoIt
	JMP	#NAME#_Nothing

#NAME#_DoIt
	LDX	#VAR07#
	LDA	#$10
	BIT 	SWCHA
	BNE	#NAME#_Up_Not_Pressed
	INX
	JMP	#NAME#_UpDown_Done
#NAME#_Up_Not_Pressed
	LDA	#$20
	BIT 	SWCHA
	BNE	#NAME#_UpDown_Done
	DEX

#NAME#_UpDown_Done

	LDY	#VAR02#
	CPX	#255
	BNE	#NAME#_No_Top
	LDX	##STEPY-1#	
	INY

	JMP	#NAME#_TopTop
#NAME#_No_Top
	CPX	##STEPY#
	BNE	#NAME#_TopTop

	LDX	#0
	DEY	
	
#NAME#_TopTop
	STY	#VAR02#
	STX	#VAR07#

	LDX	#VAR06#
	LDA	#$80
	BIT 	SWCHA
	BNE	#NAME#_Left_Not_Pressed
	INX
	JMP	#NAME#_LeftRight_Done
#NAME#_Left_Not_Pressed
	LDA	#$40
	BIT 	SWCHA
	BNE	#NAME#_LeftRight_Done
	DEX

#NAME#_LeftRight_Done

	LDY	#VAR01#
	CPX	#255
	BNE	#NAME#_No_Decrement_By_1
	DEY	
	LDX	#30
	JMP	#NAME#_End_Wandering
#NAME#_No_Decrement_By_1
	CPX	#31
	BNE	#NAME#_End_Wandering
	LDX	#0
	INY
#NAME#_End_Wandering
	STX	#VAR06#

	LDX	#VAR02#
	CPY	#255
	BNE	#NAME#_No_Decrement_By_1_Y
	LDY	##MATRIX3#
	DEX
	JMP	#NAME#_KecskeSajt
#NAME#_No_Decrement_By_1_Y
	CPY	##MATRIX1#
	BNE	#NAME#_KecskeSajt

	LDY	#0
	INX
#NAME#_KecskeSajt
	STY	#VAR01#

	CPX	#255
	BNE	#NAME#_Mehhh
	LDX	##MATRIX4#

	JMP	#NAME#_XxXxX
#NAME#_Mehhh
	CPX	##MATRIX2#
	BNE	#NAME#_XxXxX
	LDX	#0

#NAME#_XxXxX
	STX	#VAR02#

#NAME#_Nothing