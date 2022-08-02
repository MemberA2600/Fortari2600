
	CMP	#$12
	BCC	#NAME#_DigitClock_No_PM__
	SED

	SEC
	SBC	#$12
	TAX

	CLD
	
	LDA	temp17
	ORA	#%00000001
	STA	temp17

	TXA
#NAME#_DigitClock_No_PM__
	CMP	#0
	BNE	#NAME#_DigitClock_No_Set12__
	LDA	#$12
#NAME#_DigitClock_No_Set12__