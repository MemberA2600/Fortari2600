module PatternModule

    type Pattern
        integer :: length, occurence, weight
        character(8), dimension(512) :: bytes

    end type

end module

program GetOccurences

    use PatternModule
    use KeyWeightModule
    implicit none

    integer :: io, alloc, num, num2, num3, fileLen, numOfPatterns
    character :: dummy
    character(8), dimension(:), allocatable :: bytes
    character(:), allocatable :: tempPath
    character(16) :: readHere

    type(Pattern), dimension(:), allocatable :: patterns

    fileLen = 0
    tempPath = "temp/"

    open(unit = 12, file = tempPath // "Input01.txt")
    do
        read(12, *, iostat = io) dummy
        if (io /= 0) exit

        fileLen = fileLen + 1

    end do

    allocate(bytes(fileLen), stat = alloc)

    rewind(12)

    do num = 1, fileLen, 1

        read(12, "(A)") readHere
        if (readHere(1:1) == "-") then
            bytes(num) = "---     "
        else
            bytes(num) = readHere(9:16)

        end if

    end do
    close(12)

    fileLen = 0
    numOfPatterns = 0

    open(unit = 12, file = tempPath // "Input00.txt")
    do
        read(12, *, iostat = io) dummy
        if (io /= 0) exit
        if (dummy == "*") numOfPatterns = numOfPatterns + 1

        fileLen = fileLen + 1

    end do

    allocate(patterns(numOfPatterns), stat = alloc)
    rewind(12)

    num2 = 0
    num3 = 0

    do num = 1, fileLen, 1
       read(12, "(A)") readHere

       if (readHere(1:1) == "*") then
            num2 = num2 + 1
            read(readHere, *) dummy, patterns(num2)%length

            patterns(num2)%occurence = 0
            patterns(num2)%weight = 0
            patterns(num2)%bytes = "        "
            num3 = 1
       else
            patterns(num2)%bytes(num3) = readHere(1:8)
            num3 = num3 + 1

       end if
    end do

    numOfPatterns = num2


    open(unit = 12, file = tempPath // "Output.txt")

    do num = 1, numOfPatterns, 1
       patterns(num)%occurence = 0
       patterns(num)%weight = 0

       do num2 = 1, size(bytes)-patterns(num)%length, 1
          do num3 = 1, patterns(num)%length, 1

             if (patterns(num)%bytes(num3) /= bytes(num2+num3)) exit

             if (num3 /= patterns(num)%length) cycle

             patterns(num)%occurence = patterns(num)%occurence + 1

          end do
       end do
        if ( patterns(num)%occurence == 0) write(*,*) 'HOW?!'

       patterns(num)%weight = (patterns(num)%occurence **2 ) * patterns(num)%length
       write(12, "(I0, 1x, I0)") num, patterns(num)%weight

    end do
    close(12)

end program
