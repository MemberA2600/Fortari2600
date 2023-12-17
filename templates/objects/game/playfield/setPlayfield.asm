* params=data
* param1=#NAME#,playfields,##NAME##
* direction=TO
*

	LDA	#<#NAME#_00
	STA	pf0Pointer

	LDA	#>#NAME#_00
	STA	pf0Pointer+1

	LDA	#<#NAME#_01
	STA	pf1Pointer

	LDA	#>#NAME#_01
	STA	pf1Pointer+1

	LDA	#<#NAME#_02
	STA	pf2Pointer

	LDA	#>#NAME#_02
	STA	pf2Pointer+1

	LDA	#<#NAME#_FG
	STA	pfColorPointer

	LDA	#>#NAME#_FG
	STA	pfColorPointer+1
