bank1_Save_Collisions
*
*	Check if the ON/OFF bit is set. Also, if it is submenu mode.
*

	LDA	collisionVar1
	AND	#%00000001
	CMP	#%00000001
	BEQ	bank1_Save_Collisions_NoEnd

	LDA	#0
	STA	collisionVar1
	STA	collisionVar2	

	JMP	bank1_Save_Collisions_End_NoSave

bank1_Save_Collisions_NoEnd
	BIT 	SubMenu
	BVS	bank1_Save_Collisions_IsThe5thBitSet
	JMP	bank1_Save_Collisions_Start

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

	LDA	#%01000000
	STA	collisionVar1
	LDA	#0
	STA	collisionVar2
*
*	Do the loop :)
*	
	LDX	#8
	LDA	collisionVar2
bank1_Save_Collisions_TheLoop	
	STA	temp01
	LDA	CXM0P,x
	AND	#%11000000
	ORA	temp01
	STA	collisionVar2

	DEX

	LDA	collisionVar1
	STA	temp01
	LDA	CXM0P,x
	AND	#%11000000
	ORA	temp01	

	DEX
	BMI	bank1_Save_Collisions_End

	LSR
	LSR
	STA	collisionVar1	

	LDA	collisionVar2
	LSR
	LSR
	JMP	bank1_Save_Collisions_TheLoop

bank1_Save_Collisions_End_SomeWSYNC
	LDA	#0
	STA	collisionVar1
	STA	collisionVar2	

	LDX	#1
bank1_Save_Collisions_WSYNC_Wasting
	STA	WSYNC
	DEX
	BPL	bank1_Save_Collisions_WSYNC_Wasting

	JMP	bank1_Save_Collisions_End_NoSave

bank1_Save_Collisions_End
	STA	collisionVar2	

bank1_Save_Collisions_End_NoSave
