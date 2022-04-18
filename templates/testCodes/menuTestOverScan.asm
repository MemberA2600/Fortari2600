	LDA	counter
	AND	#%00000011
	BNE	NoChangeInStuff

	LDA	#$20
	BIT	SWCHA
	BNE	NotDownPressed
	INC	##NAME##_Selected_Item
	JMP	NotUpPressed
NotDownPressed
	LDA	#$10
	BIT	SWCHA
	BNE	NotUpPressed
	DEC	##NAME##_Selected_Item
NotUpPressed

	LDA	##NAME##_Selected_Item
	CMP	#255
	BNE	NoZero
	LDA	#0
	STA	##NAME##_Selected_Item
	JMP	NoChangeInStuff
NoZero
	LDA	###NAME##_Item_Number
	SEC
	SBC	#1
	CMP	##NAME##_Selected_Item
	BCS	NoChangeInStuff
	STA	##NAME##_Selected_Item

NoChangeInStuff