
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
*	temp15 + temp16: ColorBasePointer
*
#NAME#_Number_Of_Lines = #CON01#

*****   Variable for control the flow
	LDA	#VAR01#
!!!convertTo8bits!!!	
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

*****   Container Variable
	LDA	#VAR03#		; 3
	AND	#%11100000	; 2
	STA	temp19		; 3

	LDA	#VAR03#		; 3
	AND	#%01100000	; 2
	ROL			; 2
	ROL			; 2
	ROL			; 2
	ROL			; 2
	STA	temp05		; 3

*****	STA	WSYNC
	LDA	counter
	AND	#%00000011
	CMP	#%00000011
	BNE	#NAME#_NoChange1

	LDA	#VAR03#		; 3
	AND	#%00011111  	; 2
	CMP	##NAME#_Number_Of_Lines	; 2 
	BEQ	#NAME#_NoChange2	; 2
	TAX				; 2
	INX				; 2
	TXA			; 2
	ORA	temp19		; 3
	STA	#VAR03#		; 3
	JMP	#NAME#_Changed  ; 3
#NAME#_NoChange1
	sleep	7
#NAME#_NoChange2
	sleep	17
#NAME#_Changed
	STA	WSYNC
	LDA	#VAR03#
	AND	#%00011111
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

	_align	#CON02#

#NAME#_SnowFlakes_Sky_Gradient
!!!GRADIENT!!!

#NAME#_SnowFlakes_JumpBack
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1
	STX	ENAM0
	STX	ENAM1
	STX	HMCLR
