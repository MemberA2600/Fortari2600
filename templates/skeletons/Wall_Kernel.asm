
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

#BANK#_Wall_Kernel_NoSprite = 242

	_align	235
	
#BANK#_Wall_Kernel
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK	
	STX	PF0		
	STX	PF1		
	STX	PF2
	STX	GRP0
	STX	GRP1
	STX	ENAM0
	STX	ENAM1
	STX	ENABL
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF
	
	LDA	#%00000100
	STA	CTRLPF	

	LDA	temp19
	CMP	#$F0
	BNE	#BANK#_Wall_NoJump
	JMP	#BANK#_Wall_PreLoad
#BANK#_Wall_NoJump

	TSX
	INX
	STX	temp18

	CLC

	LDX	temp19
	LDA	#0
	STA	WSYNC
*
*	Min:  	4
*	Max: 	(15 * 10) + 4 = 154
*

#BANK#_Wall_Kernel_Index_Loop
	DEX
	BMI 	#BANK#_Wall_Kernel_Index_Loop_End
	ADC	temp18
	JMP	#BANK#_Wall_Kernel_Index_Loop	

*
*	+ 13
*	Proper filler num is based on 2 - ((index * 10) + 23) // 76 
*
#BANK#_Wall_Kernel_Index_Loop_End
	ADC	temp09
	STA	temp09

	LDX	temp19
	LDA	#BANK#_Wall_Filler_WSYNC,x
	TAX

#BANK#_Wall_Kernel_Filler_WSYNC_Loop
	STA	WSYNC
	DEX	
	BPL	#BANK#_Wall_Kernel_Filler_WSYNC_Loop	

*
*	Set X and NUSIZ for sprites.
*
* 0: 0 0 0 ( X = 0     , NUSIZ = $00)
* 1: 0 0 X ( X = N + 32, NUSIZ = $00)
* 2: 0 X 0 ( X = N + 16, NUSIZ = $00) 
* 3: 0 X X ( X = N + 16, NUSIZ = $01) 
* 4: X 0 0 ( X = N     , NUSIZ = $00)
* 5: X 0 X ( X = N     , NUSIZ = $02)
* 6: X X 0 ( X = N     , NUSIZ = $01)
* 7: X X X ( X = N     , NUSIZ = $03)	
*

	LDA	temp07
	AND	#%00111000
	LSR
	LSR
	LSR
	TAX

	LDA	#BANK#_Wall_NUSIZ,x
	STA	NUSIZ0
	LDA	#BANK#_Wall_P0_X,x
	STA	temp18
		
	
	LDA	temp07
	AND	#%00000111	
	TAX
	LDA	#BANK#_Wall_P1_X,x
	STA	temp19

	LDA	#BANK#_Wall_NUSIZ,x
	STA	NUSIZ1

	LDX	temp09
	LDY	temp15

	LDA	temp18
	CMP	##BANK#_Wall_Kernel_NoSprite
	BNE	#BANK#_Wall_Kernel_Sprite_Set_P0

	STY	temp09
	JMP	#BANK#_Wall_Kernel_NoSprite_Set_P0

#BANK#_Wall_Kernel_Sprite_Set_P0
	sleep	3
	STX	temp09
#BANK#_Wall_Kernel_NoSprite_Set_P0

	LDA	temp19
	CMP	##BANK#_Wall_Kernel_NoSprite
	BNE	#BANK#_Wall_Kernel_Sprite_Set_P1

	STY	temp15
	JMP	#BANK#_Wall_Kernel_NoSprite_Set_P1

#BANK#_Wall_Kernel_Sprite_Set_P1
	sleep	3
	STX	temp15
#BANK#_Wall_Kernel_NoSprite_Set_P1

	sta	WSYNC
	LDA	temp18
	CMP	##BANK#_Wall_Kernel_NoSprite
	BEQ	#BANK#_Wall_Kernel_NoWaitP0

#BANK#_Wall_Kernel_DivideLoop_P0
	sbc	#15
   	bcs	#BANK#_Wall_Kernel_DivideLoop_P0		
	sta	temp18
	NOP
#BANK#_Wall_Kernel_NoWaitP0
	STA	RESP0

	sta	WSYNC
	LDA	temp19
	CMP	##BANK#_Wall_Kernel_NoSprite
	BEQ	#BANK#_Wall_Kernel_NoWaitP1

#BANK#_Wall_Kernel_DivideLoop_P1
	sbc	#15
   	bcs	#BANK#_Wall_Kernel_DivideLoop_P1		
	sta	temp19
	NOP
#BANK#_Wall_Kernel_NoWaitP1
	STA	RESP1

	CLC
   	lda	temp18	
	ADC	#15	
	TAX
   	lda	#BANK#_Wall_Kernel_FineAdjustTable,x
   	sta	HMP0		

   	lda	temp19	
	ADC	#15	
	TAX
   	lda	#BANK#_Wall_Kernel_FineAdjustTable,x
   	sta	HMP1	

   	sta	WSYNC
   	sta	HMOVE		; 3	

*
*	Preload data!
*
#BANK#_Wall_PreLoad
	TSX
	TXA
	TAY

	LDA	(temp11),y	; 5
	STA	COLUP0		; 3
	STA	COLUP1 		; 3


	LDA	(temp15),y	; 5
	TAX			; 2
	TXS			; 2

	LDA	(temp09),y	; 5
	TAX			; 2
	
	LDA	temp14
	STA	temp18

	LDA	(temp17),y	; 5
	ADC	temp05		; 3 

	JMP	#BANK#_Wall_Loop

	_align	60

#BANK#_Wall_P0_X
	BYTE	##BANK#_Wall_Kernel_NoSprite
	BYTE	#81
	BYTE	#65
	BYTE	#65
	BYTE	#49
	BYTE	#49
	BYTE	#49
	BYTE	#49
#BANK#_Wall_P1_X
	BYTE	##BANK#_Wall_Kernel_NoSprite
	BYTE	#128
	BYTE	#112
	BYTE	#112
	BYTE	#96
	BYTE	#96
	BYTE	#96
	BYTE	#96

#BANK#_Wall_NUSIZ
	BYTE	#$00
	BYTE	#$00
	BYTE	#$00
	BYTE	#$01
	BYTE	#$00
	BYTE	#$02
	BYTE	#$01
	BYTE	#$03

#BANK#_Wall_Filler_WSYNC
	BYTE	#2
	BYTE	#2
	BYTE	#2
	BYTE	#2
	BYTE	#2	; 4
	BYTE	#1	
	BYTE	#1
	BYTE	#1
	BYTE	#1
	BYTE	#1
	BYTE	#1
	BYTE	#1	; 12
	BYTE	#0
	BYTE	#0	
	BYTE	#0
	BYTE	#0
	BYTE	#0

#BANK#_Wall_Kernel_FineAdjustTable
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
	
	_align	105

#BANK#_Wall_Loop
	STA	WSYNC		; 76
	STA	COLUPF		; 3 
	STX	GRP0		; 3 (6)
	TSX			; 2 (8)
	STX	GRP1		; 3 (11)
	 
	LDA	temp05		; 3 (14)
	STA	PF0		; 3 (17)

	LDA	temp01		; 3 (20)
	STA	PF1		; 3 (23)

	LDA	temp02		; 3 (26)
	STA	PF2		; 3 (29)

	DEY			; 2 (31)

	LDA	temp06		; 3 (34)
	STA	PF0		; 3 (37)

	NOP			; 2 (39)

	LDA	temp03		; 3 (42)
	STA	PF1		; 3 (45)

	LDA	temp04		; 3 (48)
	STA	PF2		; 3 (51)

	LDA	(temp15),y	; 5 (56)
	TAX			; 2 (58)
	TXS			; 2 (60)

	LDA	(temp09),y	; 5 (65)
	TAX			; 2 (67)

#BANK#_Wall_Loop_SecondLine
	STA	WSYNC		; 76

	LDA	temp05		; 3 
	STA	PF0		; 3 (6)

	LDA	temp01		; 3 (9)
	STA	PF1		; 3 (12)

	LDA	temp02		; 3 (15)
	STA	PF2		; 3 (18)
	
	sleep	8
	
	CPY	#255		; 2 (28)
	BEQ	#BANK#_Wall_Last_Ones	; 2 (30)

	LDA	temp06		; 3 (33)
	STA	PF0		; 3 (36)

	NOP

	LDA	temp03		; 3 (41)
	STA	PF1		; 3 (44)

	LDA	temp04		; 3 (47)
	STA	PF2		; 3 (50)
	
	LDA	(temp11),y	; 5 (55)
	STA	COLUP0		; 3 (58)
	STA	COLUP1 		; 3 (61)
	
	LDA	(temp17),y	; 5 (66)
	ADC	temp05		; 3 (69)
	JMP	#BANK#_Wall_Loop ; 3 (72)


#BANK#_Wall_Last_Ones
	LDA	temp06		; 3 
	STA	PF0		; 3 

	NOP			; 2

	LDA	temp03		; 3 
	STA	PF1		; 3 

	LDA	temp04		; 3 
	STA	PF2		; 3 

#BANK#_Wall_Reset
	JMP	(temp13)
