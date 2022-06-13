	AND	#%11000000		; 2
	CMP	#0			; 2	
	BEQ	#NAME#_NoRemoveBit	; 2

	ROL				; 2
	ROL 				; 2
	TAX				; 2
	LDA	#NAME#_BitCodes,x	; 5
	STA	temp17			; 3

	LDA	#BANK#_Bar_Inverted,y	; 5 
	AND	#%00111111		; 2
	JMP	#NAME#_GoBackToNormal	; 3

#NAME#_NoRemoveBit
	sleep	26
	LDA	#BANK#_Bar_Inverted,y	; 5 
	JMP	#NAME#_GoBackToNormal	; 3
#NAME#_BitCodes
	BYTE	#%00100010
	BYTE	#%00100010
	BYTE	#%00100010	
	BYTE	#%00110010

#NAME#_GoBackToNormal
