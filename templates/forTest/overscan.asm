	LDA	SWCHB
	AND	#%00001000
	ASL
	ASL
	ASL
	STA	temp01
	LDA	SubMenu
	AND	#%10111111
	ORA	temp01
	STA	SubMenu


	LDA	SubMenu
	AND	#%01000000
	CMP	#%01000000
	BNE	ChangeColor
	JMP	OtherWay
NoSubMenuHere 
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
	LDA	#26
	CMP	#255
	BEQ	ChangeColor
	CMP	pfIndex
	BCS	SmallerThan
	LDA	#26
	STA	pfIndex
SmallerThan
	LDA	pfIndex
	CMP	#26
	BCS	ChangeColor
	LDA	#26
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
*	LDA	#$08
*	BIT 	SWCHB
*	BEQ 	MissileDone
GoWithSprite

	bit 	SWCHA
	BVS	NoLeftMove
	DEC	P0X
	LDA	P0Mirrored 
	ORA	#%00001000
	STA	P0Mirrored

	JMP	VerticalMovementCheck
NoLeftMove
	BMI 	VerticalMovementCheck
	INC	P0X
	LDA	P0Mirrored 
	AND	#%11110111
	STA	P0Mirrored	

VerticalMovementCheck	
	LDA	#$10
	bit 	SWCHA
	BNE	NoDownMove
	DEC	P0Y
	JMP	SpriteEnded
NoDownMove
	LDA	#$20
	bit 	SWCHA
	BNE	SpriteEnded
	INC	P0Y
SpriteEnded

	LDA	counter
	STA	M0Color
	AND	#%00000111
	CMP	#%00000111
	BNE	NoINC

	LDA	P0SpriteIndex
	AND	#%00001111
	TAY
	STA	temp01
	CMP	#maxFrames
	BCC	NoSetZero
SetZero
	LDA	P0SpriteIndex
	AND	#%11110000
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
	STA	temp01
	LDA	P0SpriteIndex	
	AND	#%11110000
	ORA	temp01
SaveSpriteIndex
	STA	P0SpriteIndex
NoINC	
	
	LDA	Sound
	CMP	#0
	BNE	PlaySoundMoveMis

	bit	INPT4	
	BMI	RemoveMissile

	LDA	P0TurnOff
	AND	#%01111111	
	STA	P0TurnOff

	LDA	#12
	STA	Sound
	LDA	P0Mirrored
	AND	#%00001000
	STA	MissileDir
	CMP	#0
	BEQ 	ItsMirrored
	LDA	P0X
	CLC
	ADC	#3
	JMP	M0XDone
ItsMirrored
	LDA	P0X
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
	STA	M0X

	LDA	P0Height
	LSR
	STA	temp02

	LDA	#42
	SEC
	SBC	P0Y
	CLC
	ADC	P0Height
	SEC
	SBC	temp02
	STA	M0Y

PlaySoundMoveMis
	LDA	MissileDir
	AND	#%00001000
	CMP	#0
	BNE 	MissileLeft
	INC	M0X
	INC	M0X
	JMP 	ToSound
MissileLeft	
	DEC	M0X
	DEC	M0X

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
	LDA	P0TurnOff
	ORA	#%10000000	
	STA	P0TurnOff
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
	LDA	P0Settings
	AND	#%11001000
	ORA	NUSIZ
	STA	P0Settings

	LDA	NUSIZ
	CMP	#5
	BNE	Not5Again
	LDA	P0Settings
	AND	#%11001111
	ORA	#%00010000	
	JMP	SSSSAVE
Not5Again
	CMP	#7
	BNE	NoNUSIZChange
	LDA	P0Settings
	AND	#%11001111
	ORA	#%00110000
SSSSAVE	
	STA	P0Settings
NoNUSIZChange
	JMP	SubMenuEnded

OtherWay
	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	SubMenuEnded

	LDA	SubMenuLines
	AND	#%00000011
	CLC
	ADc	#1
	TAY
	LDA	#0
	STA	temp02
Add6ToThat2
	CPY	#0
	BEQ	NoMore62
	CLC
	ADC	#6
	DEY
	JMP 	Add6ToThat2
NoMore62
	STA	temp02

	bit 	SWCHA
	BVS	NoLeftMoveSub


	LDA	TileSelected
	CMP	#0
	BEQ	ItsZeroLOL


	AND	#%11100000
	STA	temp01
	LDA	TileSelected
	AND	#%00011111
	SEC
	SBC	#1
	JMP	SaveTileSelect

ItsZeroLOL
	LDA	temp02
	JMP	SaveTileSelect


NoLeftMoveSub
	bit 	SWCHA
	BMI	SubVertical

	LDA	TileSelected
	AND	#%11100000
	STA	temp01
	LDA	TileSelected
	ORA	#%11100000
	CLC
	ADC	#1
SaveTileSelect
	AND	#%00011111
	ORA	temp01
	STA	TileSelected

SubVertical
	LDA	#$10
	bit 	SWCHA
	BNE	NoDownMovesub


	JMP	NoVerMoveSub

NoDownMovesub
	LDA	#$20
	bit 	SWCHA
	BNE	NoVerMoveSub

NoVerMoveSub


SubMenuEnded