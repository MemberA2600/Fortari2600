module DrumSetModule

    implicit none

    type drumNote
        integer, dimension(:), allocatable :: keys
        integer :: tableNum, channel, note
    end type

    contains

    subroutine drumsInit(drumNotes)
        type(drumNote), dimension(7), intent(inout) :: drumNotes
        integer :: alloc

             !  1.
        drumNotes(1)%tableNum = 89
        drumNotes(1)%channel = 15
        drumNotes(1)%note = 20
        allocate(drumNotes(1)%keys(13), stat = alloc)
        drumNotes(1)%keys = (/ 35, 36, 41, 43, 45, 47, 48, 50, 64, 65, 66, 78, 79 /)

     !  2.
        drumNotes(2)%tableNum = 90
        drumNotes(2)%channel = 8
        drumNotes(2)%note = 0
        allocate(drumNotes(2)%keys(5), stat = alloc)
        drumNotes(2)%keys = (/ 42, 44, 51, 73, 76 /)

     !  3.
        drumNotes(3)%tableNum = 91
        drumNotes(3)%channel = 15
        drumNotes(3)%note = 2
        allocate(drumNotes(3)%keys(5), stat = alloc)
        drumNotes(3)%keys = (/ 46, 52, 55, 74, 77 /)

     !  4.
        drumNotes(4)%tableNum = 92
        drumNotes(4)%channel = 8
        drumNotes(4)%note = 8
        allocate(drumNotes(4)%keys(7), stat = alloc)
        drumNotes(4)%keys = (/ 38, 54, 56, 57, 69, 70, 75 /)

     !  5.
        drumNotes(5)%tableNum = 93
        drumNotes(5)%channel = 2
        drumNotes(5)%note = 0
        allocate(drumNotes(5)%keys(3), stat = alloc)
        drumNotes(5)%keys = (/ 37, 53, 59 /)

     !  6.
        drumNotes(6)%tableNum = 94
        drumNotes(6)%channel = 3
        drumNotes(6)%note = 0
        allocate(drumNotes(6)%keys(8), stat = alloc)
        drumNotes(6)%keys = (/ 39, 48, 57, 60, 62, 67, 71, 80 /)

     !  7.
        drumNotes(7)%tableNum = 95
        drumNotes(7)%channel = 3
        drumNotes(7)%note = 1
        allocate(drumNotes(7)%keys(3), stat = alloc)
        drumNotes(7)%keys = (/ 40, 49, 61, 63, 68, 72, 81 /)
    end subroutine
end module
