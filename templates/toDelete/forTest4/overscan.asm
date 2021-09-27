	LDA	counter
	AND	#%00000111
	CMP	#%00000111	
	BNE	NoPressedRight


	BIT	SWCHA
	BMI	NoPressedLeft

	LDA	Letter01
	CMP	#38	
	BCS	NoPressedRight
	INC	Letter01
	INC	Letter02
	INC	Letter03
	INC	Letter04
	INC	Letter05
	INC	Letter06
	INC	Letter07
	INC	Letter08
	INC	Letter09
	INC	Letter10
	INC	Letter11
	INC	Letter12

	JMP	NoPressedRight
NoPressedLeft

	BIT	SWCHA
	BVS	NoPressedRight

	LDA	#0
	CMP	Letter01
	BCS	NoPressedRight
	DEC	Letter01
	DEC	Letter02
	DEC	Letter03
	DEC	Letter04
	DEC	Letter05
	DEC	Letter06
	DEC	Letter07
	DEC	Letter08
	DEC	Letter09
	DEC	Letter10
	DEC	Letter11
	DEC	Letter12
NoPressedRight