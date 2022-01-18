program Compress

    implicit none

    integer :: num, num2, alloc, io, fileLen, origIndex, newIndex, diff, fuck

    character(8), dimension(:), allocatable :: bytes, outBytes
    character                               :: dummy

    character(8), dimension(255)            :: numbers
    logical, dimension(255)                 :: found

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

    outBytes = "00000000"

    origIndex = 1
    newIndex  = 1

    do
        if (origIndex > fileLen) exit
        tempByte = bytes(origIndex)

        do num = origIndex, fileLen, 1
           if (bytes(num) /= tempByte) exit
        end do

        if (num-origIndex < 3) then
            do num2 = origIndex, num-1, 1
               outBytes(newIndex) = bytes(num2)
               newIndex = newIndex + 1
            end do
        else
            diff = num-origIndex-1
            do while (diff > 0)
               outBytes(newIndex) = tempByte
               if (diff < 16) then
                    write(secondByte, "(B8)") diff
                    do num2 = 1, 8, 1
                        if (secondByte(num2:num2) == " ") secondByte(num2:num2) = "0"
                    end do
                    outBytes(newIndex+1) = secondByte
                    newIndex = newIndex + 2
                    diff = 0
                else
                    outBytes(newIndex+1) = "11111111"
                    newIndex = newIndex + 2
                    diff = diff - 15

               end if
            end do

        end if
        origIndex = num

    end do

    open(unit = 13, file = "temp/Output.txt")

    do num = 1, fileLen, 1
       if (outBytes(num) == "00000000") exit
       write(13, "(A)") outBytes(num)
    end do
    close(13)

end program

