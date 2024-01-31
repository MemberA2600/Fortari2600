* params=variable|stringConst|number,variable|stringConst|number
* param1=#VAR01#,!!!to8bit1!!!
* param1=#VAR02#,!!!to8bit2!!!
* direction=TO
*
	LDA	#VAR01#
!!!to8bit1!!!
	AND	#%00001111
	TAY

	LDA	#VAR02#
!!!to8bit2!!!
	CMP 	#25
	BCC	#BANK#_#MAGIC#_No24Load
	LDA	#24
#BANK#_#MAGIC#_No24Load
	SEC
	SBC	#1
	LSR
	TAX	


		