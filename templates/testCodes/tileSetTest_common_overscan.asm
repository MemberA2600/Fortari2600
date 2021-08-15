	LDA	#$08
	BIT 	SWCHB
	BNE	HandleTheSubMenu

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
	LDA	SubMenu
	AND	#%10111111
	STA	SubMenu		

	JMP	SubMenuEnded

HandleTheSubMenu
	LDA	SubMenu
	ORA	#%01000000
	STA	SubMenu		

	LDA	TileSelected
	AND	#%11100000
	STA	temp10

	LDA	#$02
	BIT	SWCHB
	BNE	NoBackColorChangeSub
	INC	frameColor
NoBackColorChangeSub
	LDA	INPT4
	BMI	NoFrontColorChangeSub
	INC	TileScreenMainColor
NoFrontColorChangeSub
	

	LDA	counter
	AND	#%00000111
	CMP	#%00000111
	BNE	SubMenuEnded

	LDA	counter
	AND	#%00001111
	CMP	#%00001111
	BNE	NoRadicalChanges

	LDA	#$01
	BIT	SWCHB
	BNE	NoChangeLineNum

	LDA	SubMenuLines
	AND	#%11111100
	STA	temp05
	LDA	SubMenuLines
	AND	#%00000011
	ORA	#%11111100
	CLC
	ADC	#1
	AND	#%00000011
	ORA	temp05			

	STA	SubMenuLines
NoChangeLineNum


NoRadicalChanges
	LDA	TileSelected
	AND	#%00011111
	ORA	temp10
	STA	TileSelected

	LDA	SubMenuLines
	AND	#%00000011
	CLC
	ADc	#1
	TAY
	LDA	#255
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
	AND	#%00011111
	CMP	#0
	BEQ	ItsZeroLOL

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
	LDA	TileSelected
	ORA	#%11100000
	CLC
	ADC	#1
SaveTileSelect
	AND	#%00011111
	STA	TileSelected

SubVertical

	LDY	#0
	LDA	TileSelected
	AND	#%00011111

SmallerThan62
	CMP	#6
	BCC	GetRowNum
	SEC
	SBC	#6
	INY
	JMP	SmallerThan62
GetRowNum
	STY	temp02

	LDA	SubMenuLines
	AND	#%00000011
	CMP	temp02
	BEQ	NoUpSub


	LDA	#$20
	bit 	SWCHA
	BNE	NoUpSub

	LDA	TileSelected
	AND	#%11100000
	LDA	TileSelected
	ORA	#%11100000
	CLC
	ADC	#6

	JMP	SaveTileSelect2

NoUpSub
	LDA	#0
	CMP	temp02
	BEQ	NoVerMoveSub


	LDA	#$10
	bit 	SWCHA
	BNE	NoVerMoveSub

	LDA	TileSelected
	AND	#%11100000
	LDA	TileSelected
	AND	#%00011111
	SEC
	SBC	#6

SaveTileSelect2
	AND	#%00011111
	STA	TileSelected
NoVerMoveSub


SubMenuEnded
	LDA	SWCHB
	AND	#%11000000
	LSR	
	STA	temp01
	LDA	OverlapScreen
	AND	#%10011111
	ORA	temp01
	STA	OverlapScreen
	