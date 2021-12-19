Attribute VB_Name = "basVGM"
Option Explicit

Private Type VGM_HEADER_TYPE
    VGM As String * 4
    LenOffset As Long
    Version As Long
    HzPSG As Long
    HzFM As Long
    GD3Offset As Long
    TotalSamples As Long
    LoopOffset As Long
    LoopSamples As Long
    Reserved As String * 28
End Type

Public VGMHeaderData As VGM_HEADER_TYPE
    
' VGM Command Constants
Public Const GG_PSG_STEREO = &H4F
Public Const PSG = &H50
Public Const YM2413 = &H51
Public Const YM2612_P0 = &H52
Public Const YM2612_P1 = &H53
Public Const YM2151 = &H54
Public Const WAIT_N_SAMPLES = &H61
Public Const WAIT_735_SAMPLES = &H62
Public Const WAIT_882_SAMPLES = &H63
Public Const END_OF_SOUND_DATA = &H66

' VGM Sound Data
Public VGMSoundData() As Byte
Public Sub VGM_File_Interpret()

    Dim filePos As Long
    Dim chrCommand As Byte, chrPort As Byte, chrRegister As Byte, chrData As Byte
    Dim Wait As Double

    Dim debugText As String, debugFilePos As Long
    
'    If Dir("c:\windows\temp\debug.txt") <> "" Then Kill ("c:\windows\temp\debug.txt")

    Conversion_Status_Current = 0
    Conversion_Status_Total = UBound(VGMSoundData)

    On Error GoTo ErrHandler

    Do
        chrCommand = VGMSoundData(filePos)
        Select Case chrCommand
        Case GG_PSG_STEREO
            chrData = VGMSoundData(filePos + 1)
'            debugText = "Game Gear Stereo: " & Hex(chrData)
            filePos = filePos + 2
        Case PSG
            chrData = VGMSoundData(filePos + 1)
            Select Case (chrData And PSG_CHANNEL_SELECT)
            Case PSG_TONE_1, PSG_TONE_2, PSG_TONE_3
                PSGCommand_Handle chrData, VGMSoundData(filePos + 3)
                filePos = filePos + 4
            Case Else
                PSGCommand_Handle VGMSoundData(filePos + 1), 0
                filePos = filePos + 2
            End Select
        Case YM2413
            chrRegister = VGMSoundData(filePos + 1)
            chrData = VGMSoundData(filePos + 2)
            YM2413Command_Handle chrRegister, chrData
            filePos = filePos + 3
        Case YM2612_P0
            chrPort = 0
            chrRegister = VGMSoundData(filePos + 1)
            chrData = VGMSoundData(filePos + 2)
            If chrRegister <> YM2612_DAC Then YM2612Command_Handle chrPort, chrRegister, chrData
            filePos = filePos + 3
        Case YM2612_P1
            chrPort = 3
            chrRegister = VGMSoundData(filePos + 1)
            chrData = VGMSoundData(filePos + 2)
            If chrRegister <> YM2612_DAC Then YM2612Command_Handle chrPort, chrRegister, chrData
            filePos = filePos + 3
        Case YM2151
            chrRegister = VGMSoundData(filePos + 1)
            chrData = VGMSoundData(filePos + 2)
'            debugText = "YM2151: " & chrRegister & ", " & chrData
            filePos = filePos + 3
        Case WAIT_N_SAMPLES
            Wait = VGMSoundData(filePos + 2)
            Wait = Wait * 256
            Wait = Wait + VGMSoundData(filePos + 1)
            DeltaTime = DeltaTime + (1 * (Wait / 735))
            'DeltaTime = DeltaTime + (1 * (Wait / 882))
'            debugText = "Wait " & Wait & " samples"
            filePos = filePos + 3
        Case WAIT_735_SAMPLES
            Wait = 735
            DeltaTime = DeltaTime + 1
'            debugText = "Wait " & Wait & " samples"
            filePos = filePos + 1
        Case WAIT_882_SAMPLES
            Wait = 882
            DeltaTime = DeltaTime + 1
'            debugText = "Wait " & Wait & " samples"
            filePos = filePos + 1
        Case END_OF_SOUND_DATA
            Exit Do
        Case Else
            filePos = filePos + 1
        End Select
    
'        debugText = debugText & vbCrLf
    
'        Open "c:\windows\temp\debug.txt" For Binary As 1
'            Put 1, 1 + debugFilePos, debugText
'        Close
        
'        debugFilePos = debugFilePos + Len(debugText)
'        debugText = ""
        
        Conversion_Status_Current = filePos
        DoEvents
    
    Loop Until filePos >= UBound(VGMSoundData)

    Exit Sub

ErrHandler:
    If Err.Number = 9 Then Exit Sub

End Sub
Public Sub VGM_File_Read(ByVal FileName As String)

    Dim DataSize As Long
        
    Open FileName For Binary As #1 Len = Len(VGMHeaderData)
        Get #1, 1, VGMHeaderData
        DataSize = LOF(1) - Len(VGMHeaderData)
        ReDim VGMSoundData(DataSize)
        VGMSoundData = InputB(DataSize + 1, 1)
    Close

End Sub
