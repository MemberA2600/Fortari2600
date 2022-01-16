program GetKeys

    implicit none

    integer :: num, num2, num3, num4, alloc, io, fileLen

    character(8), dimension(:), allocatable :: bytes
    character                               :: dummy

    character(8), dimension(255)            :: numbers
    logical, dimension(255)                 :: found

    character(8)                            :: tempByte

    open(unit = 12, file = "temp/Input.txt")

    fileLen = 0

    do
        read(12, "(A)", iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do

    rewind(12)

    allocate(bytes(fileLen), stat = alloc)

    do num = 1, fileLen, 1
        read(12, "(A)") bytes(num)
    end do

    close(12)

    open(unit=13, file="temp/Output.txt")

    do num = 0, 255, 1
       write(tempByte, "(B8)") num
       do num2 = 1, 8, 1
           if (tempByte(num2:num2) == " ") tempByte(num2:num2) = "0"
       end do

       numbers(num+1)                     = tempByte

       found(num+1) = .FALSE.

       do num2 = 1, fileLen, 1
          if (bytes(num2) == tempByte) then
              found(num + 1) = .TRUE.
              exit
          end if
       end do
       if (found(num+1) .EQV. .FALSE.) write(13, "(A)") tempByte

    end do

    close(13)

end program

