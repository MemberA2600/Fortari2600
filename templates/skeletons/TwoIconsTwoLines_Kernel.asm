*
*	JumpBack Pointer: temp01 (+ temp02)
*	Color1		: temp03	
*	Color2		: temp04
*	SpriteData1	: temp05	
*	SpriteData2	: temp06
*			0: IsDouble
*			3: Mirrored
*			4-7: frameNum	
*
*	GradientPointer : temp07 (+ temp08)
*	sprite0_Pixels	: temp09 (+ temp10)
*	sprite0_Colors	: temp11 (+ temp12)
*	sprite1_Pixels	: temp13 (+ temp14)
*	sprite1_Color	: temp15 (+ temp16)
*	
*	PF1 and PF2 is set in the Toplevel section.
*	Since we don't have enough memory for both sprites,
*	we have to flicker them. If the spritedata is
*	just copied, there won't be any flicker at all.
*
*