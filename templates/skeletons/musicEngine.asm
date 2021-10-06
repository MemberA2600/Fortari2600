CoolSong_Driver@@
	DEC	CoolSong_Duration@@
	LDA	CoolSong_Duration@@
	CMP	#0
	BNE	CoolSong_Skip@@

	LDX	#CoolSong_Pointer@@
	LDA	(0,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	CMP	#0
	BNE	CoolSong_if240@@

	STA	AUDV0
	STA	AUDF0
	STA	AUDC0
	STA	temp&1
	STA	temp&2
	JMP	CoolSong_NotSharedByte@@


CoolSong_if240@@
	CMP	#240
	BNE	CoolSong_NoRestart@@

CoolSong_Restart@@
	LDA	#<.CoolSong_Data@@
	STA	CoolSong_Pointer@@
	LDA	#>.CoolSong_Data@@
	STA	CoolSong_Pointer@@+1

	LDX	#CoolSong_Pointer@@
	LDA	(0,x)
	INC	0,x
	BNE	*+4
	INC	1,x

CoolSong_NoRestart@@

	STA	AUDV@@
	STA	temp&1
	lsr
	lsr
	lsr
	lsr
	STA	AUDC@@

	LDX	#CoolSong_Pointer@@
	LDA	(0,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	STA	temp&2
	STA	AUDF@@

	CMP	#32
	BCC	CoolSong_NotSharedByte@@

	AND	#%11100000
	lsr
	lsr
	lsr
	lsr
	lsr
	STA	CoolSong_Duration@@
	JMP	CoolSong_Skip@@

CoolSong_NotSharedByte@@
	
	LDX	#CoolSong_Pointer@@
	LDA	(0,x)
	INC	0,x
	BNE	*+4
	INC	1,x
	STA	CoolSong_Duration@@

CoolSong_Skip@@
	!!!JumpOrReturn!!!