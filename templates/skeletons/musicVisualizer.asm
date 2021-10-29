Music_Visuals

*
* As it uses the last 8 bytes of the SubMenu kernel, 
* you can only have a 2 lines SubMenu set.
*

MusicIndicator1 = $c7
MusicIndicator2 = $c8
MusicIndicator3 = $c9
MusicIndicator4 = $ca
MusicIndicator5 = $cb
MusicIndicator6 = $cc
MusicIndicator7 = $cd
MusicIndicator8 = $ce


	LDA	frameColor
	STA	WSYNC		; (76)
	STA	HMCLR		; 3
	STA	COLUBK		; 3 (6)
	STA	COLUP0
	LDA	#0		; 2 (8)
	STA	PF0		; 3 (11)
	STA	PF1		; 3 (14)
	STA	PF2		; 3 (17)
	STA	GRP0		; 3 (20)
	STA	GRP1		; 3 (23)
	STA	VDELP0		; 3 (26)
	STA	VDELP1		; 3 (29)


	LDA	#%00010000
	STA	NUSIZ0

	LDA	#%00000001	; 3
	STA	CTRLPF		; 3 (32)
	LDA	counter
	STA	RESM0

	AND	#%00000011
	CMP	#%00000011
	BEQ	Music_Visuals_DECR
	
	_sleep	34
	sleep	3
	JMP	Music_Visuals_NoLSR

Music_Visuals_DECR
	LSR	MusicIndicator1
	LSR	MusicIndicator2
	LSR	MusicIndicator3
	LSR	MusicIndicator4
	LSR	MusicIndicator5
	LSR	MusicIndicator6
	LSR	MusicIndicator7	
	LSR	MusicIndicator8

Music_Visuals_NoLSR
	LDA	#$10
	STA	HMM0

	LDA	#2
	STA	ENAM0	
	STA	WSYNC
	STA	HMOVE
*		
*	Do both channels.
*

	LDA	temp&1	
	AND	#%00001111
	STA	temp03

	LDA	temp&1	
	AND	#%11110000
	lsr
	lsr
	lsr
	TAY	; Need the double

	LDA	Music_Visuals_Data_Pointers,y
	CMP	#0
	BEQ	Music_Visuals_NoChangeChannel0

	STA	temp04
	INY
	LDA	Music_Visuals_Data_Pointers,y
	STA	temp05

	LDA	temp&2
	AND	#%00011111
	TAY
	
	LDA	(temp04),y
	TAX	
	
	LDA	temp03
	CMP	MusicIndicator1,x
	BCC	Music_Visuals_NoChangeChannel0
	STA	MusicIndicator1,x

Music_Visuals_NoChangeChannel0
	STA	WSYNC

	LDA	temp&3	
	AND	#%00001111
	STA	temp03

	LDA	temp&3	
	AND	#%11110000
	lsr
	lsr
	lsr
	TAY	; Need the double

	LDA	Music_Visuals_Data_Pointers,y
	CMP	#0
	BEQ	Music_Visuals_NoChangeChannel1

	STA	temp04
	INY
	LDA	Music_Visuals_Data_Pointers,y
	STA	temp05

	LDA	temp&4
	AND	#%00011111
	TAY
	
	LDA	(temp04),y
	TAX	
	
	LDA	temp03
	CMP	MusicIndicator1,x
	BCC	Music_Visuals_NoChangeChannel1
	STA	MusicIndicator1,x

Music_Visuals_NoChangeChannel1
	JMP	Music_Visuals_Display

Music_Visuals_Data

Music_Visuals_Data_Pointers
	BYTE	#0
	BYTE	#0				; 0
	BYTE	#<Music_Visuals_Data_Channel_1
	BYTE	#>Music_Visuals_Data_Channel_1	; 1
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 2
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 3	
	BYTE	#<Music_Visuals_Data_Channel_4
	BYTE	#>Music_Visuals_Data_Channel_4	; 4
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 6
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 6
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 7
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 8
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 9
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 10
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 11
	BYTE	#<Music_Visuals_Data_Channel_12
	BYTE	#>Music_Visuals_Data_Channel_12	; 12
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 13
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 14
	BYTE	#<Music_Visuals_Data_Channel_6
	BYTE	#>Music_Visuals_Data_Channel_6	; 15

Music_Visuals_Data_Channel_1
	BYTE	#0
	BYTE	#2
	BYTE	#4
	BYTE	#5
	BYTE	#5
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
Music_Visuals_Data_Channel_4
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#1
	BYTE	#1
	BYTE	#2
	BYTE	#2
	BYTE	#2
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#3
	BYTE	#4
	BYTE	#4
	BYTE	#4
	BYTE	#4
	BYTE	#4
	BYTE	#4
	BYTE	#4
	BYTE	#5
	BYTE	#5
	BYTE	#5
	BYTE	#5
Music_Visuals_Data_Channel_6
	BYTE	#2
	BYTE	#5
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7
Music_Visuals_Data_Channel_12
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#0
	BYTE	#2
	BYTE	#3
	BYTE	#3
	BYTE	#4
	BYTE	#4
	BYTE	#5
	BYTE	#5
	BYTE	#5
	BYTE	#5
	BYTE	#5
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#6
	BYTE	#7
	BYTE	#7
	BYTE	#7
	BYTE	#7

Music_Visuals_Data_Bars
	BYTE	#%00000000
	BYTE	#%10000000
	BYTE	#%11000000
	BYTE	#%11100000
	BYTE	#%11110000
	BYTE	#%11111000
	BYTE	#%11111100
	BYTE	#%11111110
	BYTE	#%11111111


Music_Visuals_Data_Barcolors
	BYTE	#$#COLOR5#8
	BYTE	#$#COLOR5#6
	BYTE	#$#COLOR5#4
	BYTE	#$#COLOR4#8
	BYTE	#$#COLOR4#6
	BYTE	#$#COLOR4#4
	BYTE	#$#COLOR3#8
	BYTE	#$#COLOR3#6
	BYTE	#$#COLOR3#4

	align	256
Music_Visuals_Display
	LDX	#0
Music_Visuals_LineLoop
	STA	WSYNC	; 76
	LDA	MusicIndicator1,x		; 5
	lsr					; 2 (7)
	TAY					; 2 (9)
	STA	temp04				; 3 (12)
	LDA	Music_Visuals_Data_Bars,y	; 5 (17)
	STA	PF2				; 3 (20)
	
	TXA					; 2 (22) 
	TAY					; 2 (24)

	LDA	temp04				; 3 (27)
	LSR					; 2 (29)
	
	CLC					; 2 (31)
	ADC 	Music_Visuals_Data_Barcolors,y	; 5 (36)
	STA	COLUPF				; 3 (39)
	STA	temp03				; 3 (42)

	LDY	#3	; This is the line num!
Music_Visuals_LineFiller
	STA	WSYNC
	DEC 	temp03

	LDA	temp03
	AND	#%00001111
	CMP	#$04
	BCC	Music_Visuals_NoColorDECR
	DEC	temp03
Music_Visuals_NoColorDECR
	LDA	temp03

	STA	COLUPF

	DEY
	BPL	Music_Visuals_LineFiller
	STA	WSYNC
	LDA	frameColor
	STA	COLUPF

	INX	
	CPX	#8
	BNE	Music_Visuals_LineLoop

Music_Visuals_DisplayEnded
	LDA	#0
	STA	ENAM0
	STA	HMCLR
