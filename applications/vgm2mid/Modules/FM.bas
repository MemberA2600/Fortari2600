Attribute VB_Name = "basFM"
Option Explicit

' Timing
Public Const OSC1 = 53693100
Public Const fM_YM2413_PSG = OSC1 / 15
Public Const fsam_YM2413_PSG = fM_YM2413_PSG / 72

Public Const fM_YM2612 = OSC1 / 14
Public Const fsam_YM2612 = fM_YM2612 / 72

Public Sub DoNoteOn(ByVal Note_1 As Double, ByVal Note_2 As Double, ByVal MIDIChannel As Byte, ByRef MIDINote As Byte, ByRef MIDIWheel As Integer)
    
    Dim Diff As Double
    
    Diff = Note_2 - Note_1
    Diff = Diff * PITCHBEND_STEPS
    
    If Abs(Diff) > 0 And Abs(Diff) <= (PITCHBEND_STEPS * 2) Then
        If (MIDIWheel + (Diff)) < 0 Or (MIDIWheel + Diff) > (MIDI_PITCH_WHEEL_CENTER * 2) Then GoTo DoNoteOn
        MIDIWheel = MIDIWheel + Diff
        MIDI_Event_Write MIDI_PITCH_WHEEL, MIDIChannel, MIDIWheel
    
    ElseIf Abs(Diff) > (PITCHBEND_STEPS * 2) Or Note_2 > 0 Then
DoNoteOn:
        MIDI_Event_Write MIDI_NOTE_OFF, MIDIChannel, MIDINote, &H0
        MIDIWheel = MIDI_PITCH_WHEEL_CENTER + ((Note_2 - Fix(Note_2)) * PITCHBEND_STEPS)
        MIDI_Event_Write MIDI_PITCH_WHEEL, MIDIChannel, MIDIWheel
        MIDINote = Abs(Fix(Note_2))
        MIDI_Event_Write MIDI_NOTE_ON, MIDIChannel, MIDINote, &H7F
    
    End If

End Sub
Public Function Note(ByVal Hz As Double) As Double
    
    If Hz = 0 Then Note = 0 Else Note = (((Log(Hz) - Log(440)) / (Log(2 ^ (1 / 12)))) + 69)

End Function
