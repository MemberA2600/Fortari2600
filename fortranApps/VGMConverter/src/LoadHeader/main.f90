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

        logical :: T6W28bit, YM2610B_Bit, AY8910_Legacy, AY8910_Single, AY8910_Discrete, AY8910_RAW
        logical :: FDS_Addon, K054539_Stereo, K054539_NoReverb, K054539_UpdateKeyOn, ES5506bit
        integer(kind=8) :: Loop_Offset_REAL, VGM_Data_Absolute_Offset, Number_Of_Loops
        integer(kind=8) :: Extra_Header_Absolute_Offset
        integer:: OKIM6258_Clock_Divider, OKIM6258_ADPCM, OKIM6258_Output_Bit
        character :: tv_type
        character(6) :: AY_Type
        character(30) :: C140_ChipType
        real :: volume

        contains

        procedure :: validate => validate

    end type
    contains

    subroutine validate(this)
        class(Header), intent(inout) :: this
        character(32) :: tempString
        integer :: num, num2, num3

        write(tempString, "(b32)") this%SN76489_Clock

        this%T6W28bit = .TRUE.
        if (tempString(1:1) == "0" .OR. tempString(1:1) == " ") then
            this%T6W28bit = .FALSE.
        end if

        tempString(1:1) = "0"
        read(tempString, "(b32)") this%SN76489_Clock

        write(tempString, "(b32)") this%YM2610_B_Clock

        this%YM2610B_Bit = .TRUE.
        if (tempString(1:1) == "0" .OR. tempString(1:1) == " ") then
            this%YM2610B_Bit = .FALSE.
        end if

        tempString(1:1) = "0"
        read(tempString, "(b32)") this%YM2610_B_Clock

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
                this%YM2612_Clock = this%YM2413_Clock
                this%YM2151_Clock = this%YM2413_Clock

            end if
        end if

        this%VGM_Data_Absolute_Offset = this%VGM_Data_Offset + 52

        if (this%Version < 150) then
            this%VGM_Data_Absolute_Offset = z'40'
        end if

        if (this%Version <= 151) then
            this%SF = 0
        end if

        if (this%AY8910_Clock /= 0) then
            select case(this%AYT)
                case(z'0')
                    this%AY_Type = "AY8910"
                case(z'1')
                    this%AY_Type = "AY8912"
                case(z'2')
                    this%AY_Type = "AY8913"
                case(z'3')
                    this%AY_Type = "AY8930"
                case(z'10')
                    this%AY_Type = "YM2149"
                case(z'11')
                    this%AY_Type = "YM3439"
                case(z'12')
                    this%AY_Type = "YMZ284"
                case(z'13')
                    this%AY_Type = "YMZ294"
                case default
                    this%AY_Type = "      "
            end select
        else
            this%AY_Type = "      "
        end if

        write(tempString, "(b32)") this%AY_Flags

        this%AY8910_Legacy = .FALSE.
        this%AY8910_Single = .FALSE.
        this%AY8910_Discrete = .FALSE.
        this%AY8910_RAW = .FALSE.

        if (tempString(32:32) == "1") then
            this%AY8910_Legacy = .TRUE.
        end if
        if (tempString(31:31) == "1") then
            this%AY8910_Single = .TRUE.
        end if
        if (tempString(30:30) == "1") then
            this%AY8910_Discrete = .TRUE.
        end if
        if (tempString(29:29) == "1") then
            this%AY8910_RAW = .TRUE.
        end if

        if (this%Version > 149) then
            ! Volume = 2^(num / 32)
            if (this%VM < 193) then
                num = this%VM
            else
                num = (255 - this%VM) * -1
                if (num == -63) num = -64
            end if

            num = -64
            this%volume = real(2)**(floor(real(num)/32.0))
        end if

        ! Should allow loop overwrite for the converter!
        this%Number_Of_Loops = 0

        if (this%Version > 150) then
            if (this%LM == 0) this%LM = 16
            this%Number_Of_Loops = floor(real(this%LM) / 16.0)
        end if

        if (this%Version > 160) then
            if (this%LB > 127) then
                this%LB = (256-this%LB) * - 1
            end if
            this%Number_Of_Loops = this%Number_Of_Loops - this%LB
        end if


        this%FDS_Addon = .FALSE.
        if (this%NES_APU_Clock /=0) then
            write(tempString, "(b32)") this%NES_APU_Clock

            if (tempString(1:1) == "1") this%FDS_Addon = .TRUE.

            tempString(1:1) = "0"
            read(tempString, "(b32)") this%NES_APU_Clock

        end if

        this%OKIM6258_Clock_Divider = 0
        this%OKIM6258_ADPCM = 0
        this%OKIM6258_Output_Bit = 0

        if (this%OKIM6258_Clock /= 0) then
            write(tempString, "(b32)") this%OF
            read(tempString(31:32), "(b2)") num

            select case(num)
                case (0)
                    this%OKIM6258_Clock_Divider = 1024
                case (1)
                    this%OKIM6258_Clock_Divider = 768
                case (2)
                    this%OKIM6258_Clock_Divider = 512
                case (3)
                    this%OKIM6258_Clock_Divider = 512
            end select

            if (tempString(30:30) == "1") then
                this%OKIM6258_ADPCM = 4
            else
                this%OKIM6258_ADPCM = 3
            end if

            if (tempString(29:29) == "1") then
                this%OKIM6258_Output_Bit = 10
            else
                this%OKIM6258_Output_Bit = 12
            end if

        end if


        this%K054539_UpdateKeyOn = .FALSE.
        this%K054539_NoReverb = .FALSE.
        this%K054539_Stereo = .FALSE.

        if (this%K054539_Clock /= 0) then
            write(tempString, "(b32)") this%KF
            if (tempString(32:32) == "1") this%K054539_Stereo = .TRUE.
            if (tempString(31:31) == "1") this%K054539_Stereo = .TRUE.
            if (tempString(30:30) == "1") this%K054539_Stereo = .TRUE.

        end if

        this%C140_ChipType = ""
        if (this%C140_Clock /= 0) then

            select case(this%CF)
                case(0)
                    this%C140_ChipType = "C140, Namco System 2"
                case(1)
                    this%C140_ChipType = "C140, Namco System 21"
                case(2)
                    this%C140_ChipType = "219 ASIC, Namco NA-1/2"
                case default
                    this%C140_ChipType = ""
            end select

        end if

        if (this%Extra_Header_Offset /=0) this%Extra_Header_Absolute_Offset = this%Extra_Header_Offset + z'BC'

        this%ES5506bit = .FALSE.
        if (this%ES5506_Clock /= 0) then
            write(tempString, "(b32)") this%ES5506_Clock

            if (tempString(1:1) == "1") this%ES5506bit = .TRUE.

            tempString(1:1) = "0"
            read(tempString, "(b32)") this%ES5506_Clock
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
