Channel0Buffer = $D4
Channel0Index = $D5

*
*	The soundplayer will use 4 bytes (if none is disabled).
*	2 bytes are for AUD0 and AUD1.
*	0-3: Duration countdown
*	4-6: Index for the effect (only used for selection, interrupts current sound)
*	7  : Playing
*
*	2 bytes for the pointer index, so the whole data can be 256 bytes long.
*

	LDA	Channel0Buffer
	BPL	Test_CheckFire
	
	AND	#%00000111
	SEC
	SBC	#1
	ORA	#%10000000
	STA	Channel0Buffer

	CMP	#%10000000
	BEQ	Test_CCCCCCC
	JMP	Test_NoNewData

Test_CCCCCCC
	LDX	Channel0Index
	JMP	Test_NewData	

Test_CheckFire
	BIT	INPT4
	BMI	Test_NoNewData
	LDX	#0	
Test_NewData
	LDA	#NAME#_SoundFX,x
	INX
	CMP	#$F0
	BNE	Test_Continue
	LDA	#0
	STA	AUDV0
	STA	Channel0Buffer	
	JMP	Test_NoNewData
Test_Continue
	TAY
	AND	#%00001111
	CMP	#0
	BNE	Test_NormalData
	STA	AUDV0
	TYA
	JMP	Test_SaveDuration	
Test_NormalData
	TYA
	STA	AUDV0
	LSR
	LSR
	LSR
	LSR	
	STA	AUDC0
	LDA	#NAME#_SoundFX,x
	INX	
	STA	AUDF0
	AND	#%11100000
Test_SaveDuration
	ROL
	ROL
	ROL
	ROL
	ORA	#%10000000
	STA	Channel0Buffer	
Test_SaveIndex
	STX	Channel0Index
Test_NoNewData