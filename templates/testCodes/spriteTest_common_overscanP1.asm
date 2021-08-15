	LDA	#$08
	BIT 	SWCHB
	BNE	ChangeColor

	LDA	#$20
	BIT	SWCHA
	BNE	NoScrollDown
	DEC	pfIndex
	JMP	DebugIndex
NoScrollDown
	LDA	#$10
	BIT	SWCHA
	BNE	ChangeColor
	INC	pfIndex
DebugIndex
	LDA	#!!!Max!!!
	CMP	#255
	BEQ	ChangeColor
	CMP	pfIndex
	BCS	SmallerThan
	LDA	#!!!Max!!!
	STA	pfIndex
SmallerThan
	LDA	pfIndex
	CMP	#!!!Min!!!
	BCS	ChangeColor
	LDA	#!!!Min!!!
	STA	pfIndex

ChangeColor
	LDA	#$01
	BIT	SWCHB
	BNE	NoOneUp
	INC	pfBaseColor
NoOneUp
	LDA	#$02
	BIT	SWCHB
	BNE 	AllDone
	INC	bkBaseColor
AllDone
	LDA	#$08
	BIT 	SWCHB
	BEQ 	MissileDone
GoWithSprite

	bit 	SWCHA
	BVS	NoLeftMove
	DEC	P1X
	LDA	P1Mirrored 
	ORA	#%00001000
	STA	P1Mirrored

	JMP	VerticalMovementCheck
NoLeftMove
	BMI 	VerticalMovementCheck
	INC	P1X
	LDA	P1Mirrored 
	AND	#%11110111
	STA	P1Mirrored	

VerticalMovementCheck	
	LDA	#$10
	bit 	SWCHA
	BNE	NoDownMove
	DEC	P1Y
	JMP	SpriteEnded
NoDownMove
	LDA	#$20
	bit 	SWCHA
	BNE	SpriteEnded
	INC	P1Y
SpriteEnded

	LDA	counter
	STA	M1Color
	AND	#%00000111
	CMP	#%00000111
	BNE	NoINC

	LDA	P1SpriteIndex
	lsr
	lsr
	lsr
	lsr
	AND	#%00001111
	TAY
	STA	temp01
	CMP	#maxFrames
	BCC	NoSetZero
SetZero
	LDA	P1SpriteIndex
	AND	#%00001111
	JMP	SaveSpriteIndex
NoSetZero
	LDA	Sound
	CMP	#0
	BNE 	GoForSure

	LDA	SWCHA
	AND	#%11110000
	CMP	#%11110000
	BEQ	SetZero
GoForSure
	LDA	temp01
	CLC
	ADC	#1
	ASL
	ASL
	ASL
	ASL
	STA	temp01
	LDA	P1SpriteIndex	
	AND	#%00001111
	ORA	temp01
SaveSpriteIndex
	STA	P1SpriteIndex
NoINC	
	
	LDA	Sound
	CMP	#0
	BNE	PlaySoundMoveMis

	bit	INPT4	
	BMI	RemoveMissile

	LDA	P1TurnOff
	AND	#%01111111	
	STA	P1TurnOff

	LDA	#12
	STA	Sound
	LDA	P1Mirrored
	AND	#%00001000
	STA	MissileDir
	CMP	#0
	BEQ 	ItsMirrored
	LDA	P1X
	CLC
	ADC	#3
	JMP	M0XDone
ItsMirrored
	LDA	P1X
	CLC
	ADC	#5
	LDY	NUSIZ
	CPY	#5
	BNE	Not5
	ADC	#9
	JMP	M0XDone
Not5	
	CPY	#7
	BNE	M0XDone
	ADC	#24

M0XDone
	STA	M1X

	LDA	P1Height
	LSR
	STA	temp02

	LDA	#42
	SEC
	SBC	P1Y
	CLC
	ADC	P1Height
	SEC
	SBC	temp02
	STA	M1Y

PlaySoundMoveMis
	LDA	MissileDir
	AND	#%00001000
	CMP	#0
	BNE 	MissileLeft
	INC	M1X
	INC	M1X
	JMP 	ToSound
MissileLeft	
	DEC	M1X
	DEC	M1X

ToSound
	LDA	Sound
	STA	AUDV0
	LDA	#8
	STA	AUDC0	
	SEC
	SBC	Sound
	STA	AUDF0
	DEC	Sound
	JMP	MissileDone
RemoveMissile
	LDA	P1TurnOff
	ORA	#%10000000	
	STA	P1TurnOff
	LDA	#0
	STA	AUDV0
MissileDone
	LDA	pfSettings
	BIT	SWCHB
	BVC	MoveBehind
	ORA	#%00000100
	JMP	MoveBefore
MoveBehind
	AND	#%11111011	
MoveBefore	
	STA	pfSettings	; Changes behaiour on P0 diff switch.	

	
	LDA	counter
	AND	#%011111111
	CMP	#%011111111
	BNE	NoNUSIZChange
	BIT	SWCHB
	BPL	NoNUSIZChange
	INC 	NUSIZ
	LDA	#7
	CMP	NUSIZ
	BCS	NoZeroNusiz
	LDA	#0
	STA	NUSIZ
NoZeroNusiz
	LDA	P1Settings
	AND	#%11001000
	ORA	NUSIZ
	STA	P1Settings

	LDA	NUSIZ
	CMP	#5
	BNE	Not5Again
	LDA	P1Settings
	AND	#%11001111
	ORA	#%00010000	
	JMP	SSSSAVE
Not5Again
	CMP	#7
	BNE	NoNUSIZChange
	LDA	P1Settings
	AND	#%11001111
	ORA	#%00110000
SSSSAVE	
	STA	P1Settings

NoNUSIZChange

