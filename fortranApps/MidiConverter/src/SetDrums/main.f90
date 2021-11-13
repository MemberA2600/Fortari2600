    include "modules/drumSet.f90"

program SetDrums
    use DrumSetModule

    implicit none

    character(1) :: dummy
    character(:), allocatable :: tempPath
    integer :: io, num, num2, num3, fileLen
    type(drumNote), dimension(7) :: drumNotes
    logical :: found

    integer :: velocity, time, note

    tempPath = "temp/"
    call drumsInit(drumNotes)

    fileLen = 0
    open(unit=11, file=tempPath // "Input.txt")
    open(unit=12, file=tempPath // "Output.txt")

    do
        read(11, "(A)", iostat=io) dummy
        if (io /= 0) exit
        if (dummy == " ") exit

        fileLen = fileLen + 1

    end do
    rewind(11)

    do num = 1, fileLen, 1
        read(11, *) velocity, note, time

        found = .FALSE.
        do num2 = 1, 7, 1
            do num3 = 1, size(drumNotes(num2)%keys), 1
                if (drumNotes(num2)%keys(num3) == note) then
                    found = .TRUE.
                    exit
                end if
            end do
            if (found .EQV. .TRUE.) exit
        end do
        write(12, "(I0, 1x, I0, 1x, I0, 1x, I0, 1x, I0)") velocity, drumNotes(num2)%tableNum, &
        & time, drumNotes(num2)%channel, drumNotes(num2)%note

    end do

    close(11)
    close(12)
end program

