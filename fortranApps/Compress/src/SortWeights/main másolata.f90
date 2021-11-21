module KeyWeightModule

    type KeyWeight
        integer :: key, weight
    end type

end module

program SortWeights
    use KeyWeightModule

    implicit none

    integer :: io, alloc, fileLen, num, num2, tempMax, tempKey, v1, v2, trueLen
    type(KeyWeight), dimension(:), allocatable :: keyWeights
    character(1) :: dummy
    character(:), allocatable :: tempPath

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

    trueLen = 1
    do num = 1, fileLen, 1
        read(11, *) keyWeights(trueLen)%key, keyWeights(trueLen)%weight
        if (keyWeights(trueLen)%key == 0 .OR. keyWeights(trueLen)%weight == 0) cycle
        trueLen = trueLen + 1

    end do
    close(11)

    do num = 1, trueLen, 1
       tempKey = 0
       tempMax = 0
       do num2 = num, trueLen, 1
          if (keyWeights(num2)%weight > tempMax) then
             tempKey = num2
             tempMax = keyWeights(num2)%weight

          end if
       end do

       v1 = keyWeights(num)%key
       v2 = keyWeights(num)%weight

       keyWeights(num)%key    = tempKey
       keyWeights(num)%weight = tempMax

       keyWeights(tempKey)%key    = v1
       keyWeights(tempKey)%weight = v2

    end do



end program

