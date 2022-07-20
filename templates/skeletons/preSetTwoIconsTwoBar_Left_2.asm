	LDA	temp19			; 3 
	CMP	#0			
	BEQ	#NAME#_NoAdd1_Icon2
	CLC
	ADC	#1
#NAME#_NoAdd1_Icon2

	TAY				; 2 
	LDA	#BANK#_Bar_Inverted,y	; 5 
	ASL				; 2
	ASL				; 2
	ASL				; 2
	ASL				; 2
	!!!DOTS_PF0!!!
	STA	PF0			; 3

	LDA	#BANK#_Bar_Normal,y	; 5
	ASL				; 4
	ASL				; 4
	ASL				; 4
	ASL				; 4
	ORA	temp18			; 3
	!!!DOTS_PF1_2!!!
	!!!WTF_IS_THIS!!!

	STA	temp17			; 3
	AND	#%11110111		; 2
	STA	PF1			; 3
*
*	Ball replaces this bit.
*
	LDA	temp17			; 3
	AND	#%0001000		; 2
	LSR
	LSR
	STA	temp17			; 3


	LDA	#$0f			; 2
	CMP	temp19			; 3
	BCS	#NAME#_NoSTAThat_Icon2 	; 2	
	STA	temp19			; 3
#NAME#_NoSTAThat_Icon2
	LDA	temp19			; 3
	CLC				; 2
	ADC	temp04			; 3
	STA	temp04			; 3
