CoolSong_Driver1
	DEC	CoolSong_Duration1
	LDA	CoolSong_Duration1
	CMP	#0
	BNE	CoolSong_Skip1

CoolSong_ReadFirst1
	LDX	#CoolSong_Pointer1
	LDA	($00,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	CMP	#0
	BNE	CoolSong_if2401

	STA	AUDV1
	STA	AUDF1
	STA	AUDC1
	STA	temp18
	STA	temp19
	JMP	CoolSong_NotSharedByte1

CoolSong_if2401
	CMP	#240
	BNE	CoolSong_NoRestart1

CoolSong_Restart1
	LDA	#<CoolSong_Data0
	STA	CoolSong_Pointer0
	LDA	#>CoolSong_Data0
	STA	CoolSong_Pointer0+1
	LDA	#<CoolSong_Data1
	STA	CoolSong_Pointer1
	LDA	#>CoolSong_Data1
	STA	CoolSong_Pointer1+1


	JMP	CoolSong_ReadFirst1

CoolSong_NoRestart1
	STA	temp06
	AND	#%00001111
	CMP	#0
	BNE	CoolSong_CommonNote1
	LDA	temp06
	lsr
	lsr
	lsr
	lsr
	CMP	#%00001110
	BNE	CoolSong_NoRestorePointer1
	LDA	CoolSong_PointerBackUp1
	STA	CoolSong_Pointer1
	LDA	CoolSong_PointerBackUp1+1
	STA	CoolSong_Pointer1+1
	JMP	CoolSong_ReadFirst1
CoolSong_NoRestorePointer1
	
	LDY	CoolSong_Pointer1	
	STY	CoolSong_PointerBackUp1	
	LDY	CoolSong_Pointer1+1
	STY	CoolSong_PointerBackUp1+1	

	ASL
	TAX
	LDA	CoolSong_Data1_CompressedPointerTable,x
	STA	CoolSong_Pointer1
	LDA	CoolSong_Data1_CompressedPointerTable+1,x
	STA	CoolSong_Pointer1+1
	JMP	CoolSong_ReadFirst1

CoolSong_CommonNote1
	LDA	temp06
	STA	AUDV1
	STA	temp18
	lsr
	lsr
	lsr
	lsr
	STA	AUDC1

	LDX	#CoolSong_Pointer1
	LDA	($00,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	STA	temp19
	STA	AUDF1

	CMP	#32
	BCC	CoolSong_NotSharedByte1

	AND	#%11100000
	lsr
	lsr
	lsr
	lsr
	lsr


	STA	CoolSong_Duration1
	JMP	CoolSong_Skip1

CoolSong_NotSharedByte1
	
	LDX	#CoolSong_Pointer1
	LDA	($00,x)
	INC	0,x
	BNE	*+4
	INC	1,x

	STA	CoolSong_Duration1

CoolSong_Skip1
	lda	bankToJump
	lsr
	lsr
	AND	#%00000111
	tax

	lda	temp02
   	pha
   	lda	temp01
   	pha
   	pha
   	pha
	jmp	bankSwitchJump