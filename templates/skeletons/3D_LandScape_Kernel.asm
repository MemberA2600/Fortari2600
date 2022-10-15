
	_align	100

#BANK#_3D_Thing_PF0
	BYTE	#%11110000
	BYTE	#%01110000
	BYTE	#%00110000
	BYTE	#%00010000
#BANK#_3D_Thing_Empty
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000
	BYTE	#%00000000

#BANK#_3D_Thing_Loop
	LDA	temp01	
	CLC
	ADC	temp06
	STA	temp01
	CMP	temp07
	BEQ	#BANK#_3D_Thing_Reset
	TAX

	LDY	#0
	LDA	temp01
	CMP	#4
	BCS	#BANK#_3D_Thing_NostSmaller4
	TAY
	LDA	(temp10),y
	TAY
#BANK#_3D_Thing_NostSmaller4
	STY	temp19

	BIT	temp09
	BVS	#BANK#_3D_Thing_BackWards	
	LDA	temp05
	CLC
	ADC	#1
	JMP	#BANK#_3D_Thing_Forwarded
#BANK#_3D_Thing_BackWards
	sleep	3
	LDA	temp05
	SEC
	SBC	#1
#BANK#_3D_Thing_Forwarded
	AND	temp02
	STA	temp05
	TAY

#BANK#_3D_Thing_SubLoop	
	STA	WSYNC

	LDA	temp19		; 3 
	STA	PF0		; 3 
	LDA	(temp03),y	; 5
	ADC	temp08		; 3
	STA	COLUBK		; 3

	DEX
	BPL	#BANK#_3D_Thing_SubLoop

	LDA	#$10
	BIT	temp09
	BEQ	#BANK#_3D_Thing_NoGap
	LDA	frameColor

	STA	WSYNC
	STA	COLUBK
#BANK#_3D_Thing_NoGap
	JMP	#BANK#_3D_Thing_Loop	
	
#BANK#_3D_Thing_Reset
	JMP	(temp12)