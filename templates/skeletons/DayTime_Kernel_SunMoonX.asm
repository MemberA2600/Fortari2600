******* Sun / Moon XPoz
	LDA	##NAME#_DayTime_L
	CMP	#VAR01#
	BCC	#NAME#_DayTime_Not_Smaller
	STA	#VAR01#				; 10 (54)
#NAME#_DayTime_Not_Smaller
	LDA	##NAME#_DayTime_R
	CMP	#VAR01#
	BCS	#NAME#_DayTime_Not_Larger
	STA	#VAR01#				; 10 (64)
#NAME#_DayTime_Not_Larger
