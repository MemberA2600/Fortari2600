module PatternModule

    type Pattern
        character(8), dimension(255) :: bytes
        integer                      :: lenght, occurence, weight

    end type

    type PatternWeightKey
        integer :: num, weight
    end type
end module

program SuperCompress

    use PatternModule
    implicit none

    integer :: num, num2, alloc, io, fileLen, num3, num4, num5, num6, num7
    integer :: lastOne, tempNum, tempWeight, poz, w

    character(8), dimension(:), allocatable   :: bytes
    character                                 :: dummy

    character(8), dimension(255)              :: numbers
    logical                                   :: existing

    character(8)                              :: tempByte, secondByte

    type(Pattern), dimension(:), allocatable          :: patterns
    type(PatternWeightKey), dimension(:), allocatable :: pwk

    character(2) :: fileNum

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


    !last
    num7 = fileLen*10

    allocate(patterns(num7), stat = alloc)

    patterns%lenght    = 0
    patterns%occurence = 0
    patterns%weight    = 0

    ! patternIndex
    num3 = 1

    ! size
    do num = 3, fileLen, 1

       ! start index
       do num2 = 1, fileLen-num, 1

          ! copy bytes
          do num4 = 1, num, 1
             patterns(num3)%bytes(num4) = bytes(num2+num4)
          end do
          patterns(num3)%lenght = num

          existing = .FALSE.
          ! check existing, num5 = other pattern
          if (num3 > 1) then
              do num5 = 1, num3-1, 1
                 if (patterns(num3)%lenght /=patterns(num5)%lenght) cycle
                 do num6 = 1, patterns(num3)%lenght, 1
                    if (patterns(num3)%bytes(num6) /= patterns(num5)%bytes(num6)) exit
                    if (num6 == patterns(num3)%lenght) existing = .TRUE.
                 end do

              end do
          end if
          if (num2 > 1) then
              if (bytes(num2 - 1)(1:4) == "0000" ) existing = .TRUE.
          end if

          if (num2 + num4 < fileLen) then
              if (bytes(num2 + num4)(1:4) == "0000" ) existing = .TRUE.
          end if

          if (existing .EQV. .FALSE.) then
              num3 = num3 + 1
          end if
          if (num3 > num7) exit
       end do
       if (num3 > num7) exit
    end do

    lastOne = num3-1
    allocate(pwk(lastOne), stat = alloc)
    pwk%num    = 0
    pwk%weight = 0

    ! pattern num
    do num = 1, lastOne, 1
       ! start index
       do num2 = 1, fileLen-patterns(num)%lenght, 1

          do num3 = 1, patterns(num)%lenght, 1
             if (patterns(num)%bytes(num3) /= bytes(num2+num3)) exit

             if (num3 == patterns(num)%lenght) patterns(num)%occurence = patterns(num)%occurence + 1
          end do

       end do
       if (patterns(num)%occurence > 1) patterns(num)%weight = patterns(num)%occurence * patterns(num)%lenght
       pwk(num)%num    = num
       pwk(num)%weight = patterns(num)%weight

    end do


    ! get weight order

    do num = 1, lastOne-2, 1
       tempNum    = 0
       tempWeight = 0
       poz        = num
       w          = pwk(num)%weight

       do num2 = num+1, lastOne, 1
          if (pwk(num2)%weight > w) then
              poz = num2
              w   = pwk(num2)%weight
          end if
       end do

       if (poz == num) cycle
       if (w   == 0  ) exit
       tempNum          = pwk(poz)%num
       tempWeight       = pwk(poz)%weight

       pwk(poz)%num    = pwk(num)%num
       pwk(poz)%weight = pwk(num)%weight

       pwk(num)%num     = tempNum
       pwk(num)%weight  = tempWeight

    end do

    do num = 1, 13, 1
       write(fileNum, "(I2)") num-1
       if (fileNum(1:1) == " ") fileNum(1:1) = "0"

       open(unit = 13, file = "temp/Output" // fileNum // ".txt")
       do num2 = 1, patterns(pwk(num)%num)%lenght, 1
          if (pwk(num)%weight > 0) write(13, "(A)") patterns(pwk(num)%num)%bytes(num2)
       end do

       close(13)

    end do



end program
