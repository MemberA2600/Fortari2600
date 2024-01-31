* params=variable|stringConst|number,variable|stringConst|number,variable|stringConst|number
* param1=#VAR01#,!!!to8bit1!!!
* param1=#VAR02#,!!!to8bit2!!!
* param1=#VAR03#,!!!to8bit3!!!
* direction=TO
*

	LDA	SubMenu
	ORA	#%01000000
	STA	SubMenu
