*
*	Particles
*
	JMP 	#NAME#_Fire_Particles_MiniKernel

	align	256
#NAME#_Fire_FineAdjustTable_256
	fill	49

#NAME#_Fire_Particles_MiniKernel
	LDA	#NAME#_Fire_Color
	AND	#%11110000
	STA	temp17
	LDA	#VAR01#	
	AND	#%00001111
	STA	temp16
	LSR
	LSR
	AND	#%11111110	
	CMP	#0
	BEQ	#NAME#_Fire_SaveColor
	LDA	temp16
	AND	#%11111110
	SEC
	SBC	#8
	ORA 	temp17

	
#NAME#_Fire_SaveColor
	STA	COLUP0
	STA	COLUP1

	
	LDA	##HEIGHT#
	STA	temp12

	LDA	counter
	AND	#%00001111
	TAY

	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%01111111
	STA	temp14
	
	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%10000000
	ROL
	ROL
	ORA	#%00000100
	STA	NUSIZ0

#NAME#_Fire_ParticleLoop_0
	sta	WSYNC
	LDA	#0
	STA	ENAM0
#NAME#_Fire_ParticleLoop_0	
	lda	$008f	; Force to read temp14 in 4 cycles
#NAME#_Fire_ParticleLoop_DivideLoop_0
	sbc	#15
   	bcs	#NAME#_Fire_ParticleLoop_DivideLoop_0
   	TAX	
	sleep	3
   	sta	RESM0
	LDA	#NAME#_Fire_FineAdjustTable_256,x
	STA	HMM0
	
	STA	WSYNC
	STA	HMOVE

	LDA	#2
	STA	ENAM0

	INY
	TYA
	AND	#%00001111
	TAY

	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%01111111
	STA	temp14
	
	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%10000000
	ROL
	ROL
	ORA	#%00000100
	STA	NUSIZ1

#NAME#_Fire_ParticleLoop_1
	sta	WSYNC
	LDA	#0
	STA	ENAM1
#NAME#_Fire_ParticleLoop_1	
	lda	$008f	; Force to read temp14 in 4 cycles
#NAME#_Fire_ParticleLoop_DivideLoop_1
	sbc	#15
   	bcs	#NAME#_Fire_ParticleLoop_DivideLoop_1
   	TAX	
	sleep	3
   	sta	RESM1
	LDA	#NAME#_Fire_FineAdjustTable_256,x
	STA	HMM1
	
	STA	WSYNC
	STA	HMOVE

	LDA	#2
	STA	ENAM1

	INY
	TYA
	AND	#%00001111
	TAY

	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%01111111
	STA	temp14
	
	LDA	#NAME#_Fire_Particle_Data,y
	AND	#%10000000
	ROL
	ROL
	STA	NUSIZ0

	DEC	temp12
	BMI	#NAME#_Fire_Particle_End
	JMP	#NAME#_Fire_ParticleLoop_0
#NAME#_Fire_Particle_End
	STA	WSYNC
	LDA	#0
	STA	ENAM0
	STA	ENAM1

	JMP	#NAME#_Fire_Flames

#NAME#_Fire_Particle_Data
	BYTE	#87
	BYTE	#212
	BYTE	#43
	BYTE	#119
	BYTE	#157
	BYTE	#55
	BYTE	#243
	BYTE	#67
	BYTE	#196
	BYTE	#48
	BYTE	#115
	BYTE	#95
	BYTE	#177
	BYTE	#36
	BYTE	#74
#NAME#_Fire_FineAdjustTable
	byte	#$80
	byte	#$70
	byte	#$60
	byte	#$50
	byte	#$40
	byte	#$30
	byte	#$20
	byte	#$10
	byte	#$00
	byte	#$f0
	byte	#$e0
	byte	#$d0
	byte	#$c0
	byte	#$b0
	byte	#$a0
	byte	#$90