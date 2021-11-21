module KeyWeightModule

    type KeyWeight
        integer :: key, weight
    end type

end module

program SortWeights
    use KeyWeightModule

    implicit none

    integer :: io, alloc, fileLen, num, num2, tempMax, trueLen, tempKey, theVal, num3, v1, v2
    type(KeyWeight), dimension(:), allocatable :: keyWeights
    type(KeyWeight), dimension(13) :: outKeys

    character(1) :: dummy
    character(:), allocatable :: tempPath

    logical :: existing
    integer, dimension(:), allocatable :: numbers

    fileLen = 0
    tempPath = "temp/"

    open(unit = 11, file = tempPath // "Input.txt")
    do
        read(11, *, iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1

    end do
    rewind(11)

    allocate(keyWeights(fileLen), stat = alloc)
    allocate(numbers(fileLen), stat = alloc)


    trueLen = 1
    numbers = 0

    do num = 1, fileLen, 1
        read(11, *) keyWeights(trueLen)%key, keyWeights(trueLen)%weight
        if (keyWeights(trueLen)%key == 0 .OR. keyWeights(trueLen)%weight == 0) cycle

        numbers(trueLen) = keyWeights(trueLen)%weight
        trueLen = trueLen + 1

    end do
    close(11)

    do num = 1, trueLen, 1
       tempMax = 0
       tempKey = 0
       v1 = 0
       v2 = 0
       do num2 = num, trueLen, 1
          if (numbers(num2) > tempMax) then
              v1 = tempMax
              v2 = tempKey
              tempMax = numbers(num2)
              tempKey = num2
          end if

          existing = .FALSE.
          if (num > 1) then
              do num3 = 1, num, 1
                 if (numbers(num3) == tempMax) then
                    existing = .TRUE.
                    exit
                 end if
              end do
          end if

          if (existing .EQV. .TRUE.) then
              tempMax = v1
              tempKey = v2
              numbers(num2) = 0

          end if
       end do

       theVal = numbers(num)
       numbers(num) = numbers(tempKey)
       numbers(tempKey) = theVal

    end do

    outKeys%key = 0
    outKeys%weight = 0

    num3 = 1

    do num = 1, trueLen, 1

       do num2 = 1, trueLen, 1
          if (keyWeights(num2)%weight == numbers(num)) then

              outKeys(num3)%key    = keyWeights(num2)%key
              outKeys(num3)%weight = keyWeights(num2)%weight

              num3 = num3 + 1
              if (num3 > 13) exit

          end if
          if (num3 > 13) exit

       end do
       if (num3 > 13) exit

    end do

    open(unit=14, file= tempPath // "Output.txt")
    do num = 1, 13, 1
       write(14, "(I0, 1x, I0)") outKeys(num)%key, outKeys(num)%weight

    end do
    close(14)

end program

