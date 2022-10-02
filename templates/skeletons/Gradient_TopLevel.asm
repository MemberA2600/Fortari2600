#NAME#_Gradient
	LDA	#VAR01#
!!!to8bits!!!
	STA	temp01

	LDA	##VAR02#
	STA	temp02

	LDA	#VAR03#
!!!shiftToRight!!!
	STA	temp03

	LDA	#<#NAME#_Gradient_Back
	STA	temp04
	LDA	#>#NAME#_Gradient_Back
	STA	temp05

	LDA	#<#NAME#_Gradient_Pattern
	STA	temp06
	LDA	#>#NAME#_Gradient_Pattern
	STA	temp07

	JMP	#BANK#_Gradient

#NAME#_Gradient_Pattern
!!!gradient!!!

#NAME#_Gradient_Back
