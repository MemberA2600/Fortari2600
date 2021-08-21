DoAgain
	LDA	CounterA
	BMI	OtherCount

	DEC	CounterA
	LDA	#0
	STA	frameColor
	STA	AUDV0
	STA	AUDC0
	STA	AUDF0

	LDA	#45
	STA	CounterB	

	JMP	EndAll
OtherCount
	
	LDA	CounterB
	BPL	CoolThings
	LDA	#21
	LDY	Freq
	CPY	#31
	BNE	NoADD
	CLC
	ADC	#100
NoADD
	STA	CounterA
	INC	Freq
	JMP	DoAgain

CoolThings

	DEC	CounterB
	LDA	Freq
	CMP	#32
	BNE	NOINC
	LDA	#0
	STA	Freq
	INC	Channel

NOINC	
	LDA	#8
	STA	AUDV0
	LDY	Channel
	LDA 	TheOnesToLoad,y
	STA	AUDC0
	ASL
	ASL
	ASL
	ASL
	ASL
	ORA	Freq
	STA	frameColor
	

	LDA	Freq
	STA	AUDF0



EndAll
	JMP	ZZZZ

TheOnesToLoad
	byte	#1
	byte	#3
	byte	#4
	byte	#6
	byte	#7
	byte	#8
	byte	#12
	byte	#14
	byte	#15


ZZZZ
