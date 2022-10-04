*
*	temp01:		Controller
*	temp02:		BaseColor
*	temp03+temp04:  PF Pointer
*	temp05+temp06:  PF Color Pointer
* 	temp07+temp08:  PF Inverted Pointer
*	temp09+temp10:  Back Pointer
*

#BANK#_Water_Waves
	LDA	frameColor
	LDX	#0
	STA	WSYNC
	STA	COLUBK
	
	STX	PF0
	STX	GRP0
	STX	GRP1
	STX	PF1
	STX	PF2
	STA	COLUPF	
	STX	ENAM0	
	STX	ENAM1

	LDA	#1
	STA	CTRLPF

	LDA	#<#BANK#_Water_Waves_Data
	STA	temp03
	LDA	#>#BANK#_Water_Waves_Data
	STA	temp04

	LDA	#<#BANK#_Water_Waves_Inverted_Data
	STA	temp07
	LDA	#>#BANK#_Water_Waves_Inverted_Data
	STA	temp08

	LDA	temp01
	AND	#%00000111
	ASL
	ASL
	ASL
	TAX
	ADC	temp03
	STA	temp03
	TXA
	ADC	temp07
	STA	temp07	

	LDY	#7

	JMP	#BANK#_Water_Waves_Loop

	_align	45

#BANK#_Water_Waves_Loop
	STA	WSYNC			; 3
	STA	COLUPF			; 3 (6)
	LDA	(temp03),y		; 5 (11)
	STA	PF0			; 3 (14)
	STA	PF2			; 3 (17)
	TAX				; 2 (19) 
	LDA	(temp07),y		; 5 (24)
	STA	PF1			; 3 (27)
	
	sleep	20
	STA	PF2			; 3 (43)
	STX	PF1			; 3 (46)
	STA	PF0			; 3 (49)

	DEY				; 2 (51)
	LDA	(temp05),y		; 5 (56)
	ADC	temp02			; 3 (59)
	CPY	#255			; 2 (61)
	BEQ	#BANK#_Water_Waves_Reset ; 2 (63)
	JMP	#BANK#_Water_Waves_Loop  ; 3 (66)

#BANK#_Water_Waves_Reset


	JMP	(temp09)
