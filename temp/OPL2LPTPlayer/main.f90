module routines
    implicit None
    contains

function convert8to16(byte1, byte2) result(valueWord)
    character(len = 2), intent(in) :: byte1, byte2
    character(4)                   :: word
    integer                        :: valueWord

    word = byte2 // byte1
    read(word, "(Z4)") valueWord

    return

end function

subroutine deleteFile(fname)

    character(*), intent(in) :: fname
    logical :: exists
    integer :: io

    inquire(file=fname, exist = exists)
    if (exists .EQV. .TRUE.) then
       open(unit = 666, iostat=io, file=fname, status='old')
       if (io /= 0) stop "Failed to open existing file: " // fname
       close(666, status='delete')
    end if

end subroutine

function convertHexStringToInt(input) result(output)

    character(*), intent(in) :: input
    integer              :: output
    character(20)        :: txt

    txt = input
    read(input, '(Z20)') output


end function

function getHzOfLine(line) result(hz)
    character(50), intent(in) :: line
    integer(kind = 16) :: hz
    integer :: lastOne, num

    hz      = 0
    lastOne = 0
    do num = 16, 50, 1
       if (line(num:num) == " ") exit
       lastOne = num

    end do

    if (lastOne == 0) stop "Failed to read Hz from line"

    read(line(16:lastOne), "(I16)") hz
    return

end function
end module

module LoadLib
!
! Code is from here: https://stackoverflow.com/questions/14165801/how-to-use-loadlibrary-and-getprocaddress-from-gfortran
!
  implicit none

  INTERFACE
     FUNCTION LoadLibrary(lpFileName) BIND(C,NAME='LoadLibraryA')
        USE, INTRINSIC :: ISO_C_BINDING, ONLY: C_INTPTR_T, C_CHAR
        IMPLICIT NONE
        CHARACTER(KIND=C_CHAR) :: lpFileName(*)
        !GCC$ ATTRIBUTES STDCALL :: LoadLibrary
        INTEGER(C_INTPTR_T) :: LoadLibrary
     END FUNCTION LoadLibrary

     FUNCTION GetProcAddress(hModule, lpProcName)  &
         BIND(C, NAME='GetProcAddress')
       USE, INTRINSIC :: ISO_C_BINDING, ONLY:  &
           C_FUNPTR, C_INTPTR_T, C_CHAR
       IMPLICIT NONE
       !GCC$ ATTRIBUTES STDCALL :: GetProcAddress
       TYPE(C_FUNPTR) :: GetProcAddress
       INTEGER(C_INTPTR_T), VALUE :: hModule
       CHARACTER(KIND=C_CHAR) :: lpProcName(*)
     END FUNCTION GetProcAddress
  END INTERFACE

end module

module detectOsBits

    contains
    function is32or64() result(is_64)
        use iso_c_binding
        implicit none
        type(c_ptr) :: x
        logical     :: is_64

        is_64 = c_sizeof(x) == 8

        return
    end function

end module

module sleeping

    implicit none
    contains

    subroutine sleepMilliseconds(milliseconds)
       real, intent(in) :: milliseconds
       real(kind=4) :: start, finish, temp

       temp = milliseconds / 1000.0

       call cpu_time(start)
       do
            call cpu_time(finish)
            if (finish - start >= temp) exit

       end do

       !print '("Time = ",f6.3," seconds.")',start, finish
    end subroutine

end module

module VGMPlayer
    use, intrinsic :: ISO_C_Binding
    use LoadLib
    use detectOsBits
    use sleeping

    implicit None

    integer :: lptDataPort, lptControlPort
    integer(c_short) :: portAddress, portData

    !!! This part is needed for the LoadLibrary part
    INTEGER(C_INTPTR_T) :: module_handle
    TYPE(C_FUNPTR) :: proc_address, proc_address2, proc_address3

    ABSTRACT INTERFACE
    Subroutine Out32 (PortAddress, portData) BIND(C)
      use, intrinsic :: ISO_C_BINDING
      implicit none
      integer(c_short) :: PortAddress, portData!

    END SUBROUTINE
    END INTERFACE

    ABSTRACT INTERFACE
    function Inp32 (PortAddress) BIND(C) result(portData)
      use, intrinsic :: ISO_C_BINDING
      implicit none
      integer(c_short), intent(in) :: PortAddress
      integer(c_short)             :: portData!

    END function
    END INTERFACE

    ABSTRACT INTERFACE
    function IsInpOutDriverOpen() BIND(C) result(isIt)
      use, intrinsic :: ISO_C_BINDING
      implicit none
      integer(c_bool) :: isIt

    END function
    END INTERFACE
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    PROCEDURE(Out32), BIND(C), POINTER :: doOut32
    PROCEDURE(Inp32),  BIND(C), POINTER :: doInp32
    PROCEDURE(IsInpOutDriverOpen),  BIND(C), POINTER :: isOpen

    contains

    subroutine setPorts(lpt)
        integer :: lpt

        lptDataPort    = lpt
        lptControlPort = lpt +2

    end subroutine

    subroutine getProcPointer()
        if (is32or64() .EQV. .TRUE.) then
        module_handle = LoadLibrary(C_CHAR_'inpoutx64.dll' // C_NULL_CHAR)
        else
        module_handle = LoadLibrary(C_CHAR_'inpout32.dll' // C_NULL_CHAR)
        end if
        IF (module_handle == 0) STOP 'Unable to load DLL'

        proc_address = GetProcAddress( module_handle, C_CHAR_'Out32' // C_NULL_CHAR)
        IF (.NOT. C_ASSOCIATED(proc_address)) STOP 'Unable to obtain procedure address'
        CALL C_F_PROCPOINTER(proc_address, doOut32)

        proc_address2 = GetProcAddress( module_handle, C_CHAR_'Inp32' // C_NULL_CHAR)
        IF (.NOT. C_ASSOCIATED(proc_address2)) STOP 'Unable to obtain procedure address'
        CALL C_F_PROCPOINTER(proc_address2, doInp32)

        proc_address3 = GetProcAddress( module_handle, C_CHAR_'IsInpOutDriverOpen' // C_NULL_CHAR)
        IF (.NOT. C_ASSOCIATED(proc_address2)) STOP 'Unable to obtain procedure address'
        CALL C_F_PROCPOINTER(proc_address3, isOpen)

    end subroutine

    subroutine writeReg(register, dataToWrite)
        use, intrinsic :: ISO_C_Binding
        integer, intent(in) :: register, dataToWrite
        integer           :: num
        integer(c_short) :: port, dat, filler
        integer(kind = 2), dimension(3) :: values

        values = (/ 12, 8, 12 /)

        ! Set register
        port = lptDataPort
        dat  = register
        call doOut32(port, dat)

        ! Select off (1), Strobe-Off (1), init-on-off-on(1-0-1)
        port = lptControlPort
        do num = 1, 3, 1
           dat = values(num) + 1
           call doOut32(port, dat)
        end do

        do num = 1, 6, 1
           filler = doInp32(port)
        end do

        ! Set data
        port = lptDataPort
        dat  = dataToWrite
        call doOut32(port, dat)

        ! Select off (1), Strobe-On (0), init-on-off-on(1-0-1)
        port = lptControlPort
        do num = 1, 3, 1
           call doOut32(port, values(num))
        end do

        do num = 1, 35, 1
           filler = doInp32(port)
        end do

    end subroutine

    subroutine initChip()
        integer reg, dat

        dat = Z'00'
        do reg = z'00', z'FF', z'01'
           call writeReg(reg, dat)
        end do

    end subroutine

    subroutine testPort()
       integer(c_short) :: port, dat
       port  = Z'0378'
       dat   = 255
       call doOut32(port, dat)
       write(*,*) "Test done. All data ports should be set to high."
    end subroutine

end module

program OPL2LPTPlayer
    use, intrinsic :: ISO_C_Binding
    use routines
    use VGMPlayer
    use sleeping
    implicit none

    character(:), allocatable :: fileName, fformat, nameOnly
    integer :: num, ok, io, lineNum, lastLine, lessLines, num2, lptDataAddress
    character(len = 50), dimension(:), allocatable :: dataLines
    character(1) :: dummy
    character(len=10) :: errorNum
    integer(kind = 16) :: YM3812clock, YM3526Clock
    character(len=6) :: IC
    integer, dimension(:,:), allocatable :: bytes
    character(2), dimension(:,:), allocatable :: byteStrings
    integer :: port, dat
    real :: oneSample

    logical :: w

    fileName          = "test.vgz"
    lptDataAddress    = z'0378'

    fformat  = ""
    nameOnly = ""
    lineNum  = 0
    lastLine = 0

    do num = len_trim(fileName), 1, -1
       if (fileName(num:num) == ".") then
          fformat  = fileName(num + 1 : len_trim(fileName))
          nameOnly = fileName(1 : num - 1)

          exit
       end if
    end do

    call execute_command_line("apps\vgm2txt\vgm2txt.exe " // fileName // " 0 0", wait=.TRUE., exitstat = ok)

    if (ok /= 0) stop ("Failed to convert VGM into text: " // fileName)

    open(666, file = nameOnly // ".txt", access = "SEQUENTIAL", action = "READ", iostat = io)

    do
        read(666, '(A)', iostat = io) dummy
        if (io /= 0) exit
        lineNum = lineNum + 1
    end do

    if (lineNum == 0) stop "Failed to read " // nameOnly // ".txt"

    allocate(dataLines(lineNum), stat = io)

    if (io /= 0) stop "Failed allocate array for reading: " // nameOnly // ".txt"

    rewind(666)

    do num = 1, lineNum, 1
       read(666, "(A)") dataLines(num)
       if (io /= 0) then
           write(errorNum, "(A)") num
           stop "Failed to read " // nameOnly // ".txt at line: " // errorNum
       end if

    end do

    close(666, status='delete')

    do num = 2, lineNum, 1
       if (len_trim(dataLines(num)) == 0) exit
       lastLine = num
    end do

    do num = 2, lastLine, 1
       IC = dataLines(num)(1:6)

       select case(IC)
       case("YM3812")
           YM3812clock = getHzOfLine(dataLines(num))
       case("YM3526")
           YM3526clock = getHzOfLine(dataLines(num))
       end select

    end do

    lessLines = 0

    do num = lastLine + 3, lineNum, 1
       select case(dataLines(num)(13:15))
       case("5A")
           lessLines = lessLines + 1
       case("5B")
           lessLines = lessLines + 1
       case("61")
           lessLines = lessLines + 1
       case("62")
           lessLines = lessLines + 1
       case("63")
           lessLines = lessLines + 1
       end select

    end do

    allocate(bytes(lessLines,3), stat = io)
    if (io /= 0) stop "Failed to allocate bytes array!"

    allocate(byteStrings(lessLines,3), stat = io)
    if (io /= 0) stop "Failed to allocate bytes array!"

    num2 = 0

    do num = lastLine + 3, lineNum, 1
       w = .FALSE.

       select case(dataLines(num)(13:15))
       case("5A")
           w = .TRUE.
       case("5B")
           w = .TRUE.
       case("61")
           w = .TRUE.
       case("62")
           w = .TRUE.
       case("63")
           w = .TRUE.
       end select

       if (w .EQV. .TRUE.) then
          num2 = num2 + 1
          read(dataLines(num)(13:20), "(Z2, X, Z2, X, Z2)") bytes(num2, 1), bytes(num2, 2), bytes(num2, 3)
          read(dataLines(num)(13:20), "(A2, X, A2, X, A2)") byteStrings(num2, 1), byteStrings(num2, 2), byteStrings(num2, 3)
       end if

    end do

    deallocate(dataLines)

    call setPorts(lptDataAddress)
    call getProcPointer()
    call initChip()

    oneSample = 1487.0/65535.0

    do num = 1, lessLines, 1
       !write(*,*) num, byteStrings(num, 1), byteStrings(num, 2), byteStrings(num, 3)
       select case(byteStrings(num,1))
       case("5A")
           call writeReg(bytes(num, 2), bytes(num, 3))
       case("5B")
           call writeReg(bytes(num, 2), bytes(num, 3))
       case("61")
       !    write(*,*) oneSample * convert8to16(byteStrings(num, 2), byteStrings(num, 3))

           call sleepMilliseconds(oneSample * convert8to16(byteStrings(num, 2), byteStrings(num, 3)))
       case("62")
           call sleepMilliseconds(oneSample * 735)
       case("63")
           call sleepMilliseconds(oneSample * 882)
       end select

    end do
    call initChip()

    write(*,"(L)") isOpen()
    call testPort()

end program

