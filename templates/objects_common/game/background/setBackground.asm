* params=data
* param1=#NAME#,playfields,##NAME##
* direction=TO
*
	LDA	#<#NAME#_BG
	STA	bkColorPointer

	LDA	#>#NAME#_BG
	STA	bkColorPointer+1
