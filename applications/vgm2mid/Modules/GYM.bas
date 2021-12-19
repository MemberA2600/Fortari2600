Attribute VB_Name = "basGYM"
Option Explicit

Public GYMSoundData() As Byte
Public Sub GYM_File_Read(ByVal FileName As String)
    
    Open FileName For Binary As #1
        ReDim GYMSoundData(LOF(1)) As Byte
        GYMSoundData = InputB(LOF(1), 1)
    Close
    
End Sub
Public Sub GYM_File_Interpret()
    
    Dim filePos As Long
    Dim Switch As Byte
    Dim chrPort As Byte, chrRegister As Byte, chrData As Byte, psgMSB As Byte, psgLSB As Byte

    Conversion_Status_Current = 0
    Conversion_Status_Total = UBound(GYMSoundData)

    On Error GoTo ErrHandler

    Do
        Switch = GYMSoundData(filePos)
        Select Case Switch
        Case 0
            DeltaTime = DeltaTime + 1
            filePos = filePos + 1
        Case 1, 2
            chrPort = IIf(Switch = 1, 0, 3)
            chrRegister = GYMSoundData(filePos + 1)
            chrData = GYMSoundData(filePos + 2)
            If chrRegister <> YM2612_DAC Then YM2612Command_Handle chrPort, chrRegister, chrData
            filePos = filePos + 3
        Case 3
            chrPort = 10
            psgMSB = GYMSoundData(filePos + 1)
            Select Case (psgMSB And 240)
            Case PSG_TONE_1, PSG_TONE_2, PSG_TONE_3
                psgLSB = GYMSoundData(filePos + 3)
                filePos = filePos + 4
            Case Else
                filePos = filePos + 2
            End Select
            PSGCommand_Handle psgMSB, psgLSB
        Case Else
            filePos = filePos + 1
        End Select
    
        Conversion_Status_Current = filePos
        DoEvents
        
    Loop Until filePos >= UBound(GYMSoundData)

    Exit Sub

ErrHandler:
    If Err.Number = 9 Then Exit Sub

End Sub
