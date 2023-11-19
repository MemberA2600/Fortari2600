*
* 	Original code made by OmegaMatrix!
* 	https://atariage.com/forums/topic/330847-binary-to-bcd/?tab=comments#comment-5000101
*
*	Modified to work with Fortari2600.
*	temp03 stores the hundreds temporary.
*
*	Jumpback:	temp01 (+ temp02)
*	A has the tens and ones, Y the hundreds! (A is also the input)
*
*	So temp01-temp04 are eliminated during the process.
*

#BANK#_bin2BCD
    	asl
    	sta	temp03
    	lda	#0           		; clear
#BANK#_bin2BCD_Loop
	BYTE	#$A2
#BANK#_bin2BCD_Loop_1
	BYTE	#$F8
*    	ldx	#$F8         		; SED = Opcode $F8
    	sta	temp04
    	adc	temp04
    	rol	temp03
    	inx                 		; Since we want to perform decimal mode, has to skip the first opcode 
    	bne	#BANK#_bin2BCD_Loop_1 	; and use the operand as opcode instead, nice solution!
    	cld
	LDY	temp03

	JMP	(temp01)