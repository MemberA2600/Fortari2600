
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


program GetPatterns
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

    integer :: io, fileLen, numOfBytes, numOfNotes
    integer :: channelNum, generateNotes, maximum, temp
    integer :: first, last, byteCount, lastPattern
    integer :: tempMax, tempKey

    real :: constant
    integer :: num, num2, num3, num4, starting, ending, num5

    logical :: existing

    type(Pattern), dimension(:), allocatable :: patterns
    type(Pattern) :: tempPattern
    type(keyWeight), dimension(:), allocatable :: keyWeights
    type(keyWeight) :: tempKeyWeight


    tempPath = "temp/"
    fileLen = 0
    numOfBytes = 0
    numOfNotes = 1

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

    open(unit = 11, file = tempPath // "Input01.txt")

    do
        read(11, *, iostat=io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do
    rewind(11)

    allocate(bytes(fileLen+1), stat = alloc)

    do num = 1, fileLen, 1
       read(11, "(A)") readHere

       if (readHere(1:3) == "---") then
            bytes(num) = "---"
            numOfNotes = numOfNotes + 1
       else
            bytes(num) = readHere(9:16)
            numOfBytes = numOfBytes + 1
       end if

    end do

    close(11)

    bytes(num+1) = "???"
    constant = floor(real(numOfNotes) / 128)
    if (constant < 16) constant = 16

    maximum = (constant ** 2)

    allocate(patterns(maximum), stat = alloc2)

    ! currentPattern
    num = 1

    do num2 = 1, maximum, 1
        patterns(num2)%bytes = "        "
        patterns(num2)%length = 0
        patterns(num2)%weight = 0
        patterns(num2)%occurence = 0

    end do

    ! number of notes in pattern
    do num2 = 2, constant, 1

       ! get starting position
       do num3 = 1, numOfNotes - num2, 1

          starting = num3
          ending   = num3 + num2

          temp = 0
          tempPattern%bytes = "        "
          tempPattern%length = 0
          byteCount = 0

          if (starting == 1) first = 1

          do num4 = 1, size(bytes), 1
             if (bytes(num4) == "---") then
                 temp = temp + 1
                 if (starting == temp) then
                     first = num4 + 1
                 else if (ending == temp) then
                     last = num4 - 1
                 end if
             else if (bytes(num4) == "???") then
                 last = num4 - 1
             end if
          end do

          tempPattern%length = last-first+1
          do num4 = first, last, 1

             if (bytes(num4) == "???") exit
             if (bytes(num4) /= "---") byteCount = byteCount + 1

             tempPattern%bytes(num4-first+1) = bytes(num4)

          end do


          existing = .FALSE.

          if (num > 1) then
              do num4 = 1, num, 1
                 if (patterns(num4)%length /= tempPattern%length) cycle

                 do num5 = 1, tempPattern%length, 1
                    if (patterns(num4)%bytes(num5) /= tempPattern%bytes(num5)) exit

                    if (num5 == tempPattern%length) existing = .TRUE.
                 end do
              end do
          end if

          if (existing .EQV. .FALSE.) then

              patterns(num)%length = tempPattern%length
              patterns(num)%bytes  = tempPattern%bytes

              num = num + 1
          end if
          if (num > maximum) exit

       end do
    if (num > maximum) exit
    end do

    lastPattern = num-1

    allocate(keyWeights(lastPattern), stat = alloc3)

    keyWeights%key = 0
    keyWeights%weight = 0

    do num = 1, lastPattern, 1
        patterns(num)%occurence = 0
        do num2 = 1, size(bytes)-patterns(num)%length, 1
           do num3 = 1, patterns(num)%length, 1
              if (patterns(num)%bytes(num3) /= bytes(num3+num2)) exit

              if (num3 == patterns(num)%length) &
              & patterns(num)%occurence = patterns(num)%occurence + 1

           end do
        end do
        patterns(num)%weight = patterns(num)%occurence * patterns(num)%length
        keyWeights(num)%key = num
        keyWeights(num)%weight = patterns(num)%weight

    end do

    do num = 1, lastPattern, 1
       tempMax = 0
       tempKey = 0

       do num2 = num, lastPattern, 1
          if (keyWeights(num2)%weight > tempMax) then
             tempMax = keyWeights(num2)%weight
             tempKey = num2
          end if
       end do

       tempKeyWeight = keyWeights(num)
       keyWeights(num) = keyWeights(tempKey)
       keyWeights(tempKey) = tempKeyWeight

    end do


    open(unit = 17, file = tempPath // "Output00.txt")

    do num = 1, 13, 1
       write(dummy, "(I1)") channelNum
       write(17, "(A)") title // "_Channel" // dummy // "_" // keyList(num)

       do num2 = 1, patterns(keyWeights(num)%key)%length, 1
          if (patterns(keyWeights(num)%key)%bytes(num2) /= "---") write(17,"(A)") patterns(keyWeights(num)%key)%bytes(num2)
       end do
       write(17, "(A)") "11100000"
       write(17, "(A)") ""
    end do
    close(17)



end program
