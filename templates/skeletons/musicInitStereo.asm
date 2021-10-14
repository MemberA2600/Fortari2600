CoolSong_Init
	LDA	#1
	STA	CoolSong_Duration0
	STA	CoolSong_Duration1

	LDA	#<CoolSong_Data0
	STA	CoolSong_Pointer0
	LDA	#>CoolSong_Data0
	STA	CoolSong_Pointer0+1

	LDA	#<CoolSong_Data1
	STA	CoolSong_Pointer1
	LDA	#>CoolSong_Data1
	STA	CoolSong_Pointer1+1