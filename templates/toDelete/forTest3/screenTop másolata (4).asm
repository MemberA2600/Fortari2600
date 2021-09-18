pic96px_KernelStart
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
	sleep	3		;   (34)	
	STA	RESP1		; 3 (37) Set the X pozition of sprites.

	LDA	counter		; 3 (6)
	AND	#%00000001	; 2 (8)
	CMP	#%00000001	; 2 (10)
	BNE	pic96px_OddFrame  ; 2 (12)
	JMP	pic96px_EvenFrame ; 3 (15)	

	align	256

pic96px_OddFrame
	sleep	54

	LDA	#255
	STA	GRP1
	STA	GRP0
	STA	PF2

	LDA	#$00				; 2
	STA 	HMP0				; 3 
	LDA	#$20				; 2
	STA 	HMP1				; 3 
	STA 	WSYNC				; 76

pic96px_OddFrame_Line1
	STA	HMOVE				; 3 

	lda	#$1e	
	STA	COLUP0
	STA	COLUP1				; 8 (11)
	LDA	#$58
	STA	COLUPF

	sleep	49
						; (65)
	LDA	#$80				; 2 (67)
	STA 	HMP0				; 3 (70)
	STA 	HMP1				; 3 (73)

pic96px_OddFrame_Line2
	STA 	WSYNC
	STA	HMOVE				; 3 

	sleep	48
						; (56, but 52?!)
	LDA	#$00				; 2 (58)
	STA 	HMP0				; 3 (61)
	STA 	HMP1				; 3 (64)
	DEY					; 2 (66)
	CPY	temp02				; 3 (69)
	BEQ	pic96px_Reset			; 2 (71)	
	JMP	pic96px_OddFrame_Line1		; 3 (74)

pic96px_EvenFrame
	sleep	54

	LDA	#255				
	STA	GRP1				
	STA	GRP0				
	STA	PF2

	LDA	#$80				
	STA 	HMP0				
	LDA	#$A0				
	STA 	HMP1	

pic96px_EvenFrame_Line1			
	STA 	WSYNC				; 76
	STA	HMOVE				; 3
	lda	#$1e	
	STA	COLUP0
	STA	COLUP1				; 8 (11)

	LDA	#$58
	STA	COLUPF

	sleep	46
						; (66)
	LDA	#$00				; 2 (68)
	STA 	HMP0				; 3 (71)
	STA 	HMP1				; 3 (74)
pic96px_EvenFrame_Line2
	STA	HMOVE				; 3 
	
	sleep	55				; (58)

	LDA	#$80				; 2 (60)
	STA 	HMP0				; 3 (63)
	STA 	HMP1				; 3 (66)
	DEY					; 2 (68)
	CPY	temp02				; 3 (71)
	BNE	pic96px_EvenFrame_Line1		; 2 (73)

pic96px_Reset
	LDA	frameColor
	STA	WSYNC		; (76)
	STA	COLUBK	
	STA	COLUP0
	STA	COLUP1	
	STA	COLUPF
	LDA	#0		
	STA	PF0
	STA	PF1		
	STA	PF2		
	STA	GRP0		
	STA	GRP1		
	STA	VDELP0		
	STA	VDELP1	
		

	JMP	TestEnded

pic96px_Data_Section

	align	256



TestEnded