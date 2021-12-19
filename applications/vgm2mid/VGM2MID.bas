Attribute VB_Name = "basVGM2MID"
Option Explicit

Public DAC_Data() As Byte
Public DAC_Pos As Long
Public Const CHN_DAC = 9

Public CNV_ACCURACY As Byte
Public DUAL_CHIPS As Byte
Public VGM_LOOPS As Integer
Public TEMPO_MOD As Byte
Public TEMPO_BPM As Single
Public TEMPO_MULT As Integer
Public TEMPO_DIV As Integer
Public Const MIDI_NOTE_STEPS = 12
'Public Const PITCHWHEEL_SENSITIVITY = 64 '+/- n Semitones
'Public Const PITCHWHEEL_STEPS_REAL = 8192 / PITCHWHEEL_SENSITIVITY
'Public Const PITCHWHEEL_STEPS_DEFAULT = 4096 '16384 / 4
Public Const PITCHWHEEL_SENSITIVITY_DEFAULT = 2 '+/- n Semitones
Public Const PITCHWHEEL_STEPS_DEFAULT = 4096 '16384 / 4
Public PITCHWHEEL_SENSITIVITY As Long
Public PITCHWHEEL_STEPS As Long

'Public Const MIDI_NOTE_CURVE = 2 ^ (1 / MIDI_NOTE_STEPS)
'Public Const PITCHWHEEL_CURVE = MIDI_NOTE_CURVE ^ (1 / PITCHWHEEL_STEPS)

Public Variables_Clear_PSG As Byte
Public Variables_Clear_YM2413 As Byte
Public Variables_Clear_YM2612 As Byte
Public Variables_Clear_YM2151 As Byte

' Timing
Public Const OSC1 = 53693100
Public Const fM_YM2413_PSG = OSC1 / 15
Public Const fsam_YM2413_PSG = fM_YM2413_PSG / 72
Public Const fM_YM2612 = OSC1 / 14
Public Const fsam_YM2612 = fM_YM2612 / 72

Public Const OPL_TYPE_YM3526 = &H1
Public Const OPL_TYPE_YM3812 = &H2
Public Const OPL_TYPE_YMF262 = &H3
Public Const OPL_TYPE_Y8950 = &H8
Public Const OPN_TYPE_YM2203 = &H1
Public Const OPN_TYPE_YM2608 = &H2
Public Const OPN_TYPE_YM2610 = &H3
Public Const OPN_TYPE_YM2612 = &H4

Public ClockPSG As Long
Public Clock2413 As Long
Public Clock2612 As Long
Public Clock2151 As Long
Public Clock2203 As Long
Public Clock2608 As Long
Public Clock2610 As Long
Public Clock3812 As Long
Public Clock3526 As Long
Public Clock8950 As Long
Public OPLType As Byte
Public OPNType As Byte
Public fsam2413 As Double
Public fsam2612 As Double
Public fsam3812 As Double
Public ClockAY As Long

' Options
Public PSG_CH_DISABLED(3) As Byte
Public PSG_NOISE_DISABLED As Byte
Public PSG_VOL_DISABLED(3) As Byte
Public PSG_VOLDEP_NOTES As Byte

Public YM2413_CH_DISABLED(8) As Byte
Public YM2413_VOL_DISABLED(8) As Byte
Public YM2413_PROG_DISABLED(8) As Byte
Public YM2413_PERCUSSION_DISABLED As Byte
Public YM2413_OPTIMIZED_VGMS As Byte
Public YM2413_MIDI_PATCH(15) As Byte

Public YM2612_CH_DISABLED(5) As Byte
Public YM2612_VOL_DISABLED(5) As Byte
Public YM2612_PROG_DISABLED(5) As Byte
Public YM2612_PAN_DISABLED(5) As Byte
'Public YM2612_MIDI_PATCH(5) As Byte
Public YM2612_DAC_DISABLED As Byte

Public YM2151_CH_DISABLED(7) As Byte
Public YM2151_VOL_DISABLED(7) As Byte
Public YM2151_PROG_DISABLED(7) As Byte
Public YM2151_PAN_DISABLED(7) As Byte

Public T6W28_PSG  As Boolean

' Status Variables
Public Conversion_Status_Current As Long
Public Conversion_Status_Total As Long

Public Sub MID_Data_Init(ByVal PSGOn As Boolean)
    
    Dim CH As Byte
    Dim TempoVal As Double
    
    'MIDI_Event_Write MIDI_META_EVENT, META_TEMPO, 500000
    TempoVal = 500000
    If TEMPO_MOD = &H0 Then
        TempoVal = TempoVal * 120 / TEMPO_BPM
    ElseIf TEMPO_MOD = &H1 Then
        TempoVal = TempoVal * TEMPO_MULT / TEMPO_DIV
    End If
    MIDI_Event_Write MIDI_META_EVENT, META_TEMPO, TempoVal
    
    ' I think there's no need to init the instruments for the FM Channels.
    ' Most things are done before playing the first note.
    
    ' Pan (Stereo) Settings for FM CHs 1-9 (Ch 3 Special)
    For CH = 0 To 8
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_CENTER
    Next
    
    ' Program Changes for FM CHs 1-9 (Ch 3 Special)
    'For CH = 0 To 8
    '    MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, MIDI_PATCH_Lead_8_Bass_Lead
    'Next

    ' Initial Volume Levels for FM CHs 1-9 (Ch 3 Special)
    'For CH = 0 To 8
    '    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, 95
    'Next
    
    ' Change Pitch Wheel Sensitivity for All CHs  (Ch 3 Special)
    If PITCHWHEEL_SENSITIVITY <> PITCHWHEEL_SENSITIVITY_DEFAULT Then
        For CH = &H0 To &HF
            If CH = 9 Then
                ' There's no need to set the PitchBend-Range for Ch 9 (Drum-Channel)
                CH = 10
            End If
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_RPN_MSB, RPN_PITCH_BEND_RANGE_M
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_RPN_LSB, RPN_PITCH_BEND_RANGE_L
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_DATA_ENTRY_MSB, PITCHWHEEL_SENSITIVITY
        Next
    End If
    
    ' Settings for Drum Channel
    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CHN_DAC, MIDI_PAN, MIDI_PAN_CENTER
    MIDI_Event_Write MIDI_PROGRAM_CHANGE, CHN_DAC, &H0
    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CHN_DAC, MIDI_VOLUME, 127
    
    If PSGOn Then
    ' Pan (Stereo) Settings for PSG CHs 1-3 and Noise CH
    For CH = 10 To 13
        If Not T6W28_PSG Then
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_CENTER
        Else
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH - 10, MIDI_PAN, MIDI_PAN_RIGHT
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDI_PAN_LEFT
        End If
    Next
    
    ' Program Changes for PSG CHs 1-3 and Noise CH
    For CH = 10 To 12
        If T6W28_PSG Then
            MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH - 10, MIDI_PATCH_Lead_1_Square
        End If
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, MIDI_PATCH_Lead_1_Square
    Next
    If T6W28_PSG Then
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, 3, MIDI_PATCH_Gunshot
    End If
    MIDI_Event_Write MIDI_PROGRAM_CHANGE, 13, MIDI_PATCH_Gunshot

    ' Initial Volume Levels for PSG CHs 1-3 and Noise CH
    For CH = 10 To 13
        If T6W28_PSG Then
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, 127
        End If
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, 127
    Next
    
    End If
    
End Sub

Public Function DoNoteOn(ByVal Note_1 As Double, ByVal Note_2 As Double, ByVal MIDIChannel As Byte, ByRef MIDINote As Byte, ByRef MIDIWheel As Integer, Optional Note_Type As Byte, Optional NoteVolume As Byte = &H7F) As Boolean

    ' the returned value ist used to detect written notes
    ' (and avoid notes of Length 0)
    
    If Note_Type = 255 Or Note_1 = &HFF Or Note_2 = &HFF Then GoTo DoNoteOn
    If Note_1 = 255 Then MsgBox "foo"
    
    Dim dblTestValue As Double
    dblTestValue = MIDIWheel + ((Note_2 - Note_1) * PITCHWHEEL_STEPS)
    
    'If Abs(Note_2 - Note_1) >= 0.5 Then
    '    dblTestValue = -1
    'End If
    
    Select Case dblTestValue
    Case MIDI_PITCHWHEEL_MIN To MIDI_PITCHWHEEL_MAX + 1
        If dblTestValue = MIDI_PITCHWHEEL_MAX + 1 Then
            dblTestValue = MIDI_PITCHWHEEL_MAX
        End If
        MIDIWheel = dblTestValue
        MIDI_Event_Write MIDI_PITCHWHEEL, MIDIChannel, MIDIWheel
    Case Else
        GoTo DoNoteOn
    End Select
        
    DoNoteOn = False    ' only PitchBend written
    Exit Function
    
DoNoteOn:
    If Note_2 > &HFF Then Note_2 = &HFF
    If Note_2 = &HFF Then
        If MIDINote < &HFF Then
            MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote, &H0
            MIDINote = Note_2
        End If
        DoNoteOn = True
        Exit Function
    End If
    
    Dim dblPitchWheel As Double
    Dim NewWheel As Integer
    dblPitchWheel = (Note_2 - Fix(Note_2))
    Note_2 = Abs(Fix(Note_2))
    If dblPitchWheel >= 0.5 Then
        Note_2 = Note_2 + 1
        dblPitchWheel = -1 + dblPitchWheel
    End If
    If MIDINote < &HFF Then
        MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote, &H0
    End If
    NewWheel = MIDI_PITCHWHEEL_CENTER + (dblPitchWheel * PITCHWHEEL_STEPS)
    If NewWheel <> MIDIWheel Then
        MIDIWheel = NewWheel
        If Not (MIDIChannel = CHN_DAC And Abs(dblPitchWheel) < 0.1) Then
            MIDI_Event_Write MIDI_PITCHWHEEL, MIDIChannel, MIDIWheel
        End If
    End If
    MIDINote = Note_2
    MIDI_Event_Write MIDI_NOTE_ON, MIDIChannel, MIDINote, NoteVolume
    
    DoNoteOn = True     ' wrote new Note

End Function

Public Function Note(ByVal Hz As Double) As Double
    
    If Hz = 0 Then Note = &HFF Else Note = ((Log(Hz) - Log(440)) / (Log(2 ^ (1 / 12)))) + 69

End Function
