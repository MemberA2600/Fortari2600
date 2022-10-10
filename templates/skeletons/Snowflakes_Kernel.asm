#BANK#_SnowFlakes_Kernel
	LDX	#0
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK
	STX	GRP0
	STX	GRP1
	STX	PF0
	STX	PF1
	STX	PF2
	STX	ENAM0
	STX	ENAM1
	STX	ENABL
	STX	NUSIZ0
	
	LDA	temp05
	AND	#%00000011
	ASL
	TAX
	LDA	#BANK#_SnowFlakes_Patterns,x
	STA	temp06
	LDA	#BANK#_SnowFlakes_Patterns+1,x	
	STA	temp07

	LDA	temp01
	LSR
	LSR
	AND	#%00001111
*******	STA	temp01

*
*	Y has the lines
*	X has the offset
*

	TAX
	TAY
	LDA	(temp06),y
	STA	temp04

	LDY	temp11

	TXA
	AND	#%00000011
	TAX
	TXS

	LDA	#$03
	STA	NUSIZ0

	JMP	#BANK#_SnowFlakes_Loop

	align	256
#BANK#_SnowFlakes_Kernel_FineAdjustment256
	fill	17
#BANK#_SnowFlakes_Loop

	LDA	#BANK#_SnowFlakes_Base_X0,x	
	CLC
	ADC	temp04				
	STA	temp18				; 13

	DEX			
	TXA
	AND	#%00000011
	TAX

	LDA	#BANK#_SnowFlakes_Base_X1,x	
	CLC
	ADC	temp04				
	STA	temp19				; 13

	TXS

	DEC	temp12
	BPL	#BANK#_SnowFlakes_Still_Counts
	LDA	temp10
	JMP	#BANK#_SnowFlakes_Still_JumpHere
#BANK#_SnowFlakes_Still_Counts
	LDA	temp10
	EOR	#2
#BANK#_SnowFlakes_Still_JumpHere
	STA	temp17

	LDA	#BANK#_SnowFlakes_SnowColorBase,y
	CMP	#$08
	BCC	#BANK#_SnowFlakes_Smaller_Than_8

	ADC	temp02
	JMP	#BANK#_SnowFlakes_SaveColors
#BANK#_SnowFlakes_Smaller_Than_8
	sleep	3
	ADC	temp03
#BANK#_SnowFlakes_SaveColors
	STA	COLUP0
	STA	COLUP1

	LDA	#0
#BANK#_SnowFlakes_Set_X0
	sta	WSYNC
	STA	ENAM0
	STA	ENAM1	

  	LDA	temp18
#BANK#_SnowFlakes_Set_X0_Loop
	SBC	#15
	BCS	#BANK#_SnowFlakes_Set_X0_Loop
	sleep	3
	TAX
	STA	RESM0
	LDA	#BANK#_SnowFlakes_Kernel_FineAdjustment256,x
#BANK#_SnowFlakes_Set_X1
	STA	WSYNC
	STA	HMM0
	sleep	3

	LDA	temp19
#BANK#_SnowFlakes_Set_X1_Loop
	SBC	#15
	BCS	#BANK#_SnowFlakes_Set_X1_Loop	
	TAX
	sleep	3
	STA	RESM1
	LDA	#BANK#_SnowFlakes_Kernel_FineAdjustment256,x
	STA	HMM1

	STA	WSYNC
	STA	HMOVE
	
	TSX
	LDA	(temp08),y		; 5 
	ADC	temp03			; 3 
	STA	COLUBK			; 3 

	LDA	temp17
	STA	ENAM0
	STA	ENAM1

	DEY	
	BMI	#BANK#_SnowFlakes_Loop_End_Jumper
	JMP	#BANK#_SnowFlakes_Loop
#BANK#_SnowFlakes_Loop_End_Jumper
	JMP	#BANK#_SnowFlakes_Loop_End

#BANK#_SnowFlakes_SnowColorBase
	BYTE	#$0E
	BYTE	#$0E	
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0E
	BYTE	#$0C
	BYTE	#$0A
	BYTE	#$08	
	BYTE	#$06
	BYTE	#$04
	BYTE	#$02
	BYTE	#$00

#BANK#_SnowFlakes_Base_X0
	BYTE	#24
	BYTE	#32
	BYTE	#104
	BYTE	#112

#BANK#_SnowFlakes_Base_X1
	BYTE	#72
	BYTE	#88
	BYTE	#80
	BYTE	#96

#BANK#_SnowFlakes_Patterns
	BYTE	#<#BANK#_SnowFlakes_Adder1
	BYTE	#>#BANK#_SnowFlakes_Adder1
	BYTE	#<#BANK#_SnowFlakes_Adder2
	BYTE	#>#BANK#_SnowFlakes_Adder2
	BYTE	#<#BANK#_SnowFlakes_Adder3
	BYTE	#>#BANK#_SnowFlakes_Adder3
	BYTE	#<#BANK#_SnowFlakes_Adder4
	BYTE	#>#BANK#_SnowFlakes_Adder4

#BANK#_SnowFlakes_Adder1
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3		; 16

#BANK#_SnowFlakes_Adder2
	BYTE	#3
	BYTE	#3
	BYTE	#2
	BYTE	#2
	BYTE	#1
	BYTE	#1
	BYTE	#2
	BYTE	#2
	BYTE	#3
	BYTE	#3
	BYTE	#4
	BYTE	#4
	BYTE	#5
	BYTE	#5
	BYTE	#4
	BYTE	#4		; 16

#BANK#_SnowFlakes_Adder3
	BYTE	#3
	BYTE	#3
	BYTE	#2
	BYTE	#2
	BYTE	#3
	BYTE	#3
	BYTE	#4
	BYTE	#4
	BYTE	#3
	BYTE	#2
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#4
	BYTE	#5
	BYTE	#4		; 16

#BANK#_SnowFlakes_Adder4
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#4
	BYTE	#5
	BYTE	#6
	BYTE	#7
	BYTE	#8
	BYTE	#7
	BYTE	#6
	BYTE	#5
	BYTE	#4
	BYTE	#3
	BYTE	#2
	BYTE	#1
	BYTE	#0		; 16

#BANK#_SnowFlakes_Kernel_FineAdjustment
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
	byte	#$90		; 16
	

#BANK#_SnowFlakes_Loop_End
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1
	STX	ENAM0
	STX	ENAM1

	JMP	(temp13)