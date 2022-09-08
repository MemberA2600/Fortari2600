*
* #DIVIDER#	: Sets how many frames to wait for incrementation
* #DIGIT_DATA1#	: 0-5: Hours, 6: Increment, Decrement, 7: Stop
* #DIGIT_DATA2#	: Minutes
* #DIGIT_DATA3#	: Seconds
*
* Digit0_Pointer: temp03 (+ temp04)
* Digit1_Pointer: temp05 (+ temp06)
* Digit2_Pointer: temp07 (+ temp08)
* Digit3_Pointer: temp09 (+ temp10)
* Color:	: temp17 (bit 0 is if AM/PM)
*

#NAME#_DigitClock_Set_Digits

	LDX	##DIVIDER#
	DEX
	CPX	#0
	BEQ	#NAME#_DigitClock_Set_Digits_No_Frame_Check

	STX	temp19
	LDA	counter
	AND	temp19
	BNE	#NAME#_DigitClock_Set_Digits_No_Change

#NAME#_DigitClock_Set_Digits_No_Frame_Check
	LDA	#DIGIT_DATA1#
	BMI	#NAME#_DigitClock_Set_Digits_Changed
	BIT	#DIGIT_DATA1#
	BVS	#NAME#_DigitClock_Set_Digits_Decrement

#NAME#_DigitClock_Set_Digits_Increment
	AND	#%11000000
	STA	temp18
	
	CLC
	SED
	
	LDA	#DIGIT_DATA3#	
	ADC	#$01
	STA	#DIGIT_DATA3#
	CMP	#$10	
	BNE	#NAME#_DigitClock_Set_Digits_Increment_Ended
	
	LDA	#$00
	STA	#DIGIT_DATA3#

	CLC
	LDA	#DIGIT_DATA2#	
	ADC	#$01
	STA	#DIGIT_DATA2#
	CMP	#$60	
	BNE	#NAME#_DigitClock_Set_Digits_Increment_Ended

	LDA	#$00
	STA	#DIGIT_DATA2#

	LDA	#DIGIT_DATA1#
	AND	#%00111111

	CLC
	ADC	#$01
	TAX
	ORA	temp18
	STA	#DIGIT_DATA1#
	CPX	#$24
	BNE	#NAME#_DigitClock_Set_Digits_Increment_Ended
	LDA	temp18
	STA	#DIGIT_DATA1#


#NAME#_DigitClock_Set_Digits_Increment_Ended
	CLD	

	JMP	#NAME#_DigitClock_Set_Digits_Changed
#NAME#_DigitClock_Set_Digits_Decrement
	AND	#%11000000
	STA	temp18
	
	SEC
	SED

	LDA	#DIGIT_DATA3#	
	SBC	#$01
	STA	#DIGIT_DATA3#
	CMP	#$99
	BNE	#NAME#_DigitClock_Set_Digits_Decrement_Ended

	LDA	#$09	
	STA	#DIGIT_DATA3#

	LDA	#DIGIT_DATA2#
	SEC	
	SBC	#$01
	STA	#DIGIT_DATA2#
	CMP	#$99
	BNE	#NAME#_DigitClock_Set_Digits_Decrement_Ended
	
	LDA	#$59	
	STA	#DIGIT_DATA2#

	LDA	#DIGIT_DATA1#
	AND	#%00111111
	SEC
	SBC	#$01
	TAX
	ORA	temp18
	STA	#DIGIT_DATA1#
	CPX	#$99
	BNE	#NAME#_DigitClock_Set_Digits_Decrement_Ended
	LDA	#$23
	ORA	temp18
	STA	#DIGIT_DATA1#
	
#NAME#_DigitClock_Set_Digits_Decrement_Ended
	CLD	

	JMP	#NAME#_DigitClock_Set_Digits_Changed
#NAME#_DigitClock_Set_Digits_No_Change
	STA	WSYNC

#NAME#_DigitClock_Set_Digits_Changed
*
*	Dunno if needed.
*
	STA	WSYNC

	LDA	#DIGIT_DATA1#
	AND	#%00111111
#24HOURS#
	STA	temp19
	CLC

	AND	#%11110000
	LSR	
	ADC	temp03
	STA	temp03
	
	LDA	temp19
	AND	#%00001111
	ASL
	ASL
	ASL
	ADC	temp05
	STA	temp05

	LDA	#DIGIT_DATA2#
	AND	#%11110000
	LSR
	ADC	temp07
	STA	temp07

	LDA	#DIGIT_DATA2#
	AND	#%00001111
	ASL
	ASL
	ASL
	ADC	temp09
	STA	temp09
