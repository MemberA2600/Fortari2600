Attribute VB_Name = "basYM2151"
Option Explicit

' YM2151 Register Constants
Public Const YM2151_TEST = &H1
Public Const YM2151_KEY_ON = &H8
Public Const YM2151_NOISE = &HF
Public Const YM2151_CLK_A_MSB = &H10
Public Const YM2151_CLK_A_LSB = &H11
Public Const YM2151_CLK_B = &H12
Public Const YM2151_CSM_IRQ_RESET_EN_TIMER = &H14
Public Const YM2151_LFO_FREQ = &H18
Public Const YM2151_PMD_AMD = &H19
Public Const YM2151_CT1_CT2_WAVEFORM = &H1B
Public Const YM2151_PAN_FB_CONNECTION = &H20
Public Const YM2151_BLK_FNUM = &H28
Public Const YM2151_KF = &H30
Public Const YM2151_PMS_AMS = &H38
Public Const YM2151_DT1_MUL = &H40
Public Const YM2151_TL = &H60
Public Const YM2151_KS_AR = &H80
Public Const YM2151_LFO_AM_EN_D1R = &HA0
Public Const YM2151_DT2_D2R = &HC0
Public Const YM2151_D1L_RR = &HE0

Public Function YM2151FNumToMidi(ByVal FNum As Byte, ByVal Block As Byte) As Byte

    Dim NoteVal As Byte
    
    'If FNum > &HF Then
    '    MsgBox "FNumToHz (2151): invalid fnum " & Format$(FNum)
    'End If
    If Block > &H7 Then
        Block = &H7
    End If
    
    FNum = FNum And &HF
    If Not ((FNum And &H3) = &H3) Then
        NoteVal = (FNum And &HC) / &H4
        NoteVal = NoteVal * 3 + (FNum And &H3)
        NoteVal = 61 + NoteVal
    Else
        NoteVal = &HFF
    End If
    
    If NoteVal = &HFF Then
        YM2151FNumToMidi = &HFF
    Else
        YM2151FNumToMidi = NoteVal + (Block - &H4) * 12
        If YM2151FNumToMidi = &H0 Then Stop
    End If

End Function

Public Sub YM2151Command_Handle(ByVal Register As Byte, ByVal Data As Byte)

    Const NOTE_ON_MODE As Byte = &H1
    
    Static Slot(7) As Byte
    Static CH As Byte
    Static OP As Byte
'    Static DT(5, 3) As Byte, MULTI(5, 3) As Byte
    Static TL(7, 3) As Byte
    'Static KF As Byte
'    Static KS(5, 3) As Byte, AR(5, 3) As Byte
'    Static DR(5, 3) As Byte
'    Static SR(5, 3) As Byte
'    Static SL(5, 3) As Byte, RR(5, 3) As Byte
    Static FNum_LSB(7) As Integer
    Static FNum_MSB(7) As Byte
    Static Block(7) As Byte
    Static FNum_1(7) As Long
    Static FNum_2(7) As Long
    Static Note_1(7) As Double
    Static Note_2(7) As Double
    Static Feedback(7) As Byte
    Static Connection(7) As Byte
    Static MIDIInstr(7) As Byte
    Static MIDINote(7) As Byte
    Static MIDIWheel(7) As Integer
    Static MIDIVolume(7) As Byte
    Static MIDIPan(7) As Byte
    Static NoteOn_1(7) As Byte
    Static NoteOn_2(7) As Byte
    Dim TempSng As Single
    Dim TempLng As Long
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2151 = 1 Then
        Erase Slot: Erase TL: Erase FNum_LSB: Erase FNum_MSB: Erase Block
        Erase FNum_1: Erase FNum_2: Erase Note_1: Erase Note_2
        Erase Feedback: 'Erase Connection
        Erase MIDIInstr: Erase MIDINote: Erase MIDIWheel: Erase MIDIVolume
        Erase NoteOn_1: Erase NoteOn_2
        Variables_Clear_YM2151 = 0
        For CH = &H0 To &H7
            Note_1(CH) = &HFF
            Note_2(CH) = &HFF
            NoteOn_2(CH) = &H0
            MIDIInstr(CH) = &HFF
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
            MIDIVolume(CH) = &HFF
        Next CH
    End If
    
    Select Case Register
    Case YM2151_KEY_ON
        CH = Data And &H7
        If YM2151_CH_DISABLED(CH) = 1 Then Exit Sub
        
        Slot(CH) = Fix(Data / &H8) And &HF
        NoteOn_1(CH) = NoteOn_2(CH)
        NoteOn_2(CH) = IIf(Slot(CH) > &H0, &H1, &H0)
        If CBool(NOTE_ON_MODE And &H1) Then
            If NoteOn_2(CH) <> NoteOn_1(CH) And Note_2(CH) <> &H0 Then
                If NoteOn_2(CH) = &H0 Then
                    'MIDI_Event_Write MIDI_NOTE_OFF, CH, Note_2(CH), &H0
                    DoNoteOn Note_1(CH), &HFF, CH, MIDINote(CH), MIDIWheel(CH), 255
                Else
                    'MIDI_Event_Write MIDI_NOTE_ON, CH, Note_2(CH), &H7F
                    DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH), 255
                End If
            End If
        End If
    Case YM2151_NOISE   ' NOISE: NE, NFRQ
        'nen = IIf(Data And &H80, 1, 0)
        'nfrq = Data And &H31
    Case YM2151_CLK_A_MSB
    Case YM2151_CLK_A_LSB
    Case YM2151_CLK_B
    Case YM2151_CSM_IRQ_RESET_EN_TIMER
    Case YM2151_LFO_FREQ
    Case YM2151_PMD_AMD
        'depth = Data And &H7F
        'ispm = IIf(Data And &H80, 1, 0)
    Case YM2151_CT1_CT2_WAVEFORM
        'w = Data And &H3    ' W: 0 - ramp, 1 - sq, 2 - tri, 3 - noise
    Case YM2151_PAN_FB_CONNECTION To YM2151_PAN_FB_CONNECTION + &H7
        CH = Register And &H7
        If YM2151_CH_DISABLED(CH) = 1 Then Exit Sub
        
        If YM2151_PAN_DISABLED(CH) = 0 Then
            Select Case Fix(Data / &H40) And &H3
            Case &H1
                If MIDIPan(CH) <> MIDI_PAN_LEFT Or True Then
                    MIDIPan(CH) = MIDI_PAN_LEFT
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
                End If
            Case &H2
                If MIDIPan(CH) <> MIDI_PAN_RIGHT Or True Then
                    MIDIPan(CH) = MIDI_PAN_RIGHT
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
                End If
            Case &H3, &H0
                If MIDIPan(CH) <> MIDI_PAN_CENTER Or True Then
                    MIDIPan(CH) = MIDI_PAN_CENTER
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
                End If
            End Select
        End If
        
        Feedback(CH) = Fix(Data / &H8) And &H7
        Connection(CH) = Data And &H7
        
        If YM2151_PROG_DISABLED(CH) = 0 Then
            MIDIInstr(CH) = Data And &H3F
            MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, MIDIInstr(CH)
        End If
    Case YM2151_BLK_FNUM To YM2151_BLK_FNUM + &H7
        CH = Register And &H7
        If YM2151_CH_DISABLED(CH) = 1 Then Exit Sub
        
        Block(CH) = Fix(Data / &H10) And &H7
        FNum_MSB(CH) = Data And &HF
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = FNum_MSB(CH)
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = YM2151FNumToMidi(FNum_2(CH), Block(CH)) + FNum_LSB(CH) / &H40
        'If NoteOn_2(CH) = 1 Or CBool(NOTE_ON_MODE And &H2) Then
        '    If Note_2(CH) <> Note_1(CH) Or (NOTE_ON_MODE And &H2) = &H2 Then
        '        MIDI_Event_Write MIDI_NOTE_OFF, CH, Note_1(CH), &H0
        '        MIDI_Event_Write MIDI_NOTE_ON, CH, Note_2(CH), &H7F
        '    End If
        'End If
        If NoteOn_2(CH) = 1 Then
            DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH)
        End If
    Case YM2151_KF To YM2151_KF + &H7
        CH = Register And &H7
        If YM2151_CH_DISABLED(CH) = 1 Then Exit Sub
        
        ' Key Fraction goes from &H00 to &HFC
        ' &H00 is no change, &H100 would be a full semitone
        FNum_LSB(CH) = Fix(Data / &H4) And &H3F
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = YM2151FNumToMidi(FNum_2(CH), Block(CH)) + FNum_LSB(CH) / &H40
        If NoteOn_2(CH) = 1 Then
            DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH)
        End If
        
        'TempLng = MIDI_PITCHWHEEL_CENTER + FNum_LSB(CH) * &H40     '(&H1000 / &H40)
        'If TempLng <> MIDIWheel(CH) Then
        '    MIDIWheel(CH) = TempLng
        '    MIDI_Event_Write MIDI_PITCHWHEEL, CH, MIDIWheel(CH), &H0
        'End If
    Case YM2151_PMS_AMS To YM2151_PMS_AMS + &H7
        CH = Register And &H7
        'PMS = Fix(Data / &H10) And &H7
        'AMS = Data And &H3
        TempSng = (Data And &H70) / &H70
        TempLng = TempSng * TempSng * &H7F
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_MODULATOR_WHEEL, TempLng
    Case YM2151_DT1_MUL To YM2151_DT1_MUL + &H1F
        CH = Fix((Register And &H3F) / &H8)
        'DT1 = Fix(Data / &H10) And &H7
        'MUl = Data And &HF
    Case YM2151_TL To YM2151_TL + &H1F
        CH = Register And &H7
        OP = Fix((Register And &H1F) / &H8)
        
        TL(CH, OP) = Data And &H7F
        If OP < 3 Then Exit Sub
        If YM2151_VOL_DISABLED(CH) = 1 Then Exit Sub
        
        'Select Case Connection(CH)
        'Case 0, 1, 2, 3
            TempLng = TL(CH, 3)
        'Case 4
        '    TempLng = (CLng(TL(CH, 1)) + TL(CH, 3)) \ 2
        'Case 5, 6
        '    TempLng = (CLng(TL(CH, 1)) + TL(CH, 2) + TL(CH, 3)) \ 3
        'Case 7
        '    TempLng = (CLng(TL(CH, 0)) + TL(CH, 1) + TL(CH, 2) + TL(CH, 3)) \ 4
        'End Select
        
        TempLng = DB2MidiVol(YM3812_Vol2DB(TempLng) / 4)
        If TempLng <> MIDIVolume(CH) Then
            MIDIVolume(CH) = TempLng
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, MIDIVolume(CH)
        End If
    Case YM2151_KS_AR To YM2151_KS_AR + &H1F
        CH = Fix((Register And &H3F) / &H8)
        'KS = Fix(Data / &H40) And &H3
        'AR = Data And &H1F
    Case YM2151_LFO_AM_EN_D1R To YM2151_LFO_AM_EN_D1R + &H1F
        CH = Fix((Register And &H3F) / &H8)
        'AMS_EN = IIf(Data And &H80, 1, 0)
        'D1R = Data And &H1F
    Case YM2151_DT2_D2R To YM2151_DT2_D2R + &H1F
        CH = Fix((Register And &H3F) / &H8)
        'DT2 = Fix(Data / &H40) And &H3
        'D2R = Data And &H1F
    Case YM2151_D1L_RR To YM2151_D1L_RR + &H1F
        CH = Fix((Register And &H1F) / &H4)
        'D1L = Fix(Data / &H10) And &HF
        'RR = Data And &HF
        'Abort("YM2151 ADSR - SL " & D1L & " RR " & RR);
    End Select

    Exit Sub

ErrHandler:
    Dim strPrompt As String, lngResult As Long
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "YM2151_Command_Handle")
    If lngResult = vbYes Then End
    'Resume Next
End Sub
