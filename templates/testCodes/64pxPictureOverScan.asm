*	LDA	counter
*	AND	#%00000001
*	CMP	#%00000001
*	BNE	NoIndexIncr

	LDA	#$20
	BIT	SWCHA
	BNE	NoExpand
	LDY	#FULLHEIGHT
	DEY
	CPY	picDisplayHeight
	BCC	NoExpand
	INC	picDisplayHeight
	JMP	ExpandDone
NoExpand
	LDA	#$10
	BIT	SWCHA
	BNE 	ExpandDone

	LDA	#2
	CMP	picDisplayHeight
	BEQ	ExpandDone

	DEC	picDisplayHeight	
ExpandDone
	BIT 	SWCHA
	BVS	NoIndexDecr

	LDA	picIndex
	CMP	#0
	BEQ	NoIndexIncr
	DEC	picIndex
	JMP	NoIndexIncr
NoIndexDecr
	BIT	SWCHA
	BMI	NoIndexIncr

	LDA	#FULLHEIGHT
	SEC
	SBC	picDisplayHeight
	CMP	picIndex
	BCC	NoIndexIncr
	INC	picIndex
	
NoIndexIncr
	LDY	#FULLHEIGHT
	DEY
	TYA
	SEC
	SBC	picDisplayHeight
	CMP	picIndex
	BCS	NoDebug
	STA	picIndex
NoDebug
	LDA	#FULLHEIGHT
	CMP	picDisplayHeight
	BNE	NoDebug2
	LDA	#0
	STA	picIndex
NoDebug2