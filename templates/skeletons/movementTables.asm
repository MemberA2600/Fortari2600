#BANK#_MovementTables
*
* Since there can be double and triple players and missiles,  
* sometimes X have to be checked 3 times!
*
* Nusiz:
* 00: Single
* 01: Double, 8 pixels gap
* 02: Double, 24 pixels gap 
* 03: Triple, 8 pixels gaps
* 04: Double, 56 pixes gap
* 05: Single, but double-sized
* 06: Triple, 24 pixels gaps
* 07: Single, but quad-sized
*
*	 X|X|X|X|X
*

	_align 8
*
*	cHECKS - 1
*
#BANK#_Number_Of_Checks 
	BYTE	#0
	BYTE	#1
	BYTE	#1
	BYTE	#2
	BYTE	#1
	BYTE	#0
	BYTE	#2
	BYTE	#0
*
*	Since there can be 3 of these, groups are based on the nusiz value,
*	while the inside order is based on the number of checks
*

	_align 24

#BANK#_X_Center_Adders_On_NUSIZ_For_Player
	BYTE	#4
	BYTe	#0
	BYTE	#0

	BYTE	#4
	BYTE	#20
	BYTE	#0

	BYTE	#4
	BYTE	#36
	BYTE	#0

	BYTE	#4
	BYTE	#20
	BYTE	#36

	BYTE	#4
	BYTE	#68
	BYTE	#0

	BYTE	#8
	BYTE	#0
	BYTE	#0
	
	BYTE	#4
	BYTe	#36
	BYTE	#68

	BYTE	#16
	BYTE	#0
	BYTE	#0

	_align	24
*
*	Groups are basically the same as with the player. Some are the same,
*	since NUSIZ won't fetch the missile.
*

#BANK#_X_Poz_X_On_NUSIZ_For_Missile
	BYTE 	#0
	BYTE 	#0
	BYTE 	#0

	BYTE 	#0
	BYTE 	#16
	BYTE 	#0

	BYTE 	#0
	BYTE 	#32
	BYTE 	#0

	BYTE 	#0
	BYTE 	#16
	BYTE 	#32

	BYTE 	#0
	BYTE 	#64
	BYTE 	#0
	
	BYTE 	#0
	BYTE 	#0
	BYTE 	#0

	BYTE 	#0
	BYTE 	#32
	BYTE 	#64

	BYTE 	#0
	BYTE 	#0
	BYTE 	#0

	_align	4

#BANK#_X_Center_Added_For_Missile
	BYTE	#0
	BYTE	#1
	BYTE	#2
	BYTE	#4
