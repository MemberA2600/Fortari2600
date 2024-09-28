*
*	#VAR01#:	X position of Sun / Moon
*	#VAR02#:	Hours, binary, 0-23
*			0-4: Hours
*			7  : Auto Increment
*
*	#VAR03#:	SpriteNum, auto increment, wind
*			0-3: SpriteNUm
*			4-6: Wind
*			7  : Auto Increment
*
*	#var04#:	x Position of first Cloud
*

#NAME#_DayTime_L = 35
#NAME#_DayTime_R = 128
#NAME#_DayTime_Add = 63
#NAME#_DayTime_L2 = 29
#NAME#_DayTime_R2 = 134

#NAME#_DayTime_Kernel

	LDA	frameColor
	LDX	#0
	STA	WSYNC		; 76

	STA	COLUBK		; 3 
	STA	COLUPF		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)

	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STX	ENABL		; 15 (27)
	STX	PF0		
	STX	PF1
	STX	PF2		; 9 (36)
	STX	REFP1
*
*	All sprites are double width
*
*	Since clouds should be above the Sun, Sun must be p1.
*
	LDA	#$05
	STA	NUSIZ0	
	STA	NUSIZ1		; 8 (44)

!!!SunMoonX!!!
	LDA	#0
	STA	CTRLPF

	LDA	#VAR03#
	AND	#%11110000
	STA	temp17

	sta	WSYNC
	sleep	6
	LDA	#VAR01#
#NAME#_DayTime_DivideLoop
	sbc	#15
   	bcs	#NAME#_DayTime_DivideLoop
	sleep	5
   	sta	RESP1
	TAY
   	lda	#NAME#_DayTime_FineAdjustTable256,Y
   	sta	HMP1	

	sta	WSYNC
	STA	HMOVE

******* Controller
*
*	Check if hours are between 0-23
*
	LDA	#VAR02#
	AND	#%11100000	
	STA	temp10
	BPL	#NAME#_DayTime_NoTimeINC
	LDA	#VAR02#
	AND	#%00011111
	TAX
	LDA	counter
******  speed
!!!LSRs!!!


	AND	#%00000111
	CMP	#%00000111
	BNE	#NAME#_DayTime_NoTimeINC2

	INX
#NAME#_DayTime_NoTimeINC2
	TXA
	STA	#VAR02#
	JMP	#NAME#_DayTime_TimeINCDone

#NAME#_DayTime_NoTimeINC
	sleep	18	
	LDA	#VAR02#
	AND	#%00011111
	STA	#VAR02#

#NAME#_DayTime_TimeINCDone

	LDA	#23
	CMP	#VAR02#
	BCS 	#NAME#_DayTime_Not_Larger2

	LDA	#0
	STA	#VAR02#
#NAME#_DayTime_Not_Larger2
	LDA	#VAR02#
	TAX
*
*	Set sky pointer to temp04, temp05
*
	LDA	#NAME#_DayTime_Sky_LOW,x
	STA	temp04
	LDA	#>#NAME#_DayTime_Skies
	STA	temp05
*
*	Set the Y on the sky to temp03
*

	LDA	#NAME#_DayTime_Y,x
	STA	temp03

*
*	Load cloud basecolor
*

	LDA	#NAME#_DayTime_CloudColors,x
	STA	temp14

	LDA	#NAME#_DayTime_StarColors,x
	STA	temp18

	TXA
	LSR	
	TAX

*
*	Set sprite pointer to temp05 - temp06
*	Set color  pointer to temp07 - temp08
*
	LDA	#VAR02#

	CMP	#6
	BCC	#NAME#_DayTime_ItsMoon

	CMP	#19
	BCS	#NAME#_DayTime_ItsMoon

	LDA	#<#NAME#_Sun_DayTime_Sprite
	STA	temp06
	LDA	#>#NAME#_Sun_DayTime_Sprite
	STA	temp07
	
	LDA	#<#NAME#_Sun_DayTime_SpriteColor
	STA	temp08
	LDA	#>#NAME#_Sun_DayTime_SpriteColor
	STA	temp09

	JMP 	#NAME#_DayTime_ItWasSun
#NAME#_DayTime_ItsMoon

	sleep	3
	LDA	#<#NAME#_Moon_DayTime_Sprite
	STA	temp06
	LDA	#>#NAME#_Moon_DayTime_Sprite
	STA	temp07
	
	LDA	#<#NAME#_Moon_DayTime_SpriteColor
	STA	temp08
	LDA	#>#NAME#_Moon_DayTime_SpriteColor
	STA	temp09

#NAME#_DayTime_ItWasSun
******  Controller
	LDA	#VAR03#
	BPL	#NAME#_DayTime_NoIncr
	AND	#%00001111
	TAX

	LDA	counter
******  speed
!!!LSRs2!!!
	AND	#%00000111
	CMP	#%00000111
	BNE	#NAME#_DayTime_NoIncr_Again	

	INX
#NAME#_DayTime_NoIncr_Again
	TXA
	AND	#%00001111
	ORA	temp17
	STA	#VAR03#

	JMP	#NAME#_DayTime_INCRDone
#NAME#_DayTime_NoIncr
	sleep	27

#NAME#_DayTime_INCRDone
*
*	Data already in A, drop high nibble 
*	and multiply by 8. 
*
	AND	#%00001111
	ASL
	ASL
	ASL
	CLC
	ADC	temp06
	STA	temp06

	LDA	#0
	STA	HMP1

	LDA	#VAR02#
	ORA	temp10
	STA	#VAR02#
*
*	Set Cloud things!
*
	LDA	#VAR03#
	LSR
	LSR
	LSR
	LSR
	AND	#%00000111
	STA	temp11
*
*	Set first Clouds's X
*
	TAY
	LDA	#NAME#_DayTime_Wind_X,y
	CLC
	ADC	#VAR04#
	STA	#VAR04#
*
*	If larger than 4, clouds more right 
*	and should be mirrored
*	

	TYA
	ASL
	STA	REFP0
*
*	Set cloud sprite
*
	LDA	#<#NAME#_Cloud_DayTime_Sprite
	STA	temp12
	LDA	#>#NAME#_Cloud_DayTime_Sprite
	STA	temp13

	LDA	temp11
	TAX
	LDY	#NAME#_DayTime_Wind_Sprite_Wait,x	
	
	LDA	counter
	LSR
#NAME#_DayTime_Sprite_Wait
	LSR
	DEY	
	BPL	#NAME#_DayTime_Sprite_Wait

	ASL
	ASL
	AND	#%00001100
	ADC	temp12
	STA	temp12

	LDY	#15
	STY	temp19

	LDA	#VAR04#

	STA	temp10
	STA	temp11

	LDA	#0
	STA	temp16
	STA	temp17

	LDA	(temp04),y		
	JMP	#NAME#_DayTime_Loop

	align	256

#NAME#_DayTime_FineAdjustTable256
	fill	3

#NAME#_DayTime_Star_X
	BYTE	#7
	BYTE	#23
	BYTE	#31
	BYTE	#9
	BYTE	#14
	BYTE	#27
	BYTE	#12
	BYTE	#19

#NAME#_DayTime_Wind_X
	BYTE	#253
	BYTE	#254
	BYTE	#255
	BYTE	#0
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#3

#NAME#_DayTime_Wind_Sprite_Wait
	BYTE	#0
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#2
	BYTE	#1
	BYTE	#0
	BYTE	#0

#NAME#_Moon_DayTime_Sprite
	byte	#%00111100	; (0)
	byte	#%01111110
	byte	#%11111111
	byte	#%11111111
	byte	#%11111111
	byte	#%11111111
	byte	#%01111110
	byte	#%00111100
	byte	#%00111100	; (1)
	byte	#%01111110
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%01111110
	byte	#%00111100
	byte	#%00111110	; (2)
	byte	#%01111110
	byte	#%11111100
	byte	#%11111100
	byte	#%11111100
	byte	#%11111100
	byte	#%01111110
	byte	#%00111110
	byte	#%00111110	; (3)
	byte	#%01111100
	byte	#%11111000
	byte	#%11111000
	byte	#%11111000
	byte	#%11111000
	byte	#%01111100
	byte	#%00111110
	byte	#%00111110	; (4)
	byte	#%01111000
	byte	#%11110000
	byte	#%11110000
	byte	#%11110000
	byte	#%11110000
	byte	#%01111000
	byte	#%00111110
	byte	#%00111100	; (5)
	byte	#%01110000
	byte	#%11100000
	byte	#%11100000
	byte	#%11100000
	byte	#%11100000
	byte	#%01110000
	byte	#%00111100
	byte	#%00111000	; (6)
	byte	#%01100000
	byte	#%11000000
	byte	#%11000000
	byte	#%11000000
	byte	#%11000000
	byte	#%01100000
	byte	#%00111000
	byte	#%00110000	; (7)
	byte	#%01000000
	byte	#%10000000
	byte	#%10000000
	byte	#%10000000
	byte	#%10000000
	byte	#%01000000
	byte	#%00110000
	byte	#%00000000	; (8)
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00000000
	byte	#%00001100	; (9)
	byte	#%00000010
	byte	#%00000001
	byte	#%00000001
	byte	#%00000001
	byte	#%00000001
	byte	#%00000010
	byte	#%00001100
	byte	#%00011100	; (10)
	byte	#%00000110
	byte	#%00000011
	byte	#%00000011
	byte	#%00000011
	byte	#%00000011
	byte	#%00000110
	byte	#%00011100
	byte	#%00111100	; (11)
	byte	#%00001110
	byte	#%00000111
	byte	#%00000111
	byte	#%00000111
	byte	#%00000111
	byte	#%00001110
	byte	#%00111100
	byte	#%00111100	; (12)
	byte	#%00011110
	byte	#%00001111
	byte	#%00001111
	byte	#%00001111
	byte	#%00001111
	byte	#%00011110
	byte	#%00111100
	byte	#%01111100	; (13)
	byte	#%00111110
	byte	#%00011111
	byte	#%00011111
	byte	#%00011111
	byte	#%00011111
	byte	#%00111110
	byte	#%01111100
	byte	#%01111100	; (14)
	byte	#%01111110
	byte	#%00111111
	byte	#%00111111
	byte	#%00111111
	byte	#%00111111
	byte	#%01111110
	byte	#%01111100
	byte	#%00111100	; (15)
	byte	#%01111110
	byte	#%01111111
	byte	#%01111111
	byte	#%01111111
	byte	#%01111111
	byte	#%01111110
	byte	#%00111100

#NAME#_Moon_DayTime_SpriteColor
### &COLOR
	byte	#$08
	byte	#$0A
	byte	#$0C
	byte	#$0E
	byte	#$0E
	byte	#$0C
	byte	#$0A
	byte	#$08

#NAME#_DayTime_Sky_LOW
	BYTE	#<#NAME#_DayTime_Sky_00
	BYTE	#<#NAME#_DayTime_Sky_00
	BYTE	#<#NAME#_DayTime_Sky_00
	BYTE	#<#NAME#_DayTime_Sky_01
	BYTE	#<#NAME#_DayTime_Sky_01
	BYTE	#<#NAME#_DayTime_Sky_02
	BYTE	#<#NAME#_DayTime_Sky_02
	BYTE	#<#NAME#_DayTime_Sky_03
	BYTE	#<#NAME#_DayTime_Sky_03
	BYTE	#<#NAME#_DayTime_Sky_04
	BYTE	#<#NAME#_DayTime_Sky_04
	BYTE	#<#NAME#_DayTime_Sky_05	; 12

	BYTE	#<#NAME#_DayTime_Sky_05
	BYTE	#<#NAME#_DayTime_Sky_04
	BYTE	#<#NAME#_DayTime_Sky_04
	BYTE	#<#NAME#_DayTime_Sky_06
	BYTE	#<#NAME#_DayTime_Sky_06
	BYTE	#<#NAME#_DayTime_Sky_07
	BYTE	#<#NAME#_DayTime_Sky_07
	BYTE	#<#NAME#_DayTime_Sky_01
	BYTE	#<#NAME#_DayTime_Sky_01
	BYTE	#<#NAME#_DayTime_Sky_00
	BYTE	#<#NAME#_DayTime_Sky_00
	BYTE	#<#NAME#_DayTime_Sky_00	; 24

#NAME#_DayTime_Y
	BYTE	#10
	BYTE	#12
	BYTE	#14
	BYTE	#16
	BYTE	#18
	BYTE	#20
	BYTE	#22
	BYTE	#20
	BYTE	#18
	BYTE	#16
	BYTE	#14
	BYTE	#12
	BYTE	#10
	BYTE	#12
	BYTE	#14
	BYTE	#16
	BYTE	#18
	BYTE	#20
	BYTE	#22
	BYTE	#20
	BYTE	#18
	BYTE	#16
	BYTE	#14
	BYTE	#12
	BYTE	#10		; 25


#NAME#_Cloud_DayTime_Sprite
	byte	#%01110110	; (0)
	byte	#%11111111
	byte	#%01110110
	BYTE	#0

	byte	#%00111010	; (1)
	byte	#%11111111
	byte	#%00111010
	BYTE	#0

	byte	#%01011100	; (2)
	byte	#%11111111
	byte	#%01011100
	BYTE	#0

	byte	#%01101110	; (3)
	byte	#%11111111
	byte	#%01101110
	BYTE	#0

#NAME#_Cloud_DayTime_SpriteColor
### &COLOR
	byte	#$00
	byte	#$02
	byte	#$04
	byte	#$04	

#NAME#_Sun_DayTime_SpriteColor
### &COLOR
	byte	#$0E
	byte	#$1A
	byte	#$1C
	byte	#$1E
	byte	#$1E
	byte	#$1E
	byte	#$1C
	byte	#$1A

#NAME#_DayTime_FineAdjustTable
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

	_align	152

#NAME#_Sun_DayTime_Sprite
	byte	#%00000000	; (0)
	byte	#%01010100
	byte	#%00111000
	byte	#%01111100
	byte	#%11111110
	byte	#%01111100
	byte	#%00111000
	byte	#%01010100
	byte	#%00000000	; (1)
	byte	#%10010010
	byte	#%01010100
	byte	#%00111000
	byte	#%11111110
	byte	#%00111000
	byte	#%01010100
	byte	#%10010010
	byte	#%00000000	; (2)
	byte	#%00000100
	byte	#%10001000
	byte	#%01010000
	byte	#%00111000
	byte	#%00010100
	byte	#%00100010
	byte	#%01000000
	byte	#%00000000	; (3)
	byte	#%00010000
	byte	#%01010100
	byte	#%00111000
	byte	#%11111110
	byte	#%00111000
	byte	#%01010100
	byte	#%00010000
	byte	#%00000000	; (4)
	byte	#%01000000
	byte	#%00100010
	byte	#%00010100
	byte	#%00111000
	byte	#%01010000
	byte	#%10001000
	byte	#%00000100
	byte	#%00000000	; (5)
	byte	#%10010010
	byte	#%01010100
	byte	#%00111000
	byte	#%11111110
	byte	#%00111000
	byte	#%01010100
	byte	#%10010010
	byte	#%00000000	; (6)
	byte	#%10010010
	byte	#%00111000
	byte	#%01000100
	byte	#%01000100
	byte	#%01000100
	byte	#%00111000
	byte	#%10010010
	byte	#%00000000	; (7)
	byte	#%00111000
	byte	#%01000100
	byte	#%10000010
	byte	#%10000010
	byte	#%10000010
	byte	#%01000100
	byte	#%00111000
	byte	#%00000000	; (8)
	byte	#%01111100
	byte	#%10000010
	byte	#%10000010
	byte	#%10010010
	byte	#%10000010
	byte	#%10000010
	byte	#%01111100
	byte	#%00000000	; (9)
	byte	#%00101000
	byte	#%00000000
	byte	#%10010010
	byte	#%00111000
	byte	#%10010010
	byte	#%00000000
	byte	#%00101000
	byte	#%00000000	; (10)
	byte	#%00000000
	byte	#%00010000
	byte	#%00111000
	byte	#%01111100
	byte	#%00111000
	byte	#%00010000
	byte	#%00000000
	byte	#%00000000	; (11)
	byte	#%00010000
	byte	#%01010100
	byte	#%00111000
	byte	#%11111110
	byte	#%00111000
	byte	#%01010100
	byte	#%00010000
	byte	#%00000000	; (12)
	byte	#%00010000
	byte	#%00111000
	byte	#%01111100
	byte	#%11111110
	byte	#%01111100
	byte	#%00111000
	byte	#%00010000
	byte	#%00000000	; (13)
	byte	#%00111000
	byte	#%01111100
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%01111100
	byte	#%00111000
	byte	#%00000000	; (14)
	byte	#%01111100
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%11111110
	byte	#%01111100
	byte	#%00000000	; (15)
	byte	#%00111000
	byte	#%01010100
	byte	#%10111010
	byte	#%11111110
	byte	#%10111010
	byte	#%01010100
	byte	#%00111000

#NAME#_DayTime_CloudColors
### &COLOR
	BYTE	#$02
	BYTE	#$02
	BYTE	#$02
	BYTE	#$04
	BYTE	#$04
	BYTE	#$06
	BYTE	#$06
	BYTE	#$08
	BYTE	#$08
	BYTE	#$0a
	BYTE	#$0a
	BYTE	#$0a			; 12

	BYTE	#$0a
	BYTE	#$0a
	BYTE	#$0a
	BYTE	#$18
	BYTE	#$18
	BYTE	#$36
	BYTE	#$36
	BYTE	#$04
	BYTE	#$04
	BYTE	#$02
	BYTE	#$02
	BYTE	#$02			; 24

	_align	130

#NAME#_DayTime_Skies
#NAME#_DayTime_Sky_00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
#NAME#_DayTime_Sky_01
	BYTE	#$02
	BYTE	#$04
	BYTE	#$02
	BYTE	#$00
	BYTE	#$02
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
#NAME#_DayTime_Sky_02
	BYTE	#$64
	BYTE	#$64
	BYTE	#$62
	BYTE	#$64
	BYTE	#$62
	BYTE	#$62
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
	BYTE	#$60
#NAME#_DayTime_Sky_03
	BYTE	#$84
	BYTE	#$84
	BYTE	#$86
	BYTE	#$84
	BYTE	#$86
	BYTE	#$84
	BYTE	#$86
	BYTE	#$84
	BYTE	#$82
	BYTE	#$82
	BYTE	#$82
	BYTE	#$82
	BYTE	#$82
	BYTE	#$80
	BYTE	#$80
	BYTE	#$80
#NAME#_DayTime_Sky_03
	BYTE	#$88
	BYTE	#$8a
	BYTE	#$8a
	BYTE	#$88
	BYTE	#$86
	BYTE	#$86
	BYTE	#$88
	BYTE	#$84
	BYTE	#$82
	BYTE	#$84
	BYTE	#$82
	BYTE	#$84
	BYTE	#$82
	BYTE	#$80
	BYTE	#$82
	BYTE	#$80
#NAME#_DayTime_Sky_04
	BYTE	#$84
	BYTE	#$86
	BYTE	#$88
	BYTE	#$86
	BYTE	#$88
	BYTE	#$8A
	BYTE	#$8A
	BYTE	#$8A
	BYTE	#$88
	BYTE	#$8A
	BYTE	#$88
	BYTE	#$88
	BYTE	#$88
	BYTE	#$86
	BYTE	#$84
	BYTE	#$84
#NAME#_DayTime_Sky_05
	BYTE	#$84
	BYTE	#$86
	BYTE	#$84
	BYTE	#$86
	BYTE	#$88
	BYTE	#$8A
	BYTE	#$88
	BYTE	#$8A
	BYTE	#$8C
	BYTE	#$8E
	BYTE	#$8E
	BYTE	#$8E
	BYTE	#$8E
	BYTE	#$8C
	BYTE	#$8A
	BYTE	#$88
#NAME#_DayTime_Sky_06
	BYTE	#$38
	BYTE	#$38
	BYTE	#$36
	BYTE	#$38
	BYTE	#$36
	BYTE	#$34
	BYTE	#$36
	BYTE	#$46
	BYTE	#$48
	BYTE	#$46
	BYTE	#$44
	BYTE	#$46
	BYTE	#$44
	BYTE	#$42
	BYTE	#$44
	BYTE	#$42
#NAME#_DayTime_Sky_07
	BYTE	#$34
	BYTE	#$34
	BYTE	#$32
	BYTE	#$44
	BYTE	#$42
	BYTE	#$42
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40
	BYTE	#$40

	_align	24

#NAME#_DayTime_StarColors
### &COLOR
	BYTE	#$0e
	BYTE	#$0c
	BYTE	#$0a
	BYTE	#$08
	BYTE	#$06
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$06
	BYTE	#$08
	BYTE	#$0a
	BYTE	#$0c
	BYTE	#$0e

	_align	215	

#NAME#_DayTime_Loop
	STA	WSYNC

	STA	COLUBK			; 3 
	LDA	#7			; 2 (5)
	DCP	temp03			; 5 (10)
	BCS	#NAME#_Draw_Sun_Moon	; 2 (12)
	LDA	#0			; 2 (14)
	
	sleep	11

	JMP	#NAME#_Done_Sun_Moon	; 3 (25)
#NAME#_Draw_Sun_Moon	
	LDY	temp03			; 3 (15)
	LDA	(temp08),y		; 5 (20)
	STA	COLUP1			; 3 (23)
	LDA	(temp06),y		; 5 (28)
#NAME#_Done_Sun_Moon	
	STA	GRP1			; 3 (31)

	LDA	##NAME#_DayTime_L2	; 2 (33)
	CMP	temp10			; 3 (36)
	BCC	#NAME#_DayTime_CloudX_Not_Smaller ; 2 (38)
#NAME#_DayTime_ZeroCloudSprite
	sleep	7
#NAME#_DayTime_ZeroCloudSprite2
	sleep	4
	LDA	temp19			; 3 
	AND	#%00000011		; 2 
	TAY				; 2 

	LDX	#0			; 2 (40)
	STX	temp11
	JMP	#NAME#_DayTime_SaveCloudSprite	; 3 (69)
#NAME#_DayTime_CloudX_Not_Smaller
	LDA	##NAME#_DayTime_R2	; 2 (40)
	CMP	temp10			; 3 (43)
	BCC	#NAME#_DayTime_ZeroCloudSprite2	; 2 (45)

	LDA	temp19			; 3 (48)
	AND	#%00000011		; 2 (50)
	TAY				; 2 (52)
	LDA	(temp12),y		; 5 (57)
	TAX				; 2 (59)
	LDA	temp15
	NOP
	STA	COLUP0			; 3 (67)	
#NAME#_DayTime_SaveCloudSprite
	STX	GRP0			; 3 (70)

	STA	WSYNC
	CPY	#3
	BNE	#NAME#_DayTime_SkipNewX

	sleep	2
	LDA	temp11
#NAME#_DayTime_DivideLoop2
	sbc	#15
   	bcs	#NAME#_DayTime_DivideLoop2
	sleep	5
   	sta	RESP0
	TAY
   	lda	#NAME#_DayTime_FineAdjustTable256,Y
   	sta	HMP0
	JMP	#NAME#_DayTime_NoZeroIt

#NAME#_DayTime_SkipNewX

	LDA	#0
	STA	ENABL
	LDX	temp16
	LDA	#NAME#_DayTime_Star_X,x
#NAME#_DayTime_StarXLoop
	SBC	#4
	BCS	#NAME#_DayTime_StarXLoop	
	STA	RESBL
	LDA	temp18
	STA	COLUPF
	LDA	#2
	STA	temp17

	INX
	TXA
	AND	#%00000111
	STA	temp16

	LDA	#0
	STA	HMP0

#NAME#_DayTime_NoZeroIt
	STA	WSYNC
	STA	HMOVE			; 3

	LDY	#0		
	CPY	temp18					
	BNE	#NAME#_DayTime_ThereAreStars
	STY	ENABL
	STY	temp17
	JMP	#NAME#_DayTime_NoStars
#NAME#_DayTime_ThereAreStars
	LDA	temp17
	STA	ENABL
	STY	temp17
#NAME#_DayTime_NoStars

	LDY	temp19
	DEY	
	STY	temp19

	TYA
	AND	#%00000011
	TAX

	LDA	#NAME#_Cloud_DayTime_SpriteColor,x
	ADC	temp14
	STA	temp15

	LDA	temp19
	AND	#%00000011
	CMP	#3
	BEQ	#NAME#_DayTime_ToNewX

	sleep	7
	JMP	#NAME#_DayTime_NoNewX

#NAME#_DayTime_ToNewX
	LDA	temp10
	CLC	
	ADC	#63
	STA	temp10
#NAME#_DayTime_NoNewX

	LDA	temp10
	STA	temp11

	LDY	temp19			; 3 
	LDA	(temp04),y		; 5 

	CPY	#255		
	BEQ 	#NAME#_DayTime_Reset
	JMP	#NAME#_DayTime_Loop


#NAME#_DayTime_Reset
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUPF
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1

	STX	GRP0
	STX	GRP1
	STX	ENABL
	STX	HMCLR
	STX	REFP1

	ldx	item
	txs