
*
*	temp01:	Calculated X
*	temp02 - temp16: X with offset
*
*	#VAR01#: Controller variable
*		 0-3: 	Cooldown (not editable!)
*		 4-6: 	Wind power and direction
*		 7:	Fade In/Out
*	#VAR02#: Smoke Color
*	#VAR03#: Background Color
*

#NAME#_Smoke
	LDA	frameColor
	LDX	#0
	STA	WSYNC		; 76
	
	STA	COLUBK		
	STA	COLUPF		
	STA	COLUP0
	STA	COLUP1		; 12

	STX	PF0
	STX	PF1
	STX	PF2
	STX	GRP0
	STX	GRP1		; 15 (27
	STX	NUSIZ0
	STX	REFP0		; 3 (63)
	STX	NUSIZ1
	STX	REFP1		
	STX	HMCLR

	LDA	#79	; 3 (30)
	STA	temp01		; 3 (33)

	JMP	#NAME#_Smoke_InsideJumpTable
	align	256

#NAME#_Smoke_FineAdjustTable256	
	fill	7
#NAME#_Smoke_InsideJumpTable

	LDA	#VAR01#
	BMI	#NAME#_Smoke_Off
	LDA	#<#NAME#_Smoke_Pattern_0
	STA	temp19
	JMP	#NAME#_Smoke_On
#NAME#_Smoke_Off
	LDA	#<#NAME#_Smoke_Pattern_1
	STA	temp19
#NAME#_Smoke_On

	LDX	#0
	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	Bank2_No_Smoke_Counter
	
	LDA	#VAR01#
	AND	#%00001111
	CMP	#%00001111
	BEQ	Bank2_No_Smoke_Counter
	TAY
	INY
	STY	temp18
	LDA	#VAR01#	
	AND	#%11110000
	ADC	temp18
	STA	#VAR01#
	
Bank2_No_Smoke_Counter

	LDA	counter
	AND	#%00111111
	LSR
	LSR
	TAY	
#NAME#_Smoke_Set_HorPoz
	LDA	#NAME#_Smoke_PointerNum,y
	SEC
	SBC	#6

	CLC
	ADC	temp01,x
	STA	temp02,x
	INX
	INY
	CPX	#15	
	BNE	#NAME#_Smoke_Set_HorPoz
	JMP	#NAME#_Smoke_Set_HorPoz_Ended	


#NAME#_Smoke_Movement
	BYTE	#249
	BYTE	#250
	BYTE	#251
	BYTE	#252
	BYTE	#253
	BYTE	#254
	BYTE	#255
	BYTE	#0
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#4
	BYTE	#5
	BYTE	#6
	BYTE	#7
	BYTE	#8

#NAME#_Smoke_Back_Gradient
### &COLOR
!!!GRADIENT2!!!

#NAME#_Smoke_Gradient
### &COLOR
!!!GRADIENT1!!!

#NAME#_Smoke_AND
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#15
	BYTE	#15
	BYTE	#15
	BYTE	#15
	BYTE	#15
	BYTE	#15
	BYTE	#15
	BYTE	#15

#NAME#_Smoke_PointerNum
	BYTE	#7
	BYTE	#8
	BYTE	#9
	BYTE	#10
	BYTE	#9
	BYTE	#8
	BYTE	#7
	BYTE	#6
	BYTE	#5
	BYTE	#4
	BYTE	#3
	BYTE	#2
	BYTE	#3
	BYTE	#4
	BYTE	#5
	BYTE	#6
	BYTE	#7
	BYTE	#8
	BYTE	#9
	BYTE	#10
	BYTE	#9
	BYTE	#8
	BYTE	#7
	BYTE	#6
	BYTE	#5
	BYTE	#4
	BYTE	#3
	BYTE	#2
	BYTE	#3
	BYTE	#4
	BYTE	#5
	BYTE	#6

#NAME#_Smoke_Pattern_0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
#NAME#_Smoke_Pattern_1
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#255
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0

#NAME#_Smoke_MASK
	BYTE	#%00111100
	BYTE	#%01111110
	BYTE	#%11111111
	BYTE	#%11111111
	BYTE	#%11111111
	BYTE	#%01111100
	BYTE	#%01111100
	BYTE	#%01111100
	BYTE	#%01111100
	BYTE	#%01111000
	BYTE	#%01111100
	BYTE	#%00111000
	BYTE	#%00111000
	BYTE	#%00111000
	BYTE	#%00010000
	BYTE	#%00000000

#NAME#_Smoke_FineAdjustTable
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

#NAME#_Smoke_Set_HorPoz_Ended

	LDA	#VAR01#
	AND	#%01110000
	LSR
	LSR
	LSR
	LSR
	SEC
	SBC	#4
	STA	temp18


	LDX	#15
	LDY	#0
	
#NAME#_Smoke_Add_Wind_Loop
	TYA
	CLC
	ADC	temp18	
	TAY

	CLC
	ADC	temp02,x	
	STA	temp02,x
	DEX
	BPL	#NAME#_Smoke_Add_Wind_Loop

*****	STA	WSYNC
	LDX	#0
	LDA	#$08
	STA	COLUP0

	LDA	#>#NAME#_Smoke_Pattern_0
	STA	temp18
	LDA	temp19
	STA	temp17

	LDA	#NAME#_Smoke_Gradient	
	ADC	#VAR02#			
	STA	COLUP0			

	LDA	#VAR01#			
	AND	#%00001111		
	STA	temp19			
	TXA				
	ADC	temp19			
	TAY				
	LDA	(temp17),y		
	STA	temp19

	JMP	#NAME#_Smoke_Draw_Loop_0

	_align	150

#NAME#_Smoke_Draw_Loop_0	
	
	STA	WSYNC
	LDA	#0
	STA	GRP0
	LDA	temp02,x
#NAME#_Smoke_Draw_Loop_Hor_0
	SBC	#15
	BCS	#NAME#_Smoke_Draw_Loop_Hor_0
	TAY
	sleep	3
	STA	RESP0
	LDA	#NAME#_Smoke_FineAdjustTable256,y
	STA	HMP0

	LDA	#NAME#_Smoke_Back_Gradient,x		
	STA	WSYNC			; 76
	STA	HMOVE			; 3
	ADC	#VAR03#	
	STA	COLUBK			; 3 (6)

	LDA	temp19			; 3 (9)
	AND	#NAME#_Smoke_MASK,x	; 5 (14)
	STA	GRP0			; 3 (17)

	CLC				; 2 (19)
	INX

	LDA	#VAR01#			; 2 (27)
	AND	#%00001111		; 2 (29)
	STA	temp19			; 3 (32)
	TXA				; 2 (34)
	ADC	temp19			; 3 (37)
	TAY				; 2 (39)
	LDA	(temp17),y		; 5 (44)
	STA	temp19			; 3 (47)

	LDA	#NAME#_Smoke_Gradient,x	; 5 (53)
	ADC	#VAR02#			; 3 (56)
	STA	COLUP1			; 3 (59)
	LDA	#0
	STA	HMP0

#NAME#_Smoke_Draw_Loop_1	
	
	STA	WSYNC
	LDA	#0
	STA	GRP1
	LDA	temp02,x
#NAME#_Smoke_Draw_Loop_Hor_1
	SBC	#15
	BCS	#NAME#_Smoke_Draw_Loop_Hor_1
	TAY
	sleep	3
	STA	RESP1
	LDA	#NAME#_Smoke_FineAdjustTable256,y
	STA	HMP1

	LDA	#NAME#_Smoke_Back_Gradient,x		
	STA	WSYNC			; 76
	STA	HMOVE			; 3
	ADC	#VAR03#	
	STA	COLUBK			; 3 (6)

	LDA	temp19			; 3 (9)
	AND	#NAME#_Smoke_MASK,x	; 5 (14)
	STA	GRP1			; 3 (17)

	CLC				; 2 (19)
	INX				; 2 (21)
	CPX	#16			; 2 (23)
	BEQ	#NAME#_Smoke_Reset	; 2 (25)

	LDA	#VAR01#			; 2 (27)
	AND	#%00001111		; 2 (29)
	STA	temp19			; 3 (32)
	TXA				; 2 (34)
	ADC	temp19			; 3 (37)
	TAY				; 2 (39)
	LDA	(temp17),y		; 5 (44)
	STA	temp19			; 3 (47)

	LDA	#NAME#_Smoke_Gradient,x	; 5 (53)
	ADC	#VAR02#			; 3 (56)
	STA	COLUP0			; 3 (59)
	LDA	#0
	STA	HMP1

	JMP	#NAME#_Smoke_Draw_Loop_0	; 3 (62)

#NAME#_Smoke_Reset
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STX	GRP0
	STX	GRP1
	stx	HMCLR