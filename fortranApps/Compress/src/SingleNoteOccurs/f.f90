module NoteModule

    type Note
        character(16), dimension(3) :: bytes
        integer :: occurence

    end type


end module


program hello
    use NoteModule

    implicit none

    integer :: io, alloc, num, num2, num3, num4, num5, fileLen, numOfNotes, last
    integer :: tempKey, tempMax, v1, v2, k
    character :: dummy
    character(:), allocatable :: tempPath
    character(16) :: readHere
    character(2) :: fileNum

    character(16), dimension(3) :: tempShit
    logical :: existing

    type(Note), dimension(:), allocatable :: notes
    character(16), dimension(:), allocatable :: bytes

    integer , dimension(:), allocatable :: occurences, keys

    tempPath = "temp/"

    fileLen = 0
    numOfNotes = 1

    open(unit = 12, file = tempPath // "Input.txt")

    do
       read(12, *, iostat = io) dummy
       if (io /= 0) exit
       fileLen = fileLen + 1

       if (dummy == "-") numOfNotes = numOfNotes + 1

    end do

    rewind(12)

    allocate(bytes(fileLen), stat = alloc)
    allocate(notes(numOfNotes), stat = alloc)
    allocate(occurences(numOfNotes), stat = alloc)
    allocate(keys(numOfNotes), stat = alloc)


    num2 = 1
    num3 = 1
    tempShit = "                "
    notes%occurence = 0
    notes(1)%bytes = "                "
    occurences = 0

    do num = 1, fileLen, 1
       read(12, "(A)") readHere

       bytes(num) = readHere
       if (readHere(1:1) == "-") then

            do num3 = 1, 3, 1
                notes(num2)%bytes(num3) = tempShit(num3)
            end do

            existing = .FALSE.
            if (num2 > 1) then
                do num3 = 1, num2-1, 1
                    do num4 = 1, 3, 1
                    if (notes(num3)%bytes(num4) /= notes(num2)%bytes(num4)) exit

                    if (num4 == 3) existing = .TRUE.
                end do

                end do

            end if

            if (existing .EQV. .FALSE.) num2 = num2 + 1

           num3 = 1
           notes(num2)%bytes = "                "
           tempShit = "                "
       else
           tempShit(num3) = readHere
           num3 = num3 + 1
       end if
    end do

    close(12)

    last = num2 - 1

    do num = 1, last, 1
       notes(num)%occurence = 0
       ! starting index
       do num2 = 1, fileLen-3, 1
          do num3 = 1, 3, 1
             if (notes(num)%bytes(num3) /=bytes(num2+num3)) exit

             if (num3 == 3) notes(num)%occurence = notes(num)%occurence + 1
          end do
       end do

       occurences(num) = notes(num)%occurence
       keys(num) = num
    end do

    do num = 1, last, 1
       tempMax = 0
       tempKey = 0
       k = 0
       do num2 = num, last, 1
          if (occurences(num2) > tempMax) then
              tempMax = occurences(num2)
              tempKey = keys(num2)
              k = num2
          end if

       end do

       v1 = occurences(num)
       v2 = keys(num)

       occurences(num) = tempMax
       keys(num)       = tempKey

       occurences(k)   = v1
       keys(k)         = v2
    end do

    if (last > 13) last = 13

    do num = 1, last, 1
       write(fileNum, "(I2)") num
       if (fileNum(1:1) == " ")  fileNum(1:1) = "0"

       num2 = keys(num)

       open(unit=12, file = tempPath // "Output" // fileNum // ".txt")
       do num3 = 1, 3, 1
          write(12,"(A)") notes(num2)%bytes(num3)

       end do
       close(12)
    end do


end program

