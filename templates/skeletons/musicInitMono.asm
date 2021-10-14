CoolSong_Init
	LDA	#1
	STA	CoolSong_Duration0

	LDA	#<CoolSong_Data0
	STA	CoolSong_Pointer0
	LDA	#>CoolSong_Data0
	STA	CoolSong_Pointer0+1
