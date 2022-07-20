	LDA	temp19			; 3 
	CMP	#0			
	BEQ	#NAME#_NoAdd1_Icon1
	CLC
	ADC	#1
#NAME#_NoAdd1_Icon1

	TAY				; 2 
	LDA	#BANK#_Bar_Normal,y	; 5 
	LSR				; 2
	LSR				; 2
	LSR				; 2
	LSR				; 2
	STA	temp18			; 3

	LDA	#BANK#_Bar_Inverted,y	; 5
	LSR				; 2
	LSR				; 2
	LSR				; 2
	LSR				; 2

	!!!DOTS_PF2!!!
	STA	PF2			; 3

	LDA	#$0f			; 2
	CMP	temp19			; 3
	BCS	#NAME#_NoSTAThat_Icon1 	; 2	
	STA	temp19			; 3
#NAME#_NoSTAThat_Icon1
	LDA	temp19			; 3
	CLC				; 2
	ADC	temp03			; 3
	STA	temp03			; 3
