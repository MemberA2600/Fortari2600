*
*	#VAR01#		: Letter01
*	#VAR02#		: Letter02
*	#VAR03#		: Letter03
*	#VAR04#		: Letter04
*	#VAR05#		: Letter05
*	#VAR06#		: Letter06
*	#VAR07#		: Letter07
*	#VAR08#		: Letter08
*	#VAR09#		: Letter09
*	#VAR10#		: Letter10
*	#VAR11#		: Letter11
*	#VAR12#		: Letter12
*			
*	temp18		: Text Front Color
*	temp19		: Text Back  Color
*

#NAME#_DynamicText_Begin

	LDX	#0			; 2
	LDA	frameColor		; 3
	STA	WSYNC			; 76
	STA	COLUBK			; 3
	STA	COLUPF			; 3 (6)
	STA	COLUP0			; 3 (9)
	STA	COLUP1			; 3 (12)
	
	STX	PF0			; 3 (15)
	STX	PF1			; 3 (18)
	STX	PF2			; 3 (21)
	
	STX	GRP1			; 3 (24)
	STX	GRP0			; 3 (27)
	STX	ENAM0			; 3 (30)
	STX	ENAM1			; 3 (33)
	STX	ENABL			; 3 (36)

	STX	RESP0			; 3 (39)
	STX	RESP1			; 3 (42)

	STX	REFP0			; 3 (45)
	STX	REFP1			; 3 (48)

	LDA	#$00			; 2 (50)
	STA	HMP0			; 3 (53)
	LDA	#$10			; 2 (55)
	STA	HMP1			; 3 (58)

	LDA	#$03			; 2 (62)
	STA	NUSIZ0			; 3 (65)
	STA	NUSIZ1			; 3 (68)

	STA	WSYNC			; 76
	STA	HMOVE			; 3

	LDA	temp18			; 3 (6)
	STA	COLUP0			; 3 (9)
	STA	COLUP1			; 3 (12)
	
	LDA	counter			; 3 
	AND	#%00000001		; 2 
	CMP	#%00000001		; 2 		
	BEQ	#NAME#_DynamicText_Otherjump	; 2 
	JMP	#NAME#_DynamicText_Even_Begin	; 3 
#NAME#_DynamicText_Otherjump
	JMP	#NAME#_DynamicText_Odd_Begin	; 3 
	
	_align	250

#NAME#_DynamicText_Odd_Begin

	LDY	#VAR09#				; 3 
	LDA	BankXXFont_Right_Line4,y	; 5 
	LDY	#VAR10#				; 3 
	ORA	BankXXFont_Left_Line4,y		; 5  	
	TAX					; 2 

	LDY	temp19				; 3 

#NAME#_DynamicText_Odd_Line0
	STA	WSYNC				; 76
	STY	COLUBK

	LDY	#VAR01#				; 3
	LDA	BankXXFont_Right_Line4,y	; 4 (7)
	LDY	#VAR02#				; 3 (10)
	ORA	BankXXFont_Left_Line4,y		; 4 (14) 	
	STA	GRP0				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP1				; 3 (22)

	sleep	3

	LDY	#VAR05#				; 3 (32)
	LDA	BankXXFont_Right_Line4,y	; 4 (36)
	LDY	#VAR06#				; 3 (39)
	ORA	BankXXFont_Left_Line4,y		; 4 (43) 	
	STA	GRP0				; 3 (47)

	sleep	2

	STX	GRP0				; 3 (52)

	LDY	#VAR11#				; 3 (55)
	LDA	BankXXFont_Right_Line3,y	; 4 (59)
	LDY	#VAR12#				; 3 (62)
	ORA	BankXXFont_Left_Line3,y		; 4 (66) 	
	TAX					; 2 (68)

#NAME#_DynamicText_Odd_Line1
	STA	WSYNC				; 76
	LDY	#VAR03#				; 3
	LDA	BankXXFont_Right_Line3,y	; 4 (7)
	LDY	#VAR04#				; 3 (10)
	ORA	BankXXFont_Left_Line3,y		; 4 (14) 	
	STA	GRP1				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP0				; 3 (22)

	sleep	8

	LDY	#VAR07#				; 3 (34)
	LDA	BankXXFont_Right_Line3,y	; 4 (38)
	LDY	#VAR08#				; 3 (41)
	ORA	BankXXFont_Left_Line3,y		; 4 (44) 	
	STA	GRP1				; 3 (47)

	sleep	2

	STX	GRP1				; 3 (52)

	LDY	#VAR09#				; 3 (55)
	LDA	BankXXFont_Right_Line2,y	; 4 (59)
	LDY	#VAR10#				; 3 (62)
	ORA	BankXXFont_Left_Line2,y		; 4 (66) 	
	TAX					; 2 (68)

#NAME#_DynamicText_Odd_Line2
	STA	WSYNC				; 76
	LDY	#VAR01#				; 3
	LDA	BankXXFont_Right_Line2,y	; 4 (7)
	LDY	#VAR02#				; 3 (10)
	ORA	BankXXFont_Left_Line2,y		; 4 (14) 	
	STA	GRP0				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP1				; 3 (22)

	sleep	6

	LDY	#VAR05#				; 3 (32)
	LDA	BankXXFont_Right_Line2,y	; 4 (36)
	LDY	#VAR06#				; 3 (39)
	ORA	BankXXFont_Left_Line2,y		; 4 (43) 	
	STA	GRP0				; 3 (47)

	sleep	2

	STX	GRP0				; 3 (52)

	LDY	#VAR11#				; 3 (55)
	LDA	BankXXFont_Right_Line1,y	; 4 (59)
	LDY	#VAR12#				; 3 (62)
	ORA	BankXXFont_Left_Line1,y		; 4 (66) 	
	TAX					; 2 (68)

#NAME#_DynamicText_Odd_Line3
	STA	WSYNC				; 76
	LDY	#VAR03#				; 3
	LDA	BankXXFont_Right_Line1,y	; 4 (8)
	LDY	#VAR04#				; 3 (11)
	ORA	BankXXFont_Left_Line1,y		; 4 (16) 	
	STA	GRP1				; 3 (19)

	LDA	#0				; 2 (21)
	STA	GRP0				; 3 (24)

	sleep	8

	LDY	#VAR07#				; 3 (27)
	LDA	BankXXFont_Right_Line1,y	; 4 (31)
	LDY	#VAR08#				; 3 (34)
	ORA	BankXXFont_Left_Line1,y		; 4 (38) 	
	STA	GRP1				; 3 (41)

	sleep	2

	STX	GRP1				; 3 (46)

	LDY	#VAR09#				; 3 (49)
	LDA	BankXXFont_Right_Line0,y	; 4 (54)
	LDY	#VAR10#				; 3 (57)
	ORA	BankXXFont_Left_Line0,y		; 4 (61) 	
	TAX					; 2 (63)

#NAME#_DynamicText_Odd_Line2
	STA	WSYNC				; 76
	LDY	#VAR01#				; 3
	LDA	BankXXFont_Right_Line0,y	; 4 (7)
	LDY	#VAR02#				; 3 (10)
	ORA	BankXXFont_Left_Line0,y		; 4 (14) 	
	STA	GRP0				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP1				; 3 (21)

	sleep	6

	LDY	#VAR05#				; 3 (31)
	LDA	BankXXFont_Right_Line0,y	; 4 (35)
	LDY	#VAR06#				; 3 (38)
	ORA	BankXXFont_Left_Line0,y		; 4 (42) 	
	STA	GRP0				; 3 (45)

	sleep	2

	STX	GRP0				; 3 (50)

	sleep	12
	
	JMP	#NAME#_DynamicText_Reset

	_align	250

#NAME#_DynamicText_Even_Begin
	LDY	#VAR11#				; 3 
	LDA	BankXXFont_Right_Line4,y	; 4 
	LDY	#VAR12#				; 3 
	ORA	BankXXFont_Left_Line4,y		; 4  	
	TAX					; 2 

	LDY	temp19				; 3 

#NAME#_DynamicText_Even_Line0
	STA	WSYNC				; 76
	STY	COLUBK				; 3

	LDY	#VAR03#				; 3
	LDA	BankXXFont_Right_Line4,y	; 4 (7)
	LDY	#VAR04#				; 3 (10)
	ORA	BankXXFont_Left_Line4,y		; 4 (14) 	
	STA	GRP1				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP0				; 3 (22)

	sleep	5

	LDY	#VAR07#				; 3 (34)
	LDA	BankXXFont_Right_Line4,y	; 4 (38)
	LDY	#VAR08#				; 3 (41)
	ORA	BankXXFont_Left_Line4,y		; 4 (45) 	
	STA	GRP1				; 3 (48)

	sleep	2

	STX	GRP1				; 3 (53)

	LDY	#VAR09#				; 3 (56)
	LDA	BankXXFont_Right_Line3,y	; 4 (60)
	LDY	#VAR10#				; 3 (63)
	ORA	BankXXFont_Left_Line3,y		; 4 (67) 	
	TAX					; 2 (69)

#NAME#_DynamicText_Even_Line1
	STA	WSYNC				; 76
	LDY	#VAR01#				; 3
	LDA	BankXXFont_Right_Line3,y	; 4 (7)
	LDY	#VAR02#				; 3 (10)
	ORA	BankXXFont_Left_Line3,y		; 4 (14) 	
	STA	GRP0				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP1				; 3 (21)

	sleep	6

	LDY	#VAR05#				; 3 (31)
	LDA	BankXXFont_Right_Line3,y	; 4 (35)
	LDY	#VAR06#				; 3 (38)
	ORA	BankXXFont_Left_Line3,y		; 4 (42) 	
	STA	GRP0				; 3 (45)

	sleep	2

	STX	GRP0				; 3 (50)

	LDY	#VAR11#				; 3 (53)
	LDA	BankXXFont_Right_Line2,y	; 4 (57)
	LDY	#VAR12#				; 3 (60)
	ORA	BankXXFont_Left_Line2,y		; 4 (64) 	
	TAX					; 2 (66)

#NAME#_DynamicText_Even_Line2
	STA	WSYNC				; 76
	LDY	#VAR03#				; 3
	LDA	BankXXFont_Right_Line2,y	; 4 (7)
	LDY	#VAR04#				; 3 (10)
	ORA	BankXXFont_Left_Line2,y		; 4 (14) 	
	STA	GRP1				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP0				; 3 (22)

	sleep	8

	LDY	#VAR07#				; 3 (34)
	LDA	BankXXFont_Right_Line2,y	; 4 (38)
	LDY	#VAR08#				; 3 (41)
	ORA	BankXXFont_Left_Line2,y		; 4 (45) 	
	STA	GRP1				; 3 (48)

	sleep	2

	STX	GRP1				; 3 (53)

	LDY	#VAR09#				; 3 (56)
	LDA	BankXXFont_Right_Line1,y	; 4 (60)
	LDY	#VAR10#				; 3 (63)
	ORA	BankXXFont_Left_Line1,y		; 4 (67) 	
	TAX		

#NAME#_DynamicText_Even_Line3
	STA	WSYNC				; 76
	LDY	#VAR01#				; 3
	LDA	BankXXFont_Right_Line1,y	; 4 (8)
	LDY	#VAR02#				; 3 (11)
	ORA	BankXXFont_Left_Line1,y		; 4 (16) 	
	STA	GRP0				; 3 (19)

	LDA	#0				; 2 (21)
	STA	GRP1				; 3 (24)

	sleep	6

	LDY	#VAR05#				; 3 (27)
	LDA	BankXXFont_Right_Line1,y	; 4 (32)
	LDY	#VAR06#				; 3 (35)
	ORA	BankXXFont_Left_Line1,y		; 4 (40) 	
	STA	GRP0				; 3 (43)

	sleep	2

	STX	GRP0				; 3 (46)

	LDY	#VAR11#				; 3 (49)
	LDA	BankXXFont_Right_Line0,y	; 4 (54)
	LDY	#VAR12#				; 3 (57)
	ORA	BankXXFont_Left_Line0,y		; 4 (61) 	
	TAX					; 2 (63)

#NAME#_DynamicText_Even_Line4
	STA	WSYNC				; 76
	LDY	#VAR03#				; 3
	LDA	BankXXFont_Right_Line0,y	; 4 (7)
	LDY	#VAR04#				; 3 (10)
	ORA	BankXXFont_Left_Line0,y		; 4 (14) 	
	STA	GRP1				; 3 (17)

	LDA	#0				; 2 (19)
	STA	GRP0				; 3 (22)

	sleep	8

	LDY	#VAR07#				; 3 (34)
	LDA	BankXXFont_Right_Line0,y	; 4 (38)
	LDY	#VAR08#				; 3 (41)
	ORA	BankXXFont_Left_Line0,y		; 4 (45) 	
	STA	GRP1				; 3 (48)

	sleep	2

	STX	GRP1				; 3 (53)

	sleep	13

#NAME#_DynamicText_Reset
	LDX	#0			; 2
	STX	GRP1			; 3 
	STX	GRP0			; 3

	LDA	frameColor		; 3
	STA	WSYNC			; 76
	STA	COLUBK			; 3
	STA	COLUPF			; 3 (6)
	STA	COLUP0			; 3 (9)
	STA	COLUP1			; 3 (12)
	STX	HMCLR			; 3 (30)