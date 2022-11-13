*
*	temp01:		 stepY
*	temp02:		 MatrixX (Decremented by one)
*	temp03:		 MatrixY (Decremented by one)
*	temp04: 	 ForeGround Colour
*	temp05: 	 Background Colour
*	temp06:		 Ball Colour
*	temp07 + temp08: Sprite0 Pointer
*	temp09 + temp10: Sprite1 Pointer
*	temp11:		 BallX
*	temp12:		 BallY
*	temp13 + temp14: Gradient Pointer
*	temp15:		 Ball On/Off
*	temp16 + temp17: JumpBack
*

	_align	90

#BANK#_MiniMap_Kernel_MainLoop
	STA	WSYNC		; 76

	STA	COLUPF		; 3 
	STA	COLUP0		; 3 (6)
	STA	COLUP1		; 3 (9)

	LDA	(temp07),y	; 5 (14)
	STA	GRP0		; 3 (17)

	LDA	(temp09),y	; 5 (22)
	STA	GRP1		; 3 (25)

	LDA	temp15
	BYTE	#$8D
	BYTE	#ENABL
	BYTE	#0

	LDX	temp06
	LDA	temp05		; 3 (36)
	STA	COLUBK		; 3 (39)
	STX	COLUPF

	sleep	3
	LDA	frameColor
	TSX
	STX	COLUPF
	STA	COLUBK

	STA	WSYNC		; 76

	DEY			; 2
	LDA	(temp13),y	; 5
	ADC	temp04		; 3 
	STA	temp19		; 3 (15)
	
	CPY 	temp12
	BNE	#BANK#_MiniMap_Kernel_Not_Enabled2
	LDA	#2
	JMP	#BANK#_MiniMap_Kernel_Enabled2
#BANK#_MiniMap_Kernel_Not_Enabled2
	sleep	3
	LDA	#0
#BANK#_MiniMap_Kernel_Enabled2
	STA	temp15

	INY      		; 2 

	sleep	4
	
	LDX	temp06
	LDA	temp05		
	STA	COLUBK		
	STX	COLUPF

	sleep	3
	LDA	frameColor
	TSX
	STX	COLUPF
	STA	COLUBK

	DEY	
	BMI	#BANK#_MiniMap_Kernel_EndLoop

	LDA	temp19
	TAX
	TXS

	JMP	#BANK#_MiniMap_Kernel_MainLoop
#BANK#_MiniMap_Kernel_EndLoop

	STA	WSYNC		; 76
	LDX	#0
	STX	ENABL
	STX	ENAM1

	LDA	#%11111111
	STA	PF2
	STA	WSYNC		; 76
	JMP	(temp16)
