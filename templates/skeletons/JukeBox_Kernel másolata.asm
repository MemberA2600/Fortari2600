*
* temp01 + temp02 is the Jumpback address for both.	
* temp16, temp17, temp18, temp19 sends back the music data,
* it's not a must have to store them, but, you can if you want.
*
* These kernels use the same variable addresses for their
* functions, so super easy to work with. But, because of this,
* only one should run at the same time (one per screen).
*
* Music_Pointer0 = $d1	; 16 bits
* Music_Pointer1 = $d3	; 16 bits
* Music_Duration0 = $d5
* Music_Duration1 = $d6 
***
* JukeBox_Controller = $d7 
* JukeBox_Music_Index = $d7 ; 0-2
* JukeBox_Wave_Index = $d7  ; 3-5
* JukeBox_Music_Duration0bit = $d7  ; 6
* JukeBox_Music_Duration1bit = $d7  ; 7
***
* Music_PointerBackUp0 = $d8	; 16 bits
* Music_PointerBackUp1 = $da	; 16 bits
*

#NAME#_JukeBox_Kernel

	ldx	item
	txs

	LDA	JukeBox_Controller
	AND	#%00111111
	CMP	#%00111111
	BEQ	#NAME#_JukeBox_Kernel_END
*
*	Check if there is wave to play!		
*	
	LSR
	AND	#%00011100
	CMP	#%00011100
	BEQ	#NAME#_JukeBox_NoWave
	TAY

	LDA	#<#NAME#_JukeBox_NoWave
	STA	temp01
	LDA	#>#NAME#_JukeBox_NoWave
	STA	temp02
*
*	The bank to jump back is set on the SubMenu 
*	address's 2-4th bits. (bank2 = 8)
*
*
	LDA	bankToJump
	AND	#%11100011
	ORA	#BANK_TO_JUMP
	STA	bankToJump
*
*	Get address for jumping and also bank to switch.
*
	LDA	#NAME#_PointerTable+2,y
	TAX	

*	lda	#NAME#_PointerTable,y
*   	pha
*   	lda	#NAME#_PointerTable+1,y
*   	pha
*   	pha
*   	pha
*   	jmp	bankSwitchJump

#NAME#_JukeBox_NoWave
*
*	Delete wave file (111), init save bits (00)
*	Save it to X so don't have to remove the last
*	bits again.
*
	LDA	JukeBox_Controller
	AND	#%00000111
	TAX
	ORA	#%00111000
*	
*	Check if new data will be read.
*
	LDA	Music_Duration0
	CMP	#1
	BNE	#NAME#_JukeBox_No_SAVE_6
	ORA	#%01000000
#NAME#_JukeBox_No_SAVE_6

	LDA	Music_Duration1
	CMP	#1
	BNE	#NAME#_JukeBox_No_SAVE_7
	ORA	#%10000000
#NAME#_JukeBox_No_SAVE_7
	STA 	JukeBox_Controller
	CMP	#%00111111
	BEQ	#NAME#_JukeBox_NoMusic
*
*	Same as the one with wave, but doesn't erase the music ID.
*	Multiply by 4 to get the proper starting index.
*
	TXA
	ASL
	ASL
	TAY
	
	LDA	#<#NAME#_JukeBox_NoMusic
	STA	temp01
	LDA	#>#NAME#_JukeBox_NoMusic
	STA	temp02

	LDA	bankToJump
	AND	#%11100011
	ORA	#BANK_TO_JUMP
	STA	bankToJump

	LDA	#NAME#_PointerTable+2,y
	TAX	

*	lda	#NAME#_PointerTable,y
*   	pha
*   	lda	#NAME#_PointerTable+1,y
*   	pha
*   	pha
*   	pha
*   	jmp	bankSwitchJump

#NAME#_JukeBox_NoMusic

	BIT	JukeBox_Controller
	BVC	#NAME#_JukeBox_NoSave0
	
	LDA	temp16
	STA	VAR01
	LDA	temp17
	STA	VAR02

#NAME#_JukeBox_NoSave0
	BIT	JukeBox_Controller
	BPL	#NAME#_JukeBox_NoSave1
	
	LDA	temp18
	STA	VAR03
	LDA	temp19
	STA	VAR04

#NAME#_JukeBox_NoSave1

	JMP	#NAME#_JukeBox_Kernel_END

!!!POINTERS!!!
#NAME#_JukeBox_Kernel_END
	tsx
	stx	item
