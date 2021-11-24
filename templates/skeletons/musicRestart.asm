	LDA	#<CoolSong_Data@@
	STA	CoolSong_Pointer@@
	LDA	#>CoolSong_Data@@
	STA	CoolSong_Pointer@@+1
