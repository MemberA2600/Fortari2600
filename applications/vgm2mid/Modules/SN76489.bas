Attribute VB_Name = "basSN76489"
Option Explicit

Public Const PSG_LATCH = &H80 '128
Public Const PSG_CHANNEL_SELECT = PSG_LATCH Or &H70 '240
Public Const PSG_TONE_1 = PSG_LATCH Or &H0 '128
Public Const PSG_TONE_2 = PSG_LATCH Or &H20 '160
Public Const PSG_TONE_3 = PSG_LATCH Or &H40 '192
Public Const PSG_NOISE = PSG_LATCH Or &H60 '224
Private Const PSG_CHN_MASK = &H60 '112


Private Const PSG_FB_PERIODIC = &H0
Private Const PSG_FB_WHITE = &H1

Private Const PSG_CLOCK_SOURCE_HALF = &H0
Private Const PSG_CLOCK_SOURCE_FOURTH = &H1
Private Const PSG_CLOCK_SOURCE_EIGHTH = &H2
Private Const PSG_CLOCK_SOURCE_TONE_3 = &H3

Private Const PSG_ATTENUATOR_1 = PSG_LATCH Or &H10 '144
Private Const PSG_ATTENUATOR_2 = PSG_LATCH Or &H30 '176
Private Const PSG_ATTENUATOR_3 = PSG_LATCH Or &H50 '208
Private Const PSG_ATTENUATOR_NOISE = PSG_LATCH Or &H70 '240
Private Const PSG_ATTENUATION_MIN = &H0
Private Const PSG_ATTENUATION_MAX = &HF

Public Const MIDI_CHANNEL_PSG_BASE = &HA

Public PSG_NoteDelay(&H0 To &H7) As Long    ' used for Note On/Off-Detection
'Public PSG_LastVol(&H0 To &H7) As Byte

Private GG_Pan(&H0 To &H1, &H0 To &H4) As Byte
Public PSG_NUM As Byte

Public Function Hz_PSG(ByVal FNum As Double, Optional Block As Byte) As Double

    If FNum = 0 Then Hz_PSG = 0 Else Hz_PSG = (ClockPSG / 32) / FNum

End Function

Public Sub PSGCommand_Handle(ByVal MSB As Byte, ByVal LSB As Byte)
    
    Dim CH As Byte, MIDIChannel As Byte
    Static FNum_1(7) As Long, FNum_2(7) As Long, Hz_1(7) As Double, Hz_2(7) As Double, Note_1(7) As Double, Note_2(7) As Double
    Static FB(2) As Byte, ClockSource(2) As Byte
    Static Attenuation_1(7) As Byte, Attenuation_2(7) As Byte
    Static MIDINote(7) As Byte, MIDIWheel(7) As Integer, NoteOn_1(7) As Byte, NoteOn_2(7) As Byte, MIDIVolume As Byte
    Dim DnRet As Boolean
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
        For CH = &H0 To &H3
            GG_Pan(&H0, CH) = &H0
            GG_Pan(&H1, CH) = &H0
        Next CH
        GG_Pan(&H0, &H4) = &HFF
        GG_Pan(&H1, &H4) = &HFF
        Variables_Clear_PSG = 0
    End If
    
    If (MSB And &H80) = &H0 Then Exit Sub
    
    CH = (MSB And PSG_CHN_MASK) / &H20
    If CH < &H3 Then
        If PSG_CH_DISABLED(CH) = 1 Then Exit Sub
    Else 'If CH = &H3 Then
        If PSG_NOISE_DISABLED = 1 Then Exit Sub
    End If
    
    CH = CH Or PSG_NUM * &H4
    MIDIChannel = MIDI_CHANNEL_PSG_BASE + (CH And &H3)
    If PSG_NUM = &H1 Then
        MIDIChannel = MIDIChannel - MIDI_CHANNEL_PSG_BASE
    End If
    
    Select Case (MSB And PSG_CHANNEL_SELECT)
    Case PSG_TONE_1, PSG_TONE_2, PSG_TONE_3
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = ((LSB And &H3F) * &H10) + (MSB And &HF)
                    
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_PSG(FNum_2(CH))
        
        If Not CBool(T6W28_PSG And PSG_NUM > &H0) Then
            TempNote = Note(Hz_2(CH))
            
            Note_1(CH) = Note_2(CH)
            If TempNote >= &H80 Then
                'TempNote = &H7F - FNum_2(CH)
                TempNote = &HFF
            End If
            Note_2(CH) = TempNote
            If T6W28_PSG Then
                Note_1(&H4 + CH) = Note_2(&H4 + CH)
                Note_2(&H4 + CH) = TempNote
            End If
        Else 'If T6W28_PSG And PSG_NUM > &H0 Then
            TempNote = Note(0.5 * Hz_2(CH))
            If (CH And &H3) = &H2 Then
                If TempNote < &HFF Then
                    TempNote = TempNote - 24    ' - 2 Octaves
                    If TempNote >= &H80 Then
                        TempNote = &H7F
                    End If
                End If
                Note_2(&H3) = TempNote
                Note_2(&H7) = TempNote
            End If
            Exit Sub
        End If
        
        If FNum_2(CH) = 0 Then
            If NoteOn_2(CH) <> 0 Then
                If MIDINote(CH) < &HFF Then
                    'MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote(CH), &H0
                    DnRet = DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), _
                                    MIDIWheel(CH))
                    MIDINote(CH) = &HFF     ' TODO: Check this
                End If
                NoteOn_1(CH) = NoteOn_2(CH)
                NoteOn_2(CH) = 0
            End If
        ElseIf FNum_2(CH) > 0 And FNum_2(CH) <> FNum_1(CH) Then
            DnRet = DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), _
                            MIDIWheel(CH), IIf(NoteOn_2(CH), &H0, &HFF))
            NoteOn_1(CH) = NoteOn_2(CH)
            NoteOn_2(CH) = 1
            If DnRet Then PSG_NoteDelay(CH) = &H0
        End If
        If T6W28_PSG Then
            CH = &H4 + CH
            MIDIChannel = MIDIChannel - MIDI_CHANNEL_PSG_BASE
            If Note_2(CH) = &HFF Then
                If NoteOn_2(CH) <> 0 Then
                    If MIDINote(CH) < &HFF Then
                        DnRet = DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), _
                                        MIDIWheel(CH))
                        'MIDINote(CH) = &HFF
                    End If
                    NoteOn_1(CH) = NoteOn_2(CH)
                    NoteOn_2(CH) = 0
                End If
            ElseIf Note_2(CH) < &HFF And Note_2(CH) <> Note_1(CH) Then
                DnRet = DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), _
                                MIDIWheel(CH), IIf(NoteOn_2(CH), &H0, &HFF))
                NoteOn_1(CH) = NoteOn_2(CH)
                NoteOn_2(CH) = 1
                If DnRet Then PSG_NoteDelay(CH) = &H0
            End If
        End If
        
        If (CH And &H3) = &H2 And ClockSource(PSG_NUM) = &H3 Then
            PSGCommand_Handle &HE0, (FB(PSG_NUM) * 4 Or ClockSource(PSG_NUM))
        End If
        
    Case PSG_NOISE
        FB(PSG_NUM) = (LSB And &H4) / &H4
        'If Not CBool(T6W28_PSG And PSG_NUM > &H0) Then
            ClockSource(PSG_NUM) = LSB And &H3
        'End If
    
        'If ClockSource(PSG_NUM) <> PSG_CLOCK_SOURCE_TONE_3 Then
        '    MIDIChannel = MIDI_CHANNEL_PSG_BASE + 2
        '    Dim intNote As Integer
        '    For intNote = 0 To 127
        '        MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, intNote, &H0
        '    Next
        'End If
        
        ' Noise-Frequency
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = IIf(ClockSource(PSG_NUM) = &H3, 2 * FNum_2(CH - 1), _
                                                    2 ^ (5 + ClockSource(PSG_NUM)))
        If FNum_2(CH) = 0 Then FNum_2(CH) = 1
        
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_PSG(FNum_2(CH))
        
        'If T6W28_PSG And PSG_NUM > &H0 Then Exit Sub
        
        Note_2(CH) = Note(Hz_2(CH))
        Note_2(CH) = Note_2(CH) / 1.5
        'PSG_NoteDelay(CH) = &H0
    
    Case PSG_ATTENUATOR_1, PSG_ATTENUATOR_2, PSG_ATTENUATOR_3 ', PSG_ATTENUATOR_NOISE
        Attenuation_1(CH) = Attenuation_2(CH)
        Attenuation_2(CH) = (LSB And PSG_ATTENUATION_MAX)
        
        If Attenuation_2(CH) <> Attenuation_1(CH) Then
            'Attenuation_2(CH) = (LSB And PSG_ATTENUATION_MAX) * 8.45 '(127 / 15)
            Attenuation_2(CH) = (LSB And PSG_ATTENUATION_MAX)           ' I like round values
            'MIDIVolume = MIDI_VOLUME_MAX + 1 - &H8 - Attenuation_2(CH) * &H8
            'If MIDIVolume > &H7F Then MIDIVolume = &H7F
            MIDIVolume = DB2MidiVol(PSG_Vol2DB(LSB And &HF))
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, MIDIChannel, MIDI_VOLUME, MIDIVolume
            
            ' write Note On/Off
            If PSG_VOLDEP_NOTES >= &H1 Then
                If NoteOn_2(CH) = 1 Then
                    If MIDIVolume = 0 Then
                        DnRet = DoNoteOn(Note_1(CH), &HFF, MIDIChannel, MIDINote(CH), _
                                        MIDIWheel(CH), &HFF)
                        PSG_NoteDelay(CH) = 44100
                    'ElseIf (PSG_LastVol(CH) = &H0 And PSG_NoteDelay(CH) >= 10) Or _
                        (PSG_VOLDEP_NOTES >= &H2 And PSG_NoteDelay(CH) >= 735 And _
                        PSG_LastVol(CH) + 20 < MIDIVolume) Then
                    ElseIf (Attenuation_1(CH) = &HF And PSG_NoteDelay(CH) >= 10) Or _
                        (PSG_VOLDEP_NOTES >= &H2 And PSG_NoteDelay(CH) >= 735 And _
                        Attenuation_1(CH) - 2 > Attenuation_2(CH)) Then
                        DnRet = DoNoteOn(Note_1(CH), Note_2(CH), MIDIChannel, MIDINote(CH), _
                                        MIDIWheel(CH), &HFF)
                        PSG_NoteDelay(CH) = 0
                    End If
                End If
            End If
            'PSG_LastVol(CH) = MIDIVolume
        End If

    Case PSG_ATTENUATOR_NOISE
        Attenuation_1(CH) = Attenuation_2(CH)
        'Attenuation_2(CH) = (LSB And 15) * 8.45 '(127 / 15)
        Attenuation_2(CH) = (LSB And PSG_ATTENUATION_MAX)
        MIDIVolume = MIDI_VOLUME_MAX + 1 - &H8 - Attenuation_2(CH) * &H8
         
        If Attenuation_2(CH) <> Attenuation_1(CH) Or PSG_NoteDelay(CH) >= 735 Then
            If MIDIVolume > 0 Then                              ' old Note-Height: 39
                If Note_1(CH) < &HFF Then
                    MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, Note_1(CH), &H0
                End If
                If Note_2(CH) < &HFF Then
                    MIDI_Event_Write MIDI_NOTE_ON, MIDIChannel, Note_2(CH), MIDIVolume
                End If
                Note_1(CH) = Note_2(CH)
            ElseIf MIDIVolume = 0 Then
                If Attenuation_1(CH) < &HF Then
                    If Note_1(CH) < &HFF Then
                        MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, Note_1(CH), &H0
                        Note_1(CH) = &HFF
                    End If
                End If
            End If
            PSG_NoteDelay(CH) = &H0
        End If
        'PSG_LastVol(CH) = MIDIVolume
    
'    Case Else
    
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

Public Sub GGStereo_Handle(ByVal Register As Byte)

    Dim CurBit As Integer
    Dim LeftOn As Boolean
    Dim RightOn As Boolean
    Dim PanVal As Byte
    Dim ChMask As Byte
    Dim CH As Byte
    
    For CurBit = &H0 To &H3
        ChMask = 2 ^ CurBit ' replaces "1 << CurBit"
        
        PanVal = &H0
        If CBool(Register And (ChMask * &H10)) Then
            PanVal = PanVal Or &H1  ' Left Channel On
        End If
        If CBool(Register And ChMask) Then
            PanVal = PanVal Or &H2  ' Right Channel On
        End If
        
        If GG_Pan(PSG_NUM, CurBit) <> PanVal Or GG_Pan(PSG_NUM, &H4) = Register Then
            'If CurBit = &H0 Then
            '    CH = CHN_DAC
            'Else
                CH = MIDI_CHANNEL_PSG_BASE + CurBit
                If PSG_NUM = &H1 Then
                    CH = CH - MIDI_CHANNEL_PSG_BASE
                End If
            'End If
            Select Case PanVal
            Case &H1
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_LEFT
            Case &H2
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_RIGHT
            Case &H3
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_CENTER
            End Select
        End If
        GG_Pan(PSG_NUM, CurBit) = PanVal
    Next CurBit
    
    GG_Pan(PSG_NUM, &H4) = Register

End Sub

Public Function PSG_Vol2DB(ByVal TL As Byte) As Single

    If TL < &HF Then
        PSG_Vol2DB = -TL * 2
    Else
        PSG_Vol2DB = -400   ' results in volume 0
    End If

End Function
