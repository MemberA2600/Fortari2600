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
	STA	temp09

	; Usage of temps:
	;
	; temp10, temp11: Sound Pointer
	; temp09	: WaitFlag	


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
	LDX	#temp10			; 2
	LDA	($00,x)			; 6 (8)  Load pointer, increase
	CMP	#PlaySoundXX_EOF_byte	; 2 (10)
	BEQ	PlaySoundXX_FinishHim	; 2 (12)
	INC	0,x			; 6 (18)
	BNE	*+4			; 2 (20) 
	INC	1,x 			; 6 (26) Load pointer, increase

	TAY

	LDA	#1			; 2
	SEC				; 2
	SBC	temp09			; 3
	STA	temp09			; 3
	TAX				; 2
	LDA	PlaySoundXX_WaitTimes,x ; 5
	
PlaySoundXX_Loop1
	SBC	#1
	BCS	PlaySoundXX_Loop1 	

	sleep	3


	TYA				; 2
	STA	AUDV0			; 3 (5)
	LSR				; 2 (7)
	LSR				; 2 (9)
	LSR				; 2 (11)
	LSR				; 2 (13)

	TAY				; 2 (15)

	LDA	PlaySoundXX_WaitTimes,x ; 5
PlaySoundXX_Loop2
	SBC	#1
	BCS	PlaySoundXX_Loop2

	sleep	17

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
	
	LDY	#PlaySoundXX_!!!TV!!!_Vblank
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
	LDY	#PlaySoundXX_!!!TV!!!_Overscan
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


PlaySoundXX_WaitTimes
	BYTE	#26
	BYTE	#48

!!!Data_Stuff!!!