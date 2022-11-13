*
*	temp01:		 stepY
*	temp02:		 MatrixX (Decremented by one)
*	temp03:		 MatrixY (Decremented by one)
*	temp04: 	 ForeGround Colour
*	temp05: 	 Background Colour
*	temp06:		 Ball Colour
*	temp07 + temp08: Sprite0 Pointer
*	temp09 + temp10: Sprite1 Pointer
*	temp11:		 BallX
*	temp12:		 BallY
*	temp13 + temp14: Gradient Pointer
*	temp15:		 Ball On/Off
*	temp16 + temp17: JumpBack
*


#NAME#_MiniMap_TestingSettings

	LDA	#VAR01#
!!!VAR01-LSRS!!!
	STA	temp02

	LDA	#VAR02#
!!!VAR02-LSRS!!!
	STA	temp03

	LDY	##CON01#
	STY	temp01	
	
	LDA	#VAR03#
!!!VAR03-SHIFT!!!
	STA	temp04

	LDA	#VAR04#
!!!VAR04-SHIFT!!!
	STA	temp05

	LDA	#VAR05#
!!!VAR05-SHIFT!!!
	STA	temp06

	LDA	#VAR06#
!!!VAR06-LSRS!!!
	STA 	temp11

	LDA	#VAR07#
!!!VAR07-LSRS!!!
	STA	temp12

*
*	(Matrix - 1)
*
#NAME#_MiniMap_MaxX = #CON02#
#NAME#_MiniMap_MaxY = #CON03#

#NAME#_MiniMap_Toplevel
*
*	Should be between 0 and 30!
*
	LDA	temp11
	CMP	#30
	BCC	#NAME#_MiniMap_NotLarger_30
	LDA	#30
#NAME#_MiniMap_NotLarger_30
	CLC
	ADC	#73
	STA	temp11

	LDX	temp01
	DEX
	STX	temp19

	LDA	temp12
	CMP	temp19
	BCC	#NAME#_MiniMap_NotLarger_temp12
	LDA	temp19
#NAME#_MiniMap_NotLarger_temp12
	STA	temp12

	LDA	##NAME#_MiniMap_MaxX
	CMP	temp02
	BCS	#NAME#_MiniMap_NotLarger_temp02
	STA	temp02
#NAME#_MiniMap_NotLarger_temp02

	LDA	temp02
	ASL
	ASL
	TAX
	LDA	#NAME#_MiniMap_PointerTable,x
	STA	temp07
	LDA	#NAME#_MiniMap_PointerTable+1,x
	STA	temp08

	LDA	temp02
	ASL
	ASL
	TAX
	LDA	#NAME#_MiniMap_PointerTable+2,x
	STA	temp09
	LDA	#NAME#_MiniMap_PointerTable+3,x
	STA	temp10

	LDA	##NAME#_MiniMap_MaxY
	CMP	temp03
	BCS	#NAME#_MiniMap_NotLarger_temp03
	STA	temp03
#NAME#_MiniMap_NotLarger_temp03

	LDX	temp03
	LDA	#0
	CLC
#NAME#_MiniMap_Loop_DimensionY
	DEX
	BMI	#NAME#_MiniMap_Loop_DimensionY_Ended
	ADC	temp01
	JMP	#NAME#_MiniMap_Loop_DimensionY

#NAME#_MiniMap_Loop_DimensionY_Ended
	STA	temp19
	ADC	temp07
	STA	temp07

	LDA	temp19
	ADC	temp09
	STA	temp09

	LDA	#<#NAME#_MiniMap_Gradient
	STA	temp13
	LDA	#>#NAME#_MiniMap_Gradient
	STA	temp14

#NAME#_MiniMap_Kernel
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1
	STA	COLUPF
	STX	PF0
	STX	PF1
	STX	GRP0
	STX	GRP1
	STX	ENABL
	STX	ENAM0
	STX	ENAM1	

	STX	HMCLR
	sleep	3
	STA	RESP0
	sleep	3
	STA	RESP1

	LDA	#$00
	STA	RESM1
	STA	HMP0
	LDA	#$20
	STA	HMP1

	LDA	#$F5
	STA	NUSIZ0
	STA	NUSIZ1

	STA	WSYNC

	LDA	#255
	STA	GRP0
	STA	GRP1
	STA	PF2

	LDA	#%00000001
	STA	CTRLPF

	LDY	temp01
	DEY	

	LDA	(temp13),y
	ADC	temp04
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1
	STA	temp19

	CPY 	temp12
	BNE	#NAME#_MiniMap_Kernel_Not_Enabled
	LDA	#2
	JMP	#NAME#_MiniMap_Kernel_Enabled
#NAME#_MiniMap_Kernel_Not_Enabled
	sleep	3
	LDA	#0
#NAME#_MiniMap_Kernel_Enabled
	STA	temp15

	STA	WSYNC
	sleep	6
	LDA	temp11

#NAME#_MiniMap_Kernel_BallX_Loop
	SBC	#15
	BCS	#NAME#_MiniMap_Kernel_BallX_Loop
	sleep	5
	STA	RESBL
	ADC	#16
	TAX
	LDA	#NAME#_Kernel_FineAdjustTable,x	
	STA	HMBL	
	STA	WSYNC
	STA	HMOVE

	LDA	#<#NAME#_MiniMap_Kernel_Reset
	STA	temp16
	LDA	#>#NAME#_MiniMap_Kernel_Reset
	STA	temp17

	_sleep	26	

	LDA	#%00001111
	STA	ENAM1
	STA	PF2

	LDA	temp19
	TAX
	TXS
	JMP	#BANK#_MiniMap_Kernel_MainLoop

	_align	16

#NAME#_Kernel_FineAdjustTable
	byte	#$80
	byte	#$70
	byte	#$60
	byte	#$50
	byte	#$40
	byte	#$30
	byte	#$20
	byte	#$10
	byte	#$00
	byte	#$f0
	byte	#$e0
	byte	#$d0
	byte	#$c0
	byte	#$b0
	byte	#$a0
	byte	#$90

#NAME#_MiniMap_Kernel_Reset
	LDA	frameColor
	STA	WSYNC		
	STA	COLUBK
	STA	COLUPF
	STX	GRP0
	STX	GRP1
	STA	COLUP0
	STA	COLUP1
	STX	PF2
