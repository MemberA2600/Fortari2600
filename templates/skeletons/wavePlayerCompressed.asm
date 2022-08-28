PlaySoundXX_Initialize

	LDA	#2
	STA	VBLANK ; Turn off graphics display

	; Turn off graphics and make sure we are finish overscan
	; Save the number of tics the timer had!

	LDA	#0
	STA	AUDC0
	STA	AUDF0
	STA	AUDV0
	STA	AUDV1
	STA	temp13

	LDA	#1
	STA	temp12

	; Usage of temps:
	;
	; temp10, temp11: Sound Pointer
	; temp12        : Saved Data
	; temp13	: Counter
	;	


PlaySoundXX_Constant      = 20
PlaySoundXX_NTSC_Vblank   = 37
PlaySoundXX_NTSC_Overscan = 30
PlaySoundXX_PAL_Vblank    = 67
PlaySoundXX_PAL_Overscan  = 50

!!!Init_Stuff!!!

	LDA	#<PlaySoundXX_Table
	STA	temp10
	LDA	#>PlaySoundXX_Table
	STA	temp11

	; Because in this case, there is nothing done
	; by the player and this is a temporal state,
	; we don't have to waste any of the precious
	; memory!


PlaySoundXX_EndOScan
	LDA	INTIM
	BPL	PlaySoundXX_EndOScan

	; End OverScan, so we can calculate better!

PlaySoundXX_LoadSample
	LDA	temp13			; 3
	CMP	#0			; 2
	BEQ	PlaySoundXX_LoadNew	; 2

	_sleep	42
	sleep	5

	DEC	temp13			; 5
	LDA	temp12			; 3
	JMP	PlaySoundXX_CounterDone ; 3

PlaySoundXX_LoadNew
	LDX	#temp10			; 2
	LDA	($00,x)			; 6 
	CMP	#PlaySoundXX_EOF_byte	; 2 
	BEQ	PlaySoundXX_FinishHim	; 2 
	INC	0,x			; 6
	BNE	*+4			; 2 
	INC	1,x 			; 6 

	CMP	#16			; 2
	BCS	PlaySoundXX_NoCounter	; 2

	STA	temp13			; 3

	INC	0,x			; 6
	BNE	*+4			; 2 
	INC	1,x 			; 6 

	LDA	temp12			; 3
	JMP	PlaySoundXX_CounterDone ; 3

PlaySoundXX_NoCounter
	STA	temp12			; 3
	_sleep	22

	LDA	temp12			; 3
PlaySoundXX_CounterDone
	TAY				; 2

	_sleep 50
	sleep 4

	TYA				; 2
	STA	AUDV0			; 3 (5)
	LSR				; 2 (7)
	LSR				; 2 (9)
	LSR				; 2 (11)
	LSR				; 2 (13)

	TAY				; 2 (15)
	_sleep 122
	sleep 2


	TYA				; 2
	STA	AUDV0			; 3 (5)
	JMP	PlaySoundXX_LoadSample	; 3 (8)
	
PlaySoundXX_FinishHim
	LDX	#PlaySoundXX_Constant	; 2 (14)

	LDA	#0
	STA	COLUP0
	STA	COLUP1
	STA	COLUPF
	STA	COLUBK
	JMP	PlaySoundXX_JumpHereToFake

PlaySoundXX_DebugScreen
	LDA	#2
	STA	VBLANK
	STA	VSYNC

	STA	WSYNC
	STA	WSYNC
	STA	WSYNC

	LDA	#0
	STA	VSYNC
	
	LDY	#PlaySoundXX_NTSC_Vblank
PlaySoundXX_DebugLoop1
	STA	WSYNC
	DEY
	BNE	PlaySoundXX_DebugLoop1

	LDA	#0
	STA	VBLANK
		
	LDY	#192
PlaySoundXX_JumpHereToFake
	DEX	
	CPX	#0
	BEQ	PlaySoundXX_NoMoreLoops
PlaySoundXX_DebugLoop2
	STA	WSYNC
	DEY
	BNE	PlaySoundXX_DebugLoop2

	LDA	#2
	STA	VBLANK
	LDY	#PlaySoundXX_NTSC_Overscan
PlaySoundXX_DebugLoop3
	STA	WSYNC
	DEY
	BNE	PlaySoundXX_DebugLoop3

	JMP	PlaySoundXX_DebugScreen


PlaySoundXX_NoMoreLoops
	lda	bankToJump
	lsr
	lsr
	AND	#%00000111	; Get the bank number to return
	tax		
		
	lda	#>(PlaySoundXX_Return-1)
   	pha
   	lda	#<(PlaySoundXX_Return-1)
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump

!!!Data_Stuff!!!