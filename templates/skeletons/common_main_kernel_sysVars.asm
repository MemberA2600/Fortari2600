frameColor = $#1#
			
*** Playfield Elements
pf0Pointer = $#2#		; 16 bits
pf1Pointer = $#2#		; 16 bits
pf2Pointer = $#2#		; 16 bits	
pfColorPointer = $#2#		; 16 bits 
bkColorPointer = $#2#		; 16 bits
bkBaseColor = $#1#
pfBaseColor = $#1#
pfIndex = $#1#

************************
SubMenu = $#1#		; 0-1 : SubMenuLines
NoGameMode = $#L#	; 2-4 : BankToJump
bankToJump = $#L#	; 5 : ScrollDirection
SubMenuLines = $#L#	; 6 : Go to SubMenu
ScrollDirection = $#L#	; 7 : No Game Mode
************************  

*** Player Settings
P0SpritePointer = $#2#		; 16bit
P0ColorPointer = $#2#		; 16bit
P1SpritePointer = $#2#		; 16bit
P1ColorPointer = $#2#		; 16bit

************
* Settings *
****************************************	
P0Settings = $#1#			; Bits 0-2 are sprite settings, 
P0Mirrored = $#L#			; 3 is reflection, bits 4-5 are missile settings. 
P0TurnOff  = $#L#			; 6: Turn Off Sprite
P1Settings = $#1#			; 7: Turn off Missile
P1Mirrored = $#L#			; Must be in order!
P1TurnOff  = $#L#
****************************************
pfSettings = $#1#	; Since CTRLPF 0-1 bits are fixed in the screen loop
pfEdges	= $#L#		; 0-1: free
BallTurnOff = $#L#	; 2: Players move behind the pf
#Has to be here because	; 3: Turn off Ball
#of the edge check	; 4-5: Ball Settings
#routine.		; 6-7: 00 - Nothing 01 - Mixed 10 - All stop 11 - All go through 		;
************************

P0Height = $#1#
P1Height = $#1#

****************************************
P0SpriteIndex = $#1#			; low nibble is P0 sprite index
P1SpriteIndex = $#L#			; high nibble is P1 sprite index
****************************************

*** Positions (Must be aligned!!)
P0Y = $#1#	
P1Y = $#1#	
M0Y = $#1#
M1Y = $#1#
BLY = $#1#

P0X = $#1#
P1X = $#1#
M0X = $#1#
M1X = $#1#
BLX = $#1#

*** Fake Missile Colors
M0Color = $#1#
M1Color = $#1#

*** TileScreen
TileSetPointer = $#2#	; 16 bit
TileScreenMainColor = $#1#

*** Matrix 6x4
Tile1_1 = $#1#
Tile1_2 = $#L#
Tile1_3 = $#1#
Tile1_4 = $#L#
Tile1_5 = $#1#
Tile1_6 = $#L#

Tile2_1 = $#1#
Tile2_2 = $#L#
Tile2_3 = $#1#
Tile2_4 = $#L#
Tile2_5 = $#1#
Tile2_6 = $#L#

Tile3_1 = $#1#
Tile3_2 = $#L#
Tile3_3 = $#1#
Tile3_4 = $#L#
Tile3_5 = $#1#
Tile3_6 = $#L#

Tile4_1 = $#1#
Tile4_2 = $#L#
Tile4_3 = $#1#
Tile4_4 = $#L#
Tile4_5 = $#1#
Tile4_6 = $#L#

TileColorPointer = $#2# 	; 16 bits

*******************
TileSelected = $#1#  ; 0-4th bit: Selected Tile (5 bits)
OverlapScreen = $#L# ; 5th bit: Have some part of the other screen
GrayScale     = $#L# ; 6th bit: GrayScale overlap
OverLapIndicator = $#L#
*******************
