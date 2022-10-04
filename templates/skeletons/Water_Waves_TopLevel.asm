*
*	temp01:		Controller
*	temp02:		BaseColor
*	temp03+temp04:  PF Pointer
*	temp05+temp06:  PF Color Pointer
* 	temp07+temp08:  PF Inverted Pointer
*	temp09+temp10:  Back Pointer
*
	LDA	#VAR01#
!!!to8bits!!!
!!!LSRs!!!
	STA	temp01

	LDA	#VAR02#
	STA	temp02

	LDA	#<#NAME#_Water_Waves_Gradient
	STA	temp05
	LDA	#>#NAME#_Water_Waves_Gradient
	STA	temp06

	LDA	#<#NAME#_Water_Waves_Back
	STA	temp09
	LDA	#>#NAME#_Water_Waves_Back
	STA	temp10

	JMP	#BANK#_Water_Waves
#NAME#_Water_Waves_Gradient
!!!gradient!!!

#NAME#_Water_Waves_Back
