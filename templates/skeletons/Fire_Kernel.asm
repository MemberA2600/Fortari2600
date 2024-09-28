#NAME#_Fire
	LDA	frameColor
	LDX	#0
	STA	WSYNC		; 76
	
	STA	COLUBK		
	STA	COLUPF		
	STX	GRP0
	STX	GRP1	
	STX	ENAM0	
	STX	PF0
	STX	PF1
	STX	PF2		; 24

	LDA	frameColor
	AND	#%11111110
	STA	temp19

	LDA	#%00000001
	STA	CTRLPF

	LDY	#0
	LDA	#VAR01#
	BPL	#NAME#_Fire_Up
	AND	#%00001111
	CMP	#%00000000

	BEQ	#NAME#_Fire_NoFire	
	TAY
	LDA	counter	
	AND 	#%00000011
	CMP	#%00000011
	BNE	#NAME#_Fire_FadeOut_NoINY
	DEY
	JMP	#NAME#_Fire_FadeOut_NoINY
#NAME#_Fire_NoFire	
	LDY	#15
	sleep	21

	JMP	#NAME#_Fire_FadeOut_DoneBullShit

#NAME#_Fire_Up
	AND	#%00001111
	CMP	#%00001111

	BEQ	#NAME#_Fire_FadeOut_NoBullShit
	TAY
	LDA	counter	
	AND 	#%00000011
	CMP	#%00000011
	BNE	#NAME#_Fire_FadeOut_NoINY
	INY
#NAME#_Fire_FadeOut_NoINY
	STY	temp18
	LDA	#VAR01#
	AND	#%11110000
	ORA	temp18
	STA	#VAR01#
	LDA	#NAME#_Fire_Inverted,y	
	TAY
	JMP	#NAME#_Fire_FadeOut_DoneBullShit

#NAME#_Fire_FadeOut_NoBullShit
	sleep	26
#NAME#_Fire_FadeOut_DoneBullShit
	STY	temp18

	LDY	#0
#NAME#_Fire_FadeOut_BG
	STA	WSYNC
	
	LDA	temp19				; 3	
	AND	#%00001111			; 2 (5)
	CMP	#0				; 2 (7)
	BEQ	#NAME#_Fire_FadeOut_BG_END	; 2 (9)
	LDX	temp19				; 3 (12)
	DEX					; 2 (14)
	DEX					; 2 (16)
	STX	COLUBK				; 3 (19)
	STX	temp19				; 3 (22)
	INY
	JMP	#NAME#_Fire_FadeOut_BG		

#NAME#_Fire_FadeOut_BG_END
	STA	WSYNC
	LDA	#$00
	STA	COLUBK
	STA	COLUPF
	INY
	CPY	#8
	BNE	#NAME#_Fire_FadeOut_BG_END	

!!!PARTICLES!!!

*
*	This is where the flames begin
*
#NAME#_Fire_Flames
	LDA	counter
	LDY	##SPEED#
#NAME#_Fire_Speed_Setter
	DEY
	BMI	#NAME#_Fire_Speed_Setter_END
	LSR
	JMP	#NAME#_Fire_Speed_Setter
#NAME#_Fire_Speed_Setter_END	

	CLC
	AND	#%00001111
	STA	temp19
	LDA	#32
	SEC
	SBC	temp19	
	TAX

	LDA	#>#NAME#_Fire_Shape_0
	STA	temp02
	STA	temp04	
	STA	temp06	

	TXA
	AND	#15
	TAY
	LDA	#NAME#_Fire_Shapes,y
	SEC
	ADC	temp18
	STA	temp01	

	TXA
	ADC	#3
	AND	#15
	TAY
	LDA	#NAME#_Fire_Shapes,y
	SEC
	ADC	temp18
	STA	temp03	

	TXA
	ADC	#6
	AND	#15
	TAY
	LDA	#NAME#_Fire_Shapes,y
	SEC
	ADC	temp18
	STA	temp05	

	LDY	#15

	LDA	(temp01),y		
	STA	temp07			
	LDA	(temp03),y		
	STA	temp08		
	LDA	(temp05),y		
	STA	temp09		

	JMP	#NAME#_Fire_Loop

	_align	210
#NAME#_Fire_Inverted
	BYTE	#15
	BYTE	#14
	BYTE	#13
	BYTE	#12
	BYTE	#11
	BYTE	#10
	BYTE	#9
	BYTE	#8
	BYTE	#7
	BYTE	#6
	BYTE	#5
	BYTE	#4
	BYTE	#3
	BYTE	#2
	BYTE	#1
	BYTE	#0

#NAME#_Fire_Color
### &COLOR
!!!FIRE_COLORS!!!

#NAME#_Fire_Shapes
	BYTE	#<#NAME#_Fire_Shape_0
	BYTE	#<#NAME#_Fire_Shape_1
	BYTE	#<#NAME#_Fire_Shape_2
	BYTE	#<#NAME#_Fire_Shape_3
	BYTE	#<#NAME#_Fire_Shape_4
	BYTE	#<#NAME#_Fire_Shape_5
	BYTE	#<#NAME#_Fire_Shape_6
	BYTE	#<#NAME#_Fire_Shape_7
	BYTE	#<#NAME#_Fire_Shape_7
	BYTE	#<#NAME#_Fire_Shape_6
	BYTE	#<#NAME#_Fire_Shape_5
	BYTE	#<#NAME#_Fire_Shape_4
	BYTE	#<#NAME#_Fire_Shape_3
	BYTE	#<#NAME#_Fire_Shape_2
	BYTE	#<#NAME#_Fire_Shape_1
	BYTE	#<#NAME#_Fire_Shape_0

#NAME#_Fire_Shape_0
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000001
	byte	#%00000011
	byte	#%00000111
	byte	#%10000011
	byte	#%10000011
	byte	#%11000011
	byte	#%11100001
	byte	#%11110000
	byte	#%11111000
	byte	#%11111100
	byte	#%11111100
	byte	#%11111110
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_1
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000001
	byte	#%00000011
	byte	#%00000011
	byte	#%00000111
	byte	#%10000111
	byte	#%10000111
	byte	#%11000011
	byte	#%11100001
	byte	#%11110001
	byte	#%11111001
	byte	#%11111101
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_2
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000001
	byte	#%00000011
	byte	#%00000011
	byte	#%00000111
	byte	#%00000111
	byte	#%10000111
	byte	#%11000011
	byte	#%11000011
	byte	#%11100001
	byte	#%11110001
	byte	#%11111001
	byte	#%11111011
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_3
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000001
	byte	#%10000001
	byte	#%10000011
	byte	#%10000011
	byte	#%10000011
	byte	#%11000011
	byte	#%11000011
	byte	#%11100111
	byte	#%11110111
	byte	#%11110111
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_4
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%10000000
	byte	#%10000000
	byte	#%10000000
	byte	#%11000001
	byte	#%11000001
	byte	#%11000001
	byte	#%11000011
	byte	#%11000111
	byte	#%11100111
	byte	#%11101111
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_5
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%11000000
	byte	#%11000000
	byte	#%11100000
	byte	#%11100000
	byte	#%11100000
	byte	#%11100001
	byte	#%11000001
	byte	#%11000011
	byte	#%11000111
	byte	#%11011111
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_6
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%10000000
	byte	#%11000000
	byte	#%11100000
	byte	#%11110000
	byte	#%11110000
	byte	#%11110000
	byte	#%11100000
	byte	#%11100001
	byte	#%11100011
	byte	#%11000111
	byte	#%10001111
	byte	#%10111111
	byte	#%11111111
	byte	#%11111111

#NAME#_Fire_Shape_7
	byte	#%00000000
	byte	#%00000000	
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%10000000
	byte	#%11000000
	byte	#%11100000
	byte	#%11100000
	byte	#%11100001
	byte	#%11000011
	byte	#%11000111
	byte	#%10001111
	byte	#%00011111
	byte	#%01111111
	byte	#%11111111
	byte	#%11111111

	_align	170

#NAME#_Fire_Loop
	STA	WSYNC
	LDA	#NAME#_Fire_Color,x	; 5
	STA	COLUBK			; 3 (8)

	LDA	#255			; 2 (10)
	CMP	temp18			; 3 (13)
	BEQ	#NAME#_Fire_No_Black	; 2 (15)
	LDA	#0			; 2 (17)
	STA	COLUBK			; 3 (20)
	DEC	temp18			; 5 (25)

	sleep	5

	JMP	#NAME#_Fire_Nothing

#NAME#_Fire_No_Black
	LDA	temp07			; 3 (18)
	STA	PF0			; 3 (21)
	LDA	temp08			; 3 (24)
	STA	PF1			; 3 (27)
	LDA	temp09			; 3 (30)
	STA	PF2			; 3 (33)


#NAME#_Fire_Nothing

	STA	WSYNC

	DEX	
	DEY

	LDA	(temp05),y		
	STA	temp09	

	LDA	(temp03),y		
	STA	temp08	

	LDA	(temp01),y		
	STA	temp07	

	CPY	#255
	BNE	#NAME#_Fire_Loop

#NAME#_Fire_Reset

	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	STA	COLUPF
	STX	PF0
	STX	PF1
	STX	PF2