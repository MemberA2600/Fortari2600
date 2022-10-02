#NAME#_Space_Screen
	
	LDA	#VAR01#
	STA	temp05
	LDA	#VAR02#
	STA	temp06

	LDA	#<#NAME#_Space_Screen_JMPBack
	STA	temp03
	LDA	#>#NAME#_Space_Screen_JMPBack
	STA	temp04	

	JMP	#BANK#_Space_JMP

#NAME#_Space_Screen_JMPBack
	LDA	temp05
	STA	#VAR01#
