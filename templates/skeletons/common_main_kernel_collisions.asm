bank1_Save_Collisions
*
*	Check if the ON/OFF bit is set. Also, if it is submenu mode.
*

	BIT 	SubMenu
	BVS	bank1_Save_Collisions_IsThe5thBitSet

	LDA	collisionVar1
	AND	#%00000001
	CMP	#%00000001
	BEQ	bank1_Save_Collisions_Start
	JMP	bank1_Save_Collisions_End_NoSave

bank1_Save_Collisions_IsThe5thBitSet
*
*	If submenu has overlap, must do some wsync waste.
*
	LDA	OverlapScreen
	AND	#%00100000
	CMP	#%00100000	
	BEQ	bank1_Save_Collisions_End_SomeWSYNC
	JMP	bank1_Save_Collisions_End_NoSave

bank1_Save_Collisions_Start
*
*	Init the variables.
*

	LDA	#$86
	STA	COLUBK

	LDA	#%01000000
	STA	collisionVar1
	LDA	#0
	STA	collisionVar2
*
*	Do the loop :)
*	
	LDX	#3
	LDA	collisionVar1
bank1_Save_Collisions_TheLoop	
	ORA	CXM0P,x
	STA	collisionVar1

	LDA	collisionVar2
	ORA	CXM1P,x

	DEX
	BMI	bank1_Save_Collisions_End

	LSR
	LSR
	STA	collisionVar2	

	LDA	collisionVar1
	LSR
	LSR
	JMP	bank1_Save_Collisions_TheLoop

bank1_Save_Collisions_End_SomeWSYNC
	LDA	#$18
	STA	COLUBK	

	LDX	#3
bank1_Save_Collisions_WSYNC_Wasting
	STA	WSYNC
	DEX
	BPL	bank1_Save_Collisions_WSYNC_Wasting

	JMP	bank1_Save_Collisions_End_NoSave

bank1_Save_Collisions_End
	STA	collisionVar2	

bank1_Save_Collisions_End_NoSave

	LDA	#$00
	STA	COLUBK