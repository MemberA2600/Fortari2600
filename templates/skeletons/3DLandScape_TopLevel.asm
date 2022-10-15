*
*	Number of lines = sum of to numbers from 1 to N, "4" = 1 + 2 + 3 + 4 = 10
*
*	temp01:		 Starting Num
*	temp02: 	 Len of Gradient Pattern (multiply of 2 - 1!)
*	temp03 + temp04: Pattern Pointer
*	temp05:		 Pattern Index	
*	temp06:		 Adder (1, if from top to bottom, 254 otherwise)
*	temp07:		 Goal Num
*	temp08:		 BaseColor	
*	temp09:		 Controller Saved	
*	temp10 + temp11: Shitty Pointer
*	temp12 + temp13: JumpBack Pointer
*	temp14	       : Controller	
*

*
*	Valid ones: 	0-1  -X-Y-0 (INCR)
*			X-255-0-Y-Y (DECR)
*

#NAME#_StartingNum  = 0
#NAME#_FinishNum    = #CON01#
#NAME#_LenOfPattern = #CON02# 

	LDA	#1
	STA	CTRLPF

	LDA	#VAR02#
!!!ShiftToRight!!!
	AND	#%11110000
	STA	temp08

	LDA	#VAR01#
!!!ConvertControllerIfNeeded!!!
	STA	temp14

	BIT	temp14
	BMI	#NAME#_BottomTop

	LDA	##NAME#_StartingNum
	STA	temp01

	LDA	#1
	STA	temp06

	LDA	##NAME#_FinishNum
	STA	temp07

	LDA	##NAME#_LenOfPattern
	STA	temp02

	JMP	#NAME#_TopBottomJump
#NAME#_BottomTop
	LDA	##NAME#_FinishNum
	STA	temp01

	LDA	#255
	STA	temp06

	LDA	##NAME#_StartingNum
	STA	temp07

	LDA	##NAME#_LenOfPattern
	STA	temp02

#NAME#_TopBottomJump
	LDA	#<#NAME#_Gradient
	STA	temp03	
	LDA	#>#NAME#_Gradient
	STA	temp04	

	LDA	#>Bank2_3D_Thing_PF0
	STA	temp11

	LDA	#$20
	BIT	temp14
	BEQ	#NAME#_XYZXYZ
	LDA	#<Bank2_3D_Thing_PF0
	JMP	#NAME#_ZYXZYX
#NAME#_XYZXYZ
	sleep	3
	LDA	#<Bank2_3D_Thing_Empty
#NAME#_ZYXZYX
	STA	temp10

	LDA 	counter
****	speed
!!!SLOWDOWN!!!
	AND	temp02
	STA	temp05

	LDA	temp14
	STA	temp09	

	LDA	#<#NAME#_JumpBack
	STA	temp12	
	LDA	#>#NAME#_JumpBack
	STA	temp13	

	JMP	Bank2_3D_Thing_Loop
#NAME#_Gradient
	_align	#CON03#
!!!GRADIENT!!!

#NAME#_JumpBack
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STX	PF0
	STX	PF1
	STX	PF2
	STA	CTRLPF

