
    include "modules/PiaNotes.f90"


module MidiChannelModule
    type channelItem
        integer :: key, db
    end type


    type midiChannel
        integer, dimension(:), allocatable :: velocity, note, time
        integer :: lenOfNotes, correctNotes, dominantChannel
        real :: correctNotePercent, monotony, variety
        type(channelItem), dimension(5) :: channelNumbers
        integer, dimension(88) :: noteNumbers
        integer :: lastNote
    end type

end module

program GetCorrectNotesPercent
    use PiaNotesModule
    use MidiChannelModule
    implicit none

    character(:), allocatable :: tempPath
    integer :: io, alloc, fileIndex, fileLen, num, num2, num3, num4, maximum, most
    character(1) :: dummy
    character(25) :: tempNote
    type(midiChannel), dimension(3) :: midiChannels
    logical :: broken
    integer, dimension(:), allocatable :: notes
    type(PiaNotes) :: noteDict
    type(channelItem) :: tempChannel

    tempPath = "config/"

    fileIndex = 0
    fileLen = 0
    open(unit=11, file = tempPath // "PiaNotes.txt")
    do
        read(11, *, iostat = io) dummy
        if (io /= 0) exit

        fileLen = fileLen + 1
    end do

    rewind(11)

    noteDict%lenght = fileLen
    allocate(noteDict%notes(fileLen), stat = alloc)

    do fileIndex = 1, fileLen, 1
       read(11, "(A)", iostat = io) tempNote
       call noteDict%addNote(tempNote, fileIndex)

    end do
    close(11)

    tempPath = "temp/"
    fileIndex = 0
    fileLen = 0
    open(unit=11, file = tempPath // "Input.txt")
    do
        read(11, *, iostat = io) dummy
        if (io /= 0) exit
        fileLen = fileLen + 1
    end do

    rewind(11)

    do num=1, 3, 1
        allocate(midiChannels(num)%velocity(fileLen), stat = alloc)
        allocate(midiChannels(num)%note(fileLen), stat = alloc)
        allocate(midiChannels(num)%time(fileLen), stat = alloc)
        midiChannels(num)%lenOfNotes = fileLen
        midiChannels(num)%correctNotes = 0
        midiChannels(num)%correctNotePercent = 0

        midiChannels(num)%channelNumbers%db = 0
        midiChannels(num)%channelNumbers(1)%key = 11
        midiChannels(num)%channelNumbers(2)%key = 6
        midiChannels(num)%channelNumbers(3)%key = 1
        midiChannels(num)%channelNumbers(4)%key = 12
        midiChannels(num)%channelNumbers(5)%key = 4
        midiChannels(num)%noteNumbers = 0
        midiChannels(num)%lastNote = 0

    end do

    do fileIndex = 1, fileLen, 1
       read(11, *, iostat = io) midiChannels(1)%velocity(fileIndex), &
       & midiChannels(1)%note(fileIndex), midiChannels(1)%time(fileIndex)

    end do
    close(11)

    midiChannels(2)%velocity = midiChannels(1)%velocity
    midiChannels(3)%velocity = midiChannels(1)%velocity
    midiChannels(2)%time = midiChannels(1)%time
    midiChannels(3)%time = midiChannels(1)%time
    midiChannels(2)%note = midiChannels(1)%note + 8
    midiChannels(3)%note = midiChannels(1)%note - 8


    do num=1, 3, 1
       do num2 = 1, midiChannels(num)%lenOfNotes, 1
            if (midiChannels(num)%note(num2) > 2 .AND. midiChannels(num)%note(num2)<68) then

                broken = noteDict%getIfBroken(midiChannels(num)%note(num2))
                if ( broken .EQV. .FALSE.) then
                    midiChannels(num)%correctNotes =  midiChannels(num)%correctNotes + 1
                end if

                notes = noteDict%getNotes(midiChannels(num)%note(num2))

                if (broken .EQV. .FALSE.) then
                   do num3 = 1, 5, 1
                      do num4 = 1, size(notes), 2
                        if (midiChannels(num)%channelNumbers(num3)%key == notes(num4)) then
                            midiChannels(num)%channelNumbers(num3)%db = midiChannels(num)%channelNumbers(num3)%db+1

                        end if
                      end do
                    end do

                else
                    do num3 = 1, 5, 1
                        if (midiChannels(num)%channelNumbers(num3)%key == notes(1)) then
                            midiChannels(num)%channelNumbers(num3)%db = midiChannels(num)%channelNumbers(num3)%db+1
                            exit
                        end if
                    end do
                end if

                do num3=1, 88, 1
                   if (midiChannels(num)%noteNumbers(num3) == midiChannels(num)%note(num2)) then
                        exit
                   else if (midiChannels(num)%noteNumbers(num3) == 0) then
                        midiChannels(num)%noteNumbers(num3) = midiChannels(num)%note(num2)
                        midiChannels(num)%lastNote = midiChannels(num)%lastNote+1
                        exit
                   end if

                end do
            end if

       end do
       midiChannels(num)%correctNotePercent =  real(midiChannels(num)%correctNotes) / real(midiChannels(num)%lenOfNotes)
       !write(*,*) midiChannels(num)%lastNote


       maximum = 0
       most = 0

       do num2=1, 5, 1
          if (midiChannels(num)%channelNumbers(num2)%db > maximum) then
                maximum = midiChannels(num)%channelNumbers(num2)%db
                most = midiChannels(num)%channelNumbers(num2)%key
          end if
       end do
       midiChannels(num)%dominantChannel = most

       ! I know this is bullshit, but it works this way. :o
       midiChannels(num)%monotony = real(most) / real(midiChannels(num)%lenOfNotes)
       midiChannels(num)%variety = real(midiChannels(num)%lastNote) / real(midiChannels(num)%lenOfNotes)
    end do

    open(unit=11, file=tempPath // "Output.txt")
        do num = 1, 3, 1
            write(11, "(f0.12, 1x, I0, 1X, f0.12, 1x, f0.12)") midiChannels(num)%correctNotePercent, &
             & midiChannels(num)%dominantChannel, &
             & midiChannels(num)%monotony, midiChannels(num)%variety
            do num2 = 1, 5, 1
               if (midiChannels(num)%channelNumbers(num2)%db == 0) midiChannels(num)%channelNumbers(num2)%key = 0
            end do


            write(11, "(I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0 1x, I0)") &
            & midiChannels(num)%channelNumbers(1)%key, midiChannels(num)%channelNumbers(1)%db, &
            & midiChannels(num)%channelNumbers(2)%key, midiChannels(num)%channelNumbers(2)%db, &
            & midiChannels(num)%channelNumbers(3)%key, midiChannels(num)%channelNumbers(3)%db, &
            & midiChannels(num)%channelNumbers(4)%key, midiChannels(num)%channelNumbers(4)%db, &
            & midiChannels(num)%channelNumbers(5)%key, midiChannels(num)%channelNumbers(5)%db
        end do
    close(11)

end program

