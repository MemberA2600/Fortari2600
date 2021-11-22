
module PatternModule

    type Pattern
        character(8), dimension(512) :: bytes
        integer :: length

    end type

    type Note
        character(8), dimension(3) :: bytes
        integer :: length

    end type

end module


program GetPatterns
    use PatternModule

    implicit none

    integer :: num, num2, num3, num4, io, alloc, fileLen, numOfNotes, last
    integer :: num5, num6

    character :: dummy
    character(:), allocatable :: tempPath

    character(16) :: readHere

    type(Note), dimension(:), allocatable :: notes
    type(Pattern), dimension(:), allocatable :: patterns

    integer, parameter :: constant = 48

    logical :: unique

    tempPath = "temp/"

    fileLen = 0
    numOfNotes = 1
    open(12, file = tempPath // "Input01.txt")
    do
        read(12, *, iostat = io) dummy
        if (io /= 0) exit

        fileLen = fileLen + 1
        if (dummy == "-") numOfNotes = numOfNotes + 1

    end do

    rewind(12)

    allocate(notes(numOfNotes), stat = alloc)
    allocate(patterns(constant ** 2), stat = alloc)

    num2 = 1
    num3 = 1

    notes(1)%length = 0
    notes(1)%bytes = "        "


    do num = 1, fileLen, 1
       read(12, "(A)") readHere

       if (readHere(1:3) == "---") then
           num2 = num2 + 1
           num3 = 1

           notes(num2)%length = 0
           notes(num2)%bytes = "        "
       else
           notes(num2)%bytes(num3) = readHere(9:16)
           notes(num2)%length      = num3
           num3                    = num3 + 1

       end if

    end do

    close(12)

    ! actual pattern
    num = 1

    ! byte position
    num5 = 1

    ! Number of notes joined
    do num2 = 2, constant, 1

       ! Number of Note at index 1
       do num3 = 1, size(notes)-num2, 1


          ! byte position
          num5 = 1

          patterns(num)%length = 0
          patterns(num)%bytes = "        "

          ! Actual note
          do num4 = 1, num2, 1

             do num6 = 1, notes(num4)%length, 1
                if (notes(num4+num3)%bytes(num6) == "        ") exit

                patterns(num)%bytes(num5) = notes(num4+num3)%bytes(num6)
                num5 = num5 + 1
                patterns(num)%length = num5-1
             end do

             if (num4 == num2) exit
             patterns(num)%bytes(num5) = "---     "
             num5 = num5 + 1
             patterns(num)%length = num5-1

          end do

          ! check if unique
          unique = .TRUE.

          if (num > 1) then
              do num4 = 1, num-1, 1
                 if (patterns(num4)%length /= patterns(num)%length) exit

                 do num5 = 1, patterns(num4)%length, 1
                    if (patterns(num4)%bytes(num5) /= patterns(num)%bytes(num5)) exit
                    if (num5 == patterns(num4)%length) unique = .FALSE.
                 end do

              end do
          end if

          if (unique .EQV. .TRUE.) num = num + 1

          if (num > size(patterns)) exit
       end do

    if (num > size(patterns)) exit
    end do

    last = num - 1

    open(unit=13, file=tempPath // "Output.txt")

    do num = 1, last, 1
       write(13, "(A, 1x, I0)") "***", patterns(num)%length
       do num2 = 1, patterns(num)%length, 1
          write(13, "(A)") patterns(num)%bytes(num2)
       end do

    end do

    close(13)

end program
