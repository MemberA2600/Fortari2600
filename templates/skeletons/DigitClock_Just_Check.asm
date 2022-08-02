
	TAX
	CMP	#$12
	BCC	#NAME#_DigitClock_No_PM
	LDA	temp17
	ORA	#%00000001
	STA	temp17
#NAME#_DigitClock_No_PM
	TXA