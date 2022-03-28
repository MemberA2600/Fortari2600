##NAME##_JumpToKernel
	
	LDA	#<##NAME##_JumpBack
	STA	temp01
	LDA	#>##NAME##_JumpBack
	STA	temp02

	JMP	##KERNEL_NAME##

##NAME##_JumpBack