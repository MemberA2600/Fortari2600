
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
    integer :: tempMax, tempKey, counter

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

    allocate(bytes(fileLen), stat = alloc)

    do num = 1, fileLen, 1
       read(11, "(A)") readHere

       if (readHere(1:3) == "---") then
            bytes(num) = "---     "
            numOfNotes = numOfNotes + 1
       else
            bytes(num) = readHere(9:16)
            numOfBytes = numOfBytes + 1
       end if

    end do

    close(11)

    constant = floor(real(numOfNotes) / 16)
    if (constant < 16) constant = 16
    if (constant > 64) constant = 64

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

          starting = num3 - 1
          ending   = num3 + num2 - 1

          if (ending > numOfBytes - 1) ending = numOfBytes - 1

          ! current tempPattern byte

          tempPattern%bytes = "        "
          tempPattern%length = 0
          counter = 0

          do num4 = 1, fileLen, 1

             if (counter >=starting .AND. counter < ending) then
                 tempPattern%length = tempPattern%length + 1
                 tempPattern%bytes(tempPattern%length) = bytes(num4)
             end if

             if (bytes(num4)(1:3) == "---") counter = counter + 1

          end do

          if (tempPattern%bytes(tempPattern%length) == "---     ") tempPattern%length = tempPattern%length - 1
          existing = .FALSE.

          if (num > 1) then
              do num4 = 1, num-1, 1
                 if (patterns(num4)%length /= tempPattern%length) cycle

                 do num5 = 1, tempPattern%length, 1
                    if (patterns(num4)%bytes(num5) /= tempPattern%bytes(num5)) then
                        !write(*,"(I0, 1x, A8, 1x, A8)") num5, patterns(num4)%bytes(num5), tempPattern%bytes(num5)
                        exit
                    end if

                    if (num5 == tempPattern%length) existing = .TRUE.
                 end do
              end do
          end if

          if (existing .EQV. .FALSE.) then

              patterns(num)%length = tempPattern%length
              patterns(num)%bytes  = tempPattern%bytes

              if (patterns(num)%bytes(patterns(num)%length) == "---     ") patterns(num)%length = patterns(num)%length - 1

              num = num + 1
          end if

          if (num > maximum) exit
       end do

       if (num > maximum) exit

    end do

    lastPattern = num - 1

    open(unit=17, file = tempPath // "Output.txt")
    do num = 1, lastPattern, 1
       write(17,"(A, 1x, I0)") "***", patterns(num)%length

       do num2 = 1, patterns(num)%length, 1
          write(17,"(A, 1x, I0)") patterns(num)%bytes(num2)

       end do

    end do


    close(17)

end program
