VERSION 5.00
Begin VB.Form frmMain 
   BorderStyle     =   1  'Fest Einfach
   Caption         =   "vgm2mid"
   ClientHeight    =   3015
   ClientLeft      =   150
   ClientTop       =   720
   ClientWidth     =   7470
   Icon            =   "frmMain.frx":0000
   LinkTopic       =   "frmMain"
   MaxButton       =   0   'False
   ScaleHeight     =   3015
   ScaleWidth      =   7470
   StartUpPosition =   3  'Windows-Standard
   Begin VB.CommandButton cmdConvertAll 
      Caption         =   "Con&vert All"
      Enabled         =   0   'False
      Height          =   375
      Left            =   6000
      TabIndex        =   4
      Top             =   2520
      Width           =   1335
   End
   Begin VB.CommandButton cmdConvert 
      Caption         =   "&Convert"
      Enabled         =   0   'False
      Height          =   375
      Left            =   6000
      TabIndex        =   6
      Top             =   2040
      Width           =   1335
   End
   Begin VB.ListBox lstVGM 
      Height          =   2790
      Left            =   120
      Sorted          =   -1  'True
      TabIndex        =   5
      Top             =   120
      Width           =   5775
   End
   Begin VB.CommandButton cmdRemoveAll 
      Caption         =   "R&emove All"
      Enabled         =   0   'False
      Height          =   375
      Left            =   6000
      TabIndex        =   3
      Top             =   1560
      Width           =   1335
   End
   Begin VB.CommandButton cmdAddDirectory 
      Caption         =   "Add &Directory..."
      Height          =   375
      Left            =   6000
      TabIndex        =   1
      Top             =   600
      Width           =   1335
   End
   Begin VB.Timer tmrConversionStatus 
      Enabled         =   0   'False
      Interval        =   50
      Left            =   6000
      Top             =   2520
   End
   Begin VB.CommandButton cmdRemove 
      Caption         =   "&Remove"
      Enabled         =   0   'False
      Height          =   375
      Left            =   6000
      TabIndex        =   2
      Top             =   1080
      Width           =   1335
   End
   Begin VB.CommandButton cmdAdd 
      Caption         =   "&Add File..."
      Height          =   375
      Left            =   6000
      TabIndex        =   0
      Top             =   120
      Width           =   1335
   End
   Begin VB.Menu mnuFile 
      Caption         =   "&File"
      Begin VB.Menu mnuFileExit 
         Caption         =   "E&xit"
      End
   End
   Begin VB.Menu mnuTools 
      Caption         =   "&Tools"
      Begin VB.Menu mnuToolsOptions 
         Caption         =   "&Options..."
      End
   End
   Begin VB.Menu mnuHelp 
      Caption         =   "&Help"
      Begin VB.Menu mnuHelpAbout 
         Caption         =   "&About..."
      End
   End
   Begin VB.Menu mnulstVGMPopup 
      Caption         =   "mnulstVGMPopup"
      Visible         =   0   'False
      Begin VB.Menu mnulstVGMPopupConvert 
         Caption         =   "&Convert"
      End
      Begin VB.Menu mnuSeperator 
         Caption         =   "-"
      End
      Begin VB.Menu mnulstVGMPopupRemove 
         Caption         =   "&Remove"
      End
   End
End
Attribute VB_Name = "frmMain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
Function Pathname(ByVal strFullPath As String) As String
    Dim lngPathOffset As Long
    Do
        lngPathOffset = lngPathOffset + 1
    Loop Until InStr(1, Right(strFullPath, lngPathOffset), "\") = 1
    Pathname = Left(strFullPath, Len(strFullPath) - lngPathOffset) & "\"
End Function

Public Function VGM_Convert(ByVal intListIndex As Integer) As Long
    Dim intConv As Integer, intConvFrom As Integer, intConvTo As Integer
    Dim strFilename As String, strFileExt As String, lngReturn As Long
    Dim strMIDFilename As String
    
    On Error GoTo ErrHandler
    
    Dim ctlControl As Control
    For Each ctlControl In frmMain.Controls
        ctlControl.Enabled = False
    Next ctlControl
    
    Me.MousePointer = vbHourglass
    
    frmOptions.Options_Set_All
    
    ' it's called from ConvertVGMtoMID
    'tmrConversionStatus.Enabled = True
    
    Dim vgmConv() As New VGM, bytConvFlag() As Byte
    Dim intCnt As Integer
    
    If intListIndex = -1 Then
        ReDim vgmConv(lstVGM.ListCount - 1)
        ReDim bytConvFlag(lstVGM.ListCount - 1)
        For intCnt = 0 To UBound(vgmConv)
            lngReturn = _
            vgmConv(intCnt).OpenFile(lstVGM.List(intCnt))
            If lngReturn <> 0 Then GoTo ErrHandler
            bytConvFlag(intCnt) = 1
        Next
    Else
        ReDim vgmConv(intListIndex)
        ReDim bytConvFlag(intListIndex)
        lngReturn = _
        vgmConv(intListIndex).OpenFile(lstVGM.List(intListIndex))
        If lngReturn <> 0 Then GoTo ErrHandler
        bytConvFlag(intListIndex) = 1
    End If
    
    For intCnt = 0 To UBound(vgmConv)
        If bytConvFlag(intCnt) = 1 Then
            Variables_Clear_PSG = 1
            Variables_Clear_YM2413 = 1
            Variables_Clear_YM2612 = 1
            Variables_Clear_YM2151 = 1
            
            With vgmConv(intCnt)
                MID_File_Init
                Select Case .FileExt
                Case "vgm", "vgz", "gym"
                    lstVGM.List(intCnt) = .Filename & " - Converting..."
                    .ConvertToMID
                    lstVGM.List(intCnt) = .Filename & " - Converting...Done."
                Case Else
                    MsgBox "Invalid file format.", vbCritical: GoTo ErrHandler
                End Select
                'strMIDFilename = Left(.FullPathname, InStr(1, .FullPathname, .FileExt) - 1) & "mid"
                strMIDFilename = Left(.FullPathname, InStrRev(.FullPathname, .FileExt) - 1) & "mid"
                If strMIDFilename = "" Then GoTo ErrHandler
                MID_File_Write (strMIDFilename)
            End With
            Set vgmConv(intCnt) = Nothing
        End If
    Next

    If intListIndex = -1 Then
        lstVGM.Clear
    Else
        lstVGM.RemoveItem (intListIndex)
    End If

ResetControls:
    For Each ctlControl In frmMain.Controls
        ctlControl.Enabled = True
    Next ctlControl
    cmdRemove.Enabled = IIf(lstVGM.ListIndex = -1, False, True)
    cmdRemoveAll.Enabled = IIf(lstVGM.ListCount = 0, False, True)
    cmdConvert.Enabled = IIf(lstVGM.ListIndex = -1, False, True)
    cmdConvertAll.Enabled = IIf(lstVGM.ListCount = 0, False, True)
    
    Me.MousePointer = vbNormal
    
    tmrConversionStatus.Enabled = False
    Me.Caption = "vgm2mid"
    
    Exit Function

ErrHandler:
    Dim strPrompt As String
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'"
    MsgBox strPrompt, vbCritical
    VGM_Convert = 255
    GoTo ResetControls
End Function
Private Sub cmdAdd_Click()
    Dim strFilename As String, lngReturn As Long
 
    strFilename = Trim(File_Open(Me, "Please select a file", _
    "All Supported Files", "*.vgm;*.gym;*.vgz;*.vgm.gz", _
    "VGM Log (*.vgm;*.vgz;*.vgm.gz)", "*.vgm;*.vgz;*.vgm.gz", _
    "GYM Log (*.gym)", "*.gym*"))
    If strFilename = "" Then Exit Sub
    
    With lstVGM
        .AddItem strFilename, .ListCount
    End With
    
    If lstVGM.ListCount > 0 Then
        cmdConvertAll.Enabled = True
        cmdRemoveAll.Enabled = True
    Else
        cmdConvertAll.Enabled = False
        cmdRemoveAll.Enabled = False
    End If

End Sub
Private Sub cmdAddDirectory_Click()
    Dim strFilename As String, strFileExt As String, lngReturn As Long
 
    strFilename = Trim(File_Open(Me, _
    "Please select a file in the desired directory", _
    "All Supported Files", "*.vgm;*.gym;*.vgz", _
    "VGM Log (*.vgm;*.vgz)", "*.vgm;*.vgz", _
    "GYM Log (*.gym)", "*.gym*"))
    If strFilename = "" Then Exit Sub
    
    Dim NewVGM As New VGM
    lngReturn = NewVGM.OpenFile(strFilename)
    If lngReturn <> 0 Then
        MsgBox "Error", vbCritical: Exit Sub
    End If
    With NewVGM
        strFilename = Dir(.Pathname & "\*." & .FileExt)
        Do Until strFilename = ""
            If strFilename <> "" Then lstVGM.AddItem .Pathname & "\" & strFilename
            strFilename = Dir()
        Loop
    End With
    Set NewVGM = Nothing
    
    If lstVGM.ListCount > 0 Then
        cmdConvertAll.Enabled = True
        cmdRemoveAll.Enabled = True
    Else
        cmdConvertAll.Enabled = False
        cmdRemoveAll.Enabled = False
    End If

End Sub
Private Sub cmdConvert_Click()
    Dim lngReturn As Long
    lngReturn = VGM_Convert(lstVGM.ListIndex)
End Sub
Private Sub cmdConvertAll_Click()
    Dim lngReturn As Long
    lngReturn = VGM_Convert(-1)
End Sub
Private Sub cmdRemove_Click()
    With lstVGM
        If .ListIndex <> -1 Then .RemoveItem (.ListIndex)
        If .ListCount > 0 Then
            cmdConvert.Enabled = IIf(.ListIndex = -1, False, True)
            cmdConvertAll.Enabled = True
            cmdRemove.Enabled = IIf(.ListIndex = -1, False, True)
            cmdRemoveAll.Enabled = True
        Else
            cmdConvert.Enabled = False
            cmdConvertAll.Enabled = False
            cmdRemove.Enabled = False
            cmdRemoveAll.Enabled = False
        End If
    End With
End Sub
Private Sub cmdRemoveAll_Click()
    lstVGM.Clear
    cmdRemove.Enabled = False
    cmdRemoveAll.Enabled = False
    cmdConvert.Enabled = False
    cmdConvertAll.Enabled = False
End Sub


Private Sub Form_Initialize()
    If App.PrevInstance Then End
End Sub

Private Sub Form_Load()
    Load frmOptions
End Sub

Private Sub Form_Unload(Cancel As Integer)
    Unload frmOptions
    If Me.MousePointer = vbHourglass Then
        End
    End If
End Sub


Private Sub lstVGM_MouseDown(Button As Integer, Shift As Integer, X As Single, Y As Single)
    If lstVGM.ListIndex <> -1 Then
        cmdRemove.Enabled = True
        cmdConvert.Enabled = True
        mnulstVGMPopupConvert.Enabled = True
        mnulstVGMPopupRemove.Enabled = True
    Else
        cmdRemove.Enabled = False
        cmdConvert.Enabled = False
        mnulstVGMPopupConvert.Enabled = False
        mnulstVGMPopupRemove.Enabled = False
    End If
End Sub
Private Sub lstVGM_MouseUp(Button As Integer, Shift As Integer, X As Single, Y As Single)
'    If Button = vbRightButton Then
'        Me.PopupMenu mnulstVGMPopup, , X, Y, mnulstVGMPopupConvert
'    End If
End Sub
Private Sub mnuFileExit_Click()
    End
End Sub

Private Sub mnuHelpAbout_Click()
    Dim Prompt As String
    Prompt = App.ProductName & " Version " & App.Major & "." & App.Minor & " Revision " & App.Revision & " (" & FileDateTime(App.Path & "\" & App.EXEName & ".exe") & ")"
    Prompt = Prompt & vbCrLf & App.FileDescription
    Prompt = Prompt & vbCrLf & "Created by " & App.CompanyName
    Prompt = Prompt & vbCrLf & "Updated by Valley Bell to support VGM version 1.51"
    Prompt = Prompt & vbCrLf & App.Comments
    MsgBox Prompt, vbOKOnly + vbInformation + vbApplicationModal + vbMsgBoxSetForeground, "About " & App.ProductName
End Sub

Private Sub mnulstVGMPopupConvert_Click()
    cmdConvert_Click
End Sub

Private Sub mnulstVGMPopupRemove_Click()
    cmdRemove_Click
End Sub


Private Sub mnuToolsOptions_Click()
    frmOptions.Show vbModal, Me
End Sub


Public Sub tmrConversionStatus_Timer()
    Dim Percent_Complete As Single
    
    If Conversion_Status_Total <> 0 Then Percent_Complete = Conversion_Status_Current / Conversion_Status_Total
    Me.Caption = "vgm2mid - converting file... (" & Format$(Percent_Complete, "0.0 %") & " completed)"
    'DoEvents
End Sub
