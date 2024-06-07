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
	BPL	#NAME#_Channel�__CheckForNew
	
	AND	#%00000111
	SEC
	SBC	#1
	ORA	#%10000000
	STA	#VAR01#

	CMP	#%10000000
	BEQ	#NAME#_Channel�__CCCCCCC
	JMP	#NAME#_Channel�__NoSoundPLay

#NAME#_Channel�__CCCCCCC
	LDX	#VAR02#
	JMP	#NAME#_Channel�__NewData	

#NAME#_Channel�__CheckForNew
        AND	#%01111000
	LSR
	LSR
	LSR
	CMP	#0
	BNE	#NAME#_Channel�__GetNewPointer
	JMP	#NAME#_Channel�__NoSoundPLay
#NAME#_Channel�__GetNewPointer
	CMP	##NUM#
	BCC 	#NAME#_Channel�__NotLargerThanMax
	LDA	#1
#NAME#_Channel�__NotLargerThanMax
	TAX	
	DEX
	LDA 	#NAME#_PointerTable,x
	TAX		
#NAME#_Channel�__NewData
	LDA	#NAME#_SoundFX,x
	INX
	CMP	#$F0
	BNE	#NAME#_Channel�__Continue
	LDA	#0
	STA	AUDV�
	STA	#VAR01#	
	JMP	#NAME#_Channel�__NoSoundPLay
#NAME#_Channel�__Continue
	TAY
	AND	#%00001111
	CMP	#0
	BNE	#NAME#_Channel�__NormalData
	STA	AUDV�
	TYA
	JMP	#NAME#_Channel�__SaveDuration	
#NAME#_Channel�__NormalData
	TYA
	STA	AUDV�
	LSR
	LSR
	LSR
	LSR	
	STA	AUDC�
	LDA	#NAME#_SoundFX,x
	INX	
	STA	AUDF�
	AND	#%11100000
#NAME#_Channel�__SaveDuration
	ROL
	ROL
	ROL
	ROL
	ORA	#%10000000
	STA	#VAR01#	
#NAME#_Channel�__SaveIndex
	STX	#VAR02#
#NAME#_Channel�__NoSoundPLay