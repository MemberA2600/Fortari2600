* params=variable|register,variable|stringConst|number|register,variable|stringConst|number|register
* param1=#VAR01#,!!!from8bit!!!
* param2=#VAR02#,!!!to8bit1!!!
* param3=#VAR03#,!!!to8bit2!!!
* direction=FROM
*
	LDA	#VAR02#
!!!to8bit1!!!
	TAY

	LDA	#VAR03#
!!!to8bit2!!!
	TAX

	LDA	#BANK#_X_Values_#MAGIC#,x
	SEC
	SBC  	#BANK#_X_Values_#MAGIC#,y
!!!from8bit!!!
	STA	#VAR01#

*
* PlayerNumberSpacing_10000 0
* PlayerNumberSpacing_01000 1
* PlayerNumberSpacing_00100 2
* PlayerNumberSpacing_00010 3
* PlayerNumberSpacing_00001 4
* PlayerNumberSpacing_11000 5
* PlayerNumberSpacing_01100 6
* PlayerNumberSpacing_00110 7
* PlayerNumberSpacing_00011 8
* PlayerNumberSpacing_11100 9
* PlayerNumberSpacing_01110 10
* PlayerNumberSpacing_00111 11
* PlayerNumberSpacing_10100 12
* PlayerNumberSpacing_01010 13
* PlayerNumberSpacing_00101 14
* PlayerNumberSpacing_10001 15
* PlayerNumberSpacing_10101 16
*
* X_O_X_O_X_O_X_O_X
* 1 2 3 4 5 6 7 8 9
* 0 | | | | | | | |
*   8 | | | | | | |
*     16| | | | | |
*       24| | | | |
*         32| | | |
*           40| | |
*             48| | 
*               56|
*                 64

	JMP	#BANK#_Jump_Over_Table_#MAGIC#

#BANK#_X_Values_#MAGIC#
	BYTE	#0	; 0
	BYTE	#16	; 1
	BYTE	#32	; 2
	BYTE	#48	; 3
	BYTE	#64	; 4
	BYTE	#0	; 5
	BYTE	#16	; 6
	BYTE	#32	; 7
	BYTE	#48	; 8
	BYTE	#0	; 9
	BYTE	#16	; 10
	BYTE	#32	; 11
	BYTE	#0	; 12
	BYTE	#16	; 13
	BYTE	#32	; 14
	BYTE	#0	; 15
	BYTE	#0	; 16

#BANK#_Jump_Over_Table_#MAGIC#

	
