*
*	temp01:		DataVar
*	temp02: 	Number of Lines
*	temp03+temp04:	Gradient Pointer
*	temp05+temp06:	Back Pointer
*	temp07:		Direction
*

#NAME#_Gradient_Hor
	LDA	#VAR01#
!!!to8bits!!!
	STA	temp01

	LDA	##VAR02#
	STA	temp02

	LDA	##VAR04#
	STA	temp07

*	LDA	#VAR03#
!!!shiftToRight!!!
*	CMP	#255
*	BEQ	#NAME#_Gradient_Hor_No_Change
*	AND	#%11110000
*	STA	temp19
*	LDA	temp01
*	AND	#%00001111
*	ORA	temp19
*	STA	temp01

#NAME#_Gradient_Hor_No_Change
	LDA	#<#NAME#_Gradient_Hor_Back
	STA	temp05
	LDA	#>#NAME#_Gradient_Hor_Back
	STA	temp06

	LDA	#<#NAME#_Gradient_Hor_Pattern
	STA	temp03
	LDA	#>#NAME#_Gradient_Hor_Pattern
	STA	temp04

	JMP	#BANK#_Horizontal_Rainbow

#NAME#_Gradient_Hor_Pattern
!!!gradient!!!

#NAME#_Gradient_Hor_Back
