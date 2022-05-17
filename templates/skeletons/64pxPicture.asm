pic64px_KernelStart
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)
	STA	COLUP0		; 3 (9)
	STA	COLUP1		; 3 (12)
	STA	COLUPF		; 3 (15)

	LDA	#0		; 2 (17)
	STA	PF0		; 3 (20)
	STA	PF1		; 3 (23)
	STA	PF2		; 3 (26)
	STA	GRP0		; 3 (29)
	STA	GRP1		; 3 (32)
	STA	VDELP0		; 3 (35)
	STA	VDELP1		; 3 (38)

	LDA	#$02		; 2 (40)
	STA	NUSIZ0		; 3 (43)
	STA	NUSIZ1		; 3 (46) 

	LDA	#%00000001	; mirrored pf with regular colors 2 (48)
 	STA	CTRLPF		; 3 (51)

	LDA	#picHeight	; height of the picture 3 (53)
	SEC			; 2 (55)
	SBC	picIndex	; index of scrolling 3 (58)
	STA	temp01		; starting point 3 (61)
	TAY			; 2 (63)
	SEC			; 2 (65)
	SBC 	picDisplayHeight ; 3 (68)
	STA 	temp02		; displayed height (stops if Y gets here) 3 (71)
	STA	WSYNC		; (76)	- One line wasted

	_sleep	26
	sleep 3

	STA	RESP0		; 3 (32)
	sleep	3		;   (35)	
	STA	RESP1		; 3 (38) Set the X pozition of sprites.

	DEY			; 2 (40)

	LDA	counter		; 3 (43)
	AND	#%00000001	; 2 (45)
	CMP	#%00000001	; 2 (47)
	BNE	pic64px_OddFrameJMP  ; 2 (49)
	JMP	pic64px_EvenFrame ; 3 (52)	
pic64px_OddFrameJMP
	JMP	pic64px_OddFrame  ; 3 (52)

******	align	256
	_align	80

pic64px_OddFrame
	STA	WSYNC
	STA	WSYNC

	LDA	#0				; 2
	STA	GRP0				; 3 (5)
	STA	GRP1				; 3 (8)

	LAX	pic64px_06,y			; 4 (12)
		
	LDA	#$00				; 2 (14)
	STA 	HMP0				; 3 (17) 
	LDA	#$20				; 2 (19)
	STA 	HMP1				; 3 (22)
	LDA	pic64px_00,y			; 4 (26)
	STA	GRP0				; 3 (29)
	LDA	pic64px_02,y			; 4 (33)
	STA	GRP1				; 3 (36)

	STA	WSYNC
pic64px_OddFrame_LineDummy
	STA	HMOVE				; 3 

	sleep	7
						; 3 (10)	
	LDA	pic64px_PF,y			; 4 (14)
	STA	PF2				; 3 (17)
	LDA	frameColor
	sleep	2
	STA	COLUPF				; 3 (24)
	STA	COLUP0				; 3 (31)
	STA	COLUP1				; 3 (34)
	
	LDA	pic64px_00,y			; 4 (38)
	STA	GRP0				; 3 (41)
	LDA	pic64px_02,y			; 4 (45)
	STA	GRP1				; 3 (48)

	LDA	pic64px_04,y			; 4 (52)
	STA	GRP0				; 3 (55)

	STX	GRP1				; 3 (58)

	LDA	#$80				; 2 (67)
	STA 	HMP0				; 3 (70)
	STA 	HMP1				; 3 (73)
	JMP	pic64px_OddFrame_Line2

pic64px_OddFrame_Line1
	STA	HMOVE				; 3 

	LDA	pic64px_BGColor,y		; 4 (7)
	STA	COLUBK				; 3 (10)	
	LDA	pic64px_PF,y			; 4 (14)
	STA	PF2				; 3 (17)
	LDA	pic64px_PFColor,y		; 4 (21)
	STA	COLUPF				; 3 (24)
		
	LDA	pic64px_Color,y			; 4 (28)
	STA	COLUP0				; 3 (31)
	STA	COLUP1				; 3 (34)
	
	LDA	pic64px_00,y			; 4 (38)
	STA	GRP0				; 3 (41)
	LDA	pic64px_02,y			; 4 (45)
	STA	GRP1				; 3 (48)

	LDA	pic64px_04,y			; 4 (52)
	STA	GRP0				; 3 (55)

	STX	GRP1				; 3 (58)

	LDA	#$80				; 2 (67)
	STA 	HMP0				; 3 (70)
	STA 	HMP1				; 3 (73)

pic64px_OddFrame_Line2
	STA 	WSYNC
	STA	HMOVE				; 3 

	LDA	pic64px_01,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_03,y			; 4 
	STA	GRP1				; 3 

	DEY
	LAX	pic64px_06,y			; 4

	INY

	sleep	12

	LDA	pic64px_05,y			; 4 
	STA	GRP0				; 3 

	LDA	pic64px_07,y			; 4 
	STA	GRP1				; 3 

						; (56, but 52?!)
	LDA	#$00				; 2 (58)
	STA 	HMP0				; 3 (61)
	STA 	HMP1				; 3 (64)
	DEY					; 2 (66)
	CPY	temp02				; 3 (69)
	BEQ	pic64px_Reset			; 2 (71)	
	JMP	pic64px_OddFrame_Line1		; 3 (74)
	

pic64px_EvenFrame
	_sleep	30
	sleep	3

	LDA	#0
	STA	GRP0
	STA	GRP1

	LAX	pic64px_07,y
	TXS
	LAX	pic64px_05,y

	LDA	#$00				
	STA 	HMP0				
	LDA	#$20				
	STA 	HMP1

pic64px_EvenFrame_LineDummy	
	STA 	WSYNC
	STA	HMOVE
	_sleep	50
	sleep	3

	LDA	pic64px_PFColor,y		
	STA	COLUPF	

	LDA	#$00				; 2 
	STA 	HMP0				; 3 
	STA 	HMP1				; 3 
	JMP	pic64px_EvenFrame_Line2

pic64px_EvenFrame_Line1			
	STA 	WSYNC				; 76
	STA	HMOVE				; 3

	LDA	pic64px_BGColor,y		; 4 (7)
	STA	COLUBK				; 3 (10)	
	LDA	pic64px_PF,y			; 4 (14)
	STA	PF2				; 3 (17)
	sleep	5
		
	LDA	pic64px_Color,y			; 4 
	STA	COLUP0				; 3 
	STA	COLUP1				; 3 (34 - 31)

	LDA	pic64px_01,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_03,y			; 4 

	STA	GRP1				; 3 
	STX	GRP0				; 3 
	TSX					; 2
	STX	GRP1				; 3

	sleep	8

						; (66)
	LDA	#$00				; 2 (68)
	STA 	HMP0				; 3 (71)
	STA 	HMP1				; 3 (74)
pic64px_EvenFrame_Line2
	STA	HMOVE				; 3 

	LDA	pic64px_00,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_02,y			; 4 
	STA	GRP1				; 3 
	
	DEY
	LAX	pic64px_07,y	
	TXS
	LAX	pic64px_05,y
	INY

	LDA	#$80				; 2 
	STA 	HMP0				; 3 
	STA 	HMP1				; 3 

	sleep	6
	
	LDA	pic64px_04,y			; 4 
	STA	GRP0				; 3 
	LDA	pic64px_06,y			; 4 
	STA	GRP1				; 3 

	DEY
	LDA	pic64px_PFColor,y		
	STA	COLUPF

	CPY	temp02				; 3 (71)
	BNE	pic64px_EvenFrame_Line1		; 2 (73)

pic64px_Reset