CoolSong_Move_text
	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	CoolSong_Move_Ended

	LDA	TextDir
	CMP	#0
	BNE	CoolSong_Text_Reversed

	LDA	TextPoz
	CMP	#TextEnd
	BNE	CoolSong_INCR

	LDA	#1
	STA	TextDir
	JMP	CoolSong_DECR	
CoolSong_INCR
	INC	TextPoz
	JMP	CoolSong_Move_Ended

CoolSong_Text_Reversed
	LDA	TextPoz
	CMP	#0
	BNE	CoolSong_DECR
	STA	TextDir
	JMP	CoolSong_INCR
CoolSong_DECR
	DEC	TextPoz
CoolSong_Move_Ended

	LDY	TextPoz
	LDX	#255
	

CoolSong_Text_Create_Loop
	INX
	CPX	#12
	BEQ	CoolSong_Text_Create_End

	LDA	CoolSong_ReallyNiceText,y
	STA	Letter01,x
	INY
	JMP	CoolSong_Text_Create_Loop

CoolSong_Text_Create_End