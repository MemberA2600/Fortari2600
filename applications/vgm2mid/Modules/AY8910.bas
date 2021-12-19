Attribute VB_Name = "basAY8910"
Option Explicit

Private Const AY_AFINE = &H0
Private Const AY_ACOARSE = &H1
Private Const AY_BFINE = &H2
Private Const AY_BCOARSE = &H3
Private Const AY_CFINE = &H4
Private Const AY_CCOARSE = &H5
Private Const AY_NOISEPER = &H6
Private Const AY_ENABLE = &H7
Private Const AY_AVOL = &H8
Private Const AY_BVOL = &H9
Private Const AY_CVOL = &HA
Private Const AY_EFINE = &HB
Private Const AY_ECOARSE = &HC
Private Const AY_ESHAPE = &HD

Private Const AY_PORTA = &HE
Private Const AY_PORTB = &HF


Private Const MIDI_CHANNEL_PSG_BASE = &HA

'Public AY_NoteDelay(&H0 To &H7) As Long    ' used for Note On/Off-Detection
'Public AY_LastVol(&H0 To &H7) As Byte

Private PSG_NUM As Byte
Private PSG_TYPE(&H0 To &H1) As Byte

Private Function Hz_AY(ByVal FNum As Double) As Double

    If FNum = 0 Then Hz_AY = 0 Else Hz_AY = (ClockAY / 16) / FNum

End Function

'234567890123456789012345678901234567890123456789012345678901234567890123456789012345678
'000000011111111112222222222333333333344444444445555555555666666666666777777778888888888
Public Sub AYCommand_Handle(ByVal ChipID As Byte, ByVal Reg As Byte, ByVal Data As Byte)
    
    Dim CH As Byte, MIDIChannel As Byte
    Static FNum_1(7) As Long, FNum_2(7) As Long, Hz_1(7) As Double, Hz_2(7) As Double, Note_1(7) As Double, Note_2(7) As Double
    Static FB(2) As Byte, ClockSource(2) As Byte
    Static Attenuation_1(7) As Byte, Attenuation_2(7) As Byte
    Static MIDINote(7) As Byte, MIDIWheel(7) As Integer, NoteOn_1(7) As Byte, NoteOn_2(7) As Byte, MIDIVolume As Byte
    Dim CurCH As Byte
    Dim TempByt As Byte
    Dim TempNote As Double
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_PSG = 1 Then
        Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        FB(&H0) = 0: ClockSource(&H0) = 0
        FB(&H1) = 0: ClockSource(&H1) = 0
        Erase Attenuation_1: Erase Attenuation_2
        Erase MIDINote: Erase MIDIWheel: Erase NoteOn_1: Erase NoteOn_2: MIDIVolume = 0
        For CH = &H0 To &H7
            Attenuation_2(CH) = &HFF
            PSG_NoteDelay(CH) = 0
            'PSG_LastVol(CH) = &H0
            Note_1(CH) = &HFF
            Note_2(CH) = &HFF
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
        Next CH
        Variables_Clear_PSG = 0
    End If
    
    'If CH < &H3 Then
    '    If PSG_CH_DISABLED(CH) = 1 Then Exit Sub
    'Else 'If CH = &H3 Then
    '    If PSG_NOISE_DISABLED = 1 Then Exit Sub
    'End If
    
    Select Case Reg
    Case AY_AFINE, AY_ACOARSE, AY_BFINE, AY_BCOARSE, AY_CFINE, AY_CCOARSE
        CH = Reg \ &H2
        CurCH = ChipID * &H3 + CH
        MIDIChannel = IIf(ChipID, &H0, MIDI_CHANNEL_PSG_BASE) + CH
        
        FNum_1(CH) = FNum_2(CH)
        If Reg And &H1 Then
            ' AY_xCOARSE
            Data = Data And &HF
            FNum_2(CurCH) = (FNum_2(CurCH) And &HFF) Or (Data * &H100)
        Else
            ' AY_xFINE
            FNum_2(CurCH) = (FNum_2(CurCH) And &HF00) Or (Data * &H1)
        End If
        
        Hz_1(CurCH) = Hz_2(CurCH)
        Hz_2(CurCH) = Hz_AY(FNum_2(CurCH))
        
        Note_1(CurCH) = Note_2(CurCH)
        TempNote = Note(Hz_2(CurCH))
        If TempNote >= &H80 Then
            'TempNote = &H7F - FNum_2(CH)
            TempNote = &H7F
        End If
        Note_2(CurCH) = TempNote
        
        If Note_1(CurCH) <> Note_2(CurCH) Then
            DoNoteOn Note_1(CurCH), Note_2(CurCH), MIDIChannel, MIDINote(CurCH), MIDIWheel(CurCH)
        End If
    Case AY_AVOL, AY_BVOL, AY_CVOL
        CH = Reg - AY_AVOL
        CurCH = ChipID * &H3 + CH
        MIDIChannel = IIf(ChipID, &H0, MIDI_CHANNEL_PSG_BASE) + CH
        
        If Data And &H10 Then
            ' use Envelope data
            Attenuation_2(CurCH) = &HFF
            MIDIVolume = &H7F
        Else
            Attenuation_2(CurCH) = Data And &HF
            MIDIVolume = Attenuation_2(CurCH) * &H8
        End If
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, MIDIChannel, MIDI_VOLUME, MIDIVolume
    Case AY_ENABLE
        TempByt = Not Data
        For CH = &H0 To &H5
            CurCH = ChipID * &H6 + CH
            NoteOn_1(CurCH) = NoteOn_2(CurCH)
            NoteOn_2(CurCH) = TempByt And &H1
            TempByt = TempByt \ &H2
            
            If NoteOn_1(CurCH) <> NoteOn_2(CurCH) Then
                MIDIChannel = IIf(ChipID, &H0, MIDI_CHANNEL_PSG_BASE) + CH
                If NoteOn_2(CurCH) Then
                    DoNoteOn Note_2(CurCH), Note_2(CurCH), MIDIChannel, MIDINote(CurCH), MIDIWheel(CurCH), 255
                ElseIf MIDINote(CurCH) <> &HFF Then
                    MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CurCH), &H0
                    MIDINote(CurCH) = &HFF
                End If
            End If
        Next CH
    Case AY_NOISEPER
        ' Noise Frequency
    Case AY_EFINE, AY_ECOARSE
    Case AY_ESHAPE
    Case AY_PORTA, AY_PORTB
        ' ignore
    End Select

    Exit Sub
ErrHandler:
    Dim strPrompt As String, lngResult As Long
    
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "PSG_Command_Handle")
    If lngResult = vbYes Then End
    'Resume
End Sub

Public Function AY_Vol2DB(ByVal TL As Byte) As Single

    If TL > &H0 Then
        AY_Vol2DB = TL - &HF
    Else
        AY_Vol2DB = -400   ' results in volume 0
    End If

End Function

