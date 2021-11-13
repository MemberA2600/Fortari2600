module FileExistsModule

    contains
    subroutine fileExists(fname, unittag)
        logical :: ex
        character(:), allocatable, intent(in) :: fname
        integer, intent(in) :: unittag


        inquire(unittag, exist = ex)

        if (ex .EQV. .FALSE.) then
            write(*,*) "'" // fname // "' does not exist!"
            pause
        end if

    end subroutine


end module
