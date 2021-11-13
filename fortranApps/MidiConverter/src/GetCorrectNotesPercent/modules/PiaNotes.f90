module PiaNotesModule

    implicit none

    public :: AddNote, GetIfBroken, GetNumberOfNotes, GetNotes

    type PiaNote
        integer :: key
        integer, dimension(3) :: channel, note
        integer :: numberOfNotes

        logical :: broken

    end type

    type PiaNotes
        type(PiaNote), dimension(:), allocatable :: notes
        integer :: lenght

        contains

        procedure :: addNote => AddNote
        procedure :: getIfBroken => GetIfBroken
        procedure :: getNumberOfNotes => GetNumberOfNotes
        procedure :: getNotes => getNotes

    end type

    contains
        function getNotes(this, key) result(channel_note)
        class(PiaNotes) :: this
        integer :: key, counter, alloc, counter2
        integer, dimension(:), allocatable :: channel_note


        do counter = 1, this%lenght, 1
            if (key == this%notes(counter)%key) then
                allocate(channel_note((this%notes(counter)%numberOfNotes)*2), stat=alloc)

                do counter2 = 1, this%notes(counter)%numberOfNotes, 1
                    channel_note(((counter2-1)*2)+1) = this%notes(counter)%channel(counter2)
                    channel_note((counter2)*2) = this%notes(counter)%note(counter2)
                end do

                exit
            end if
        end do

    end function



    function getNumberOfNotes(this, key) result(num)
        class(PiaNotes) :: this
        integer :: key, counter, num

        num = 0

        do counter = 1, this%lenght, 1
            if (key == this%notes(counter)%key) then
                num = this%notes(counter)%numberOfNotes
                exit
            end if
        end do

    end function

    function getIfBroken(this, key) result(state)
        class(PiaNotes) :: this
        logical :: state
        integer :: key, counter

        state = .TRUE.

        do counter = 1, this%lenght, 1
            if (key == this%notes(counter)%key) then
                state = this%notes(counter)%broken
                exit
            end if
        end do

    end function

    subroutine addNote(this, line, itemIndex)
        class(PiaNotes), intent(inout) :: this
        character(25) :: line, temp
        integer :: num, itemIndex, starting

        temp = ""

        this%notes(itemIndex)%channel(1) = 255
        this%notes(itemIndex)%channel(2) = 255
        this%notes(itemIndex)%channel(3) = 255

        this%notes(itemIndex)%note(1) = 255
        this%notes(itemIndex)%note(2) = 255
        this%notes(itemIndex)%note(3) = 255

        starting = 0

        do num = 1, len_trim(line), 1
            if (line(num:num) == "=") then
                temp = line(1:num-1)
                read(temp, "(I2)") this%notes(itemIndex)%key
                starting = num + 1
                exit
            end if
            starting = num + 1
        end do

        if (line(starting:starting) == "#") then
            this%notes(itemIndex)%broken=.TRUE.
            starting = starting + 2
        else
            this%notes(itemIndex)%broken=.FALSE.
        end if

        this%notes(itemIndex)%numberOfNotes = 1

        do num = starting, len_trim(line), 1

            if (line(num:num) == ":") then
                temp = line(starting:num-1)

                starting = num+1
                read(temp, *) this%notes(itemIndex)%channel(&
                &this%notes(itemIndex)%numberOfNotes)

            else if (line(num:num) == ",") then
                temp = line(starting:num-1)

                read(temp, *) this%notes(itemIndex)%note(&
                &this%notes(itemIndex)%numberOfNotes)

                this%notes(itemIndex)%numberOfNotes = &
                &this%notes(itemIndex)%numberOfNotes + 1

                starting = num+1
            else if (line(num:num) == " " .OR. line(num:num) == ")") then
                temp = line(starting:num-1)

                read(temp, *) this%notes(itemIndex)%note(&
                &this%notes(itemIndex)%numberOfNotes)

                this%notes(itemIndex)%numberOfNotes = &
                &this%notes(itemIndex)%numberOfNotes + 1
            else if (num == len_trim(line)) then
                temp = line(starting:num)


                read(temp, *) this%notes(itemIndex)%note(&
                &this%notes(itemIndex)%numberOfNotes)

                this%notes(itemIndex)%numberOfNotes = &
                &this%notes(itemIndex)%numberOfNotes + 1

                exit
            end if
        end do
        this%notes(itemIndex)%numberOfNotes = &
        &this%notes(itemIndex)%numberOfNotes - 1


    end subroutine

end module
