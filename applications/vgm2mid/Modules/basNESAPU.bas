Attribute VB_Name = "basNESAPU"
Option Explicit

Private Const APU_WRA0    As Byte = &H0
Private Const APU_WRA1    As Byte = &H1
Private Const APU_WRA2    As Byte = &H2
Private Const APU_WRA3    As Byte = &H3
Private Const APU_WRB0    As Byte = &H4
Private Const APU_WRB1    As Byte = &H5
Private Const APU_WRB2    As Byte = &H6
Private Const APU_WRB3    As Byte = &H7
Private Const APU_WRC0    As Byte = &H8
Private Const APU_WRC2    As Byte = &HA
Private Const APU_WRC3    As Byte = &HB
Private Const APU_WRD0    As Byte = &HC
Private Const APU_WRD2    As Byte = &HE
Private Const APU_WRD3    As Byte = &HF
Private Const APU_WRE0    As Byte = &H10
Private Const APU_WRE1    As Byte = &H11
Private Const APU_WRE2    As Byte = &H12
Private Const APU_WRE3    As Byte = &H13
Private Const APU_SMASK   As Byte = &H15
Private Const APU_IRQCTRL As Byte = &H17

' N2A03 clock: 21 477 270 / 12 = 1 789 772.5
'N2A03 clock / 16
Private Const NES_CLK_BASE = 111860.78125

Private Function Hz_NES(ByVal FNum As Long) As Double

    Hz_NES = NES_CLK_BASE / (FNum + 1)

End Function

Private Function Hz_NESNoise(ByVal FreqMode As Long) As Double

    Dim FNum As Integer
    
    FNum = Choose(1 + FreqMode, 4, 8, 16, 32, 64, 96, 128, 160, 202, 254, 380, 508, 762, 1016, 2034, 2046)
    Hz_NESNoise = NES_CLK_BASE / (FNum + 1)

End Function

Public Sub NesApuCommand_Handle(ByVal Register As Byte, ByVal Data As Byte)

    Dim CH As Byte, MIDIChannel As Byte
    Static FNum_MSB(4) As Byte, FNum_LSB(4) As Byte
    Static FNum_1(4) As Long, FNum_2(4) As Long, Hz_1(4) As Double, Hz_2(4) As Double, Note_1(4) As Double, Note_2(4) As Double
    Static Envelope_1(4) As Byte, Envelope_2(4) As Byte
    Static VBLen_1(4) As Byte, VBLen_2(4) As Byte, Hold(4) As Byte, TriLen As Byte
    Static Duty_1(4) As Byte, Duty_2(4) As Byte
    Static MIDINote(4) As Byte, MIDIWheel(4) As Integer, NoteOn_1(4) As Byte, NoteOn_2(4) As Byte, MIDIVolume As Byte
    Static NoteEn_1(4) As Byte, NoteEn_2(4) As Byte
    Dim TempNote As Double
    Dim TempByt As Byte
    Dim TempLng As Long
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2612 = 1 Then
        Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        Erase Envelope_1: Erase Envelope_2: Erase VBLen_1: Erase VBLen_2: Erase Hold
        Erase Duty_1: Erase Duty_2: Erase NoteOn_1: Erase NoteOn_2
        Erase MIDINote: Erase MIDIWheel: Erase NoteOn_1: Erase NoteOn_2: MIDIVolume = 0
        For CH = &H0 To &H4
            Envelope_2(CH) = &HFF
            VBLen_2(CH) = &H0
            Hold(CH) = &H0
            Duty_2(CH) = &HFF
            Note_1(CH) = &HFF
            Note_2(CH) = &HFF
            NoteEn_2(CH) = &H0 Or IIf(CH = &H2, &H0, &H4)
            NoteOn_2(CH) = &H0
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
        Next CH
        TriLen = &H0
        Variables_Clear_YM2612 = 0
        
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, MIDI_CHANNEL_PSG_BASE + &H2, &H0, &H8
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDI_CHANNEL_PSG_BASE + &H2, &H50
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDI_CHANNEL_PSG_BASE + &H3, &H7F
    End If
    
    CH = Register \ &H4
    If CH < &H3 Then
        If PSG_CH_DISABLED(CH) = 1 Then Exit Sub
    ElseIf CH = &H3 Then
        If PSG_NOISE_DISABLED = 1 Then Exit Sub
    ElseIf CH = &H4 Then
        If YM2612_DAC_DISABLED = 1 Then Exit Sub
    End If
    
    MIDIChannel = IIf(CH = &H4, CHN_DAC, MIDI_CHANNEL_PSG_BASE + CH)
    Select Case Register
    Case APU_WRA0, APU_WRB0, APU_WRD0   ' Volume, Envelope, Hold, Duty Cycle
        If (Register = APU_WRA0 Or Register = APU_WRB0) And (Data And &HF) > &H0 Then
            Duty_1(CH) = Duty_2(CH)
            Duty_2(CH) = (Data And &HC0) \ &H40
            
            If Duty_1(CH) <> Duty_2(CH) Then
                TempByt = &H4F + (Not Duty_2(CH) And &H3)
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, MIDIChannel, TempByt
            End If
        End If
        
        Envelope_1(CH) = Envelope_2(CH)
        ' output is 1 * envelope
        Envelope_2(CH) = Data And &HF
        Hold(CH) = Data And &H20
        
        If Envelope_1(CH) <> Envelope_2(CH) Then
            If Envelope_2(CH) = &H0 Then
                MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                MIDINote(CH) = &HFF
                PSG_NoteDelay(CH) = 10000
            End If
            MIDIVolume = DB2MidiVol(Lin2DB(Envelope_2(CH) / &HF))
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, MIDIChannel, MIDI_VOLUME, MIDIVolume
        End If
    Case APU_WRC0
        Hold(CH) = Data And &H80
        TempByt = Data And &H7F
        If TempByt <> TriLen Then
            TriLen = TempByt
            NoteEn_1(CH) = NoteEn_2(CH)
            NoteEn_2(CH) = (NoteEn_2(CH) And Not &H4) Or (CBool(TriLen) And &H4)
            If NoteEn_1(CH) <> NoteEn_2(CH) And (NoteEn_2(CH) And &H3) = &H3 Then
                If CBool(NoteEn_2(CH) And &H4) Then
                    DoNoteOn Note_2(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
                    PSG_NoteDelay(CH) = 0
                ElseIf MIDINote(CH) <> &HFF Then
                    ' Note got silenced by setting TriLen = 0
                    MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                    MIDINote(CH) = &HFF
                    PSG_NoteDelay(CH) = 10000
                End If
            End If
        End If
    Case APU_WRA1, APU_WRB1 ' Sweep
        ' impossible to do in this version of vgm2mid
    Case APU_WRA2, APU_WRB2, APU_WRC2, APU_WRA3, APU_WRB3, APU_WRC3
        If (Register And &H3) = &H2 Then
            FNum_LSB(CH) = Data
            'Exit Sub
        ElseIf (Register And &H3) = &H3 Then
            FNum_MSB(CH) = Data
            VBLen_1(CH) = VBLen_2(CH)
            If Hold(CH) Then
                VBLen_2(CH) = &HFF
            Else
                VBLen_2(CH) = (Data And &HF8) \ &H8
            End If
            NoteEn_1(CH) = NoteEn_2(CH)
            NoteEn_2(CH) = (NoteEn_2(CH) And Not &H2) Or (CBool(VBLen_2(CH)) And &H2)
            If NoteEn_1(CH) <> NoteEn_2(CH) And (NoteEn_2(CH) And &H5) = &H5 Then
                If Not CBool(NoteEn_2(CH) And &H2) And MIDINote(CH) <> &HFF Then
                    ' Note got silenced by setting VBLen = 0
                    MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                    MIDINote(CH) = &HFF
                    PSG_NoteDelay(CH) = 10000
                End If
            End If
        End If
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = ((FNum_MSB(CH) And &H7) * &H100) Or (FNum_LSB(CH) * &H1)
        
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_NES(FNum_2(CH))
        If CH = &H2 Then
            Hz_2(CH) = Hz_2(CH) / 2
        End If
        
        TempNote = Note(Hz_2(CH))
        If TempNote >= &H80 Then
            'TempNote = &H7F - FNum_2(CH)
            TempNote = &H7F
        End If
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = TempNote
        
        If (NoteEn_2(CH) And &H7) = &H7 Then
            If (Register And &H3) = &H3 And PSG_NoteDelay(CH) > 10 Then
                ' writing to register 3 restarts the notes
                DoNoteOn Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
                PSG_NoteDelay(CH) = 0
            ElseIf Note_1(CH) <> Note_2(CH) Then
                If DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH)) Then
                    PSG_NoteDelay(CH) = 0
                End If
            End If
        End If
    Case APU_WRD2   ' Noise Freq
        FNum_LSB(CH) = Data
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = FNum_LSB(CH) And &HF
                    
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_NESNoise(FNum_2(CH))
        
        TempNote = Note(Hz_2(CH))
        If TempNote >= &H80 Then
            'TempNote = &H7F - FNum_2(CH)
            TempNote = &H7F
        End If
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = TempNote
        
        If (NoteEn_2(CH) And &H7) = &H7 And Note_1(CH) <> Note_2(CH) Then
            If DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH)) Then
                PSG_NoteDelay(CH) = 0
            End If
        End If
    Case APU_WRD3
        VBLen_1(CH) = VBLen_2(CH)
        If Hold(CH) Then
            VBLen_2(CH) = 1
        Else
            VBLen_2(CH) = (Data And &HF8) \ &H8
        End If
        NoteEn_1(CH) = NoteEn_2(CH)
        NoteEn_2(CH) = (NoteEn_2(CH) And Not &H2) Or (CBool(VBLen_2(CH)) And &H2)
        If NoteEn_1(CH) <> NoteEn_2(CH) And (NoteEn_2(CH) And &H5) = &H5 Then
            If Not CBool(NoteEn_2(CH) And &H2) And MIDINote(CH) <> &HFF Then
                ' Note got silenced by setting VBLen = 0
                MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                MIDINote(CH) = &HFF
                PSG_NoteDelay(CH) = 10000
            End If
        End If
        
        If (NoteEn_2(CH) And &H7) = &H7 And PSG_NoteDelay(CH) > 10 Then
            ' writing to register 3 restarts the notes
            DoNoteOn Note_2(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
            PSG_NoteDelay(CH) = 0
        End If
    Case APU_WRE0   ' IRQ, Looping, Frequency
        FNum_LSB(CH) = Data
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = FNum_LSB(CH) And &HF
        
        If FNum_1(CH) <> FNum_2(CH) Then
            MIDIWheel(CH) = FNum_2(CH) * &H400  '(&H4000 / &H10)
            MIDI_Event_Write MIDI_PITCHWHEEL, MIDIChannel, MIDIWheel(CH), &H0
        End If
    Case APU_WRE1
        TempByt = Data And &H7F
        MIDI_Event_Write MIDI_NOTE_ON, MIDIChannel, TempByt, &H7F
        MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, TempByt, &H0
    Case APU_WRE2
        FNum_MSB(CH) = Data
        
        FNum_1(CH) = FNum_2(CH)
        Note_2(CH) = FNum_MSB(CH) And &H7F
        ' note is activated by setting the DAC bit in APU_SMASK
    Case APU_SMASK
        For CH = 0 To &H4
            TempByt = 2 ^ CH
            MIDIChannel = IIf(CH = &H4, CHN_DAC, MIDI_CHANNEL_PSG_BASE + CH)
            NoteOn_1(CH) = NoteOn_2(CH)
            NoteOn_2(CH) = Data And TempByt
            
            NoteEn_1(CH) = NoteEn_2(CH)
            NoteEn_2(CH) = (NoteEn_2(CH) And Not &H1) Or (CBool(NoteOn_2(CH)) And &H1)
            If NoteEn_1(CH) <> NoteEn_2(CH) Then
                If (NoteEn_2(CH) And &H7) = &H7 Then
                    DoNoteOn Note_2(CH), Note_2(CH), MIDIChannel, MIDINote(CH), MIDIWheel(CH), 255
                    PSG_NoteDelay(CH) = 0
                ElseIf MIDINote(CH) <> &HFF Then
                    ' Note got silenced via Channel Mask
                    MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                    MIDINote(CH) = &HFF
                    PSG_NoteDelay(CH) = 10000
                End If
            End If
        Next CH
    End Select

    Exit Sub
ErrHandler:
    Dim strPrompt As String, lngResult As Long
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "GameBoyCommand_Handle")
    If lngResult = vbYes Then End
    Resume
End Sub

