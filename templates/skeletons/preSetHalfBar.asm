	LDA	frameColor		; 3		
	STA	COLUPF			; 3

	LDA	temp03			; 3 
	CMP	#8			; 2 
	BCS	#NAME#_LargerThan7	; 2 
	STY	PF1			; 3 
	TAY				; 2 
	LDA	#BANK#_Bar_Normal,y	; 5 
	STA	PF2			; 3 
	JMP	#NAME#_Values_Done	; 3 
#NAME#_LargerThan7
	SEC				; 2 
	SBC	#8			; 2 
	STX	PF2			; 3 
	TAY				; 2 
	LDA	#BANK#_Bar_Inverted,y	; 5 
	STA	PF1			; 3 
#NAME#_Values_Done
	LDA	temp03			; 3
	LSR				; 2
	CLC				; 2
	ADC	temp04			; 3
	STA	temp04			; 3
	
	LDA	temp03			; 3
	LSR				; 2
	CLC				; 2
	ADC	temp05			; 3
	STA	temp05			; 3
