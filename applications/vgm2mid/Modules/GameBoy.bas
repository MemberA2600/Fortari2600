Attribute VB_Name = "basGBDMG"
Option Explicit

Private Const NR10 As Byte = &H0
Private Const NR11 As Byte = &H1
Private Const NR12 As Byte = &H2
Private Const NR13 As Byte = &H3
Private Const NR14 As Byte = &H4
Private Const NR21 As Byte = &H6
Private Const NR22 As Byte = &H7
Private Const NR23 As Byte = &H8
Private Const NR24 As Byte = &H9
Private Const NR30 As Byte = &HA
Private Const NR31 As Byte = &HB
Private Const NR32 As Byte = &HC
Private Const NR33 As Byte = &HD
Private Const NR34 As Byte = &HE
Private Const NR41 As Byte = &H10
Private Const NR42 As Byte = &H11
Private Const NR43 As Byte = &H12
Private Const NR44 As Byte = &H13
Private Const NR50 As Byte = &H14
Private Const NR51 As Byte = &H15
Private Const NR52 As Byte = &H16

Private GB_Pan(&H0 To &H4) As Byte

Private Function Hz_GameBoy(ByVal FNum As Long) As Double

    Hz_GameBoy = 131072 / (2048 - FNum)

End Function

Private Function Hz_GameBoyNoise(ByVal PolyCntr As Byte) As Double

    Dim FreqDiv As Single   ' Division Ratio of Freq
    Dim ShftFrq As Integer  ' Shift Clock Freq (poly cntr)
    
    FreqDiv = PolyCntr And &H7
    If FreqDiv = 0 Then FreqDiv = 0.5
    ShftFrq = (PolyCntr And &HF0) \ &H10
    Hz_GameBoyNoise = 524288 / FreqDiv / 2 ^ (ShftFrq + &H1)

End Function

Public Sub GameBoyCommand_Handle(ByVal Register As Byte, ByVal Data As Byte)

    Dim CH As Byte, MIDIChannel As Byte
    Static FNum_MSB(3) As Byte, FNum_LSB(3) As Byte
    Static FNum_1(3) As Long, FNum_2(3) As Long, Hz_1(3) As Double, Hz_2(3) As Double, Note_1(3) As Double, Note_2(3) As Double
    Static Envelope_1(3) As Byte, Envelope_2(3) As Byte
    Static Duty_1(3) As Byte, Duty_2(3) As Byte
    Static MIDINote(3) As Byte, MIDIWheel(3) As Integer, NoteOn_1(3) As Byte, NoteOn_2(3) As Byte, MIDIVolume As Byte
    Dim TempNote As Double
    Dim TempByt As Byte
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2612 = 1 Then
        Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        Erase Envelope_1: Erase Envelope_2: Erase Duty_1: Erase Duty_2: Erase NoteOn_1: Erase NoteOn_2
        Erase MIDINote: Erase MIDIWheel: Erase NoteOn_1: Erase NoteOn_2: MIDIVolume = 0
        For CH = &H0 To &H3
            Envelope_2(CH) = &HFF
            Duty_2(CH) = &HFF
            Note_1(CH) = &HFF
            Note_2(CH) = &HFF
            NoteOn_2(CH) = &H0
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
        Next CH
        For CH = &H0 To &H3
            GB_Pan(CH) = &H0
        Next CH
        GB_Pan(&H4) = &HFF
        Variables_Clear_YM2612 = 0
        
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDI_CHANNEL_PSG_BASE + &H2, &H50
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDI_CHANNEL_PSG_BASE + &H3, &H7F
    End If
    
    ' Wave RAM
    If Register >= &H20 Then Exit Sub
    
    CH = Register \ &H5
    If CH < &H3 Then
        If PSG_CH_DISABLED(CH) = 1 Then Exit Sub
    ElseIf CH = &H3 Then
        If PSG_NOISE_DISABLED = 1 Then Exit Sub
    End If
    
    MIDIChannel = MIDI_CHANNEL_PSG_BASE + CH
    Select Case Register
    Case NR30   ' Wave Channel - Note On
        NoteOn_1(CH) = NoteOn_2(CH)
        NoteOn_2(CH) = Data And &H80
        
        If NoteOn_1(CH) <> NoteOn_2(CH) Then
            If NoteOn_2(CH) Then
                DoNoteOn Note_2(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
            ElseIf MIDINote(CH) <> &HFF Then
                MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                MIDINote(CH) = &HFF
            End If
        End If
    Case NR11, NR21, NR31, NR41 ' Sound Length, Wave pattern duty
        ' how do I do this?
        If Register = NR11 Or Register = NR21 Then
            ' Wave duties are: 12.5%, 25%, 50%, 75%
            Duty_1(CH) = Duty_2(CH)
            Duty_2(CH) = (Data And &HC0) \ &H40
            
            If Duty_1(CH) <> Duty_2(CH) Then
                TempByt = &H4F + (Not Duty_2(CH) And &H3)
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDIChannel, TempByt
            End If
        End If
    Case NR12, NR22, NR32, NR42 ' Envelope
        Envelope_1(CH) = Envelope_2(CH)
        
        If Register <> NR32 Then
            ' output is 1 * envelope
            Envelope_2(CH) = (Data And &HF0) \ &H10
            MIDIVolume = DB2MidiVol(Lin2DB(Envelope_2(CH) / &HF))
        Else
            ' output is &HF >> (envelope - 1)
            ' >> 1 = 6 db
            Envelope_2(CH) = (Data And &H60) \ &H20
            MIDIVolume = DB2MidiVol(-Envelope_2(CH) * 6)
        End If
        
        If Envelope_1(CH) <> Envelope_2(CH) Then
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, MIDIChannel, MIDI_VOLUME, MIDIVolume
        End If
    Case NR13, NR23, NR33, NR43, NR14, NR24, NR34, NR44 ' Frequency Low, High
        If (Register Mod &H5) = &H3 Then
            FNum_LSB(CH) = Data
            'Exit Sub
        ElseIf (Register Mod &H5) = &H4 Then
            FNum_MSB(CH) = Data
        End If
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = ((FNum_MSB(CH) And &H7) * &H100) Or (FNum_LSB(CH) * &H1)
                    
        Hz_1(CH) = Hz_2(CH)
        If CH <= &H1 Then
            Hz_2(CH) = Hz_GameBoy(FNum_2(CH))
        ElseIf CH = &H2 Then
            Hz_2(CH) = Hz_GameBoy(FNum_2(CH)) / 2
        ElseIf CH = &H3 Then
            Hz_2(CH) = Hz_GameBoyNoise(FNum_LSB(CH)) / 32
        End If
        
        Note_1(CH) = Note_2(CH)
        TempNote = Note(Hz_2(CH))
        If TempNote >= &H80 Then
            'TempNote = &H7F - FNum_2(CH)
            TempNote = &H7F
        End If
        Note_2(CH) = TempNote
        
        If (Register Mod &H5) = &H4 Then
            If CH = &H2 Then
                NoteOn_1(CH) = NoteOn_2(CH)
            Else    ' force NoteOn for all channels but the Wave channel
                NoteOn_1(CH) = &H0
            End If
            NoteOn_2(CH) = NoteOn_1(CH) Or (Data And &H80)
            
            If NoteOn_1(CH) <> NoteOn_2(CH) And CBool(NoteOn_2(CH)) Then
                DoNoteOn Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
            ElseIf NoteOn_2(CH) And Note_1(CH) <> Note_2(CH) Then
                DoNoteOn Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH)
            End If
        ElseIf Note_1(CH) <> Note_2(CH) Then
            DoNoteOn Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH)
        End If
    Case NR51
        Call GameBoy_Stereo(Data)
    End Select

    Exit Sub
ErrHandler:
    Dim strPrompt As String, lngResult As Long
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "GameBoyCommand_Handle")
    If lngResult = vbYes Then End
    'Resume
End Sub


Private Sub GameBoy_Stereo(ByVal Data As Byte)

    Dim CurBit As Integer
    Dim LeftOn As Boolean
    Dim RightOn As Boolean
    Dim PanVal As Byte
    Dim ChMask As Byte
    Dim CH As Byte
    
    If GB_Pan(&H4) = Data Then Exit Sub
    
    For CurBit = &H0 To &H3
        ChMask = 2 ^ CurBit ' replaces "1 << CurBit"
        
        PanVal = &H0
        If CBool(Data And (ChMask * &H10)) Then
            PanVal = PanVal Or &H1  ' Left Channel On
        End If
        If CBool(Data And ChMask) Then
            PanVal = PanVal Or &H2  ' Right Channel On
        End If
        
        If GB_Pan(CurBit) <> PanVal Or GB_Pan(&H4) = Data Then
            CH = MIDI_CHANNEL_PSG_BASE + CurBit
            Select Case PanVal
            Case &H1
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_LEFT
            Case &H2
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_RIGHT
            Case &H3
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_CENTER
            End Select
        End If
        GB_Pan(CurBit) = PanVal
    Next CurBit
    
    GB_Pan(&H4) = Data

End Sub
