
*
*	temp01:		 Wall Data1
*	temp02:		 Wall Data2
*	temp03:		 Wall Data3
*	temp04:		 Wall Data4
*	temp05:		 Wall Data5
*	temp06:		 Wall Data6
*	temp07:		 Sprite Positions
*
*	temp08	       : Wall Base Color	
*	temp09 + temp10: Sprite Pointer / P0 Sprite Pointer
*	temp11 + temp12: Sprite Color Pointer
*	temp13 + temp14: JumpBack Pointer 	
*	temp15 + temp16: Empty Sprite Pointer / P1 Sprite Pointer
*	temp17 + temp18: Wall Gradient	
*	temp19	       : Index	
*
*	Set temp19 to $F0 is there is no sprite attached!
*


#NAME#_Number_Of_Lines = #CON01#

#NAME#_Wall
******* PF1 - Left
	LDA	#VAR01#
	STA	temp01

******* PF2 - Left
	LDA	#VAR02#
	STA	temp02

******* PF1 - Right 
	LDA	#VAR03#
	STA	temp03

******* PF2 - Right
	LDA	#VAR04#
	STA	temp04

******* PF0 Both
	LDA	#VAR05#
	STA	temp05

	LDA	#VAR05#
	ASL
	ASL
	ASL
	ASL
	STA	temp06

******* Sprite Positions
	LDA	#VAR06#
	STA	temp07

******* Base Color + Sprite Index
	LDA	#VAR07#
	AND	#%11110000
	STA	temp08

	LDA	#VAR07#
	AND	#%00001111
!!!NoSpriteTemp19Code!!!
	STA	temp19

!!!SetSpriteIfExists!!!

	LDA	#<##NAME##_Empty
	STA	temp15
	LDA	#>##NAME##_Empty
	STA	temp16	

	LDA	#<#NAME#_JumpBack
	STA	temp13
	LDA	#>#NAME#_JumpBack
	STA	temp14	

	LDA	#<#NAME#_Wall_Gradient
	STA	temp17
	LDA	#>#NAME#_Wall_Gradient
	STA	temp18	

	LDX	##NAME#_Number_Of_Lines
	TXS

	JMP	Bank2_Wall_Kernel
*
*	Should be size + 1, so it will have the same page as the
*	Jumpback Pointer! 
*
	_align	#CON02#

#NAME#_Wall_Gradient
### &COLOR
!!!GRADIENTS!!!	

#NAME#_JumpBack
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STX	PF0
	STX	PF1
	STX	PF2
	STX	GRP0
	STX	GRP1
	STA	CTRLPF

