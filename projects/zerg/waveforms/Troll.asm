Troll_Initialize

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


Troll_Constant      = 8
Troll_NTSC_Vblank   = 37
Troll_NTSC_Overscan = 30
Troll_PAL_Vblank    = 67
Troll_PAL_Overscan  = 50


Troll_EOF_byte = %00000000


	LDA	#<Troll_Table
	STA	temp10
	LDA	#>Troll_Table
	STA	temp11

	; Because in this case, there is nothing done
	; by the player and this is a temporal state,
	; we don't have to waste any of the precious
	; memory!


Troll_EndOScan
	LDA	INTIM
	BPL	Troll_EndOScan

	; End OverScan, so we can calculate better!

Troll_LoadSample
	LDA	temp13			; 3
	CMP	#0			; 2
	BEQ	Troll_LoadNew	; 2

	_sleep	42
	sleep	5

	DEC	temp13			; 5
	LDA	temp12			; 3
	JMP	Troll_CounterDone ; 3

Troll_LoadNew
	LDX	#temp10			; 2
	LDA	($00,x)			; 6 
	CMP	#Troll_EOF_byte	; 2 
	BEQ	Troll_FinishHim	; 2 
	INC	0,x			; 6
	BNE	*+4			; 2 
	INC	1,x 			; 6 

	CMP	#16			; 2
	BCS	Troll_NoCounter	; 2

	STA	temp13			; 3

	INC	0,x			; 6
	BNE	*+4			; 2 
	INC	1,x 			; 6 

	LDA	temp12			; 3
	JMP	Troll_CounterDone ; 3

Troll_NoCounter
	STA	temp12			; 3
	_sleep	22

	LDA	temp12			; 3
Troll_CounterDone
	TAY				; 2

	_sleep 174
	sleep 4

	TYA				; 2
	STA	AUDV0			; 3 (5)
	LSR				; 2 (7)
	LSR				; 2 (9)
	LSR				; 2 (11)
	LSR				; 2 (13)

	TAY				; 2 (15)
	_sleep 242
	sleep 2


	TYA				; 2
	STA	AUDV0			; 3 (5)
	JMP	Troll_LoadSample	; 3 (8)
	
Troll_FinishHim
	LDX	#Troll_Constant	; 2 (14)

	LDA	#0
	STA	COLUP0
	STA	COLUP1
	STA	COLUPF
	STA	COLUBK
	JMP	Troll_JumpHereToFake

Troll_DebugScreen
	LDA	#2
	STA	VBLANK
	STA	VSYNC

	STA	WSYNC
	STA	WSYNC
	STA	WSYNC

	LDA	#0
	STA	VSYNC
	
	LDY	#Troll_NTSC_Vblank
Troll_DebugLoop1
	STA	WSYNC
	DEY
	BNE	Troll_DebugLoop1

	LDA	#0
	STA	VBLANK
		
	LDY	#192
Troll_JumpHereToFake
	DEX	
	CPX	#0
	BEQ	Troll_NoMoreLoops
Troll_DebugLoop2
	STA	WSYNC
	DEY
	BNE	Troll_DebugLoop2

	LDA	#2
	STA	VBLANK
	LDY	#Troll_NTSC_Overscan
Troll_DebugLoop3
	STA	WSYNC
	DEY
	BNE	Troll_DebugLoop3

	JMP	Troll_DebugScreen


Troll_NoMoreLoops
	lda	bankToJump
	lsr
	lsr
	AND	#%00000111	; Get the bank number to return
	tax		
		
	lda	#>(Troll_Return-1)
   	pha
   	lda	#<(Troll_Return-1)
   	pha
   	pha
   	pha
   	jmp	bankSwitchJump


Troll_Table
	BYTE	#%01110111
	BYTE	#%00000100
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%00001010
	BYTE	#%01110111
	BYTE	#%00001001
	BYTE	#%10001000
	BYTE	#%00001010
	BYTE	#%01110111
	BYTE	#%00000111
	BYTE	#%10001000
	BYTE	#%00000101
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000101
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%10011010
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01010110
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10011001
	BYTE	#%10101001
	BYTE	#%10101010
	BYTE	#%10101011
	BYTE	#%10101011
	BYTE	#%10011010
	BYTE	#%01111000
	BYTE	#%01010110
	BYTE	#%01000101
	BYTE	#%01000100
	BYTE	#%01010100
	BYTE	#%01100101
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%00000011
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10101010
	BYTE	#%00000011
	BYTE	#%10011011
	BYTE	#%10011010
	BYTE	#%10001010
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01000101
	BYTE	#%01000100
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%10101010
	BYTE	#%10111010
	BYTE	#%10101011
	BYTE	#%10011010
	BYTE	#%10001001
	BYTE	#%01100111
	BYTE	#%01000101
	BYTE	#%01000100
	BYTE	#%01000100
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10101010
	BYTE	#%10011010
	BYTE	#%10001001
	BYTE	#%01100111
	BYTE	#%01010110
	BYTE	#%01010101
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%11001010
	BYTE	#%11011011
	BYTE	#%11001100
	BYTE	#%10111011
	BYTE	#%10001001
	BYTE	#%01010110
	BYTE	#%00100100
	BYTE	#%00100011
	BYTE	#%00110011
	BYTE	#%01010100
	BYTE	#%01110110
	BYTE	#%10011001
	BYTE	#%10111010
	BYTE	#%10101010
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10111011
	BYTE	#%11001101
	BYTE	#%11001100
	BYTE	#%10101010
	BYTE	#%01111000
	BYTE	#%01000110
	BYTE	#%00110011
	BYTE	#%00110010
	BYTE	#%01000011
	BYTE	#%01100101
	BYTE	#%10010111
	BYTE	#%10101001
	BYTE	#%10101010
	BYTE	#%10001001
	BYTE	#%01101000
	BYTE	#%01010110
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%10000110
	BYTE	#%10011000
	BYTE	#%10101001
	BYTE	#%10111010
	BYTE	#%11001100
	BYTE	#%10111100
	BYTE	#%10101011
	BYTE	#%10011001
	BYTE	#%01110111
	BYTE	#%01000101
	BYTE	#%00110011
	BYTE	#%00110011
	BYTE	#%01010100
	BYTE	#%01110110
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10001010
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01100101
	BYTE	#%01100110
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%11101011
	BYTE	#%11011010
	BYTE	#%10001100
	BYTE	#%01101101
	BYTE	#%01101000
	BYTE	#%01000100
	BYTE	#%01000011
	BYTE	#%01100010
	BYTE	#%01110100
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%01111001
	BYTE	#%01011000
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01100110
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10101010
	BYTE	#%11111101
	BYTE	#%11111010
	BYTE	#%10101001
	BYTE	#%01011011
	BYTE	#%01100111
	BYTE	#%00110011
	BYTE	#%00110100
	BYTE	#%01110100
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%01010110
	BYTE	#%01010110
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10001001
	BYTE	#%10011001
	BYTE	#%10011010
	BYTE	#%10001001
	BYTE	#%10011001
	BYTE	#%11011010
	BYTE	#%10111011
	BYTE	#%10001011
	BYTE	#%10011001
	BYTE	#%01110101
	BYTE	#%00110110
	BYTE	#%01000100
	BYTE	#%01000100
	BYTE	#%01100111
	BYTE	#%10001000
	BYTE	#%01111001
	BYTE	#%01111000
	BYTE	#%01010110
	BYTE	#%01000110
	BYTE	#%01100101
	BYTE	#%01100110
	BYTE	#%01111000
	BYTE	#%10101000
	BYTE	#%10101011
	BYTE	#%10111011
	BYTE	#%11011100
	BYTE	#%10111111
	BYTE	#%10001100
	BYTE	#%01101000
	BYTE	#%01000111
	BYTE	#%01000101
	BYTE	#%00110100
	BYTE	#%01000100
	BYTE	#%01110110
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%00000100
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10101001
	BYTE	#%10111010
	BYTE	#%10101011
	BYTE	#%11001010
	BYTE	#%10101100
	BYTE	#%10011011
	BYTE	#%01100111
	BYTE	#%01010111
	BYTE	#%01010101
	BYTE	#%01000101
	BYTE	#%01010100
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%00000011
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10101001
	BYTE	#%10101010
	BYTE	#%10111011
	BYTE	#%11011011
	BYTE	#%10111101
	BYTE	#%10011011
	BYTE	#%01100111
	BYTE	#%01011000
	BYTE	#%01000101
	BYTE	#%00110101
	BYTE	#%01010100
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01100110
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10101010
	BYTE	#%10011001
	BYTE	#%11001010
	BYTE	#%10111101
	BYTE	#%10011011
	BYTE	#%01101000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01000110
	BYTE	#%01010101
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01010111
	BYTE	#%01100101
	BYTE	#%01010110
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10101010
	BYTE	#%10111010
	BYTE	#%10111110
	BYTE	#%10011011
	BYTE	#%01101001
	BYTE	#%10000111
	BYTE	#%01010110
	BYTE	#%01100101
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01100111
	BYTE	#%01100101
	BYTE	#%01100111
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10111100
	BYTE	#%10101011
	BYTE	#%10001001
	BYTE	#%10010111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01000110
	BYTE	#%01010101
	BYTE	#%01000100
	BYTE	#%01010101
	BYTE	#%01100101
	BYTE	#%01110111
	BYTE	#%10010111
	BYTE	#%11001010
	BYTE	#%11001101
	BYTE	#%10101100
	BYTE	#%10001010
	BYTE	#%10011000
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01010110
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10011000
	BYTE	#%01111001
	BYTE	#%10001000
	BYTE	#%01010110
	BYTE	#%01100101
	BYTE	#%01000101
	BYTE	#%01100101
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%01110110
	BYTE	#%11011001
	BYTE	#%10101011
	BYTE	#%10111011
	BYTE	#%01110111
	BYTE	#%10101000
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%01100101
	BYTE	#%10101001
	BYTE	#%10011000
	BYTE	#%10111011
	BYTE	#%10011001
	BYTE	#%10011010
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01000100
	BYTE	#%01010101
	BYTE	#%01000011
	BYTE	#%01010101
	BYTE	#%01010100
	BYTE	#%10111000
	BYTE	#%10101001
	BYTE	#%10111011
	BYTE	#%10001000
	BYTE	#%10111010
	BYTE	#%10001000
	BYTE	#%10011010
	BYTE	#%01110111
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%10001001
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01010101
	BYTE	#%01000101
	BYTE	#%01010100
	BYTE	#%01010101
	BYTE	#%00000011
	BYTE	#%01100110
	BYTE	#%10101000
	BYTE	#%10111101
	BYTE	#%10111100
	BYTE	#%10001011
	BYTE	#%10011000
	BYTE	#%01111010
	BYTE	#%10001000
	BYTE	#%01101000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%01010101
	BYTE	#%01010110
	BYTE	#%01100101
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10101010
	BYTE	#%10011001
	BYTE	#%10011010
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%01111001
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%01110111
	BYTE	#%00000101
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000101
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%00001000
	BYTE	#%01110111
	BYTE	#%00001000
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%00001001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00001010
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00001100
	BYTE	#%01111000
	BYTE	#%00000100
	BYTE	#%01110111
	BYTE	#%00000110
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10010111
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%10010110
	BYTE	#%10001000
	BYTE	#%10010111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01010111
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10000111
	BYTE	#%01111001
	BYTE	#%10000111
	BYTE	#%01101000
	BYTE	#%01110110
	BYTE	#%01101000
	BYTE	#%10000111
	BYTE	#%01111001
	BYTE	#%10010110
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01101000
	BYTE	#%01111000
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110101
	BYTE	#%10001001
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10010111
	BYTE	#%01111000
	BYTE	#%10010110
	BYTE	#%01101000
	BYTE	#%10001000
	BYTE	#%10000110
	BYTE	#%01111001
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%01101000
	BYTE	#%01101000
	BYTE	#%01100110
	BYTE	#%01111000
	BYTE	#%01101000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10010111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%00000100
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01010110
	BYTE	#%01100101
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10011010
	BYTE	#%10011001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01100101
	BYTE	#%01010110
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10101001
	BYTE	#%10101011
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01010101
	BYTE	#%01000100
	BYTE	#%01100100
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10111011
	BYTE	#%10011010
	BYTE	#%10001001
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10011000
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%10000110
	BYTE	#%10101001
	BYTE	#%10111011
	BYTE	#%10011011
	BYTE	#%10001000
	BYTE	#%01010111
	BYTE	#%01010101
	BYTE	#%01010101
	BYTE	#%10000110
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01100101
	BYTE	#%01110110
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10011010
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%01101000
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10101000
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01010111
	BYTE	#%01100101
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%10010111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01111001
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10101000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01010111
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10000110
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%10101000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10111001
	BYTE	#%10011000
	BYTE	#%01110110
	BYTE	#%01000110
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%01101011
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%01110101
	BYTE	#%10010110
	BYTE	#%10111001
	BYTE	#%10001001
	BYTE	#%01101000
	BYTE	#%01010111
	BYTE	#%01100101
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%10101010
	BYTE	#%01110111
	BYTE	#%10010110
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10011001
	BYTE	#%01111101
	BYTE	#%01111001
	BYTE	#%01100110
	BYTE	#%01100100
	BYTE	#%10010101
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%01111001
	BYTE	#%01010111
	BYTE	#%01110111
	BYTE	#%10101000
	BYTE	#%10001010
	BYTE	#%01110110
	BYTE	#%01011000
	BYTE	#%01010110
	BYTE	#%10010111
	BYTE	#%11001011
	BYTE	#%10011000
	BYTE	#%01100110
	BYTE	#%01000101
	BYTE	#%01110101
	BYTE	#%10001010
	BYTE	#%01111001
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01110101
	BYTE	#%10100111
	BYTE	#%11001001
	BYTE	#%10000111
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%01100110
	BYTE	#%10101010
	BYTE	#%10011101
	BYTE	#%01011000
	BYTE	#%01100101
	BYTE	#%01100100
	BYTE	#%10100110
	BYTE	#%10101001
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%01010111
	BYTE	#%10000111
	BYTE	#%10101011
	BYTE	#%10101001
	BYTE	#%01110110
	BYTE	#%01100100
	BYTE	#%10010101
	BYTE	#%10010111
	BYTE	#%10101001
	BYTE	#%10001011
	BYTE	#%01000111
	BYTE	#%01100100
	BYTE	#%01110111
	BYTE	#%10101000
	BYTE	#%10001001
	BYTE	#%01010110
	BYTE	#%10000110
	BYTE	#%01101000
	BYTE	#%10011000
	BYTE	#%10011010
	BYTE	#%10011000
	BYTE	#%10010110
	BYTE	#%01110100
	BYTE	#%10100110
	BYTE	#%10010110
	BYTE	#%10010111
	BYTE	#%11001010
	BYTE	#%01010111
	BYTE	#%10000100
	BYTE	#%10000110
	BYTE	#%10010110
	BYTE	#%10101001
	BYTE	#%01100110
	BYTE	#%10000101
	BYTE	#%01111000
	BYTE	#%10010110
	BYTE	#%10111010
	BYTE	#%01011000
	BYTE	#%01110111
	BYTE	#%01101001
	BYTE	#%01110110
	BYTE	#%10011010
	BYTE	#%01101001
	BYTE	#%10000111
	BYTE	#%10001011
	BYTE	#%01000111
	BYTE	#%01111000
	BYTE	#%01101010
	BYTE	#%01110111
	BYTE	#%01111001
	BYTE	#%01010110
	BYTE	#%10001000
	BYTE	#%10001010
	BYTE	#%10000111
	BYTE	#%10001010
	BYTE	#%01010111
	BYTE	#%10011000
	BYTE	#%01101010
	BYTE	#%01100110
	BYTE	#%10011001
	BYTE	#%01011000
	BYTE	#%10010111
	BYTE	#%10001101
	BYTE	#%00110111
	BYTE	#%01110111
	BYTE	#%01011001
	BYTE	#%01110111
	BYTE	#%10001010
	BYTE	#%01000110
	BYTE	#%10000111
	BYTE	#%01111001
	BYTE	#%10000110
	BYTE	#%10011010
	BYTE	#%01010111
	BYTE	#%10010111
	BYTE	#%01101011
	BYTE	#%01100110
	BYTE	#%10001010
	BYTE	#%01001001
	BYTE	#%10000110
	BYTE	#%10011110
	BYTE	#%00110111
	BYTE	#%01110110
	BYTE	#%01101001
	BYTE	#%10000101
	BYTE	#%10111010
	BYTE	#%01000110
	BYTE	#%10000100
	BYTE	#%10101000
	BYTE	#%10000110
	BYTE	#%11001010
	BYTE	#%01011000
	BYTE	#%01110010
	BYTE	#%10111010
	BYTE	#%01010110
	BYTE	#%10100111
	BYTE	#%10001010
	BYTE	#%01010100
	BYTE	#%11011000
	BYTE	#%01111010
	BYTE	#%01110100
	BYTE	#%10011000
	BYTE	#%01010101
	BYTE	#%10100110
	BYTE	#%01111010
	BYTE	#%01010101
	BYTE	#%10101001
	BYTE	#%01011001
	BYTE	#%10000110
	BYTE	#%10011011
	BYTE	#%01000110
	BYTE	#%10110111
	BYTE	#%10001011
	BYTE	#%01010011
	BYTE	#%10110111
	BYTE	#%01100111
	BYTE	#%10010101
	BYTE	#%11001011
	BYTE	#%01000111
	BYTE	#%10000100
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%10111010
	BYTE	#%00111001
	BYTE	#%01010100
	BYTE	#%10011010
	BYTE	#%01101000
	BYTE	#%10101000
	BYTE	#%01111010
	BYTE	#%01010100
	BYTE	#%11001000
	BYTE	#%10001001
	BYTE	#%01110100
	BYTE	#%10011000
	BYTE	#%01010110
	BYTE	#%10100111
	BYTE	#%10101100
	BYTE	#%00110111
	BYTE	#%01110110
	BYTE	#%01001000
	BYTE	#%10000111
	BYTE	#%10101100
	BYTE	#%00111001
	BYTE	#%01010011
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%11001001
	BYTE	#%10001010
	BYTE	#%01000100
	BYTE	#%10110110
	BYTE	#%10101010
	BYTE	#%01110110
	BYTE	#%10011000
	BYTE	#%01010110
	BYTE	#%10010101
	BYTE	#%11011011
	BYTE	#%01011001
	BYTE	#%01100110
	BYTE	#%01010111
	BYTE	#%01100110
	BYTE	#%11001011
	BYTE	#%01011011
	BYTE	#%01000100
	BYTE	#%01110101
	BYTE	#%10000111
	BYTE	#%11001001
	BYTE	#%10011011
	BYTE	#%01010110
	BYTE	#%01100101
	BYTE	#%10010111
	BYTE	#%10111001
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10101010
	BYTE	#%01011010
	BYTE	#%01000101
	BYTE	#%01101000
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%01111010
	BYTE	#%01000011
	BYTE	#%01110101
	BYTE	#%10101000
	BYTE	#%10101000
	BYTE	#%10011011
	BYTE	#%01000110
	BYTE	#%01000100
	BYTE	#%10101000
	BYTE	#%10111011
	BYTE	#%10001000
	BYTE	#%01110110
	BYTE	#%01100100
	BYTE	#%10010110
	BYTE	#%11011010
	BYTE	#%01111001
	BYTE	#%01010101
	BYTE	#%01100110
	BYTE	#%01111000
	BYTE	#%10101011
	BYTE	#%01101011
	BYTE	#%00110110
	BYTE	#%01100101
	BYTE	#%10010111
	BYTE	#%11001001
	BYTE	#%10111011
	BYTE	#%01010110
	BYTE	#%01000011
	BYTE	#%01110101
	BYTE	#%11001010
	BYTE	#%10001100
	BYTE	#%01001000
	BYTE	#%01000110
	BYTE	#%01010110
	BYTE	#%10111001
	BYTE	#%10101101
	BYTE	#%01000111
	BYTE	#%01110100
	BYTE	#%10000110
	BYTE	#%10100111
	BYTE	#%10111010
	BYTE	#%01010111
	BYTE	#%01010100
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%10101011
	BYTE	#%01101010
	BYTE	#%01000101
	BYTE	#%01100101
	BYTE	#%10100111
	BYTE	#%10111100
	BYTE	#%01111000
	BYTE	#%01100100
	BYTE	#%01110101
	BYTE	#%10010101
	BYTE	#%11011011
	BYTE	#%01111001
	BYTE	#%01000100
	BYTE	#%01100111
	BYTE	#%01101000
	BYTE	#%10101011
	BYTE	#%01101011
	BYTE	#%01000101
	BYTE	#%10000101
	BYTE	#%10000110
	BYTE	#%10111000
	BYTE	#%10101010
	BYTE	#%01010110
	BYTE	#%01010101
	BYTE	#%01100110
	BYTE	#%10011000
	BYTE	#%10101110
	BYTE	#%01011000
	BYTE	#%01100100
	BYTE	#%10000101
	BYTE	#%10100101
	BYTE	#%11101010
	BYTE	#%01111000
	BYTE	#%01000011
	BYTE	#%01111000
	BYTE	#%01101001
	BYTE	#%10011011
	BYTE	#%01101011
	BYTE	#%01000101
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%10111000
	BYTE	#%10011001
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%01100111
	BYTE	#%10011001
	BYTE	#%10011110
	BYTE	#%00101001
	BYTE	#%01100101
	BYTE	#%01110111
	BYTE	#%10100111
	BYTE	#%11101010
	BYTE	#%01110111
	BYTE	#%01100001
	BYTE	#%10000110
	BYTE	#%10001000
	BYTE	#%10101011
	BYTE	#%01011011
	BYTE	#%00110101
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10001001
	BYTE	#%01100101
	BYTE	#%01110101
	BYTE	#%01110110
	BYTE	#%10010111
	BYTE	#%10111010
	BYTE	#%10011010
	BYTE	#%01100011
	BYTE	#%01100100
	BYTE	#%10010111
	BYTE	#%10101001
	BYTE	#%10001101
	BYTE	#%00011000
	BYTE	#%01000110
	BYTE	#%10001001
	BYTE	#%10101010
	BYTE	#%10111011
	BYTE	#%01000101
	BYTE	#%01100011
	BYTE	#%10000110
	BYTE	#%10101000
	BYTE	#%10101011
	BYTE	#%01010111
	BYTE	#%01010101
	BYTE	#%01010110
	BYTE	#%10000111
	BYTE	#%10101010
	BYTE	#%10111011
	BYTE	#%01011000
	BYTE	#%00110011
	BYTE	#%01110110
	BYTE	#%10011000
	BYTE	#%11001100
	BYTE	#%01111100
	BYTE	#%00110010
	BYTE	#%01110100
	BYTE	#%10010111
	BYTE	#%11011010
	BYTE	#%01111011
	BYTE	#%01000100
	BYTE	#%01100101
	BYTE	#%01110110
	BYTE	#%11001010
	BYTE	#%10001011
	BYTE	#%01010110
	BYTE	#%01010101
	BYTE	#%01100100
	BYTE	#%10101000
	BYTE	#%10011010
	BYTE	#%10101001
	BYTE	#%01101001
	BYTE	#%01000011
	BYTE	#%01110101
	BYTE	#%10001000
	BYTE	#%11011010
	BYTE	#%10001100
	BYTE	#%00110101
	BYTE	#%01100100
	BYTE	#%01110101
	BYTE	#%11001010
	BYTE	#%10101100
	BYTE	#%01010111
	BYTE	#%00110100
	BYTE	#%01100011
	BYTE	#%10111001
	BYTE	#%10111100
	BYTE	#%01111001
	BYTE	#%00110101
	BYTE	#%01010011
	BYTE	#%10010111
	BYTE	#%10101010
	BYTE	#%10111011
	BYTE	#%01111001
	BYTE	#%01000100
	BYTE	#%01100100
	BYTE	#%10000111
	BYTE	#%11001010
	BYTE	#%10111100
	BYTE	#%01011000
	BYTE	#%01000100
	BYTE	#%01100101
	BYTE	#%10101000
	BYTE	#%10111011
	BYTE	#%01111001
	BYTE	#%01010101
	BYTE	#%01010100
	BYTE	#%10000111
	BYTE	#%10101001
	BYTE	#%10001001
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10101001
	BYTE	#%10011010
	BYTE	#%01111000
	BYTE	#%01010110
	BYTE	#%01100110
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01100111
	BYTE	#%01110110
	BYTE	#%10010111
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10011001
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01010110
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10001001
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%10011000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01110101
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10000110
	BYTE	#%10001000
	BYTE	#%10001001
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10011000
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01100111
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%00000011
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10011010
	BYTE	#%10011010
	BYTE	#%10001000
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10101001
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%00000110
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10011001
	BYTE	#%10101001
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00001010
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10101001
	BYTE	#%10101001
	BYTE	#%01111000
	BYTE	#%01101000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01101000
	BYTE	#%01110111
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10101000
	BYTE	#%10101000
	BYTE	#%01111000
	BYTE	#%01011001
	BYTE	#%01111001
	BYTE	#%10100110
	BYTE	#%01110111
	BYTE	#%01011001
	BYTE	#%01101010
	BYTE	#%10010111
	BYTE	#%10010110
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10101000
	BYTE	#%10111000
	BYTE	#%01101000
	BYTE	#%00111010
	BYTE	#%01111010
	BYTE	#%11000101
	BYTE	#%10010101
	BYTE	#%01011001
	BYTE	#%01011011
	BYTE	#%10001001
	BYTE	#%10010110
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%01001011
	BYTE	#%01001011
	BYTE	#%10011000
	BYTE	#%11010011
	BYTE	#%10010100
	BYTE	#%01011001
	BYTE	#%01001011
	BYTE	#%01111001
	BYTE	#%10010110
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01111000
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%01011011
	BYTE	#%01101100
	BYTE	#%10011000
	BYTE	#%11010100
	BYTE	#%11000010
	BYTE	#%01000111
	BYTE	#%00111100
	BYTE	#%01011011
	BYTE	#%10001000
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10010110
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10111000
	BYTE	#%11010100
	BYTE	#%10010101
	BYTE	#%01001000
	BYTE	#%01011110
	BYTE	#%01001110
	BYTE	#%10011000
	BYTE	#%10110100
	BYTE	#%10100100
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%00000110
	BYTE	#%10101000
	BYTE	#%10100110
	BYTE	#%01100111
	BYTE	#%01001010
	BYTE	#%00111100
	BYTE	#%01011011
	BYTE	#%10011000
	BYTE	#%10100101
	BYTE	#%10010101
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01101000
	BYTE	#%01101000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%01111010
	BYTE	#%00111100
	BYTE	#%01101100
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10010110
	BYTE	#%10010101
	BYTE	#%10000110
	BYTE	#%01101001
	BYTE	#%01111001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%00000100
	BYTE	#%10001000
	BYTE	#%10001011
	BYTE	#%10111001
	BYTE	#%11010011
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%10010110
	BYTE	#%01100101
	BYTE	#%01001010
	BYTE	#%01111010
	BYTE	#%10100111
	BYTE	#%10010101
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01101000
	BYTE	#%01101000
	BYTE	#%01110110
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%01011011
	BYTE	#%01111101
	BYTE	#%11000111
	BYTE	#%10000101
	BYTE	#%00111010
	BYTE	#%01101011
	BYTE	#%11000100
	BYTE	#%01110100
	BYTE	#%01011011
	BYTE	#%10001010
	BYTE	#%10100110
	BYTE	#%01100111
	BYTE	#%01101001
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%01100111
	BYTE	#%01111000
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10011000
	BYTE	#%01101011
	BYTE	#%01101101
	BYTE	#%11001010
	BYTE	#%11000010
	BYTE	#%00110111
	BYTE	#%00111100
	BYTE	#%10011000
	BYTE	#%10100100
	BYTE	#%01110111
	BYTE	#%10001001
	BYTE	#%10000110
	BYTE	#%01100111
	BYTE	#%01101001
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%10111001
	BYTE	#%11000101
	BYTE	#%01111000
	BYTE	#%00111110
	BYTE	#%10111001
	BYTE	#%11001100
	BYTE	#%01100100
	BYTE	#%01011010
	BYTE	#%01111010
	BYTE	#%01111001
	BYTE	#%01111001
	BYTE	#%10010110
	BYTE	#%10000100
	BYTE	#%01100111
	BYTE	#%01101001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%10001010
	BYTE	#%11011000
	BYTE	#%11000101
	BYTE	#%00101010
	BYTE	#%00111101
	BYTE	#%10010111
	BYTE	#%10100011
	BYTE	#%10000110
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01101010
	BYTE	#%10001000
	BYTE	#%10010101
	BYTE	#%01110110
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01101000
	BYTE	#%01100111
	BYTE	#%01110110
	BYTE	#%10010110
	BYTE	#%01101001
	BYTE	#%01101101
	BYTE	#%10111011
	BYTE	#%11010011
	BYTE	#%01100100
	BYTE	#%01001001
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10100111
	BYTE	#%01110111
	BYTE	#%01011000
	BYTE	#%01101000
	BYTE	#%10000111
	BYTE	#%00000011
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%01110111
	BYTE	#%10101001
	BYTE	#%11000110
	BYTE	#%10011000
	BYTE	#%01001011
	BYTE	#%01011100
	BYTE	#%10010110
	BYTE	#%10000100
	BYTE	#%10000110
	BYTE	#%01111000
	BYTE	#%01111001
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000110
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%01101011
	BYTE	#%10111010
	BYTE	#%10111000
	BYTE	#%10010110
	BYTE	#%01010111
	BYTE	#%01001000
	BYTE	#%01110111
	BYTE	#%10010110
	BYTE	#%10100111
	BYTE	#%10001001
	BYTE	#%01111001
	BYTE	#%01101000
	BYTE	#%01110110
	BYTE	#%10000110
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10001010
	BYTE	#%10111010
	BYTE	#%10101000
	BYTE	#%10001000
	BYTE	#%01100110
	BYTE	#%01010111
	BYTE	#%01110111
	BYTE	#%10010111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10011010
	BYTE	#%10111010
	BYTE	#%10011001
	BYTE	#%01111001
	BYTE	#%01110110
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%10000111
	BYTE	#%10101001
	BYTE	#%10111010
	BYTE	#%10101010
	BYTE	#%10001001
	BYTE	#%01100110
	BYTE	#%01010101
	BYTE	#%01110110
	BYTE	#%10010111
	BYTE	#%10011001
	BYTE	#%10001001
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000100
	BYTE	#%10011001
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%10001000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%00000100
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10011001
	BYTE	#%10011001
	BYTE	#%01111000
	BYTE	#%01100111
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10001000
	BYTE	#%10011000
	BYTE	#%10001001
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01100110
	BYTE	#%01100110
	BYTE	#%01110110
	BYTE	#%10000111
	BYTE	#%10011000
	BYTE	#%10001000
	BYTE	#%00000100
	BYTE	#%01110111
	BYTE	#%00000100
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%00000100
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000100
	BYTE	#%01110111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%00000100
	BYTE	#%01110111
	BYTE	#%00000110
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%00000101
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%00000011
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%10001000
	BYTE	#%00000011
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%01110111
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%10001000
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01111000
	BYTE	#%00000011
	BYTE	#%10000111
	BYTE	#%10000111
	BYTE	#%01110111
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%00000011
	BYTE	#%01111000
	BYTE	#%01111000
	BYTE	#%10000111
	BYTE	#%00000000
