	LDA	temp19			; 3 
	CMP	#0			
	BEQ	#NAME#_NoAdd1_PF2
	CLC
	ADC	#1
#NAME#_NoAdd1_PF2

	TAY				; 2 
	LDA	#BANK#_Bar_Inverted,y	; 5 

!!!PF2_REMOVE_LASTBIT!!!
!!!AND0_PF2_Inverted!!!
	STA	PF2			; 3 

	LDA	#$0f			; 2
	CMP	temp19			; 3
	BCS	#NAME#_NoSTAThat_PF2 	; 2	
	STA	temp19			; 3
#NAME#_NoSTAThat_PF2
	LDA	temp19			; 3
	CLC				; 2
	ADC	tempCC			; 3
	STA	tempCC			; 3

