*
*	This is the standalone version of the 48pxPicture kernel, so there are no
*	pointers used and also not much to replace on the fly.
*

* I always forget these!!
*
* X < Y
* LDA	X	
* CMP	Y
* BCS   else 	 
*
* X <= Y
*
* LDA	Y
* CMP	X
* BCC	else
*
* X > Y 
*
* LDA	Y
* CMP	X
* BCS	else
*
* X >= Y
*
* LDA	X
* CMP	Y
* BCC 	else
*
#NAME#_48PxPicture

	LDA	#SETTERS#			; 3 
	LSR					
	LSR
	LSR
	LSR	
	AND	#%00000111			; 8 
	TAX					; 2 
	LDA	#BACKGROUND#			; 3
	STA	WSYNC				; 3

	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)
	STA	COLUPF		; 3 (15)
	LDA	#0		; 2 (17)
	STA	ENABL		; 3 (20)
	STA	ENAM0		; 3 (23)
	STA	ENAM1		; 3 (26)

#NAME#_48PxPicture_Checks
	CPX	#0					; 2 (28)
	BNE	#NAME#_48PxPicture_Checks_Continue	; 2 (30)
	JMP	#NAME#_48PxPicture_FrameNum_SYNC   	; 3
#NAME#_48PxPicture_Checks_Continue
	LDA	counter				; 3 (33)
	AND	#NAME#_48PxPicture_BitMask,x	; 4 (37)
	CMP	#NAME#_48PxPicture_BitMask,x	; 4 (41)
	BNE	#NAME#_48PxPicture_JumpOver_SYNC ; 2 (43)
	LDA	#SETTERS#			; 3 (46)
	AND	#$0F				; 2 (48)
	CLC					; 2 (50)
	ADC	#1				; 2 (52)
	AND	#$F0				; 2 (54)
	CMP	##NAME#_Frames_Max_Index	; 2 (56)
	BCC	#NAME#_48PxPicture_FrameNum_OK	; 2 (58)
	LDA	##NAME#_Frames_Max_Index	; 2 (60)
#NAME#_48PxPicture_FrameNum_OK	
	STA	temp01				; 3 (63)	
	LDA	#SETTERS#			; 3 (66)
	AND	#$F0				; 2 (68)
	ORA	temp01				; 3 (71)
	STA	#SETTERS#			; 3 (74)	
#NAME#_48PxPicture_FrameNum_OK	
	JMP	#NAME#_48PxPicture_FrameNum_Jump_Over
*
*	One frame wasted!!
*
#NAME#_48PxPicture_FrameNum_SYNC
	STA	WSYNC
#NAME#_48PxPicture_FrameNum_Jump_Over
	LDA	#0	
	STA	PF0				; 3 
	STA	PF1				; 3 
 	STA	CTRLPF				; 3 
	LDA	#$03				; 2 
	STA	NUSIZßS				; 3 
	LDA	#NAME#_Repeating_NUSIZ		; 2 
	STA	NUSIZßR				; 3 

	JMP	#NAME#_48PxPicture_JumpOver	; 3 	

	_align	8
#NAME#_48PxPicture_BitMask
	BYTE	#0
	BYTE	#%01111111
	BYTE	#%00111111
	BYTE	#%00011111
	BYTE	#%00000111
	BYTE	#%00000011
	BYTE	#%00000001
	BYTE	#%00000000
#NAME#_48PxPicture_JumpOver_SYNC
	STA	WSYNC
#NAME#_48PxPicture_JumpOver
	LDA	counter
	AND	#1
	TAY

	STA	WSYNC				; 3 (76)
*
*	Should wait 9 cycles before the loop?
*

	LDA	#NAME#_48PxPicture_Base_X,y
	SEC
	sleep	2				
#NAME#_48PxPicture_Set_X_PßS_Loop
	sbc	#15
   	bcs	#NAME#_48PxPicture_Set_X_PßS_Loop
	SBC	#239
	sta	temp01
   	sta	RESPßS	

	LDA	##NAME#_Repeating_Add_To_X
	CLC
	STA	WSYNC
	ADC	#NAME#_48PxPicture_Base_X,y
	SEC
	sleep	2
#NAME#_48PxPicture_Set_X_PßR_Loop
	sbc	#15
   	bcs	#NAME#_48PxPicture_Set_X_PßR_Loop
	SBC	#239
	sleep 	3
   	sta	RESPßR	
	tax

	LDA	#NAME#_48PxPicture_FineAdjustTable,x
	STA	HMPßR
	LDX	temp01
	LDA	#NAME#_48PxPicture_FineAdjustTable,x
	STA	HMPßS

	STA	WSYNC
	STA	HMOVE				; 3
	LDA	#SETTERS#			; 3 (6) 
	AND	#$0F				; 2 (8)
	TAX					; 2 (10)
	TAY					; 2 (12)
	LDA	#0				; 2 (14)
	DEX					; 2 (16)
	BMI	#NAME#_48PxPicture_SetIndexEnd  ; 2 (18)
	CLC					; 2 (20)
*
*	6 * index, max: 15 * 6 = 90!!
*
*	0: 18 (no extra 2 at beginning)
*	1: 20 + 6  = 26
*	2:    + 12 = 32
*	.......
*       8:    + 48 = 68 !!!
*       9:    + 54 = 76 !!!
*	.......
*       15:   + 90 = 107 (76 + 31)
*
#NAME#_48PxPicture_SetIndex
	ADC	#NAME#_LineNum_Number_Of_Lines			; 2 
	DEX					; 2 
	BPL	#NAME#_48PxPicture_SetIndex	; 2  
#NAME#_48PxPicture_SetIndexEnd
	CPY	#9				; 2
	BCS	#NAME#_48PxPicture_NoExtraSync  ; 2
	STA	WSYNC				; 3 (7)
#NAME#_48PxPicture_NoExtraSync
	STA	WSYNC
	STA	temp19				; 3 
	LDA	#SETTERS#
*
*	temp19 holds the first index of the current frame!
*	
	LDA	#DSPHEIGHT#			; 3 (6)
	CMP	#70				; 2 (8)
	BCC	#NAME#_48PxPicture_THANKGOD_SMALLER ; 2 (10)
	LDA	#70				; 2 (12)
#NAME#_48PxPicture_THANKGOD_SMALLER
	CMP 	##NAME#_LineNum_Number_Of_Lines	; 2 (14)
	BCC	#NAME#_48PxPicture_THANKGOD_SMALLER2 ; 2 (17)
	LDA	##NAME#_LineNum_Number_Of_Lines	; 2 (20)
#NAME#_48PxPicture_THANKGOD_SMALLER2
	STA	#DSPHEIGHT#			; 3 (23)

	LDA	##NAME#_LineNum_Number_Of_Lines	; 2 (25)
	SEC					; 2 (27)
	SBC	#DSPHEIGHT#			; 3 (30)
	LSR					; 2 (32)
	STA	temp01				; 3 (35)
	TAX					; 2 (37)
*
*	temp01 is the number of line to skip on start and end
*	
	CLC					; 2 (39)
	ADC	temp19				; 3 (42)
	SBC	#1				; 2 (44)
	STA	temp02				; 3 (47)
*
*	temp02 is the index of the last line to not display.
*
	LDA	##NAME#_LineNum_Max_Index	; 2 (47)
	SEC					; 2 (49)
	SBC	temp01				; 3 (52)
	CLC					; 2 (54)
	ADC	temp19				; 3 (57)
	STA	temp03				; 3 (60)
*
*	temp03 is the number of additional indexes.
*
	DEX	
	BMI	#NAME#_48PxPicture_ExtraLines_1_End ; 2
#NAME#_48PxPicture_ExtraLines_1
	STA	WSYNC				; 3	
	DEX
	BPL	#NAME#_48PxPicture_ExtraLines_1
#NAME#_48PxPicture_ExtraLines_1_End		
	LDY	temp03

***	LDA	#255
***	STA	PF2
***	STA	GRPßS

***	LDA	#$88
***	STA	COLUPF

**	LDA	#$1e
**	STA	COLUPßS
	
	STA	WSYNC
	LDA	counter		; 3
	AND	#1		; 2 (5)
	CMP	#1		; 2 (7)
	BEQ	#NAME#_48PxPicture_Even_Start ; 2 (9)
	JMP	#NAME#_48PxPicture_Odd_Start  ; 3 (12)

	align	256
#NAME#_48PxPicture_Even_Start	
	LDA	#$00		; 2 (11)
	STA	HMP0		; 3 (14)
	STA	HMP1		; 3 (17)
	INY			; 2 (19)

	LDA	#NAME#_Simple_Color,y  ; 4
	STA	COLUPßS			; 3 

	LDA	#NAME#_Repeating_Color,y ; 4
	STA	COLUPßR			 ; 3

	LDX 	#NAME#_Simple_6,y	 ; 4

#NAME#_48PxPicture_Even_FirstLine
	STA	WSYNC			    ; 3 
	STA	HMOVE			    ; 3 

	LDA	#NAME#_Playfield_Color,y ; 4
	STA	COLUPF			 ; 3 (10)

	LDA	#NAME#_Repeating_2,y 	 ; 4
	STA	GRPßR			 ; 3 (17)
	
	LDA	#NAME#_Simple_2,y 	 ; 4
	STA	GRPßS			 ; 3 (24)	

	LDA	#NAME#_PF2_Data_2,y 	 ; 4
	STA	PF2			 ; 3 (31)	

	sleep	5			 ; 5 (36)

	LDA	#NAME#_Simple_4,y 	 ; 4
	STA	GRPßS			 ; 3 (43)

	LDA	#$00
	STX	GRPßS			 ; 3 
	STA	HMP0
	STA	HMP1			    
	STA	PF2			 ; 14 (60)

	LDA	#NAME#_Simple_1,y 	 ; 4 (64) 
	STA	GRPßS			 ; 3 (67)
	
	DEY				 ; 2 (69)
	LDX	#NAME#_Simple_6,y	 ; 4 (73)

#NAME#_48PxPicture_Even_SecondLine
	STA	HMOVE			 ; 3 (1)

	TXS				 ; 2 (3)
	INY				 ; 2 (5)

	LDA	#NAME#_Repeating_1,y 	 ; 4 (9)
	STA	GRPßR			 ; 3 (12)

	LDA	#NAME#_PF2_Data_1,y 	 ; 4 (16)
	STA	PF2			 ; 3 (19)

	LDA	#$80			    ; 2 (21)
	STA	HMP0			    ; 3 (24) 
	STA	HMP1			    ; 3 (27)

	sleep	5			    ; 32	

	LDX 	#NAME#_Simple_5,y	 ; 4 (36)
	LDA	#NAME#_Simple_3,y  	 ; 4 (40)

	STA	GRPßS			 ; 3 (43)	
	DEY 				 ; 2 (45)

	STX	GRPßS			 ; 3 (48)
	LDA	#0			 ; 2 (50)
	STA	PF2			 ; 3 (53)

	LDA	#NAME#_Simple_Color,y       ; 4 (57)
	STA	COLUPßS			    ; 3 (60)
	
	LDA	#NAME#_Repeating_Color,y    ; 4 (64) 
	STA	COLUPßR			    ; 3 (67)

	TSX 				    ; 2 (69)

	CPY	temp02			; 3 (71)
	BNE	#NAME#_48PxPicture_Even_FirstLine (73)
	JMP	#NAME#_48PxPicture_Kernel_End

	align	256
#NAME#_48PxPicture_Odd_Start
	LDA	#$00			; 2 
	STA	HMP0			; 3
	STA	HMP1			; 3
	INY

	sleep	37

	LDA	#NAME#_Simple_Color,y  ; 4
	STA	COLUPßS			; 3 

	LDX 	#NAME#_Simple_5,y	 ; 4

#NAME#_48PxPicture_Odd_FirstLine
	STA	HMOVE	(1)

	LDA	#NAME#_Repeating_Color,y    ; 4  
	STA	COLUPßR			    ; 3 (9)

	LDA	#NAME#_Repeating_1,y 	 ; 4 (9)
	STA	GRPßR			 ; 3 (12)

	LDA	#NAME#_PF2_Data_1,y 	 ; 4 (16)
	STA	PF2			 ; 3 (19)

	LDA	#NAME#_Simple_1,y 	 ; 4 (25)
	STA	GRPßS			 ; 3 (28)

	LDA	#NAME#_Playfield_Color,y ; 4 (32)
	STA	COLUPF			 ; 3 (35)

	LDA	#NAME#_Simple_3,y 	 ; 4 (47)
	STA	GRPßS			 ; 3 (50)

	LDA	#$80			 ; 2 (37)

	STX	GRPßS			 ; 3 (53)
	STA	HMP0			 ; 3 (40) 
	STA	HMP1			 ; 3 (43)

	LDA	#0			 ; 2 (55)
	STA	PF2			 ; 3 (58)

	LDA	#NAME#_Simple_2,y 	 ; 4 (62) 
	STA	GRPßS			 ; 3 (65)

	DEY				 ; 2 (67)
	LDX	#NAME#_Simple_5,y	 ; 4 (71)
	TXS				 ; 2 (73)

#NAME#_48PxPicture_Odd_SecondLine
	STA	WSYNC	(76)
	STA	HMOVE   		 ; 3

	LDX	#NAME#_Simple_Color,y    ; 4 (7)
	INY 				 ; 2 (9)
	
	LDA	#NAME#_Repeating_2,y 	 ; 4 (13)
	STA	GRPßR			 ; 3 (16)

	LDA	#NAME#_PF2_Data_2,y 	 ; 4 (20)
	STA	PF2			 ; 3 (23) 

	LDA	#$00			  ; 
	STA	HMP0			  ;  
	STA	HMP1			  ; 8 (31)

	sleep	3

	LDA	#NAME#_Simple_4,y 	 ; 4 (35)
	STA	GRPßS			 ; 3 (38)

	LDA	#NAME#_Simple_6,y 	 ; 4 (42)	
*****	STA	GRPßS		 
	BYTE	#$8D
	BYTE	#GRPßS	
	BYTE	#0

	LDA	#0
*****	STA	PF2	
	BYTE	#$8D
	BYTE	#PF2	
	BYTE	#0

	DEY	
		
	STX	COLUPßS			    ; 3 (60)
	TSX 				    ; 2 (69)

	CPY	temp02				 ; 3 (71)
	BNE	#NAME#_48PxPicture_Odd_FirstLine ; 2 (74)
	JMP	#NAME#_48PxPicture_Kernel_End

	_align 2
#NAME#_48PxPicture_Base_X
	BYTE	#58		; Odd
	BYTE	#58		; Even

	_align	16
#NAME#_48PxPicture_FineAdjustTable
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

#NAME#_48PxPicture_Kernel_End
	LDA	frameColor
	STA	WSYNC
	STA	COLUPF
	STA	COLUP0
	STA	COLUP1

	LDA	#0
	STA	GRP0
	STA	GRP1
	STA	PF2
	STA	PF0

	LDX	temp01
	DEX	
	BMI	#NAME#_48PxPicture_ExtraLines_2_End
#NAME#_48PxPicture_ExtraLines_2
	STA	WSYNC					
	DEX
	BPL	#NAME#_48PxPicture_ExtraLines_2
#NAME#_48PxPicture_ExtraLines_2_End	
