*
*	The soundplayer will use 4 bytes (if none is disabled).
*	2 bytes are for AUD0 and AUD1.
*	0-2: Duration countdown
*	3-6: Index for the effect (only used for selection, interrupts current sound)
*	7  : Playing
*
*	2 bytes for the pointer index, so the whole data can be 256 bytes long.
*

	LDA	#VAR01#
	BPL	#NAME#_Channelﬂ__CheckForNew
	
	AND	#%00000111
	SEC
	SBC	#1
	ORA	#%10000000
	STA	#VAR01#

	CMP	#%10000000
	BEQ	#NAME#_Channelﬂ__CCCCCCC
	JMP	#NAME#_Channelﬂ__NoSoundPLay

#NAME#_Channelﬂ__CCCCCCC
	LDX	#VAR02#
	JMP	#NAME#_Channelﬂ__NewData	

#NAME#_Channelﬂ__CheckForNew
        AND	#%01111000
	LSR
	LSR
	LSR
	CMP	#0
	BNE	#NAME#_Channelﬂ__GetNewPointer
	JMP	#NAME#_Channelﬂ__NoSoundPLay
#NAME#_Channelﬂ__GetNewPointer
	CMP	##NUM#
	BCC 	#NAME#_Channelﬂ__NotLargerThanMax
	LDA	#1
#NAME#_Channelﬂ__NotLargerThanMax
	TAX	
	DEX
	LDA 	#NAME#_PointerTable,x
	TAX		
#NAME#_Channelﬂ__NewData
	LDA	#NAME#_SoundFX,x
	INX
	CMP	#$F0
	BNE	#NAME#_Channelﬂ__Continue
	LDA	#0
	STA	AUDVﬂ
	STA	#VAR01#	
	JMP	#NAME#_Channelﬂ__NoSoundPLay
#NAME#_Channelﬂ__Continue
	TAY
	AND	#%00001111
	CMP	#0
	BNE	#NAME#_Channelﬂ__NormalData
	STA	AUDVﬂ
	TYA
	JMP	#NAME#_Channelﬂ__SaveDuration	
#NAME#_Channelﬂ__NormalData
	TYA
	STA	AUDVﬂ
	LSR
	LSR
	LSR
	LSR	
	STA	AUDCﬂ
	LDA	#NAME#_SoundFX,x
	INX	
	STA	AUDFﬂ
	AND	#%11100000
#NAME#_Channelﬂ__SaveDuration
	ROL
	ROL
	ROL
	ROL
	ORA	#%10000000
	STA	#VAR01#	
#NAME#_Channelﬂ__SaveIndex
	STX	#VAR02#
#NAME#_Channelﬂ__NoSoundPLay