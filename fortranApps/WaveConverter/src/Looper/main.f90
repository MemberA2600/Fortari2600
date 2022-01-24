
program Looper
    implicit none

    integer :: num, num2, alloc, io, fileLen, origIndex, newIndex, eof, remainder, num3

    character(8), dimension(:), allocatable :: bytes, outBytes
    character                               :: dummy

    character(8), dimension(255)            :: numbers
    character(8), dimension(8)              :: bytes8
    logical                                 :: found

    character(8)                            :: tempByte, secondByte

    open(unit = 12, file = "temp/Input.txt")

    fileLen = 0

    do
        read(12, "(A)", iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do

    rewind(12)

    allocate(bytes(fileLen), stat = alloc)
    allocate(outBytes(fileLen), stat = alloc)

    do num = 1, fileLen, 1
        read(12, "(A)") bytes(num)
    end do

    close(12)

    outBytes = "        "

    eof = fileLen / 9
    remainder = fileLen - eof
    newIndex = 0

    do num = 1, eof, 9
       do num2 = 1, 9, 1
          if (num2 < 9) then
              bytes8(num2) = bytes(num+num2)
          else
              do num3 = 1, 8, 1
                 bytes8(num3)(1:1) = bytes(num+9)(num3:num3)
              end do
          end if
       end do
       do num2 = 1, 8, 1
          outBytes(num2+newIndex) = bytes8(num2)
       end do
       newIndex = newIndex + 8
    end do

    open(unit = 12, file = "temp/Output.txt")
    do num = 1, newIndex-1, 1
       write(12, "(A)") outBytes(num)
    end do

    do num = eof+1, fileLen, 1
        write(12, "(A)") bytes(num)
    end do
    close(12)


end program

