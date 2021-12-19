module piModule

    real(kind=16) :: PI=2.D0*DASIN(1.D0)

end module

module ChipModule

    use piModule
    implicit none


    type ChipNote
        integer          :: duration
        real             :: volume, note
    end type

    type ChipChannel

        logical          :: FM_modulation
        real(kind=16)    :: modulation_factor
        integer          :: attack_OP0, decay_OP0, attack_OP1, decay_OP1
        integer          :: sustain_OP0, release_OP0, sustain_OP1, release_OP1
        integer          :: multi_OP0, multi_OP1
        logical          :: KSR_OP0, KSR_OP1, egTYP_OP0, egTYP_OP1
        logical          :: Vibratio_OP0, Vibratio_OP1, AM_OP0, AM_OP1
        integer          :: waveform_OP0, waveform_OP1
        real             :: keyScale_OP0, keyScale_OP1, totalLevel_OP0, totalLevel_OP1
        character(10)    :: FNumBytes
        integer(kind=2 ) :: FNum
        integer(kind=1)  :: Octave

        logical                                   :: soundOn

        integer(kind = 8)                         :: lenght
        type(ChipNote), dimension(:), allocatable :: chipNotes

        integer :: tempVolume, tempNote

    end type


    type Chip

        real    :: AM_depth
        integer :: Vibratio_depth
        logical :: rythm_mode, waveform_select

        ! If waveform select = FALSE, we do things in OPL (YM3526)

        ! Slots: 14, 18, 15, 17, 13/16
        logical :: HH, Top_Cym, Tom, SD, BD

        type(ChipChannel), dimension(9) :: chipChannels

        contains

        procedure :: register_CX => register_CX, register_6X => register_6X
        procedure :: register_8X => register_8X, register_2X => register_2X
        procedure :: register_EX => register_EX, register_4X => register_4X
        procedure :: setFNum => setFNum, updateKey=>updateKey

    end type

    contains

    subroutine updateKey(this, channelNum, key)
        class(Chip), intent(inout)     :: this
        integer(kind = 1), intent(in)  :: channelNum
        logical                        :: key
        real   (kind = 1)              :: attenuate

        if (this%chipChannels(channelNum)%soundOn .NEQV. key) then

            this%chipChannels(channelNum)%soundOn = key
            !this%chipChannels(channelNum)%lenght = this%chipChannels(channelNum)%lenght + 1

            if (key .EQV. .FALSE.) then
                this%chipChannels(channelNum)%tempVolume = 0
                this%chipChannels(channelNum)%tempNote = 0
            else
                attenuate = this%chipChannels(channelNum)%Octave

            end if
        end if

    end subroutine

    subroutine setFNum(this, channelNum)
        class(Chip), intent(inout) :: this
        integer(kind = 1)          :: channelNum

        read(this%chipChannels(channelNum)%FNumBytes, "(B10)") this%chipChannels(channelNum)%FNum

    end subroutine

    subroutine register_4X (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        integer(kind=1)            :: channelNum, byteInt, OP
        character                  :: dummy
        character(2)               :: dummy2
        character(6)               :: dummy6
        real                       :: temp, temp2

        call setChannelOP(channelNum, OP, "40", byte1)

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        dummy2 = oneByte(1:2)
        dummy6 = oneByte(3:8)

        read(dummy2, "(B2)") byteInt
        select case(byteInt)
            case(0)
                temp = 0.0
            case(1)
                temp = 1.5
            case(2)
                temp = 3.0
            case(3)
                temp = 6.0
        end select

        temp2 = 0

        if (dummy6(1:1) == "1") temp2 = temp2 + 24
        if (dummy6(2:2) == "1") temp2 = temp2 + 12
        if (dummy6(3:3) == "1") temp2 = temp2 + 6
        if (dummy6(4:4) == "1") temp2 = temp2 + 3
        if (dummy6(5:5) == "1") temp2 = temp2 + 1.5
        if (dummy6(6:6) == "1") temp2 = temp2 + 0.75

        if (OP == 1) then
            this%chipChannels(channelNum)%keyScale_OP1   = temp
            this%chipChannels(channelNum)%totalLevel_OP1 = temp2
        else
            this%chipChannels(channelNum)%keyScale_OP0   = temp
            this%chipChannels(channelNum)%totalLevel_OP0 = temp2

        end if

    end subroutine

    subroutine register_EX (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        integer(kind=1)            :: channelNum, byteInt, OP
        character                  :: dummy

        call setChannelOP(channelNum, OP, "E0", byte1)

        dummy = byte2(2:2)

        if (OP == 1) then
            read(dummy, "(Z1)") this%chipChannels(channelNum)%waveform_OP1
        else
            read(dummy, "(Z1)") this%chipChannels(channelNum)%waveform_OP0
        end if

    end subroutine

    subroutine register_2X (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        integer(kind=1)            :: channelNum, byteInt, OP
        character                  :: dummy

        call setChannelOP(channelNum, OP, "20", byte1)

        if (OP == 1) then
            dummy = byte2(1:1)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%sustain_OP1
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%release_OP1
        else
            dummy = byte2(1:1)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%sustain_OP0
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%release_OP0
        end if


    end subroutine

    subroutine register_8X (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        character(4)               :: nibble
        integer(kind=1)            :: channelNum, byteInt, OP
        character                  :: dummy

        call setChannelOP(channelNum, OP, "80", byte1)

        if (OP == 1) then
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%multi_OP1

            dummy = byte2(1:1)
            read(dummy, "(Z1)") byteInt
            write(nibble, "(b4)") byteInt

            this%chipChannels(channelNum)%AM_OP1       = .FALSE.
            this%chipChannels(channelNum)%Vibratio_OP1 = .FALSE.
            this%chipChannels(channelNum)%egTYP_OP1    = .FALSE.
            this%chipChannels(channelNum)%KSR_OP1      = .FALSE.

            if (nibble(1:1) == "1") this%chipChannels(channelNum)%AM_OP1       = .TRUE.
            if (nibble(2:2) == "1") this%chipChannels(channelNum)%Vibratio_OP1 = .TRUE.
            if (nibble(3:3) == "1") this%chipChannels(channelNum)%egTYP_OP1    = .TRUE.
            if (nibble(4:4) == "1") this%chipChannels(channelNum)%KSR_OP1      = .TRUE.

        else
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%multi_OP0

            dummy = byte2(1:1)
            read(dummy, "(Z1)") byteInt
            write(nibble, "(b4)") byteInt

            this%chipChannels(channelNum)%AM_OP0       = .FALSE.
            this%chipChannels(channelNum)%Vibratio_OP0 = .FALSE.
            this%chipChannels(channelNum)%egTYP_OP0    = .FALSE.
            this%chipChannels(channelNum)%KSR_OP0      = .FALSE.

            if (nibble(1:1) == "1") this%chipChannels(channelNum)%AM_OP0       = .TRUE.
            if (nibble(2:2) == "1") this%chipChannels(channelNum)%Vibratio_OP0 = .TRUE.
            if (nibble(3:3) == "1") this%chipChannels(channelNum)%egTYP_OP0    = .TRUE.
            if (nibble(4:4) == "1") this%chipChannels(channelNum)%KSR_OP0      = .TRUE.


        end if

    end subroutine

    subroutine register_6X (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        integer(kind=1)            :: channelNum, byteInt, OP
        character                  :: dummy

        call setChannelOP(channelNum, OP, "60", byte1)

        dummy = byte2(1:1)
        if (OP == 1) then
            dummy = byte2(1:1)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%attack_OP1
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%decay_OP1
        else
            dummy = byte2(1:1)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%attack_OP0
            dummy = byte2(2:2)
            read(dummy, "(Z1)") this%chipChannels(channelNum)%decay_OP0
        end if


    end subroutine

    subroutine setChannelOP(channelNum, OP, zero, actual)
        character(2), intent(in)       :: zero, actual
        character(8)                   :: oneByte
        integer(kind=1)                :: byteInt, zeroInt
        integer(kind=1), intent(inout) :: channelNum, OP
        character                      :: dummy

        read(zero, '(Z2)') zeroInt
        read(actual, '(Z2)') byteInt

        byteInt = byteInt - zeroInt

        select case(byteInt)
            case(z'00')
                channelNum = 1
                OP         = 0

            case(z'01')
                channelNum = 2
                OP         = 0

            case(z'02')
                channelNum = 3
                OP         = 0

            case(z'03')
                channelNum = 1
                OP         = 1

            case(z'04')
                channelNum = 2
                OP         = 1

            case(z'05')
                channelNum = 3
                OP         = 1

            case(z'08')
                channelNum = 4
                OP         = 0

            case(z'09')
                channelNum = 5
                OP         = 0

            case(z'0A')
                channelNum = 6
                OP         = 0

            case(z'0B')
                channelNum = 4
                OP         = 1

            case(z'0C')
                channelNum = 5
                OP         = 1

            case(z'0D')
                channelNum = 6
                OP         = 1

            case(z'10')
                channelNum = 7
                OP         = 0

            case(z'11')
                channelNum = 8
                OP         = 0

            case(z'12')
                channelNum = 9
                OP         = 0

            case(z'13')
                channelNum = 7
                OP         = 1

            case(z'14')
                channelNum = 8
                OP         = 1

            case(z'15')
                channelNum = 9
                OP         = 1

        end select

    end subroutine

    subroutine register_CX (this, byte1, byte2)
        class(Chip), intent(inout) :: this
        character(2)               :: byte1, byte2
        character(8)               :: oneByte
        integer(kind=1)            :: channelNum, byteInt
        character                  :: dummy

        dummy = byte1(2:2)
        read(dummy, "(Z1)") channelNum
        channelNum = channelNum + 1

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(b8)") byteInt

        this%chipChannels%FM_modulation = .FALSE.
        if (oneByte(8:8) == "1") this%chipChannels%FM_modulation = .TRUE.
        read(oneByte(5:7), "(I1)") byteInt

        select case(byteInt)

            case(0)
                this%chipChannels(channelNum)%modulation_factor = 0
            case(1)
                this%chipChannels(channelNum)%modulation_factor = PI/16.0
            case(2)
                this%chipChannels(channelNum)%modulation_factor = PI/8.0
            case(3)
                this%chipChannels(channelNum)%modulation_factor = PI/4.0
            case(4)
                this%chipChannels(channelNum)%modulation_factor = PI/2.0
            case(5)
                this%chipChannels(channelNum)%modulation_factor = PI
            case(6)
                this%chipChannels(channelNum)%modulation_factor = PI*2.0
            case(7)
                this%chipChannels(channelNum)%modulation_factor = PI*4.0
        end select

    end subroutine

end module

program YM3812
    use ChipModule
    implicit none

    integer         :: fileLen, io, alloc, num, num2, num3, num4, num5
    integer(kind=1) :: channelNum
    character       :: dummy
    integer(kind=8) :: noteOn

    real :: volume, rate
    character(2), dimension(:,:), allocatable :: byteStrings
    integer, dimension(:,:), allocatable :: bytes
    character(4) :: chipType

    type(Chip)   :: chipYM3812
    logical      :: changed, logic
    character(8) :: oneByte

    integer(kind=1) :: b1, b2

    open(unit = 12, file = "temp/Args.txt")
    read(12, *) volume, rate, noteOn, chipType
    close(12)

    fileLen = 0
    changed = .FALSE.

    open(unit = 12, file = "temp/Input.txt")
    do
        read(12, *, iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1

    end do

    rewind(12)

    allocate(byteStrings(fileLen,3), stat=alloc)
    allocate(bytes(fileLen,3), stat=alloc)

    do num = 1, fileLen, 1
        read(12, *) byteStrings(num,1), byteStrings(num,2), byteStrings(num,3)
        do num2 = 1, 3, 1
            read(byteStrings(num,num2), "(z4)") bytes(num,num2)
        end do
    end do
    close(12)

    chipYM3812%waveform_select            = .FALSE.

    chipYM3812%chipChannels%AM_OP0        = .FALSE.
    chipYM3812%chipChannels%AM_OP1        = .FALSE.

    chipYM3812%chipChannels%attack_OP0    = 0
    chipYM3812%chipChannels%attack_OP1    = 0

    chipYM3812%chipChannels%decay_OP0     = 0
    chipYM3812%chipChannels%decay_OP1     = 0

    chipYM3812%chipChannels%egTYP_OP0     = .FALSE.
    chipYM3812%chipChannels%egTYP_OP1     = .FALSE.

    chipYM3812%chipChannels%FM_modulation = .FALSE.

    chipYM3812%chipChannels%FNumBytes = "0000000000"

    chipYM3812%chipChannels%lenght = 0

    chipYM3812%rythm_mode                 = .FALSE.
    chipYM3812%SD                         = .FALSE.
    chipYM3812%Tom                        = .FALSE.
    chipYM3812%Top_Cym                    = .FALSE.
    chipYM3812%BD                         = .FALSE.
    chipYM3812%Vibratio_depth             = 0

    do num = 1, 9, 1
       allocate(chipYM3812%chipChannels(num)%chipNotes(noteOn), stat = alloc)
    end do

    !if (chipType == "OPL3") chipYM3812%waveform_select = .TRUE.

    do num = 1, fileLen, 1
        select case(bytes(num, 1))
            case (z'5A':z'5B')
                select case(bytes(num, 2))
                    case(z'01')
                        if (chipType == "OPL2" .AND. byteStrings(num, 3) == "20") &
                        &chipYM3812%waveform_select = .TRUE.

                    case(z'BD')
                        write(oneByte, "(B8)") bytes(num, 3)
                        chipYM3812%HH         = .FALSE.
                        chipYM3812%Tom        = .FALSE.
                        chipYM3812%Top_Cym    = .FALSE.
                        chipYM3812%SD         = .FALSE.
                        chipYM3812%BD         = .FALSE.
                        changed               = .FALSE.
                        if (oneByte(3:3) == '0') then
                            if (chipYM3812%rythm_mode .EQV. .TRUE.) changed = .TRUE.
                            chipYM3812%rythm_mode = .FALSE.

                        else
                            if (chipYM3812%rythm_mode .EQV. .FALSE.) changed = .TRUE.
                            chipYM3812%rythm_mode = .TRUE.
                            if (oneByte(8:8) == "1") chipYM3812%HH      = .TRUE.
                            if (oneByte(7:7) == "1") chipYM3812%Top_Cym = .TRUE.
                            if (oneByte(6:6) == "1") chipYM3812%Tom     = .TRUE.
                            if (oneByte(5:5) == "1") chipYM3812%SD      = .TRUE.
                            if (oneByte(4:4) == "1") chipYM3812%BD      = .TRUE.
                        end if

                        !  Slots: 14, 18, 15, 17, 13/16
                        !  Logical :: HH, Top_Cym, Tom, SD, BD

                        if (changed .EQV. .TRUE.) then
                            b1 = 7
                            b2 = 0
                            call chipYM3812%updateKey(b1, chipYM3812%BD)
                            b1 = 7
                            b2 = 1
                            call chipYM3812%updateKey(b1, chipYM3812%HH)
                            b1 = 8
                            b2 = 0
                            call chipYM3812%updateKey(b1, chipYM3812%Tom)
                            b1 = 8
                            b2 = 1
                            call chipYM3812%updateKey(b1, chipYM3812%BD)
                            b1 = 9
                            b2 = 0
                            call chipYM3812%updateKey(b1, chipYM3812%SD)
                            b1 = 9
                            b2 = 1
                            call chipYM3812%updateKey(b1, chipYM3812%Top_Cym)

                        end if

                        if (oneByte(2:2) == "1") then
                            chipYM3812%Vibratio_depth = 14
                        else
                            chipYM3812%Vibratio_depth = 7
                        end if

                        if (oneByte(1:1) == "1") then
                            chipYM3812%AM_depth = 4.8
                        else
                            chipYM3812%AM_depth = 1.0
                        end if

                    case(z'C0':z'C8')
                            call chipYM3812%register_CX(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'60':z'75')
                            call chipYM3812%register_6X(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'80':z'95')
                            call chipYM3812%register_8X(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'20':z'35')
                            call chipYM3812%register_2X(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'E0':z'F5')
                            call chipYM3812%register_EX(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'40':z'55')
                            call chipYM3812%register_4X(byteStrings(num, 2), byteStrings(num, 3))

                    case(z'A0':z'A8')
                            dummy = byteStrings(num, 2)(2:2)
                            read(dummy, "(I1)") channelNum
                            channelNum = channelNum + 1

                            write(oneByte, "(B0)") bytes(num, 3)
                            chipYM3812%chipChannels(channelNum)%FNumBytes(3:10) = oneByte
                            call chipYM3812%setFNum(channelNum)

                    case(z'B0':z'B8')
                            dummy = byteStrings(num, 2)(2:2)
                            read(dummy, "(I1)") channelNum
                            channelNum = channelNum + 1
                            write(oneByte, "(B0)") bytes(num, 3)

                            chipYM3812%chipChannels(channelNum)%FNumBytes(1:2) = oneByte(7:8)
                            call chipYM3812%setFNum(channelNum)

                            read(oneByte(4:6), "(B3)") chipYM3812%chipChannels(channelNum)%Octave

                            logic = .FALSE.
                            if (oneByte(3:3) == "1") logic = .TRUE.


                            call chipYM3812%updateKey(channelNum, logic)
                            call chipYM3812%updateKey(channelNum, logic)

                end select
            case (z'61')
                cycle

        end select


    end do


end program

