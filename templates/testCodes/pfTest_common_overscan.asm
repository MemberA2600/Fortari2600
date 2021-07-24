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

	