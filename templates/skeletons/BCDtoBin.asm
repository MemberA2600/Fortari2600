#BANK#_BCD2BIN
	STA	temp03
	AND	#%00001111
	STA	temp04
	LDA	temp03
	AND	#%11110000
	LSR
	LSR
	LSR
	LSR	
	TAX
	LDA	#BANK#_BCD2BIN_Table,x
	CLC
	ADC	temp04

	JMP	(temp01)
