
##BANK##_BigSprite_Kernel_Begin

* BigSprite_0: 		temp03 - temp04
* BigSprite_1: 		temp05 - temp06
* BigSpriteColor_0:     temp07 - temp08
* BigSpriteColor_1:   	temp09 - temp10
* BigSpriteBG: 		temp11 - temp12
* Height:		temp13
* LineHeight:		temp14
* xPoz:			temp15
* bgColorMod: 		temp16
* spriteSettings:	temp17
* X2Offset:		temp18
* mono:			temp19

	LDA	frameColor
	STA	WSYNC		; (76)
	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)

*
*	(8 bytes)
*	Initialize sprite settings.
*
	LDA	#0		; 2 (8)
	STA	PF0		; 3 (11)
	STA	PF1		; 3 (14)
	STA	PF2		; 3 (17)
	STA	GRP0		; 3 (20)
	STA	GRP1		; 3 (23)
*
*	Get spritenum and calc offset
*
	
	LDA	temp17		; 3 (26)
	AND	#%00000111	; 2 (28) 
	TAX			; 2 (30)
	LDA	##BANK##_BigSprite_Multiply_Offset,x ; 5 (35)
	TAX			; 2 (37)

*
*	Can have the values 0, 1 or 2.
*	It takes (n * 14) + 4 cycles (4, 18, 32)
*
##BANK##_BigSprite_OffSet_Loop
	CPX	#0		; 2
	BEQ	##BANK##_BigSprite_OffSet_Loop_End ; 2
	ASL	temp18		; 5
	DEX			; 2
	JMP	##BANK##_BigSprite_OffSet_Loop ; 3

##BANK##_BigSprite_OffSet_Loop_End
*
*	(16 (24) bytes)	
*	Set offset if mode is "double"
*
*	WSYNC needed so it won't fail in sync
*
	STA	WSYNC		; 3 (76)	

	LDA	temp18		; 3 (3)
	CMP	#0		; 2 (5)
	BEQ	##BANK##_BigSprite_Kernel_Offset_Done	; 2 (7)
	JMP	##BANK##_BigSprite_Kernel_Color_0_To_1  ; 3 (10)

##BANK##_BigSprite_Kernel_Offset_Done

*
*	(9 (33) bytes)
*	If "mono", the two sprites must have the same values
*
##BANK##_BigSprite_FineTable256
	LDA	temp19		; 3 (13)
	CMP	#0		; 2 (15)
	BEQ	##BANK##_BigSprite_Kernel_Not_Mono	; 2 (17)


	LDA	temp03		; 3 (20)
	STA	temp05		; 3 (23)
	LDA	temp04		; 3 (26)
	STA	temp06		; 3 (29)
##BANK##_BigSprite_Kernel_Color_0_To_1	
	LDA	temp07		; 3 (32)
	STA	temp09		; 3 (35)
	LDA	temp08		; 3 (38)
	STA	temp10		; 3 (41)
##BANK##_BigSprite_Kernel_Not_Mono

*	
*	(22 bytes (55) bytes)
*

*
*	Set the sprite NUSIZ and reflection.
*

	LDA	temp17		; 3 	(37)
	AND	#%00001111	; 2 	(39)
	STA	NUSIZ0		; 3 	(42)
	STA	REFP0		; 3 	(45)
	STA	NUSIZ1		; 3 	(48)
	STA	REFP1		; 3 	(51)


*	
*	(14 bytes (69))
*	Flip sprite data if double and mirrored
*	Use mono as temp, it is not used anymore.
*

	STA	WSYNC			; 3 (76)

	LDA	temp18		; 3 
	CMP	#0			; 2 (5)
	BEQ	##BANK##_BigSprite_Kernel_NO_FLIP	; 2 (7)
	LDA	temp17	; 3 (10)
	AND	#%00001000		; 2 (12)
	CMP	#%00001000		; 2 (14)
	BNE	##BANK##_BigSprite_Kernel_NO_FLIP	; 2 (16)

	LDA	temp03		; 3 (19)
	TAY			; 2 (21)
	LDA	temp04		; 3 (24)
	TAX			; 2 (26)
	LDA	temp05		; 3 (29)
	STA	temp03		; 3 (32)
	LDA	temp06		; 3 (35)
	STA	temp04		; 3 (38)
	TYA			; 2 (40)
	STA	temp05		; 3 (43)
	TXA			; 2 (45)
	STA	temp06		; 3 (48)

##BANK##_BigSprite_Kernel_NO_FLIP
*	
*	(36 bytes (105))
*	Get sprite frame num.	
*

	LDA	temp17		; 3 (51)
	LSR			; 2 	
	LSR			; 2 
	LSR			; 2 
	LSR			; 2 
	AND	#%00001111	; 2
	TAY		 	; 2 (63)

*
*	(9 bytes (114))
*	Check if X position is wrong. Use "mono" since
*	won't use it anymore.
*

	STA	WSYNC				; 3 (76)	
	
	LDA	temp15			; 3 
	CMP	#28				; 2 (5)
	BCS	##BANK##_BigSprite_XNotSmaller	; 2 (7)
	LDA	#28				; 2 (9)
	STA	temp15			; 3 (12)
	JMP	##BANK##_BigSprite_X16Done	; 3 (15)
##BANK##_BigSprite_XNotSmaller

	LDA	temp17				; 3 (18)
	AND	#%00000111			; 2 (20)
	TAX					; 2 (22)
	TXS					; 2 (24)
	LDA	##BANK##_BigSprite_AddToX,x 	; 4 (28)
	
	LDX	temp18				; 3 (31)
	CPX	#0				; 2 (33)
	BEQ	##BANK##_BigSprite_NoDouble	; 2 (35) 
	TSX					; 2 (37)
	LDA	##BANK##_BigSprite_AddToX_Double,x ; 5 (42)
##BANK##_BigSprite_NoDouble
	STA 	temp19				; 3 (45)
	LDA	#143				; 2 (47)
	SEC					; 2 (49)
	SBC	temp19				; 3 (52)	
	CMP	temp15				; 3 (55)
	BCS	##BANK##_BigSprite_X16Done 	; 2 (57)
	STA	temp15				; 3 (60)

##BANK##_BigSprite_X16Done

*	
*	(38 bytes (152))
*	Get the actual sprite's last line.
*
	sta	WSYNC			; 3 (76)
	LDA	#0			; 2 
##BANK##_BigSprite_Kernel_SpriteSetLoop	
	CPY	#0			; 5 (4)
	BEQ	##BANK##_BigSprite_Kernel_SpriteSetLoop_Ended	; 2 (6)
	CLC				; 2 (8)
	ADC	temp13			; 3 (11)
	DEY				; 2 (13)
	JMP	##BANK##_BigSprite_Kernel_SpriteSetLoop	; 3 (16)	

##BANK##_BigSprite_Kernel_SpriteSetLoop_Ended
*
*	(15 bytes (167))
*	Save real sprite indicator to X. 
*	Y is used for the kernel and the color.
*
	TAX				; 2 (18)
	CLC				; 2
	ADC	temp03			; 3 (21)	
	STA	temp03			; 3 (24)
	TXA				; 2 (26)
	CLC				; 2
	ADC	temp05			; 3 (28)
	STA	temp05			; 3 (31)
*
*	(168)
*	
*	Set X position on hw.
*

	

##BANK##_BigSprite_SetXoFSprites

	sta	WSYNC			; 3 (76)

	sleep	7		; Must wait 7 cycles since there is only one X here and it's a simple load-	
	LDA	temp15
##BANK##_BigSprite_DivideLoop_0
	sbc	#15
   	bcs	##BANK##_BigSprite_DivideLoop_0
   	TAY
	sleep	2
   	sta	RESP0

   	lda	##BANK##_BigSprite_FineTable256,y
   	sta	HMP0	
	sta	WSYNC			; 3 (76)
	
	LDA	temp15
	NOP	
	CLC
	ADC	temp18

##BANK##_BigSprite_DivideLoop_1
	sbc	#15
   	bcs	##BANK##_BigSprite_DivideLoop_1
   	TAY
	sleep	2
   	sta	RESP1

   	lda	##BANK##_BigSprite_FineTable256,Y
   	sta	HMP1	

	LDY	temp13		
*	
*	(42 (210) bytes)
*	Height is saved to Y, so we don't need it anymore.
*	Keep the lineHeight instead.
*

	LDA #1			; 3
	STA temp13		; 3

*	(4 (214) bytes)
*
*	Preload the colors!
*

	LDA	#0
	STA	VDELP0		; 3 
	STA	VDELP1		; 3 

	LDA	(temp07),y	; 5
	STA	COLUP0		; 3

	LDA	(temp09),y	; 5
	STA	COLUP1		; 3

*	LDA	(temp11),y		
*	CLC							
*	ADC	temp16

	sleep	10

	STA	WSYNC				; 3 (76)
	STA	HMOVE				; 3
*	STA	COLUBK			

	JMP	##BANK##_BigSprite_MainLoopFirst	; 3 (10)

*	9 (234)
*
*	The Tables
*
	
##BANK##_BigSprite_Dummy
*	fill 3
	fill 5	

##BANK##_BigSprite_AddToX
	byte	#8	
	byte	#24
	byte	#40
	byte	#40
	byte	#72
	byte	#16
	byte	#72
	byte	#32

##BANK##_BigSprite_FineTable
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

##BANK##_BigSprite_Multiply_Offset
	byte	#0
	byte	#0
	byte	#0
	byte	#0
	byte	#0
	byte	#1
	byte	#0
	byte	#2

##BANK##_BigSprite_AddToX_Double
	byte	#16	
	byte	#32
	byte	#48
	byte	#48
	byte	#80
	byte	#32
	byte	#80
	byte	#64

*
*	Drawing!
*	(should be at paging!)
*
* BigSprite_0: 		temp03 - temp04
* BigSprite_1: 		temp05 - temp06
* BigSpriteColor_0:     temp07 - temp08
* BigSpriteColor_1:   	temp09 - temp10
* BigSpriteBG: 		temp11 - temp12
* Height:		temp13
* LineHeight:		temp14
* xPoz:			temp15
* bgColorMod: 		temp16
* spriteSettings:	temp17
* X2Offset:		temp18
* mono:			temp19

	_align	45

##BANK##_BigSprite_MainLoop	
	STA	WSYNC			; 3 (76)
##BANK##_BigSprite_MainLoop_NoSync
	LDA	(temp11),y		; 5
	CLC				; 2 (7)	
	ADC	temp16			; 3 (10)
	STA	COLUBK			; 3 (13)

	LDA	(temp03),y 		; 5 (18)
	STA	GRP0			; 3 (21)
	LDA	(temp05),y		; 5 (26)
	STA	GRP1			; 3 (29)
##BANK##_BigSprite_MainLoopFirst	

	LDA	#0			; 2 (31)
	DCP	temp13			; 5 (36)
	BNE	##BANK##_BigSprite_NoEnd 	; 2 (38)
	DEY				; 2 (40)
	CPY	#255			; 2 (42) 
	BEQ	##BANK##_BigSprite_DrawEnd	; 2 (44)
	LDA	temp14			; 3 (47)
	STA	temp13			; 3 (50)
	
##BANK##_BigSprite_NoEnd
	LAX	(temp07),y		; 5 (55)
	LDA	(temp09),y		; 5 (60)
	
	sleep	4

	STX	COLUP0			; 3 (67) 
	STA	COLUP1			; 3 (70)

	JMP	##BANK##_BigSprite_MainLoop ; 3 (73)

##BANK##_BigSprite_DrawEnd	
	LDA	frameColor
	STA	WSYNC
	STA	COLUBK
	STA	COLUP0
	STA	COLUP1
	STA	GRP0
	STA	GRP1
	STA	REFP0
	STA	REFP1

	JMP	(temp01)
