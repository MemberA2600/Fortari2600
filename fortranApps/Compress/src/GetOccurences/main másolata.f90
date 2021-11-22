module PatternModule

    type Pattern
        integer :: length, occurence, weight
        character(8), dimension(512) :: bytes

    end type

end module

module KeyWeightModule

    type keyWeight
        integer :: key, weight
    end type


end module

program GetOccurences

    use PatternModule
    use KeyWeightModule
    implicit none

    character(8), dimension(:), allocatable :: bytes
    character(:), allocatable :: tempPath, title
    character(1) :: dummy
    character(30) :: readHere
    character(4) :: nibble
    character(8), dimension(13) :: keyList

    integer :: alloc, alloc2, alloc3

    integer :: io, fileLen, numOfBytes, numOfNotes, numOfPatterns
    integer :: channelNum, generateNotes, maximum, temp
    integer :: first, last, byteCount, lastPattern
    integer :: tempMax, tempKey

    integer :: num, num2, num3, num4, starting, ending, num5

    type(Pattern), dimension(:), allocatable :: patterns
    type(keyWeight), dimension(:), allocatable :: keyWeights
    type(keyWeight) :: tempKeyWeight


    tempPath = "temp/"
    fileLen = 0

    open(unit = 11, file = tempPath // "Args.txt")
    read(11, *) channelNum, generateNotes, readHere

    title = trim(readHere)

    close(11)

    do num = 1, 13, 1
        write(nibble, "(b4)") num
        do num2 = 1, 4, 1
            if (nibble(num2:num2) == " ") nibble(num2:num2) = "0"
        end do
        keyList(num) = nibble // "0000"
    end do

    open(unit = 21, file = tempPath // "Input00.txt")

    do
        read(21, "(A)", iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do

    rewind(21)

    numOfPatterns = 0

    do num = 1, fileLen, 1
       read(21, "(A)") readHere

       if (readHere(1:3) == "***") numOfPatterns = numOfPatterns + 1
    end do

    allocate(patterns(numOfPatterns), stat = alloc)

    rewind(21)

    ! number of pattern
    num2 = 0


    do num = 1, fileLen, 1
       read(21, "(A)") readHere

       if (readHere(1:3) == "***") then
           num2 = num2 + 1

           ! location of byte
           num3 = 0

           read(readHere(4:30), *) patterns(num2)%length
           patterns(num2)%occurence = 0
           patterns(num2)%weight = 0

       else
           num3 = num3+1
           patterns(num2)%bytes(num3) = readHere(1:8)

       end if
    end do

    close(21)

    open(unit = 12, file = tempPath // "Input01.txt")
    fileLen = 0

    do
        read(12, "(A)", iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do

    rewind(12)

    allocate(bytes(fileLen), stat = alloc2)

    do num = 1, fileLen, 1
       read(12, "(A)") readHere
       if (readHere(1:3) == "---") then
           bytes(num) = "---     "
       else
           bytes(num) = readHere(9:17)
       end if

    end do

    close(12)

    open(13, file = tempPath // "Output.txt")

    do num = 1, size(patterns), 1
       do num2 = 1, fileLen - patterns(num)%length, 1
          do num3 = 1, patterns(num)%length, 1

             if (patterns(num)%bytes(num3) /= bytes(num2+num3)) exit
             if (num3 == patterns(num)%length) patterns(num)%occurence = patterns(num)%occurence + 1

          end do
       end do
       patterns(num)%weight = (patterns(num)%occurence ** 2) * patterns(num)%length

       write(13, "(I0, 1x ,I0)") num, patterns(num)%weight

    end do

    close(13)

end program

