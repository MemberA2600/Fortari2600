	LDA	#$20
	BIT	SWCHA
	BEQ	NoScrollDown
	DEC	pfIndex
	JMP	DebugIndex
NoScrollDown
	LDA	#$10
	BIT	SWCHA
	BEQ	ChangeColor
	INC	pfIndex
DebugIndex
	LDA	!!!Max!!!
	CMP	#255
	BEQ	ChangeColor

	CMP	pfIndex
	BCS	ChangeColor
	DEC	pfIndex
ChangeColor
	LDA	#$01
	BIT	SWCHA
	BEQ	NoOneUp
	INC	pfBaseColor
NoOneUp
	LDA	#$02
	BIT	SWCHA
	BEQ	AllDone
	INC	bkBaseColor
AllDone

	