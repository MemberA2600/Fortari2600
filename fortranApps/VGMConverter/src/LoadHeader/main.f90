module HeaderDictModule

    implicit none

    type HeaderDict
        character(20), dimension(124) :: keys
        integer, dimension(124) :: starting, ending, lenght
        character(2), dimension(124,4) :: bytes
        character(8), dimension(124) :: byteString
        integer(8), dimension(124) :: values

        contains

        procedure :: processLines => processLines

    end type

    contains

    subroutine processLines(this, path, fileLen)
        class(HeaderDict), intent(inout) :: this
        integer, intent(in) :: fileLen
        integer :: num, num2, num3, starting, ending
        character(20) :: name
        character(:), allocatable :: path

        starting = 1
        num3 = 1

        open(12, file=path)

        do num = 1, fileLen, 1

            read(12, *) name, num2

            ending = starting + num2 - 1

            this%keys(num3) = name
            this%starting(num3) = starting
            this%ending(num3) = ending

            if (name /= "#") then
                num3 = num3 + 1
            end if
            !write(*,*) name, starting, ending

            starting = ending + 1
        end do

        close(12)

    end subroutine

end module

module HeaderModule

    implicit none

    type Header
        integer(kind = 8) :: EOF_Offset, File_Len, SN76489_Clock, YM2413_Clock
        integer(kind = 8) :: GD3_Offset, Total_Waits, Loop_Offset, Total_Loops
        integer(kind = 8) :: Rate
        integer :: Version, SN_FB
        integer(kind = 2) :: SNW, SF
        integer(kind=8) :: YM2612_Clock, YM2151_Clock, VGM_Data_Offset, Sega_PCM_Clock
        integer(kind=8) :: SPCM_Interface, RF5C68_Clock, YM2203_Clock, YM2608_Clock
        integer(kind=8) :: YM2610_B_Clock, YM3812_Clock, YM3526_Clock, Y8950_Clock
        integer(kind=8) :: YMF262_Clock, YMF278B_Clock, YMF271_Clock, YMZ280B_Clock
        integer(kind=8) :: RF5C164_Clock, PWM_Clock, AY8910_Clock
        integer(kind=2) :: AYT
        integer(kind=8) :: AY_Flags
        integer(kind=2) :: VM, LB, LM
        integer(kind=8) :: GB_DMG_Clock, NES_APU_Clock, MultiPCM_Clock, uPD7759_Clock, OKIM6258_Clock
        integer(kind=2) :: OF, KF, CF
        integer(kind=8) :: OKIM6295_Clock, K051649_Clock, K054539_Clock, HuC6280_Clock
        integer(kind=8) :: C140_Clock, K053260_Clock, Pokey_Clock, QSound_Clock
        integer(kind=8) :: SCSP_Clock, Extra_Header_Offset, WonderSwan_Clock, VSU_Clock
        integer(kind=8) :: SAA1099_Clock, ES5503_Clock, ES5506_Clock
        integer(kind=4) :: ES_CHNS, CD
        integer(kind=8) :: X1_10_Clock, C352_Clock, GA20_Clock

        logical :: T6W28bit
        integer(kind=8) :: Loop_Offset_REAL

        character :: tv_type

        contains

        procedure :: validate => validate

    end type
    contains

    subroutine validate(this)
        class(Header), intent(inout) :: this
        character(32) :: tempString

        write(tempString, "(b32)") this%SN76489_Clock

        this%T6W28bit = .TRUE.
        if (tempString(1:1) == "0" .OR. tempString(1:1) == " ") then
            this%T6W28bit = .FALSE.
        end if

        if (this%Loop_Offset /= 0) this%Loop_Offset_REAL = this%Loop_Offset + z'1C'
        if (this%Rate == 60) then
            this%tv_type = "N"
        else if (this%Rate == 50) then
            this%tv_type = "P"
        else
            this%tv_type = "U"
        end if

        if (this%Version <= 101 ) then
            if (this%SN76489_Clock /=0) then
                this%SN_FB = z'0009'
                this%SNW = 16

                this%YM2612_Clock = this%YM2413_Clock
                this%YM2151_Clock = this%YM2413_Clock

            end if
        end if

        if (this%Version <= 151) then
            this%SF = 0
        end if



    end subroutine


end module

program LoadHeader
    use HeaderDictModule
    use HeaderModule
    implicit none

    integer :: fileLen, io, alloc, num, num2, num3, cut
    character :: dummy
    character(25) :: line
    type(HeaderDict) :: headerD
    integer :: last
    character(:), allocatable :: path
    character(2) :: byte
    character(8) :: temp

    integer(kind=8) :: dummy2

    character(2), dimension(256) :: bytes
    type(Header) :: head

    fileLen = 0
    path = "config/VGMHeaderDict.txt"

    open(unit = 12, file = path)

    cut = 0

    do
        read(12, *, iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
        if (dummy == "#") cut = cut + 1
    end do

    close(12)

    call headerD%processLines(path, fileLen)

    close(12)
    last = fileLen - cut

    !do num = 1, last, 1
    !   write(*,*) headerD%keys(num), headerD%starting(num), headerD%ending(num)
    !end do

    path = "temp/Input.txt"
    fileLen = 256

    open(unit = 12, file = path)

    do num = 1, fileLen, 1
       read(12, "(A)") byte
       if (byte(2:2) == " ") byte = "0" // byte(1:1)

       bytes(num) = byte

    end do

    close(12)

    do num = 1, last, 1
       num3 = headerD%ending(num) - headerD%starting(num) + 1
       headerD%bytes(num, 1) = "  "
       headerD%bytes(num, 2) = "  "
       headerD%bytes(num, 3) = "  "
       headerD%bytes(num, 4) = "  "

       headerD%lenght(num) = num3
       do num2 = 1, num3, 1
            headerD%bytes(num, num2) = bytes(num2 + headerD%starting(num) - 1)
       end do

       temp = headerD%bytes(num, 4) // headerD%bytes(num, 3) // headerD%bytes(num, 2) // headerD%bytes(num, 1)
       do num2 = 1, 8, 1
          if (temp(num2:num2) == " ") temp(num2:num2) = "0"
       end do

       headerD%byteString(num) = temp

       read(temp, "(Z8)") headerD%values(num)

    end do

    !do num = 1, last, 1
    !   write(*,*) headerD%keys(num), headerD%bytes(num,1), headerD%bytes(num,2), &
    !   & headerD%bytes(num,3), headerD%bytes(num,4)
    !
    !end do

    ! Check if it is a valid VGM file.

    if (headerD%byteString(1) /= "206D6756" .AND. headerD%byteString(1) /= "206d6756") stop
    read(headerD%byteString(3), "(I8)") head%version

    head%EOF_Offset = headerD%values(2)
    head%File_Len = headerD%values(2) + 4
    head%SN76489_Clock = headerD%values(4)
    head%YM2413_Clock = headerD%values(5)
    head%GD3_Offset = headerD%values(6)
    head%Total_Waits = headerD%values(7)
    head%Loop_Offset = headerD%values(8)
    head%Total_Loops  = headerD%values(9)
    head%Rate  = headerD%values(10)
    head%SN_FB = headerD%values(11)
    head%SNW  = headerD%values(12)
    head%SF  = headerD%values(13)
    head%YM2612_Clock = headerD%values(14)
    head%YM2151_Clock = headerD%values(15)
    head%VGM_Data_Offset = headerD%values(16)
    head%Sega_PCM_Clock = headerD%values(17)
    head%SPCM_Interface = headerD%values(18)
    head%RF5C68_Clock = headerD%values(19)
    head%YM2203_Clock = headerD%values(20)
    head%YM2608_Clock = headerD%values(21)
    head%YM2610_B_Clock = headerD%values(22)
    head%YM3812_Clock = headerD%values(23)
    head%YM3526_Clock = headerD%values(24)
    head%Y8950_Clock = headerD%values(25)
    head%YMF262_Clock = headerD%values(26)
    head%YMF278B_Clock = headerD%values(27)
    head%YMF271_Clock = headerD%values(28)
    head%YMZ280B_Clock = headerD%values(29)
    head%RF5C164_Clock = headerD%values(30)
    head%PWM_Clock = headerD%values(31)
    head%AY8910_Clock = headerD%values(32)
    head%AYT = headerD%values(33)
    head%AY_Flags = headerD%values(34)
    head%VM = headerD%values(35)
    head%LB = headerD%values(36)
    head%LM = headerD%values(37)
    head%GB_DMG_Clock = headerD%values(38)
    head%NES_APU_Clock = headerD%values(39)
    head%MultiPCM_Clock = headerD%values(40)
    head%uPD7759_Clock = headerD%values(41)
    head%OKIM6258_Clock = headerD%values(42)
    head%OF = headerD%values(43)
    head%KF = headerD%values(44)
    head%CF = headerD%values(45)
    head%OKIM6295_Clock = headerD%values(46)
    head%K051649_Clock = headerD%values(47)
    head%K054539_Clock = headerD%values(48)
    head%HuC6280_Clock = headerD%values(49)
    head%C140_Clock = headerD%values(50)
    head%K053260_Clock = headerD%values(51)
    head%Pokey_Clock = headerD%values(52)
    head%QSound_Clock = headerD%values(53)
    head%SCSP_Clock = headerD%values(54)
    head%Extra_Header_Offset = headerD%values(55)
    head%WonderSwan_Clock = headerD%values(56)
    head%VSU_Clock = headerD%values(57)
    head%SAA1099_Clock = headerD%values(58)
    head%ES5503_Clock = headerD%values(59)
    head%ES5506_Clock = headerD%values(60)
    head%ES_CHNS = headerD%values(61)
    head%CD = headerD%values(62)
    head%X1_10_Clock = headerD%values(63)
    head%C352_Clock = headerD%values(64)
    head%GA20_Clock = headerD%values(65)

    call head%validate()

end program
