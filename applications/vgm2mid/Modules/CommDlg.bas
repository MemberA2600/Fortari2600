Attribute VB_Name = "CommDlg"
Option Explicit

' *   commdlg.bas -- This module defines the 32-Bit Common Dialog APIs      *

Public Const WM_USER = &H400

Public Const LF_FACESIZE = 32

Type LOGFONT
    lfHeight As Long
    lfWidth As Long
    lfEscapement As Long
    lfOrientation As Long
    lfWeight As Long
    lfItalic As Byte
    lfUnderline As Byte
    lfStrikeOut As Byte
    lfCharSet As Byte
    lfOutPrecision As Byte
    lfClipPrecision As Byte
    lfQuality As Byte
    lfPitchAndFamily As Byte
    lfFaceName(LF_FACESIZE) As Byte
End Type

Type POINTAPI
    x As Long
    y As Long
End Type

Type RECT
    Left As Long
    Top As Long
    Right As Long
    Bottom As Long
End Type

Type OPENFILENAME
    lStructSize As Long
    hwndOwner As Long
    hInstance As Long
    lpstrFilter As String
    lpstrCustomFilter As String
    nMaxCustFilter As Long
    nFilterIndex As Long
    lpstrFile As String
    nMaxFile As Long
    lpstrFileTitle As String
    nMaxFileTitle As Long
    lpstrInitialDir As String
    lpstrTitle As String
    flags As Long
    nFileOffset As Integer
    nFileExtension As Integer
    lpstrDefExt As String
    lCustData As Long
    lpfnHook As Long
    lpTemplateName As String
End Type

Declare Function GetOpenFileName Lib "comdlg32.dll" Alias "GetOpenFileNameA" (pOpenfilename As OPENFILENAME) As Long

Declare Function GetSaveFileName Lib "comdlg32.dll" Alias "GetSaveFileNameA" (pOpenfilename As OPENFILENAME) As Long

Declare Function GetFileTitle Lib "comdlg32.dll" Alias "GetFileTitleA" (ByVal lpszFile As String, ByVal lpszTitle As String, ByVal cbBuf As Integer) As Integer

Public Const OFN_READONLY = &H1
Public Const OFN_OVERWRITEPROMPT = &H2
Public Const OFN_HIDEREADONLY = &H4
Public Const OFN_NOCHANGEDIR = &H8
Public Const OFN_SHOWHELP = &H10
Public Const OFN_ENABLEHOOK = &H20
Public Const OFN_ENABLETEMPLATE = &H40
Public Const OFN_ENABLETEMPLATEHANDLE = &H80
Public Const OFN_NOVALIDATE = &H100
Public Const OFN_ALLOWMULTISELECT = &H200
Public Const OFN_EXTENSIONDIFFERENT = &H400
Public Const OFN_PATHMUSTEXIST = &H800
Public Const OFN_FILEMUSTEXIST = &H1000
Public Const OFN_CREATEPROMPT = &H2000
Public Const OFN_SHAREAWARE = &H4000
Public Const OFN_NOREADONLYRETURN = &H8000
Public Const OFN_NOTESTFILECREATE = &H10000
Public Const OFN_NONETWORKBUTTON = &H20000
Public Const OFN_NOLONGNAMES = &H40000                      '  force no long names for 4.x modules
Public Const OFN_EXPLORER = &H80000                         '  new look commdlg
Public Const OFN_NODEREFERENCELINKS = &H100000
Public Const OFN_LONGNAMES = &H200000                       '  force long names for 3.x modules

Public Const OFN_SHAREFALLTHROUGH = 2
Public Const OFN_SHARENOWARN = 1
Public Const OFN_SHAREWARN = 0

Type NMHDR
    hwndFrom As Long
    idfrom As Long
    code As Long
End Type

Type OFNOTIFY
    hdr As NMHDR
    lpOFN As OPENFILENAME
    pszFile As String        '  May be NULL
End Type

Public Const CDM_FIRST = (WM_USER + 100)
Public Const CDM_LAST = (WM_USER + 200)
Public Const CDM_GETSPEC = (CDM_FIRST + &H0)
Public Const CDM_GETFILEPATH = (CDM_FIRST + &H1)
Public Const CDM_GETFOLDERPATH = (CDM_FIRST + &H2)
Public Const CDM_GETFOLDERIDLIST = (CDM_FIRST + &H3)
Public Const CDM_SETCONTROLTEXT = (CDM_FIRST + &H4)
Public Const CDM_HIDECONTROL = (CDM_FIRST + &H5)
Public Const CDM_SETDEFEXT = (CDM_FIRST + &H6)

Type ChooseColor
    lStructSize As Long
    hwndOwner As Long
    hInstance As Long
    rgbResult As Long
    lpCustColors As Long
    flags As Long
    lCustData As Long
    lpfnHook As Long
    lpTemplateName As String
End Type

Declare Function ChooseColor Lib "comdlg32.dll" Alias "ChooseColorA" (pChoosecolor As ChooseColor) As Long

Public Const CC_RGBINIT = &H1
Public Const CC_FULLOPEN = &H2
Public Const CC_PREVENTFULLOPEN = &H4
Public Const CC_SHOWHELP = &H8
Public Const CC_ENABLEHOOK = &H10
Public Const CC_ENABLETEMPLATE = &H20
Public Const CC_ENABLETEMPLATEHANDLE = &H40
Public Const CC_SOLIDCOLOR = &H80
Public Const CC_ANYCOLOR = &H100

Type FINDREPLACE
    lStructSize As Long        '  size of this struct 0x20
    hwndOwner As Long          '  handle to owner's window
    hInstance As Long          '  instance handle of.EXE that
                                '    contains cust. dlg. template
    flags As Long              '  one or more of the FR_??
    lpstrFindWhat As String      '  ptr. to search string
    lpstrReplaceWith As String   '  ptr. to replace string
    wFindWhatLen As Integer       '  size of find buffer
    wReplaceWithLen As Integer    '  size of replace buffer
    lCustData As Long          '  data passed to hook fn.
    lpfnHook As Long            '  ptr. to hook fn. or NULL
    lpTemplateName As String     '  custom template name
End Type

Public Const FR_DOWN = &H1
Public Const FR_WHOLEWORD = &H2
Public Const FR_MATCHCASE = &H4
Public Const FR_FINDNEXT = &H8
Public Const FR_REPLACE = &H10
Public Const FR_REPLACEALL = &H20
Public Const FR_DIALOGTERM = &H40
Public Const FR_SHOWHELP = &H80
Public Const FR_ENABLEHOOK = &H100
Public Const FR_ENABLETEMPLATE = &H200
Public Const FR_NOUPDOWN = &H400
Public Const FR_NOMATCHCASE = &H800
Public Const FR_NOWHOLEWORD = &H1000
Public Const FR_ENABLETEMPLATEHANDLE = &H2000
Public Const FR_HIDEUPDOWN = &H4000
Public Const FR_HIDEMATCHCASE = &H8000
Public Const FR_HIDEWHOLEWORD = &H10000

Declare Function FindText Lib "comdlg32.dll" Alias "FindTextA " (pFindreplace As FINDREPLACE) As Long

Declare Function ReplaceText Lib "comdlg32.dll" Alias "ReplaceTextA" (pFindreplace As FINDREPLACE) As Long

Type ChooseFont
    lStructSize As Long
    hwndOwner As Long          '  caller's window handle
    hdc As Long                '  printer DC/IC or NULL
    lpLogFont As LOGFONT          '  ptr. to a LOGFONT struct
    iPointSize As Long         '  10 * size in points of selected font
    flags As Long              '  enum. type flags
    rgbColors As Long          '  returned text color
    lCustData As Long          '  data passed to hook fn.
    lpfnHook As Long           '  ptr. to hook function
    lpTemplateName As String     '  custom template name
    hInstance As Long          '  instance handle of.EXE that
                                   '    contains cust. dlg. template
    lpszStyle As String          '  return the style field here
                                   '  must be LF_FACESIZE or bigger
    nFontType As Integer          '  same value reported to the EnumFonts
                                   '    call back with the extra FONTTYPE_
                                   '    bits added
    MISSING_ALIGNMENT As Integer
    nSizeMin As Long           '  minimum pt size allowed &
    nSizeMax As Long           '  max pt size allowed if
                                   '    CF_LIMITSIZE is used
End Type

Declare Function ChooseFont Lib "comdlg32.dll" Alias "ChooseFontA" (pChoosefont As ChooseFont) As Long

Public Const CF_SCREENFONTS = &H1
Public Const CF_PRINTERFONTS = &H2
Public Const CF_BOTH = (CF_SCREENFONTS Or CF_PRINTERFONTS)
Public Const CF_SHOWHELP = &H4&
Public Const CF_ENABLEHOOK = &H8&
Public Const CF_ENABLETEMPLATE = &H10&
Public Const CF_ENABLETEMPLATEHANDLE = &H20&
Public Const CF_INITTOLOGFONTSTRUCT = &H40&
Public Const CF_USESTYLE = &H80&
Public Const CF_EFFECTS = &H100&
Public Const CF_APPLY = &H200&
Public Const CF_ANSIONLY = &H400&
Public Const CF_SCRIPTSONLY = CF_ANSIONLY
Public Const CF_NOVECTORFONTS = &H800&
Public Const CF_NOOEMFONTS = CF_NOVECTORFONTS
Public Const CF_NOSIMULATIONS = &H1000&
Public Const CF_LIMITSIZE = &H2000&
Public Const CF_FIXEDPITCHONLY = &H4000&
Public Const CF_WYSIWYG = &H8000 '  must also have CF_SCREENFONTS CF_PRINTERFONTS
Public Const CF_FORCEFONTEXIST = &H10000
Public Const CF_SCALABLEONLY = &H20000
Public Const CF_TTONLY = &H40000
Public Const CF_NOFACESEL = &H80000
Public Const CF_NOSTYLESEL = &H100000
Public Const CF_NOSIZESEL = &H200000
Public Const CF_SELECTSCRIPT = &H400000
Public Const CF_NOSCRIPTSEL = &H800000
Public Const CF_NOVERTFONTS = &H1000000

Public Const SIMULATED_FONTTYPE = &H8000
Public Const PRINTER_FONTTYPE = &H4000
Public Const SCREEN_FONTTYPE = &H2000
Public Const BOLD_FONTTYPE = &H100
Public Const ITALIC_FONTTYPE = &H200
Public Const REGULAR_FONTTYPE = &H400

Public Const WM_CHOOSEFONT_GETLOGFONT = (WM_USER + 1)
Public Const WM_CHOOSEFONT_SETLOGFONT = (WM_USER + 101)
Public Const WM_CHOOSEFONT_SETFLAGS = (WM_USER + 102)

Public Const LBSELCHSTRING = "commdlg_LBSelChangedNotify"
Public Const SHAREVISTRING = "commdlg_ShareViolation"
Public Const FILEOKSTRING = "commdlg_FileNameOK"
Public Const COLOROKSTRING = "commdlg_ColorOK"
Public Const SETRGBSTRING = "commdlg_SetRGBColor"
Public Const HELPMSGSTRING = "commdlg_help"
Public Const FINDMSGSTRING = "commdlg_FindReplace"

Public Const CD_LBSELNOITEMS = -1
Public Const CD_LBSELCHANGE = 0
Public Const CD_LBSELSUB = 1
Public Const CD_LBSELADD = 2

Type PrintDlg
    lStructSize As Long
    hwndOwner As Long
    hDevMode As Long
    hDevNames As Long
    hdc As Long
    flags As Long
    nFromPage As Integer
    nToPage As Integer
    nMinPage As Integer
    nMaxPage As Integer
    nCopies As Integer
    hInstance As Long
    lCustData As Long
    lpfnPrintHook As Long
    lpfnSetupHook As Long
    lpPrintTemplateName As String
    lpSetupTemplateName As String
    hPrintTemplate As Long
    hSetupTemplate As Long
End Type

Declare Function PrintDlg Lib "comdlg32.dll" Alias "PrintDlgA" (pPrintdlg As PrintDlg) As Long

Public Const PD_ALLPAGES = &H0
Public Const PD_SELECTION = &H1
Public Const PD_PAGENUMS = &H2
Public Const PD_NOSELECTION = &H4
Public Const PD_NOPAGENUMS = &H8
Public Const PD_COLLATE = &H10
Public Const PD_PRINTTOFILE = &H20
Public Const PD_PRINTSETUP = &H40
Public Const PD_NOWARNING = &H80
Public Const PD_RETURNDC = &H100
Public Const PD_RETURNIC = &H200
Public Const PD_RETURNDEFAULT = &H400
Public Const PD_SHOWHELP = &H800
Public Const PD_ENABLEPRINTHOOK = &H1000
Public Const PD_ENABLESETUPHOOK = &H2000
Public Const PD_ENABLEPRINTTEMPLATE = &H4000
Public Const PD_ENABLESETUPTEMPLATE = &H8000
Public Const PD_ENABLEPRINTTEMPLATEHANDLE = &H10000
Public Const PD_ENABLESETUPTEMPLATEHANDLE = &H20000
Public Const PD_USEDEVMODECOPIES = &H40000
Public Const PD_USEDEVMODECOPIESANDCOLLATE = &H40000
Public Const PD_DISABLEPRINTTOFILE = &H80000
Public Const PD_HIDEPRINTTOFILE = &H100000
Public Const PD_NONETWORKBUTTON = &H200000

Type DEVNAMES
    wDriverOffset As Integer
    wDeviceOffset As Integer
    wOutputOffset As Integer
    wDefault As Integer
End Type

Public Const DN_DEFAULTPRN = &H1

Declare Function CommDlgExtendedError Lib "comdlg32.dll" () As Long

Public Const WM_PSD_PAGESETUPDLG = (WM_USER)
Public Const WM_PSD_FULLPAGERECT = (WM_USER + 1)
Public Const WM_PSD_MINMARGINRECT = (WM_USER + 2)
Public Const WM_PSD_MARGINRECT = (WM_USER + 3)
Public Const WM_PSD_GREEKTEXTRECT = (WM_USER + 4)
Public Const WM_PSD_ENVSTAMPRECT = (WM_USER + 5)
Public Const WM_PSD_YAFULLPAGERECT = (WM_USER + 6)

Type PageSetupDlg
    lStructSize As Long
    hwndOwner As Long
    hDevMode As Long
    hDevNames As Long
    flags As Long
    ptPaperSize As POINTAPI
    rtMinMargin As RECT
    rtMargin As RECT
    hInstance As Long
    lCustData As Long
    lpfnPageSetupHook As Long
    lpfnPagePaintHook As Long
    lpPageSetupTemplateName As String
    hPageSetupTemplate As Long
End Type

Declare Function PageSetupDlg Lib "comdlg32.dll" Alias "PageSetupDlgA" (pPagesetupdlg As PageSetupDlg) As Long

Public Const PSD_DEFAULTMINMARGINS = &H0 '  default (printer's)
Public Const PSD_INWININIINTLMEASURE = &H0 '  1st of 4 possible

Public Const PSD_MINMARGINS = &H1 '  use caller's
Public Const PSD_MARGINS = &H2 '  use caller's
Public Const PSD_INTHOUSANDTHSOFINCHES = &H4 '  2nd of 4 possible
Public Const PSD_INHUNDREDTHSOFMILLIMETERS = &H8 '  3rd of 4 possible
Public Const PSD_DISABLEMARGINS = &H10
Public Const PSD_DISABLEPRINTER = &H20
Public Const PSD_NOWARNING = &H80 '  must be same as PD_*
Public Const PSD_DISABLEORIENTATION = &H100
Public Const PSD_RETURNDEFAULT = &H400 '  must be same as PD_*
Public Const PSD_DISABLEPAPER = &H200
Public Const PSD_SHOWHELP = &H800 '  must be same as PD_*
Public Const PSD_ENABLEPAGESETUPHOOK = &H2000 '  must be same as PD_*
Public Const PSD_ENABLEPAGESETUPTEMPLATE = &H8000 '  must be same as PD_*
Public Const PSD_ENABLEPAGESETUPTEMPLATEHANDLE = &H20000 '  must be same as PD_*
Public Const PSD_ENABLEPAGEPAINTHOOK = &H40000
Public Const PSD_DISABLEPAGEPAINTING = &H80000
Public Function File_Open(frmForm As Form, strDialogTitle As String, strFileDesc As String, strFileExt As String, Optional strFileDesc_2 As String, Optional strFileExt_2 As String, Optional strFileDesc_3 As String, Optional strFileExt_3 As String) As String
    Dim OFN As OPENFILENAME, lReturn As Long
    Dim strFilename As String
    
    With OFN
        .lStructSize = Len(OFN)
        .hwndOwner = frmForm.hWnd
        .hInstance = App.hInstance
        .lpstrFilter = strFileDesc & Chr(0) & strFileExt & Chr(0) & strFileDesc_2 & Chr(0) & strFileExt_2 & Chr(0) & strFileDesc_3 & Chr(0) & strFileExt_3
        .nFilterIndex = 1
        .lpstrFile = String(257, 0)
        .nMaxFile = Len(.lpstrFile) - 1
        .lpstrFileTitle = .lpstrFile
        .nMaxFileTitle = .nMaxFile
        .lpstrInitialDir = ""
        .lpstrTitle = strDialogTitle
        .flags = OFN_HIDEREADONLY + OFN_PATHMUSTEXIST + OFN_FILEMUSTEXIST ' + OFN_NOLONGNAMES
        .lpstrDefExt = strFileExt
        
        lReturn = GetOpenFileName(OFN)
        If lReturn <> 0 Then
            strFilename = .lpstrFile
            strFilename = Left(strFilename, InStr(1, strFilename, Chr(0)) - 1)
            File_Open = Trim(strFilename)
        Else
            File_Open = ""
        End If
    
    End With

End Function
Public Function File_Save(frmForm As Form, ByVal strDialogTitle As String, ByVal strFileDesc As String, ByVal strFileExt As String, Optional ByVal strFileDesc_2 As String, Optional ByVal strFileExt_2 As String, Optional strFileDesc_3 As String, Optional ByVal strFileExt_3 As String) As String
    Dim OFN As OPENFILENAME, lReturn As Long
    With OFN
        .lStructSize = Len(OFN)
        .hwndOwner = frmForm.hWnd
        .hInstance = App.hInstance
        .lpstrFilter = strFileDesc & Chr(0) & strFileExt & Chr(0) & strFileDesc_2 & Chr(0) & strFileExt_2 & Chr(0) & strFileDesc_3 & Chr(0) & strFileExt_3
        .nFilterIndex = 1
        .lpstrFile = String(257, 0)
        .nMaxFile = Len(.lpstrFile) - 1
        .lpstrFileTitle = .lpstrFile
        .nMaxFileTitle = .nMaxFile
        .lpstrInitialDir = ""
        .lpstrTitle = strDialogTitle
        .flags = OFN_HIDEREADONLY + OFN_PATHMUSTEXIST + OFN_OVERWRITEPROMPT
        .lpstrDefExt = strFileExt
        
        lReturn = GetSaveFileName(OFN)
        If lReturn <> 0 Then
            File_Save = LCase(Trim(.lpstrFile))
        Else
            File_Save = ""
        End If
    
    End With

End Function
