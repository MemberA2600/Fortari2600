module MidiNoteModule

    implicit none

    type midiNote
        integer :: noteOn, channel, note, velocity
        real :: time
    end type
    type midiChannel
        type(midiNote), dimension(:), allocatable :: theNotes
        integer :: noteIndex, noteLen

    end type

    integer :: numOfNotes

    contains

end module

program ExtractChannels
    use MidiNoteModule
    implicit none

    type(midiNote), dimension(:), allocatable :: midiNotes
    integer :: fileLen, io, lineNum, alloc, realIndex, theIndex, maxTime, num
    integer :: starter, ender
    real :: remainder, tempLen
    type(midiChannel), dimension(16) :: midiChannels

    character(:), allocatable :: tempPath
    character(len=1) :: dummy
    character(len=12) :: fileName
    logical :: doStuff, cutIt, secondZero

    integer, dimension(100) :: cutOut

    numOfNotes = 0
    fileLen = 0

    tempPath = "temp/"

    open(unit=11, file=tempPath // "Args.txt")

    read(11, *) cutOut

    close(11)

    open(unit=11, file=tempPath // "Input.txt")
    do
        read(11, "(A)", iostat=io) dummy
        if (io /= 0) exit

        fileLen = fileLen + 1
    end do
    rewind(11)

    allocate(midiNotes(fileLen), stat=alloc)

    do lineNum=1, fileLen, 1
        read(11, *) midiNotes(lineNum)%noteOn, midiNotes(lineNum)%channel,&
        &midiNotes(lineNum)%note, midiNotes(lineNum)%velocity, midiNotes(lineNum)%time

    end do
    close(11)

    do theIndex = 1, 16, 1
        allocate (midiChannels(theIndex)%theNotes(fileLen), stat=alloc)
        midiChannels(theIndex)%noteIndex = 2
        midiChannels(theIndex)%theNotes%noteOn = 0
        midiChannels(theIndex)%theNotes%velocity = 0
        midiChannels(theIndex)%theNotes%note = 0
        midiChannels(theIndex)%theNotes%time = 0
        midiChannels(theIndex)%theNotes%channel = theIndex
        midiChannels(theIndex)%noteLen = 0
        tempLen = 0
        remainder = 0

        do lineNum=1, fileLen, 1
            tempLen = tempLen + midiNotes(lineNum)%time

            if (midiNotes(lineNum)%channel /= theIndex-1) cycle

            if (midiNotes(lineNum)%noteOn == 0 .OR. midiNotes(lineNum)%velocity == 0 .OR.&
            & midiNotes(lineNum)%note == 0) then
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity = 0
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%note = 0
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%channel = theIndex-1
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%noteOn = 0
            else
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%channel = theIndex-1
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%noteOn = 1
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity = &
                & midiNotes(lineNum)%velocity
                midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%note = &
                & midiNotes(lineNum)%note

                if (midiNotes(lineNum)%channel == 9) then
                    midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity = &
                    &midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity / 14
                else
                    midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%note = &
                    &midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%note - 20
                end if

                if (midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%channel == 9) then
                    ! Nothing to do here

                else if (midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%note < 32) then
                    midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity = &
                    &midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity / 24

                else
                    midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity = &
                    &midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%velocity / 10

                end if
            end if
            midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%channel = theIndex-1
            midiChannels(theIndex)%theNotes((midiChannels(theIndex)%noteIndex)-1)%time = &
            &floor(tempLen+remainder)
            midiChannels(theIndex)%noteLen = midiChannels(theIndex)%noteLen + &
            & int(midiChannels(theIndex)%theNotes((midiChannels(theIndex)%noteIndex)-1)%time)

            remainder = (tempLen+remainder)-floor(tempLen+remainder)
            tempLen = 0
            midiChannels(theIndex)%noteIndex = midiChannels(theIndex)%noteIndex + 1

        end do
    end do

    maxTime = 0
    do theIndex=1, 16, 1
        if (midiChannels(theIndex)%noteLen > maxTime) maxTime = midiChannels(theIndex)%noteLen
    end do

    do theIndex=1, 16, 1
        if (midiChannels(theIndex)%noteLen < maxTime) then
            midiChannels(theIndex)%noteIndex = midiChannels(theIndex)%noteIndex + 1
            midiChannels(theIndex)%theNotes(midiChannels(theIndex)%noteIndex)%channel = theIndex-1
            midiChannels(theIndex)%theNotes((midiChannels(theIndex)%noteIndex)-1)%time = &
            & real(maxTime - midiChannels(theIndex)%noteLen)
            midiChannels(theIndex)%noteLen = midiChannels(theIndex)%noteLen &
            & + int(midiChannels(theIndex)%theNotes((midiChannels(theIndex)%noteIndex)-1)%time)
        end if
    end do

    do theIndex=1, 16, 1
       if (midiChannels(theIndex)%noteLen > 0) then
          write(fileName, "(A6, I2, A4)") "Output", theIndex, ".txt"
          if (fileName(7:7) == " ") fileName(7:7) = "0"

          open(unit=12, file=tempPath // fileName)
             do lineNum=1, midiChannels(theIndex)%noteIndex, 1
                if (midiChannels(theIndex)%theNotes(lineNum)%time > 0) then
                    cutIt = .FALSE.
                    secondZero = .FALSE.

                    do num = 1, 100, 1
                       if (cutOut(num) == midiChannels(theIndex)%theNotes(lineNum)%note) then
                           cutIt = .TRUE.
                           exit

                       end if

                       if (cutOut(num) == 0) then
                           if (secondZero .EQV. .FALSE.) then
                               secondZero = .TRUE.
                           else
                               exit

                           end if

                       end if

                    end do


                    if (midiChannels(theIndex)%theNotes(lineNum)%velocity == 0 .OR. &
                    & midiChannels(theIndex)%theNotes(lineNum)%note == 0 .OR. &
                    & cutIt .EQV. .TRUE. ) then
                        write(12, "(I0, 1x, I0, 1x, f0.0)") 0, 0, midiChannels(theIndex)%theNotes(lineNum)%time
                    else
                        write(12, "(I0, 1x, I0, 1x, f0.0)") midiChannels(theIndex)%theNotes(lineNum)%velocity&
                        &, midiChannels(theIndex)%theNotes(lineNum)%note, midiChannels(theIndex)%theNotes(lineNum)%time
                    end if
                end if
             end do
          close(12)
        end if
    end do

end program

