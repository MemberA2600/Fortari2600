
	JMP	#NAME#_Space
	_align	135

#NAME#_Space
#NAME#_Space_FineAdjustTable256
	LDX	#0
	STA	WSYNC		; 76

	STX	COLUBK


	STX	GRP0
	STX	GRP1
	STX	PF0
	STX	ENAM0
	STX	ENAM1
	STX	ENABL
	STX	PF1		; Visible from here
	STX	PF2

	STX	COLUPF
	STX	COLUP0	
	STX	COLUP1		; 33

	LDA	#$01
	STA	NUSIZ0

****** 	direction

	LDA	#VAR02#		; 3 (36)		
	AND	#%00000111	; 2 (38)
	TAX			; 2 (40)
	LDA	#NAME#_Space_Adder,x  ; 5 (45)
	CLC			; 2 (47)
******  first X 
	ADC	#VAR01#		; 3 (50)
	STA	#VAR01#		; 3 (53)
	STA	temp01		; 3 (56)

******  number of lines

	LDA	#VAR02#		; 3 
	LSR			
	LSR
	LSR	
	TAY			; 8 

#NAME#_Space_Loop
****	STA	WSYNC

	LDA	temp01		; 3 (24)
	CLC			; 2 (26)
	ADC	#46		; 2 (28)
	STA	temp01		; 3 (31)
	
	LDA	#18		; 2 (35)
	CMP	temp01		; 3 (38)
	BCC	#NAME#_Space_NotSmaller	; 2 (40)
#NAME#_Space_Zero_X
	sleep	7
#NAME#_Space_Zero_X2
	LDA	#0			
	JMP	#NAME#_Space_Zeroed
#NAME#_Space_NotSmaller
	LDA	#134		; 2 (42)
	CMP	temp01		; 3 (45)
	BCC	#NAME#_Space_Zero_X2
	LDA	temp01
#NAME#_Space_Zeroed
	
	STA	temp02		; 3
 
	STA	WSYNC
	LDA	#0
	
	BYTE	#$8d
	BYTE	#$1D
	BYTE	#$00	; STA	ENAM0

#NAME#_Space_HorPosLoop		
   	lda	temp02
#NAME#_Space_DivideLoop
	sbc	#15
   	bcs	#NAME#_Space_DivideLoop
	sleep	5
	STA	RESM0

	TAX
   	lda	#NAME#_Space_FineAdjustTable256,x
   	sta	HMM0			
	STA	WSYNC		; 76
	STA	HMOVE		; 3

	LDA	temp02		; 3 
	LSR
	LSR
	LSR
	TAX
	LDA	#NAME#_Space_Star_Color,x
	STA	COLUP0		; 3 
	
	LDA	#2		; 2 
	STA	ENAM0		; 3 

	DEY			; 2 (16)
	BMI	#NAME#_Space_Reset_Jump	; 2 (18)
	JMP 	#NAME#_Space_Loop	; 3 (21)

#NAME#_Space_Reset_Jump
	JMP	#NAME#_Space_Reset	

	fill	77
#NAME#_Space_Adder
	BYTE	#253
	BYTE	#254
	BYTE	#255
	BYTE	#0
	BYTE	#1
	BYTE	#2
	BYTE	#3
	BYTE	#3

#NAME#_Space_Star_Color
	BYTE	#$00	; 8	
	BYTE	#$00	; 16
	BYTE	#$02	; 24
	BYTE	#$06	; 32
	BYTE	#$0a	; 40
	BYTE	#$0e	; 48
	BYTE	#$0e	; 56
	BYTE	#$0c	; 64
	BYTE	#$0a	; 72
	BYTE	#$0e	; 80
	BYTE	#$0a	; 88
	BYTE	#$0c	; 96
	BYTE	#$0e	; 104
	BYTE	#$0e	; 112
	BYTE	#$0a	; 120
	BYTE	#$06	; 128
	BYTE	#$02	; 134
	BYTE	#$00	; 142

#NAME#_Space_FineAdjustTable
	byte	#$80
	byte	#$70
	byte	#$60
	byte	#$50
	byte	#$40
	byte	#$30
	byte	#$20
	byte	#$10
	byte	#$00
	byte	#$f0
	byte	#$e0
	byte	#$d0
	byte	#$c0
	byte	#$b0
	byte	#$a0
	byte	#$90	

#NAME#_Space_Reset
	LDA	frameColor
	LDX	#0
	STA	WSYNC		; 76

	STX	ENAM0
	STA	COLUP0		
	STX	HMCLR		

	ldx	item
	txs