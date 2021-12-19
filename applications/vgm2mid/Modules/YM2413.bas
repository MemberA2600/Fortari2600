Attribute VB_Name = "basYM2413"
Option Explicit

' YM2413 Register Constants
Public Const YM2413_REG_USER = &H0

Public Const YM2413_REG_RHYTHM = &HE
Public Const YM2413_REG_RHYTHM_MODE = 32
Public Const YM2413_REG_BD = 16
Public Const YM2413_REG_SD = 8
Public Const YM2413_REG_TOM = 4
Public Const YM2413_REG_TCT = 2
Public Const YM2413_REG_HH = 1

Public Const YM2413_REG_TEST = &HF
Public Const YM2413_REG_FNum_LSB = &H10

Public Const YM2413_REG_SUS_KEY_BLOCK_FNum_MSB = &H20
Public Const YM2413_REG_SUS = 32
Public Const YM2413_REG_KEY = 16
Public Const YM2413_REG_BLOCK = 14
Public Const YM2413_REG_FNum_MSB = 1

Public Const YM2413_REG_INST_VOL = &H30
Public Const YM2413_REG_INST = 240
Public Const YM2413_REG_VOL = 15

' Tone Data (INST) Constants
Public Const INST_ORIGINAL = 0
Public Const INST_VIOLIN = 1
Public Const INST_GUITAR = 2
Public Const INST_PIANO = 3
Public Const INST_FLUTE = 4
Public Const INST_CLARINET = 5
Public Const INST_OBOE = 6
Public Const INST_TRUMPET = 7
Public Const INST_ORGAN = 8
Public Const INST_HORN = 9
Public Const INST_SYNTHESIZER = 10
Public Const INST_HARPSICHORD = 11
Public Const INST_VIBRAPHONE = 12
Public Const INST_BASS_SYNTH = 13
Public Const INST_BASS_ACOUSTIC = 14
Public Const INST_GUITAR_ELECTRIC = 15

Public Function Hz_YM2413(ByVal FNum As Double, Optional Block As Byte) As Double

    If Block = 0 And FNum = 0 Then Hz_YM2413 = 0 Else Hz_YM2413 = FNum * fsam2413 * 2 ^ (Block - 19)

End Function

Public Sub YM2413Command_Handle(Register As Byte, Data As Byte)
    
    Dim CH As Byte
    Static FNum_MSB(8) As Byte
    Static SUS_ON(8) As Byte, KEY_ON(8) As Byte, Block(8) As Byte, FNum_LSB(8) As Byte, FNum_1(8) As Long, FNum_2(8) As Long, Hz_1(8) As Double, Hz_2(8) As Double, Note_1(8) As Double, Note_2(8) As Double
    Static InsVol(8) As Byte, Instrument(8) As Byte, Volume(8) As Byte, BD_VOL As Byte, HH_VOL As Byte, SD_VOL As Byte, TOM_VOL As Byte, TCT_VOL As Byte
    Static MIDINote(8) As Byte, MIDIWheel(8) As Integer, MIDIVolume(8) As Byte, NoteOn_1(8) As Byte, NoteOn_2(8) As Byte, Percussion_On(5) As Byte
    Dim TempByt As Byte
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2413 = 1 Then
        CH = 0
        Erase FNum_MSB
        Erase SUS_ON: Erase KEY_ON:  Erase Block: Erase FNum_LSB: Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        Erase InsVol: Erase Instrument: Erase Volume: BD_VOL = &H7F: HH_VOL = &H7F: SD_VOL = &H7F: TOM_VOL = &H7F: TCT_VOL = &H7F
        Erase MIDINote: Erase MIDIWheel: Erase MIDIVolume: Erase NoteOn_1: Erase NoteOn_2: Erase Percussion_On
        For CH = &H0 To &H8
            InsVol(CH) = &H0
            Instrument(CH) = &HFF
            Volume(CH) = &HFF
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
            MIDIVolume(CH) = &HFF
        Next CH
        Variables_Clear_YM2413 = 0
    End If
        
    Select Case Register
'    Case YM2413_REG_USER To (YM2413_REG_USER + 7)
    
    Case YM2413_REG_RHYTHM
        
        If YM2413_PERCUSSION_DISABLED = 1 Then Exit Sub
        
        CH = CHN_DAC
        If (Data And YM2413_REG_RHYTHM_MODE) = 0 Then
            Data = &H0
        End If
        
        If (Data And YM2413_REG_BD) = 0 Then
            If Percussion_On(0) = 1 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, 35, &H0
                Percussion_On(0) = 0
            End If
        Else
            If Percussion_On(0) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 35, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 35, BD_VOL
                Percussion_On(0) = 1
            End If
        End If
        If (Data And YM2413_REG_SD) = 0 Then
            If Percussion_On(1) = 1 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, 38, &H0
                Percussion_On(1) = 0
            End If
        Else
            If Percussion_On(1) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 38, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 38, SD_VOL
                Percussion_On(1) = 1
            End If
        End If
        If (Data And YM2413_REG_TOM) = 0 Then
            If Percussion_On(2) = 1 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, 45, &H0
                Percussion_On(2) = 0
            End If
        Else
            If Percussion_On(2) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 45, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 45, TOM_VOL
                Percussion_On(2) = 1
            End If
        End If
        If (Data And YM2413_REG_HH) = 0 Then
            If Percussion_On(4) = 1 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, 42, &H0
                Percussion_On(4) = 0
            End If
        Else
            If Percussion_On(4) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 42, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 42, HH_VOL
                Percussion_On(4) = 1
            End If
        End If
        ' Note Value 46 (Open HiHat) replaced with 51 (Ride Cymbal 1),
        ' because REG_TCT is often used with REG_HH at the same time and
        ' prevents the Cymbal from playing
        If (Data And YM2413_REG_TCT) = 0 Then
            If Percussion_On(3) = 1 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, 46, &H0
                Percussion_On(3) = 0
            End If
        Else
            If Percussion_On(3) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 51, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 46, TCT_VOL
                Percussion_On(3) = 1
            End If
        End If
    
'    Case YM2413_REG_TEST
    
    'Case YM2413_REG_FNum_LSB To (YM2413_REG_FNum_LSB + 8)
        'CH = Register - YM2413_REG_FNum_LSB
        '
        'If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        '
        'FNum_LSB(CH) = Data
    
    'Case YM2413_REG_SUS_KEY_BLOCK_FNum_MSB To (YM2413_REG_SUS_KEY_BLOCK_FNum_MSB + 8)
    Case YM2413_REG_FNum_LSB To (YM2413_REG_FNum_LSB + 8), _
        YM2413_REG_SUS_KEY_BLOCK_FNum_MSB To (YM2413_REG_SUS_KEY_BLOCK_FNum_MSB + 8)
        'CH = Register - YM2413_REG_SUS_KEY_BLOCK_FNum_MSB
        CH = Register And &HF
        
        If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        
        If (Register And &HF0) = YM2413_REG_FNum_LSB Then
            FNum_LSB(CH) = Data
            If YM2413_OPTIMIZED_VGMS = 0 Then
                Exit Sub
            End If
        ElseIf (Register And &HF0) = YM2413_REG_SUS_KEY_BLOCK_FNum_MSB Then
            SUS_ON(CH) = IIf((Data And YM2413_REG_SUS) = 0, 0, 1)
            KEY_ON(CH) = IIf((Data And YM2413_REG_KEY) = 0, 0, 1)
            Block(CH) = ((Data And YM2413_REG_BLOCK) / 2)
            FNum_MSB(CH) = (Data And YM2413_REG_FNum_MSB)
        End If
        
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = (FNum_MSB(CH) * 256) + FNum_LSB(CH)
        
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_YM2413(FNum_2(CH), Block(CH))
        
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = Note(Hz_2(CH))
        
        NoteOn_1(CH) = NoteOn_2(CH)
        If (Register And &HF0) = YM2413_REG_SUS_KEY_BLOCK_FNum_MSB Then
            NoteOn_2(CH) = KEY_ON(CH)
        End If
        
        If KEY_ON(CH) = 0 Then
            If NoteOn_1(CH) <> 0 And Note_1(CH) <> 0 Then
                MIDI_Event_Write MIDI_NOTE_OFF, CH, MIDINote(CH), &H0
                MIDINote(CH) = &HFF
            End If
        ElseIf KEY_ON(CH) = 1 Then
            If NoteOn_2(CH) <> NoteOn_1(CH) Then
                DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH), 255
            Else 'If (Register And &HF0) = YM2413_REG_SUS_KEY_BLOCK_FNum_MSB And _
                    Note_1(CH) <> Note_2(CH) Then
                DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH)
            End If
        End If
    
    Case YM2413_REG_INST_VOL To (YM2413_REG_INST_VOL + 5)
        CH = Register - YM2413_REG_INST_VOL
        
        TempByt = Instrument(CH)
        Instrument(CH) = (Data And YM2413_REG_INST) \ 16
        If YM2413_PROG_DISABLED(CH) = 0 And (InsVol(CH) = Data Or TempByt <> Instrument(CH)) Then
            Select Case Instrument(CH)
            Case INST_ORIGINAL
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(0)
            Case INST_VIOLIN
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(1)
            Case INST_GUITAR
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(2)
            Case INST_PIANO
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(3)
            Case INST_FLUTE
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(4)
            Case INST_CLARINET
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(5)
            Case INST_OBOE
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(6)
            Case INST_TRUMPET
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(7)
            Case INST_ORGAN
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(8)
            Case INST_HORN
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(9)
            Case INST_SYNTHESIZER
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(10)
            Case INST_HARPSICHORD
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(11)
            Case INST_VIBRAPHONE
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(12)
            Case INST_BASS_SYNTH
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(13)
            Case INST_BASS_ACOUSTIC
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(14)
            Case INST_GUITAR_ELECTRIC
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, YM2413_MIDI_PATCH(15)
            End Select
        End If
        
        TempByt = Volume(CH)
        Volume(CH) = Data And YM2413_REG_VOL
        If YM2413_VOL_DISABLED(CH) = 0 And (InsVol(CH) = Data Or TempByt <> Volume(CH)) Then
            'Volume(CH) = MIDI_VOLUME_MAX - ((Data And YM2413_REG_VOL) * 8) + 1
            'If Volume(CH) = &H80 Then Volume(CH) = &H7F
            MIDIVolume(CH) = DB2MidiVol(YM2413_Vol2DB(Volume(CH)))
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, MIDIVolume(CH)
        End If
        InsVol(CH) = Data
    
    Case (YM2413_REG_INST_VOL + 6) To (YM2413_REG_INST_VOL + 8)
        If YM2413_PERCUSSION_DISABLED = 1 Then Exit Sub
        
        Select Case Register
        Case (YM2413_REG_INST_VOL + 6)
            ''BD_VOL = (MIDI_VOLUME_MAX - ((Data And 15) * 8)) * 0.8
            'BD_VOL = (MIDI_VOLUME_MAX - ((Data And &HF) * &H8)) + 1
            'If BD_VOL = &H80 Then BD_VOL = &H7F
            BD_VOL = DB2MidiVol(YM2413_Vol2DB(Data And &HF))
        Case (YM2413_REG_INST_VOL + 7)
            'HH_VOL = MIDI_VOLUME_MAX - (((Data And &HF0) / &H10) * 8) + 1
            'If HH_VOL = &H80 Then HH_VOL = &H7F
            HH_VOL = DB2MidiVol(YM2413_Vol2DB((Data And &HF0) \ &H10))
            ''SD_VOL = (MIDI_VOLUME_MAX - ((Data And 15) * 8)) * 0.8
            'SD_VOL = (MIDI_VOLUME_MAX - ((Data And &HF) * &H8)) + 1
            'If SD_VOL = &H80 Then SD_VOL = &H7F
            SD_VOL = DB2MidiVol(YM2413_Vol2DB(Data And &HF))
        Case (YM2413_REG_INST_VOL + 8)
            ''TOM_VOL = (MIDI_VOLUME_MAX - (((Data And 240) / 16) * 8)) * 0.6
            'TOM_VOL = (MIDI_VOLUME_MAX - (((Data And &HF0) / &H10) * 8)) + 1
            'If TOM_VOL = &H80 Then TOM_VOL = &H7F
            TOM_VOL = DB2MidiVol(YM2413_Vol2DB((Data And &HF0) \ &H10))
            'TCT_VOL = MIDI_VOLUME_MAX - ((Data And &HF) * &H8) + 1
            'If TCT_VOL = &H80 Then TCT_VOL = &H7F
            TCT_VOL = DB2MidiVol(YM2413_Vol2DB(Data And &HF))
        End Select
    
'    Case Else
    
    End Select

    Exit Sub
ErrHandler:
    Dim strPrompt As String, lngResult As Long
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "YM2413_Command_Handle")
    If lngResult = vbYes Then End
End Sub

Public Function YM2413_Vol2DB(ByVal TL As Byte) As Single

    YM2413_Vol2DB = -TL * 3

End Function
