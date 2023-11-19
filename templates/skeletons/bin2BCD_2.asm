    	asl
    	sta	#TEMP1#
    	lda	#0           		
#BANK#_bin2BCD_#MAGIC#_Loop
	BYTE	#$A2
#BANK#_bin2BCD_#MAGIC#_Loop_1
	BYTE	#$F8
*    	ldx	#$F8         		
    	sta	#TEMP2#
    	adc	#TEMP2#
    	rol	#TEMP1#
    	inx                 		
    	bne	#BANK#_bin2BCD_#MAGIC#_Loop_1 	
    	cld
	LDY	#TEMP1#