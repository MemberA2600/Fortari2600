module piModule

    real(kind=16) :: PI=2.D0*DASIN(1.D0)

end module

module AttackDecayTableModule
    implicit none

    type AttackDecayTableRow
        integer(kind=1) ::  rate4bit, rks2bit
        real, dimension(2) :: attack, decay

    end type

    type AttackDecayTable
        type(AttackDecayTableRow), dimension(60) :: rows

        contains

        procedure :: fillTable => fillTable

    end type

    contains

    subroutine fillTable(this)
        class(AttackDecayTable), intent(inout) :: this
        character(:), allocatable              :: fileName
        integer                                :: fileLen, io, alloc, num, octave, fnum
        character                              :: dummy
        real                                   :: temp

        fileName = "config/attack_decay.txt"
        fileLen  = 0

        open(unit = 13, file = fileName)

        do
            read(13, *, iostat = io)
            if (io /= 0) exit
            fileLen = fileLen + 1

        end do

        rewind(13)

        do num = 1, fileLen, 1
           read(13, *) this%rows(num)%rate4bit, this%rows(num)%rks2bit, this%rows(num)%attack(1), &
           & this%rows(num)%decay(1), this%rows(num)%attack(2), this%rows(num)%decay(2)

        end do

        close(13)


    end subroutine

end module


module AttenuationTableModule
    implicit none


    type AttenuationTable

        real, dimension(8,16) :: attenuation

        contains

        procedure             :: loadTable => loadTable

    end type

    contains

    subroutine loadTable(this)
        class(AttenuationTable), intent(inout) :: this
        character(:), allocatable              :: fileName
        integer                                :: fileLen, io, alloc, num, octave, fnum
        character                              :: dummy
        real                                   :: temp

        fileName = "config/attenuation.txt"
        fileLen  = 0

        open(unit = 13, file = fileName)

        do
            read(13, *, iostat = io)
            if (io /= 0) exit
            fileLen = fileLen + 1

        end do

        rewind(13)

        do num = 1, fileLen, 1
           read(13, *) octave, fnum, temp

           this%attenuation(octave+1,fnum+1) = temp

        end do

        close(13)

    end subroutine

end module

module ChipModule
    use piModule
    use AttenuationTableModule
    use AttackDecayTableModule

    implicit none

    type OPLChipChannelSlot
        integer            :: multiplier, KSL
        logical            :: KSR, egTyp, VIB, AM
        real               :: totalLevel, attenuation_degree
        integer(kind=1)    :: attackRate, decayRate, sustainLevel, releaseRate, sustainRate
        integer(kind=1)    :: Rks
        integer(kind=2)    :: attackKSR, decayKSR, sustainKSR, releaseKSR

    end type

    type OPLChipChannel

        type(OPLChipChannelSlot), dimension(2) :: slots
        real :: multiplier

        integer(kind=1)    :: octave_block, FNum_HI, feedBack
        integer(kind=2)    :: FNum_LO, keyScaleNumber
        logical            :: keyOn, slotConnection
        real               :: modulationFactor

    end type

    type OPLChipMusicData
        !


    end type


    type OPLChip

        type(OPLChipChannel), dimension(9) :: channels
        logical            :: HH, topCy, Tom, SD, BD, rythmMode, keySplit
        real               :: vibratio, amDepth

        contains

        procedure :: setRegister08  => setRegister08
        procedure :: setRegister2X  => setRegister2X
        procedure :: setRegister4X  => setRegister4X
        procedure :: setRegister6X  => setRegister6X
        procedure :: setRegister8X  => setRegister8X
        procedure :: setRegisterAX  => setRegisterAX
        procedure :: setRegisterBX  => setRegisterBX
        procedure :: setRegisterCX  => setRegisterCX
        procedure :: setRegisterBD  => setRegisterBD
        procedure :: init           => init
        procedure :: setChannelData => setChannelData
        procedure :: getFrequency   => getFrequency
        procedure :: getAttenuation => getAttenuation
        procedure :: setScaleNumber => setScaleNumber


    end type

    contains

    subroutine setChannelData(this, b1, b2, AT, ADT)
        class(OPLChip), intent(inout)      :: this
        integer(kind=1)                    :: num, num2
        integer                            :: waitTime, fnum
        character(2), intent(in)           :: b1, b2
        real                               :: freq
        real, dimension(2)                 :: attenuation, volume, slotFreq
        character(8)                       :: oneByte
        character(10)                      :: tenBits

        character(4)                       :: together
        type(AttenuationTable), intent(in) :: AT
        type(AttackDecayTable), intent(in) :: ADT

        together = b2 // b1
        read(together, "(Z4)") waitTime

        do num = 1, 9, 1
           freq = this%getFrequency(num)

            write(oneByte, "(B8)") this%channels(num)%FNum_LO
            tenBits(3:10) = oneByte

            write(oneByte, "(B8)") this%channels(num)%FNum_HI
            tenBits(1:2) = oneByte(7:8)

            read(tenBits, "(B10)") fnum

            call this%setScaleNumber(num)

            do num2 = 1, 2, 1
               attenuation(num2) = this%getAttenuation(num, num2, AT)
               slotFreq(num2)    = fnum * real(this%channels(num)%slots(num2)%multiplier)

               if (this%channels(num)%slots(num2)%KSR .EQV. .TRUE.) then
                   this%channels(num)%slots(num2)%rks  = this%channels(num)%keyScaleNumber
               else
                   select case(this%channels(num)%keyScaleNumber)
                        case(0:3)
                            this%channels(num)%slots(num2)%rks  = 0
                        case(4:7)
                            this%channels(num)%slots(num2)%rks  = 1
                        case(8:11)
                            this%channels(num)%slots(num2)%rks  = 2
                        case(12:15)
                            this%channels(num)%slots(num2)%rks  = 3
                   end select
               end if

              this%channels(num)%slots(num2)%attackKSR              = 0
              this%channels(num)%slots(num2)%decayKSR               = 0
              this%channels(num)%slots(num2)%sustainKSR             = 0
              this%channels(num)%slots(num2)%releaseKSR             = 0

              if (this%channels(num)%slots(num2)%attackRate > 0) then
                  this%channels(num)%slots(num2)%attackKSR = &
                  & (4 * this%channels(num)%slots(num2)%attackRate) + &
                  & this%channels(num)%slots(num2)%rks

              end if

              if (this%channels(num)%slots(num2)%decayRate > 0) then
                  this%channels(num)%slots(num2)%decayKSR = &
                  & (4 * this%channels(num)%slots(num2)%decayRate) + &
                  & this%channels(num)%slots(num2)%rks

              end if

              if (this%channels(num)%slots(num2)%sustainRate > 0) then
                  this%channels(num)%slots(num2)%sustainKSR = &
                  & (4 * this%channels(num)%slots(num2)%sustainRate) + &
                  & this%channels(num)%slots(num2)%rks

              end if

              if (this%channels(num)%slots(num2)%releaseRate > 0) then
                  this%channels(num)%slots(num2)%releaseKSR = &
                  & (4 * this%channels(num)%slots(num2)%releaseRate) + &
                  & this%channels(num)%slots(num2)%rks

              end if



            end do

            ! write(*,*) num, freq, slotFreq, attenuation
        end do

    end subroutine

    subroutine setScaleNumber(this, channelNum)
        class(OPLChip), intent(inout)      :: this
        integer(kind=1)                    :: num, num2
        integer(kind=1), intent(in)        :: channelNum
        character(8)                       :: oneByte
        character(2)                       :: twoBits

        integer(kind=1)                    :: importantBit

        write(twoBits, "(B2)") this%channels(num)%FNum_HI

        importantBit = 0
        if (this%keySplit .EQV. .TRUE.) then
            if (twoBits(1:1) == "1") importantBit = 1
        else
            if (twoBits(2:2) == "1") importantBit = 1
        end if

        this%channels(channelNum)%keyScaleNumber = (this%channels(channelNum)%octave_block * 2) + importantBit


    end subroutine


    function getFrequency(this, channelNum) result(freq)
        class(OPLChip)       :: this
        integer(kind=1)      :: channelNum
        integer              :: fnum

        real                 :: freq, tempNum1, tempNum2, tempNum3
        character(10)        :: tenBits
        character(8)         :: oneByte


        !f-num = freq * 2^(20 - block) / 49716 ( or 50000? )

        !tempNum1 = 20.0-real(this%channels(channelNum)%octave_block)
        !tempNum2 = 2.0 ** tempNum1
        !tempNum3 = tempNum2 / real(49716)

        write(oneByte, "(B8)") this%channels(channelNum)%FNum_LO
        tenBits(3:10) = oneByte

        write(oneByte, "(B8)") this%channels(channelNum)%FNum_HI
        tenBits(1:2) = oneByte(7:8)

        read(tenBits, "(B10)") fnum
        !freq     = real(fnum) / tempNum3

        tempNum1 = real(fnum) * real(50000)
        tempNum2 = 20.0-real(this%channels(channelNum)%octave_block)
        freq = tempNum1 / real(2**tempNum2)

    end function

    function getAttenuation(this, channelNum, slot, AT) result(attenuation)
        class(OPLChip)                    :: this
        character(8)                      :: oneByte
        character(2)                      :: oneDoubleBit
        character(4)                      :: nibble
        integer(kind=1), intent(in)       :: channelNum, slot
        integer(kind=1)                   :: FNumHi4
        real                              :: attenuation
        type(AttenuationTable, intent(in) :: AT

        write(oneByte, "(B8)") this%channels(channelNum)%FNum_LO
        write(oneDoubleBit, "(B2)") this%channels(channelNum)%FNum_HI

        nibble = oneDoubleBit // oneByte(1:2)
        read(nibble, "(B4)") FNumHi4

        attenuation = AT%attenuation(this%channels(channelNum)%octave_block+1, FNumHi4 +1)

        select case(this%channels(channelNum)%slots(slot)%KSL)
            case(0)
                attenuation = 0
            case(2)
                attenuation = attenuation / 2
            case(3)
                attenuation = attenuation * 2
        end select

    end function


    subroutine init(this)
        class(OPLChip), intent(inout) :: this
        integer :: num, num2

        this%amDepth         = 0.0
        this%BD              = .FALSE.
        this%HH              = .FALSE.
        this%rythmMode       = .FALSE.
        this%SD              = .FALSE.
        this%Tom             = .FALSE.
        this%topCy           = .FALSE.
        this%keySplit           = .FALSE.
        this%vibratio        = 0.0

        do num = 1, 9, 1
           this%channels(num)%feedBack          = 0
           this%channels(num)%FNum_HI           = 0
           this%channels(num)%FNum_LO           = 0
           this%channels(num)%keyOn             = .FALSE.
           this%channels(num)%modulationFactor  = 0.0
           this%channels(num)%multiplier        = 0.0
           this%channels(num)%octave_block      = 0
           this%channels(num)%slotConnection    = .FALSE.
           this%channels(num)%keyScaleNumber    = 0

           do num2 = 1, 2, 1
              this%channels(num)%slots(num2)%AM                     = .FALSE.
              this%channels(num)%slots(num2)%attackRate             = 0
              this%channels(num)%slots(num2)%attenuation_degree     = 0.0
              this%channels(num)%slots(num2)%decayRate              = 0
              this%channels(num)%slots(num2)%egTyp                  = .FALSE.
              this%channels(num)%slots(num2)%KSL                    = 0
              this%channels(num)%slots(num2)%KSR                    = 0
              this%channels(num)%slots(num2)%multiplier             = 0
              this%channels(num)%slots(num2)%releaseRate            = 0
              this%channels(num)%slots(num2)%sustainLevel           = 0
              this%channels(num)%slots(num2)%totalLevel             = 0.0
              this%channels(num)%slots(num2)%VIB                    = .FALSE.
              this%channels(num)%slots(num2)%attackKSR              = 0
              this%channels(num)%slots(num2)%decayKSR               = 0
              this%channels(num)%slots(num2)%sustainKSR             = 0
              this%channels(num)%slots(num2)%releaseKSR             = 0
              this%channels(num)%slots(num2)%Rks                    = 0

           end do

        end do

   end subroutine

   subroutine setChannelOP(channelNum, OP, zero, actual)
        character(2), intent(in)       :: zero, actual
        character(8)                   :: oneByte
        integer(kind=1)                :: byteInt, zeroInt
        integer(kind=1), intent(inout) :: channelNum, OP
        character                      :: dummy

        integer, dimension(22)         :: channels, slots

        channels = (/ 1, 2, 3, 1, 2, 3, -1, -1, 4, 5, 6, 4, 5, 6, -1, -1, 7, 8, 9, 7, 8, 9 /)
        slots    = (/ 1, 1, 1, 2, 2, 2, -1, -1, 1, 1, 1, 2, 2, 2, -1, -1, 1, 1, 1, 2, 2, 2 /)

        read(zero, '(Z2)') zeroInt
        read(actual, '(Z2)') byteInt

        byteInt = byteInt - zeroInt + 1

        channelNum = channels(byteInt)
        OP         = slots(byteInt)

    end subroutine

    subroutine setRegister08(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        read(byte2, "(Z2)")    byteInt
        write(oneByte, "(B8)") byteInt

        this%keySplit = .FALSE.
        if (oneByte(2:2) == "1") this%keySplit = .TRUE.


    end subroutine


    subroutine setRegister2X(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        tempByte = "0" // byte2(2:2)

        call setChannelOP(channelNum, slot, "20", byte1)

        read(tempByte, "(Z2)") this%channels(channelNum)%slots(slot)%multiplier

        this%channels(channelNum)%slots(slot)%AM    = .FALSE.
        this%channels(channelNum)%slots(slot)%egTyp = .FALSE.
        this%channels(channelNum)%slots(slot)%KSR   = .FALSE.
        this%channels(channelNum)%slots(slot)%VIB   = .FALSE.

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        if (oneByte(1:1) == "1") this%channels(channelNum)%slots(slot)%AM    = .TRUE.
        if (oneByte(2:2) == "1") this%channels(channelNum)%slots(slot)%egTyp = .TRUE.
        if (oneByte(3:3) == "1") this%channels(channelNum)%slots(slot)%KSR   = .TRUE.
        if (oneByte(4:4) == "1") this%channels(channelNum)%slots(slot)%VIB   = .TRUE.

        select case(this%channels(channelNum)%slots(slot)%multiplier)

            case(z'1':z'9')
                this%channels(channelNum)%multiplier = this%channels(channelNum)%slots(slot)%multiplier
            case(z'0')
                this%channels(channelNum)%multiplier = 0.5
            case(z'A':z'B')
                this%channels(channelNum)%multiplier = 10
            case(z'C':z'D')
                this%channels(channelNum)%multiplier = 12
            case(z'E':z'F')
                this%channels(channelNum)%multiplier = 15

        end select

        ! TODO : Lot of stupid calculations I don't understand yet.

    end subroutine

    subroutine setRegister4X(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        real                          :: totalVal

        tempByte = "0" // byte2(2:2)

        call setChannelOP(channelNum, slot, "40", byte1)

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        totalVal = 0.0

        if (oneByte(3:3) == "1") totalVal = totalVal + 24.00
        if (oneByte(4:4) == "1") totalVal = totalVal + 12.00
        if (oneByte(5:5) == "1") totalVal = totalVal +  6.00
        if (oneByte(6:6) == "1") totalVal = totalVal +  3.00
        if (oneByte(7:7) == "1") totalVal = totalVal +  1.50
        if (oneByte(8:8) == "1") totalVal = totalVal +  0.75

        this%channels(channelNum)%slots(slot)%totalLevel = totalVal

        byteSlice = "000000" // oneByte(1:2)

        read(byteSlice, "(B8)") this%channels(channelNum)%slots(slot)%KSL

        select case(this%channels(channelNum)%slots(slot)%KSL)

            case(0)
                this%channels(channelNum)%slots(slot)%attenuation_degree = 0.0
            case(1)
                this%channels(channelNum)%slots(slot)%attenuation_degree = 3.0
            case(2)
                this%channels(channelNum)%slots(slot)%attenuation_degree = 1.5
            case(3)
                this%channels(channelNum)%slots(slot)%attenuation_degree = 6
        end select

        ! TODO: A lot of calculations

    end subroutine

    subroutine setRegister6X(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        call setChannelOP(channelNum, slot, "60", byte1)

        tempByte = "0" // byte2(1:1)
        read(tempByte, "(Z2)") this%channels(channelNum)%slots(slot)%attackRate

        tempByte = "0" // byte2(2:2)
        read(tempByte, "(Z2)") this%channels(channelNum)%slots(slot)%decayRate

        ! TODO: Calculations

    end subroutine

    subroutine setRegister8X(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt, sustainLevel
        character                     :: dummy

        call setChannelOP(channelNum, slot, "80", byte1)

        tempByte = "0" // byte2(1:1)
        read(tempByte, "(Z2)")   byteInt
        write(byteSlice, "(B8)") byteInt

        sustainLevel = 0
        if (byteSlice(5:5) == "1") sustainLevel = sustainLevel + 24
        if (byteSlice(6:6) == "1") sustainLevel = sustainLevel + 12
        if (byteSlice(7:7) == "1") sustainLevel = sustainLevel + 6
        if (byteSlice(8:8) == "1") sustainLevel = sustainLevel + 3

        this%channels(channelNum)%slots(slot)%sustainLevel = sustainLevel

        tempByte = "0" // byte2(2:2)
        read(tempByte, "(Z2)") this%channels(channelNum)%slots(slot)%releaseRate

        tempByte = "0" // byte2(1:1)
        read(tempByte, "(Z2)") this%channels(channelNum)%slots(slot)%sustainRate

        ! TODO: Calculations

    end subroutine


    subroutine setRegisterAX(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        real                          :: freq

        tempByte = "0" // byte1(2:2)
        read(tempByte, "(Z2)") channelNum

        read(byte2, "(Z2)") this%channels(channelNum)%FNum_LO


    end subroutine

    subroutine setRegisterBX(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy


        tempByte = "0" // byte1(2:2)
        read(tempByte, "(Z2)") channelNum

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        byteSlice = "000000" // oneByte(6:8)
        read(byteSlice, "(B8)") this%channels(channelNum)%FNum_HI

        byteSlice = "00000" // oneByte(4:6)
        read(byteSlice, "(B8)") this%channels(channelNum)%octave_block

        this%channels(channelNum)%keyOn = .FALSE.
        if (oneByte(3:3) == "1") this%channels(channelNum)%keyOn = .TRUE.


    end subroutine

    subroutine setRegisterCX(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        real                          :: totalVal

        tempByte = "0" // byte1(2:2)
        read(tempByte, "(Z2)") channelNum

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        this%channels(channelNum)%slotConnection = .FALSE.
        if (oneByte(8:8) == "1") this%channels(channelNum)%slotConnection = .TRUE.

        byteSlice = "00000" // oneByte(5:7)
        read(byteSlice, "(B8)") this%channels(channelNum)%feedBack

        select case(this%channels(channelNum)%feedBack)
            case(0)
                this%channels(channelNum)%modulationFactor = 0
            case(1)
                this%channels(channelNum)%modulationFactor = PI / 16.0
            case(2)
                this%channels(channelNum)%modulationFactor = PI / 8.0
            case(3)
                this%channels(channelNum)%modulationFactor = PI / 4.0
            case(4)
                this%channels(channelNum)%modulationFactor = PI / 2.0
            case(5)
                this%channels(channelNum)%modulationFactor = PI
            case(6)
                this%channels(channelNum)%modulationFactor = PI * 2.0
            case(7)
                this%channels(channelNum)%modulationFactor = PI * 4.0

        end select

    end subroutine

    subroutine setRegisterBD(this, byte1, byte2)
        class(OPLChip), intent(inout) :: this
        character(2)                  :: byte1, byte2, tempByte
        character(8)                  :: oneByte, byteSlice
        integer(kind=1)               :: channelNum, slot
        integer(kind=2)               :: byteInt
        character                     :: dummy

        real                          :: totalVal, freq

        tempByte = "0" // byte1(2:2)
        read(tempByte, "(Z2)") channelNum

        read(byte2, "(Z2)") byteInt
        write(oneByte, "(B8)") byteInt

        this%rythmMode =.FALSE.
        this%HH        =.FALSE.
        this%topCy     =.FALSE.
        this%Tom       =.FALSE.
        this%SD        =.FALSE.
        this%BD        =.FALSE.

        if (oneByte(3:3) == "1") then
            this%rythmMode =.TRUE.

            if (oneByte(8:8) == "1") this%HH        =.TRUE.
            if (oneByte(7:7) == "1") this%topCy     =.TRUE.
            if (oneByte(6:6) == "1") this%Tom       =.TRUE.
            if (oneByte(5:5) == "1") this%SD        =.TRUE.
            if (oneByte(4:4) == "1") this%BD        =.TRUE.

        end if

        this%amDepth = 1.0
        if (oneByte(1:1) == "1") this%amDepth = 4.8

        this%vibratio = 7.0
        if (oneByte(2:2) == "1") this%vibratio = 14.0

    end subroutine

end module

program OPL2TIA
    use ChipModule
    use AttenuationTableModule
    use AttackDecayTableModule

    implicit none

    type(OPLChip)   :: chip

    integer         :: fileLen, io, alloc, num, num2, num3, num4, num5
    integer(kind=2) :: channelNum
    character       :: dummy
    integer(kind=8) :: noteOn

    real :: volume, rate
    character(2), dimension(:,:), allocatable :: byteStrings
    integer, dimension(:,:), allocatable :: bytes
    character(4) :: chipType

    logical      :: changed, logic
    character(8) :: oneByte

    type(AttenuationTable) :: AT
    type(AttackDecayTable) :: ADT


    open(unit = 12, file = "temp/Args.txt")
    read(12, *) volume, rate, noteOn, chipType
    close(12)

    fileLen = 0
    changed = .FALSE.

    call chip%init()
    call AT%loadTable()
    call ADT%fillTable()

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

    ! MSB: right bit, LSB: left bit

    do num = 1, fileLen, 1
       if (bytes(num, 1) == z"5A" .OR. bytes(num, 1) == z"5B" &
       &.OR. bytes(num, 1) == z"5E" .OR. bytes(num, 1) == z"5F") then

           select case (bytes(num, 2))
                case(z'08')
                    call chip%setRegister08(byteStrings(num, 2), byteStrings(num, 3))
                case(z'20':z'35')
                    call chip%setRegister2X(byteStrings(num, 2), byteStrings(num, 3))
                case(z'40':z'55')
                    call chip%setRegister4X(byteStrings(num, 2), byteStrings(num, 3))
                case(z'60':z'75')
                    call chip%setRegister6X(byteStrings(num, 2), byteStrings(num, 3))
                case(z'80':z'95')
                    call chip%setRegister8X(byteStrings(num, 2), byteStrings(num, 3))
                case(z'A0':z'A8')
                    call chip%setRegisterAX(byteStrings(num, 2), byteStrings(num, 3))
                case(z'B0':z'B8')
                    call chip%setRegisterBX(byteStrings(num, 2), byteStrings(num, 3))
                case(z'C0':z'C8')
                    call chip%setRegisterCX(byteStrings(num, 2), byteStrings(num, 3))
                case(z'BD')
                    call chip%setRegisterBD(byteStrings(num, 2), byteStrings(num, 3))

           end select

      else if (bytes(num, 1) == z"61") then
           call chip%setChannelData(byteStrings(num, 2), byteStrings(num, 3), AT, ADT)

      end if

    end do

end program

