##NAME##_TopBottom
*
*	variables:
*
*	##NAME##_Selected_Item
*
*	Constants
*
*	##NAME##_Item_Number
*	##NAME##_Largest_Number
*
*	Sprite_Ponter0:		temp01-temp02
*	Sprite_Ponter1:		temp03-temp04
*	Sprite_Ponter2:		temp05-temp06
*	Sprite_Ponter3:		temp07-temp08
*	Sprite_Ponter4:		temp09-temp10
*	Sprite_Ponter5:		temp11-temp12
*	LastDisplay		temp13
*	CurrentDisplayed	temp14
*	FontColor_Pointer	temp15-temp16
*	Selected + Offset	temp18
*	BackColorSaved		temp19		
*
*	I cannot find a proper reason why you would have more than one of these
*	on one screen, so there won't be any kernel
*	Don't need color pointers, since things are pretty fixed.
*

##NAME##_TopBottom_Begin

	LDA	frameColor
	STA	WSYNC		; 76
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

	sleep	2
	STA	RESP0		; 3 (40) Set the X pozition of sprite.	
	STA	temp14		; 3 (44)

	LDA	#$03		; 2 (46)
	STA	NUSIZ0		; 3 (49)

	LDA	#1		; 2 (51)
	STA	CTRLPF		; 3 (54)
	LDA	#255		; 2 (56) 
	STA	PF1		; 3 (59)
	STA	PF2		; 3 (62)

	LDA	##NAME##_Selected_Item	; 3 (65)
!!!Insert_Here_Calculation!!!
	LDX	#254		; 2 (67)

	STA	WSYNC		; 76

*
*	Get segmentNumber based on the selected one.
*	MaxNum of Segments: 6 (66 cycles)
*
##NAME##_GetSegmentLoopXX
	INX					; 2
	INX					; 2
	CMP	##NAME##_segmentBorders,x	; 5
	BCS	##NAME##_GetSegmentLoopXX	; 2
	STX	$f0

	DEX
	DEX					; 4
	STA	WSYNC				; 76

*
*	Get the first to display
*

	LDA 	##NAME##_segmentBorders,x	; 5
	STA	temp19				; 3 (8)
	ASL
	ASL
	ASL					; 6 (14)
	STA	temp18				; 3 (17)

*
*	Initizalize pointers
*
	LDA	#<##NAME##__spriteData_0	; 2 (19)
	CLC					; 2 (21)
	ADC	temp18				; 3 (24)
	STA	temp01				; 3 (27)
	LDA	#>##NAME##__spriteData_0	; 2 (29)
	STA	temp02				; 3 (32)

	LDA	#<##NAME##__spriteData_1	; 2 (34)
	CLC					; 2 (36)
	ADC	temp18				; 3 (39)
	STA	temp03				; 3 (42)
	LDA	#>##NAME##__spriteData_1	; 2 (44)
	STA	temp04				; 3 (47)

	LDA	#<##NAME##__spriteData_2	; 2 (49)
	CLC					; 2 (51)
	ADC	temp18				; 3 (54)
	STA	temp05				; 3 (57)
	LDA	#>##NAME##__spriteData_2	; 2 (59)
	STA	temp06				; 3 (62)

	LDA	#<##NAME##__spriteData_3	; 2 (64)
	CLC					; 2 (66)
	ADC	temp18				; 3 (69)
	STA	temp07				; 3 (72)
	LDA	#>##NAME##__spriteData_3	; 2 (74)
	STA	temp08				; 3 (1)

	LDA	#<##NAME##__spriteData_4	; 2 (3)
	CLC					; 2 (5)
	ADC	temp18				; 3 (8)
	STA	temp09				; 3 (11)
	LDA	#>##NAME##__spriteData_4	; 2 (13)
	STA	temp10				; 3 (16)

	LDA	#<##NAME##__spriteData_5	; 2 (18)
	CLC					; 2 (20)
	ADC	temp18				; 3 (23)
	STA	temp11				; 3 (26)
	LDA	#>##NAME##__spriteData_5	; 2 (28)
	STA	temp12				; 3 (31)
*
*	Set the number of items to be displayed.	
*
	LDA	##NAME##_segmentBorders+1,x	; 5 (36)
	SEC					; 2 (38)
	SBC	temp19				; 3 (41)
	STA	temp13				; 3 (44)
	
	LDA	##NAME##_Selected_Item		; 3 (47)
!!!Insert_Here_Calculation!!!
	SEC					; 2 (49)
	SBC	temp19				; 3 (52)	
	STA	temp18				; 3 (55)


	JMP	##NAME##_Skip_Increment		; 3 (58)
*
*	Set the next line of data
*

##NAME##_Get_Next_Data

	LDA	frameColor			
	STA	WSYNC				; 76	
	STA	COLUPF				; 3
	LDA	#0				; 2 (5)
	STA	GRP0				; 3 (8)
*	STA	PF1				; 3 (11)
*	STA	PF2				; 3 (14)
	DEC	temp13				; 5 (19)
	INC	temp14				; 5 (24)
	LDA	temp13				; 3 (27)
	CMP	#255				; 3 (30)
	BEQ	##NAME##_FinishThisShit		; 2 (32)
*
*	Increment pointers
*
	LDA	temp01		; 3 (29)
	CLC			; 2 (31)
	ADC	#8		; 2 (33)
	STA	temp01		; 3 (36)

	LDA	temp03		; 3 (39)
	CLC			; 2 (41)
	ADC	#8		; 2 (43)
	STA	temp03		; 3 (46)

	LDA	temp05		; 3 (49)
	CLC			; 2 (51)
	ADC	#8		; 2 (53)
	STA	temp05		; 3 (56)

	LDA	counter		; 3 (59)
	AND	#%00000001	; 2 (61)
	CMP	#%00000001	; 2 (63)
	BNE	##NAME##_NoCorrection	; 2 (65)
	sleep	6
	STA	HMOVE		; 3 (74)
	STA	WSYNC
	JMP	##NAME##_Corrected
##NAME##_NoCorrection
	sleep	12
##NAME##_Corrected

	LDA	temp07		; 3 (1)
	CLC			; 2 (3)
	ADC	#8		; 2 (5)
	STA	temp07		; 3 (8)

	LDA	temp09		; 3 (11)
	CLC			; 2 (13)
	ADC	#8		; 2 (15)
	STA	temp09		; 3 (18)

	LDA	temp11		; 3 (21)
	CLC			; 2 (23)
	ADC	#8		; 2 (25)
	STA	temp11		; 3 (28)

##NAME##_Skip_Increment

	LDA	temp14				; 3 (40)
	CMP	temp18 				; 3 (43)
	BNE 	##NAME##_No_SelectedColor	; 2 (46)

	LDA	#<##NAME##_Color_SELECTED_FG	; 2
	LDY	#>##NAME##_Color_SELECTED_FG	; 2
	JMP	##NAME##_SelectedColorDone	; 3 (53)
##NAME##_No_SelectedColor
	sleep	3
	LDA	#<##NAME##_Color_UNSELECTED	; 2
	LDY	#>##NAME##_Color_UNSELECTED	; 2 (53)
##NAME##_SelectedColorDone
	STA	temp15				; 3 (56)
	STY	temp16				; 3 (59)

	LDA	counter				; 3 (62)
	AND	#%00000001			; 2 (64)
	TAY					; 2 (66)

	LDA	##NAME##_First_Offset,y		; 4 (73)
	STA	HMP0				; 3 (76)	
	STA	WSYNC				; 76
	STA	HMOVE				; 3 

	JMP	##NAME##_Get_Next_Data_NoWSYNC	; 3 (6)

##NAME##_First_Offset
	BYTE	#$c0
	BYTE	#$80

	align	256
##NAME##_Get_Next_Data_NoWSYNC

*
*	Set the line height, and also the number of lines.
*
	LDY	#7					; 2 (10)
*
*	Get First Color
*
	LDA	temp18					; 3 (13)
	CMP	temp14					; 3 (16)
	BEQ	##NAME##_SelectedColor			; 2 (18)

	NOP						; 2 (20)
	LDA	frameColor				; 3 (22)
	JMP	##NAME##_NotSelectedColor		; 3 (25)

##NAME##_SelectedColor
	sleep	3
	LDA	##NAME##_Color_SELECTED_BG,y		; 8 (25)
##NAME##_NotSelectedColor
	STA	temp19					; 3 (29)

	LDA	counter					; 3 (30)
	AND	#%00000001				; 2 (32)
	CMP	#%00000001				; 2 (34)
	BNE	##NAME##_OddFrame_Begin			; 2 (36)
	JMP	##NAME##_EvenFrame_Begin		; 3 (39)

##NAME##_OddFrame_Begin
	sta	WSYNC		; 76
##NAME##_Odd_Loop_Begin
	STA	HMOVE		; 3

	LDA	temp19		; 3 (6)
	STA	COLUPF		; 3 (12)

	LDA	(temp03),y		; 5 (17)
	STA	GRP0			; 3 (20)	

	LDA	(temp15),y		; 5 (25)
	STA	COLUP0			; 3 (28)
	
	sleep	11
	
	LAX	(temp11),y		; 5 (38)

	LDA	(temp07),y		; 5 (43)
	STA	GRP0			; 3 (46)
	STX	GRP0			; 3 (51)

	LDA	#$00			; 2 (53)
	STA	HMP0			; 3 (56)
	
	sleep	16
*
*	This is the early HMOVE!
*
##NAME##_Odd_Second_Line

	STA	HMOVE		; 3 (1)
	LDA	#$80		; 2 (3)
	STA 	HMP0		; 3 (6)

	LDA	(temp01),y	; 5 (11)
	STA	GRP0		; 3 (14)

	LDA	temp18				; 3 (17)
	CMP	temp14				; 3 (20)
	BEQ	##NAME##_SelectedColor2		; 2 (22)

	NOP						; 2 (25)
	LDA	frameColor				; 3 (27)
	JMP	##NAME##_NotSelectedColor2		; 3 (30)

##NAME##_SelectedColor2
	sleep	3
	LDA	##NAME##_Color_SELECTED_BG,y		; 8 (30)
##NAME##_NotSelectedColor2
	STA	temp19					; 3 (33)
	
	LAX	(temp09),y		; 5 (37)
	LDA	(temp05),y		; 5 (43)
	STA	GRP0			; 3 (46)
	sleep	3
	STX	GRP0			; 3 (50)
	
	sleep	5			
	LDX	frameColor		; 3 (55)
	LDA	#0			; 2 (57)
	STA	GRP0			; 3 (60)

	DEY				; 2 (63)
	CPY	#255			; 2 (65)
	BNE	##NAME##_OddFrame_Begin ; 2 (67)		
	STX	COLUPF			; 3 (70)
	JMP	##NAME##_Get_Next_Data	; 3 (73)

##NAME##_EvenFrame_Begin
	LDA	#$00		; 2
	STA	HMP0		; 3
	sleep	16

##NAME##_Even_Loop_Begin_Dummy_Wait
	sleep	9
##NAME##_Even_Loop_Begin_Dummy_Wait2
	sleep	3
##NAME##_Even_Loop_Begin
	STA	HMOVE		; 3 (1)
	LDA	#$80		; 2 (3)
	STA 	HMP0		; 3 (6)

	LDA	temp19		; 3 (9)
	STA	COLUPF		; 3 (12)

	LDA	(temp01),y	; 5 (17)
	STA	GRP0		; 3 (20)

	LDA	(temp15),y		; 5 (25)
	STA	COLUP0			; 3 (28)

	sleep	5	
	
	LAX	(temp09),y		; 5 (37)
	LDA	(temp05),y		; 5 (43)
	STA	GRP0			; 3 (46)
	sleep	3
	STX	GRP0			; 3 (50)
	
	STA	WSYNC			; 76

##NAME##_Even_Loop_SecondLine
	STA	HMOVE		; 3

	LDA	(temp03),y		; 5 (8)
	STA	GRP0			; 3 (11)	

	LDA	temp18				; 3 (14)
	CMP	temp14				; 3 (17)
	BEQ	##NAME##_SelectedColor3		; 2 (19)

	NOP					; 2 (22)
	LDA	frameColor			; 3 (24)
	JMP	##NAME##_NotSelectedColor3	; 3 (27)

##NAME##_SelectedColor3
	sleep	3
	LDA	##NAME##_Color_SELECTED_BG,y	; 8 (27)
##NAME##_NotSelectedColor3
	STA	temp19				; 3 (30)
	
	sleep	6
	
	LAX	(temp11),y		; 5 (38)

	LDA	(temp07),y		; 5 (43)
	STA	GRP0			; 3 (46)
	STX	GRP0			; 3 (51)

	LDA	#$00			; 2 (53)
	STA	HMP0			; 3 (56)

	sleep	3	

	DEY				; 2 (67)
	CPY	#255			; 2 (69)
	BNE	##NAME##_Even_Loop_Begin_Dummy_Wait2 ; 2 (71)
	JMP	##NAME##_Get_Next_Data	; 3 (74)

##NAME##_FinishThisShit
	LDA	#0
	STA	GRP0
	STA	PF1
	STA	PF2
	STA	HMCLR
	STA	WSYNC
	LDA	counter
	AND	#%00000001
	CMP	#%00000001
	BNE	##NAME##_ZOOLMOTHERFUCKERZOOL
	STA	WSYNC
##NAME##_ZOOLMOTHERFUCKERZOOL
	LDA	###NAME##_Largest_Number
	SEC
	SBC	temp14
	TAX
	INX
##NAME##_FillerLoop
	CPX	#0
	BEQ	##NAME##_FillerLoopEnd
	DEX
	LDY	#20
##NAME##_FillerLoop2
	STA	WSYNC
	DEY
	CPY	#0	
	BNE	##NAME##_FillerLoop2
	JMP	##NAME##_FillerLoop
##NAME##_FillerLoopEnd
	STA	WSYNC
*
*	Uncomment for testing.
*
*	LDA	#$8a
*	STA	COLUBK
*	STA	WSYNC
*	STA	WSYNC	
*	STA	WSYNC
*	LDA	frameColor
*	STA	COLUBK