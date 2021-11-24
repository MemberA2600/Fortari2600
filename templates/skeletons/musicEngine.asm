CoolSong_Driver@@
	DEC	CoolSong_Duration@@
	LDA	CoolSong_Duration@@
	CMP	#0
	BNE	CoolSong_Skip@@

CoolSong_ReadFirst@@
	LDX	#CoolSong_Pointer@@
	LDA	($00,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	CMP	#0
	BNE	CoolSong_if240@@

	STA	AUDV@@
	STA	AUDF@@
	STA	AUDC@@
	STA	temp&1
	STA	temp&2
	JMP	CoolSong_NotSharedByte@@

CoolSong_if240@@
	CMP	#240
	BNE	CoolSong_NoRestart@@

CoolSong_Restart@@
!!!Song_Restart!!!

	JMP	CoolSong_ReadFirst@@

CoolSong_NoRestart@@
	STA	temp06
	AND	#%00001111
	CMP	#0
	BNE	CoolSong_CommonNote@@
	LDA	temp06
	lsr
	lsr
	lsr
	lsr
	CMP	#%00001110
	BNE	CoolSong_NoRestorePointer@@
	LDA	CoolSong_PointerBackUp@@
	STA	CoolSong_Pointer@@
	LDA	CoolSong_PointerBackUp@@+1
	STA	CoolSong_Pointer@@+1
	JMP	CoolSong_ReadFirst@@
CoolSong_NoRestorePointer@@
	
	LDY	CoolSong_Pointer@@	
	STY	CoolSong_PointerBackUp@@	
	LDY	CoolSong_Pointer@@+1
	STY	CoolSong_PointerBackUp@@+1	

	ASL
	TAX
	LDA	CoolSong_Data@@_CompressedPointerTable,x
	STA	CoolSong_Pointer@@
	LDA	CoolSong_Data@@_CompressedPointerTable+1,x
	STA	CoolSong_Pointer@@+1
	JMP	CoolSong_ReadFirst@@

CoolSong_CommonNote@@
	LDA	temp06
	STA	AUDV@@
	STA	temp&1
	lsr
	lsr
	lsr
	lsr
	STA	AUDC@@

	LDX	#CoolSong_Pointer@@
	LDA	($00,x)
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
!!!ASL!!!

	STA	CoolSong_Duration@@
	JMP	CoolSong_Skip@@

CoolSong_NotSharedByte@@
	
	LDX	#CoolSong_Pointer@@
	LDA	($00,x)
	INC	0,x
	BNE	*+4
	INC	1,x
!!!ASL!!!
	STA	CoolSong_Duration@@

CoolSong_Skip@@
!!!JumpOrReturn!!!