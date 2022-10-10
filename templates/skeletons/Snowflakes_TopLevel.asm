
*
*	temp01:		 BaseData
*	temp02:		 BaseColor
*	temp03:		 BaseBackColor
*	temp04:		 FineAdjustment
*	temp05:		 Pattern Number
*	temp06 + temp07: Pattern Pointer
*	temp08 + temp09: Background Gradient Pointer
*	temp10: 	 ENAM Const
*	temp11:          Line Number
*	temp12: 	 BackCounter	
*	temp13 + temp14: JumpBack
*
#NAME#_Number_Of_Lines = #CON01#

*****   Variable for control the flow
	LDA	#VAR01#
	STA	temp01

	LDA	##NAME#_Number_Of_Lines
	STA	temp11

*****   Color Variable / Constant
	LDA	#VAR02#
	AND	#%00001111
	ASL
	ASL
	ASL
	ASL
	STA	temp02

	LDA	#VAR02#
	AND	#%11110000
	STA	temp03

	LDA	#<#NAME#_SnowFlakes_Sky_Gradient
	STA	temp08
	LDA	#>#NAME#_SnowFlakes_Sky_Gradient
	STA	temp09

	LDA	counter
	AND	#%00000011
	CMP	#%00000011
	BNE	#NAME#_NoChange1

*****   Container Variable
	LDA	#VAR03#
	AND	#%11100000
	STA	temp19

	LDA	#VAR03#
	AND	#%01100000
	ROL
	ROL
	ROL
	ROL
	STA	temp05

	LDA	#VAR03#
	AND	#%00011111
	CMP	##NAME#_Number_Of_Lines
	BEQ	#NAME#_NoChange2
	TAX
	INX
	TXA
	ORA	temp19
	STA	#VAR03#
	JMP	#NAME#_Changed
#NAME#_NoChange1
	sleep	17
#NAME#_NoChange2
	sleep	15
#NAME#_Changed
	LDA	#VAR03#
	AND	#%00001111
	ADC	#1
	STA	temp12

	LDX	#2
	LDA	#VAR03#
	BMI	#NAME#_Negative_Stuff
	LDX	#0
#NAME#_Negative_Stuff
	STX	temp10
	
	LDA	#<#NAME#_SnowFlakes_JumpBack
	STA	temp13
	LDA	#>#NAME#_SnowFlakes_JumpBack
	STA	temp14

	JMP	#BANK#_SnowFlakes_Kernel
Bank2_SnowFlakes_Sky_Gradient
!!!GRADIENT!!!

#NAME#_SnowFlakes_JumpBack
