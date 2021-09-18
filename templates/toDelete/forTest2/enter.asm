Volume = $e0
Channel = $e1
Freq = $e2
CounterA = $e3
CounterB = $e4

	LDA	#0
	STA	Volume
	STA	Channel
	STA	Freq
	STA	CounterB

	LDA	#127
	STA	CounterA

	LDA	Zero
	STA	pf0Pointer
	STA	pf0Pointer+1
	STA	pf1Pointer
	STA	pf1Pointer+1
	STA	pf2Pointer
	STA	pf2Pointer+1
	STA	pfColorPointer
	STA	pfColorPointer+1
	STA	bkColorPointer
	STA	bkColorPointer+1

	LDA	P0TurnOff
	AND	#%00111111
	ORA	#%01000000
	STA	P0TurnOff	; Turn Off P0 and M0

	LDA	P1TurnOff
	AND	#%00111111
	ORA	#%01000000
	STA	P1TurnOff	; Turn Off P1 and M1

	LDA	BallTurnOff
	ORA	#%00001000
	STA	BallTurnOff	; Turn off Ball