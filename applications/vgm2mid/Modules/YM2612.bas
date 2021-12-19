Attribute VB_Name = "basYM2612"
Option Explicit

' YM2612 Register Select Constants
Public Const YM2610_DELTAT_ADPCM = &H10  ' DELTA-T/ADPCM
Public Const YM2612_TEST = &H21  ' LSI Test Data
Public Const YM2612_LFO_EN_LFO_FREQ = &H22
Public Const YM2612_LFO_EN = 8
Public Const YM2612_LFO_FREQ = 7
Public Const YM2612_TIMER_A_MSB = &H24
Public Const YM2612_TIMER_A_LSB = &H25
Public Const YM2612_TIMER_B = &H26
Public Const YM2612_CH3_MODE_RESET_ENABLE_LOAD = &H27
Public Const YM2612_CH3_MODE = 192
Public Const YM2612_TIMER_RESET = 48
Public Const YM2612_TIMER_ENABLE = 12
Public Const YM2612_TIMER_LOAD = 3
Public Const YM2612_SLOT_CH = &H28  ' Key On/Off
Public Const YM2612_SLOT = 240
Public Const YM2612_CH = 7
Public Const YM2612_DAC = &H2A  ' DAC Data
Public Const YM2612_DAC_DATA = 255
Public Const YM2612_DAC_EN = &H2B  ' DAC Data
Public Const YM2612_DAC_EN_BIT = 127
Public Const YM2612_DT_MULTI = &H30  ' Detune/Multiple
Public Const YM2612_DT = 112
Public Const YM2612_MULTI = 15
Public Const YM2612_TL = &H40  ' Total Level
Public Const YM2612_KS_AR = &H50  ' Key Scale/Attack Rate
Public Const YM2612_KS = 192
Public Const YM2612_AR = 31
Public Const YM2612_DR = &H60  ' Decay Rate
Public Const YM2612_SR = &H70  ' Sustain Rate
Public Const YM2612_SL_RR = &H80  ' Sustain Level/Release Rate
Public Const YM2612_SL = 240
Public Const YM2612_RR = 15
Public Const YM2612_SSG_EG = &H90  ' SSG-Type Envelope Control
Public Const YM2612_FNum_LSB = &HA0
Public Const YM2612_Block_FNum_MSB = &HA4
Public Const YM2612_Block = 56
Public Const YM2612_FNum_MSB = 7
Public Const YM2612_CH3_SPECIAL_FNum_MSB = &HA8
Public Const YM2612_CH3_SPECIAL_BLOCK_FNum_LSB = &HAC
Public Const YM2612_CH3_SPECIAL_Block = 56
Public Const YM2612_CH3_SPECIAL_FNum_LSB = 7
Public Const YM2612_FB_CONNECTION = &HB0  ' Self-Feedback/Connection
Public Const YM2612_FB = 56
Public Const YM2612_CONNECTION = 7
Public Const YM2612_L_R = &HB4  ' Pan Select
Public Const YM2612_L = 128
Public Const YM2612_R = 64
Public Const YM2612_BOTH_L_R = 192

Public DAC_DataByte As Byte
Private ADPCM_DN(&H0 To &H5) As Byte    ' ADPCM Drum Notes

Public Function Hz_YM2612(ByVal FNum As Double, Optional Block As Byte) As Double

    Hz_YM2612 = FNum * fsam2612 * (2 ^ (Block - 22))

End Function

Public Sub YM2612Command_Handle(ByVal Port As Byte, ByVal Register As Byte, ByVal Data As Byte)

'    Static LFO_Freq As Byte
'    Static TimerA_MSB As Byte, TimerA_LSB As Byte, TimerA As Integer
'    Static TimerB As Byte
'    Static CH3_Mode As Byte ', Timer_RESET As Byte, Timer_ENABLE As Byte, Timer_LOAD As Byte
    Static Slot(5) As Byte, CH As Byte, OP As Byte
    Static DAC_EN As Byte
'    Static DT(5, 3) As Byte, MULTI(5, 3) As Byte
    Static TL(5, 3) As Byte
    Static Volume(5) As Byte
'    Static KS(5, 3) As Byte, AR(5, 3) As Byte
'    Static DR(5, 3) As Byte
'    Static SR(5, 3) As Byte
'    Static SL(5, 3) As Byte, RR(5, 3) As Byte
'    Static SSG_EG(5, 3) As Byte
    Static FNum_MSB(5) As Byte
    Static Block(5) As Byte, FNum_LSB(5) As Byte, FNum_1(5) As Long, FNum_2(5) As Long, Hz_1(5) As Double, Hz_2(5) As Double, Note_1(5) As Double, Note_2(5) As Double
'    Static CH3_Special_FNum_MSB(2) As Byte
'    Static CH3_Special_Block(2) As Byte, CH3_Special_FNum_LSB(2) As Byte, CH3_Special_FNum_1(2) As Integer, CH3_Special_FNum_2(2) As Integer
    Static Feedback(5) As Byte, Connection(5) As Byte
    Static MIDINote(5) As Byte, MIDIWheel(5) As Integer, MIDIVolume(5) As Byte, MIDIPan(5) As Byte, MIDIMod(5) As Byte, NoteOn_1(5) As Byte, NoteOn_2(5) As Byte
    Dim TempByt As Byte
    Dim TempSng As Single
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2612 = 1 Then
        Erase Slot: CH = 0: OP = 0
        DAC_EN = 0
        Erase TL: Erase Volume
        Erase FNum_MSB
        Erase Block: Erase FNum_LSB: Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        Erase Feedback: Erase Connection
        Erase MIDINote: Erase MIDIWheel: Erase MIDIVolume: Erase MIDIPan: Erase MIDIMod: Erase NoteOn_1: Erase NoteOn_2
        ADPCM_DN(&H0) = &H23    ' Bass Drum
        ADPCM_DN(&H1) = &H26    ' Snare Drum
        ADPCM_DN(&H2) = &H33    ' Top Cymbal
        ADPCM_DN(&H3) = &H2A    ' High Hat
        ADPCM_DN(&H4) = &H2D    ' Tom Tom
        ADPCM_DN(&H5) = &H25    ' Rim Shot
        Variables_Clear_YM2612 = 0
        For CH = &H0 To &H5
            Volume(CH) = &HFF
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
            MIDIVolume(CH) = &HFF
            MIDIPan(CH) = &HFF
            MIDIMod(CH) = &HFF
        Next CH
    End If
    
    Select Case Register
    Case &H0 To &H1F
        If Port = &H0 Then
            If OPNType = OPN_TYPE_YM2608 Then
                If (Register And &H10) = &H10 Then
                    Call FMOPN_ADPCM_Write(Register And &HF, Data)
                End If
            ElseIf OPNType = OPN_TYPE_YM2610 Then
                If (Register And &H10) = &H0 Then
                    Call YM_ADPCM_Write(Register And &HF, Data)
                End If
            End If
        Else
            If OPNType = OPN_TYPE_YM2608 Then
                If (Register And &H10) = &H0 Then
                    Call YM_ADPCM_Write(Register And &HF, Data)
                End If
            ElseIf OPNType = OPN_TYPE_YM2610 Then
                If Register < &H30 Then
                    Call FMOPN_ADPCM_Write(Register And &HF, Data)
                End If
            End If
        End If
'    Case YM2612_TEST
    
'    Case YM2612_LFO_EN_LFO_FREQ
    
'    Case YM2612_TIMER_A_MSB
    
'    Case YM2612_TIMER_A_LSB
    
'    Case YM2612_TIMER_B
    
'    Case YM2612_CH3_MODE_RESET_ENABLE_LOAD
'        CH3_Mode = (Data And YM2612_CH3_MODE) / 96
    
    Case YM2612_SLOT_CH
        CH = (Data And YM2612_CH)
        CH = IIf(CH > 3, CH - 1, CH)
        
        CH = IIf(CH > 5, 5, CH)
        
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        
        Slot(CH) = (Data And YM2612_SLOT) / 8
        
        If Slot(CH) = 0 Then
            If NoteOn_2(CH) <> 0 Then
                MIDIWheel(CH) = MIDI_PITCHWHEEL_CENTER
'                MIDI_Event_Write MIDI_PITCHWHEEL, CH, MIDIWheel(CH)
                MIDI_Event_Write MIDI_NOTE_OFF, CH, MIDINote(CH), &H0
                MIDINote(CH) = &HFF
                NoteOn_1(CH) = NoteOn_2(CH)
                NoteOn_2(CH) = 0
            End If
        Else
            If NoteOn_2(CH) = 0 Then
                DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH), 255
                NoteOn_1(CH) = NoteOn_2(CH)
                NoteOn_2(CH) = 1
            End If
        End If
    
    Case YM2612_DAC
    
        If YM2612_DAC_DISABLED = 1 Then Exit Sub
        If OPNType <> OPN_TYPE_YM2612 Then Exit Sub
        
        Static LastDACNote As Byte
        
        'If Data = &HF Then
        '    Data = &H14    ' Sonic 3K Bass Drum
        'ElseIf Data = &H10 Then
        '    Data = &H16    ' Sonic 3K Snare Drum
        'Else
        '    Data = &HFF
        'End If
        'If Data = &H22 Then
        '    Data = &H23     ' Sonic Crackers Bass Drum
        'ElseIf Data = &H23 Then
        '    Data = &H26     ' Sonic Crackers Snare Drum
        'ElseIf Data = &HC4 Then
        '    Data = &H2D     ' Sonic Crackers Tom Tom
        'Else
        '    Data = &HFF
        'End If
        'If Data = &H1A Then
        '    Data = &H23     ' Sonic 1 Bass Drum
        'ElseIf Data = &HB Then
        '    Data = &H26     ' Sonic 1 Snare Drum
        'Else
        '    Data = &HFF
        'End If
        If Data >= &H20 Then Data = &HFF
        
        If Data <> &HFF Then
            MIDI_Event_Write MIDI_NOTE_OFF, CHN_DAC, LastDACNote, &H0
            'MIDI_Event_Write MIDI_NOTE_ON, CHN_DAC, 35, Data
            MIDI_Event_Write MIDI_NOTE_ON, CHN_DAC, Data, &H7F
            LastDACNote = Data
        End If
    
    Case YM2612_DAC_EN
        If (Register And YM2612_DAC_EN) = YM2612_DAC_EN Then DAC_EN = 1 Else DAC_EN = 0
    
'    Case YM2612_DT_MULTI
    
    Case YM2612_TL To (YM2612_TL + &HF)
        CH = ((Register Xor YM2612_TL) Mod 4) + Port
        
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        If YM2612_VOL_DISABLED(CH) = 1 Then Exit Sub
            
        OP = Fix((Register Xor YM2612_TL) / 4)
    
        CH = IIf(CH > 5, 5, CH)
        TL(CH, OP) = Data And &H7F
        If OP < 3 Then Exit Sub
        
        TempByt = MIDIVolume(CH)
        Select Case Connection(CH)
        Case 0, 1, 2, 3
            Volume(CH) = TL(CH, 3)
        Case 4
            Volume(CH) = (CLng(TL(CH, 1)) + TL(CH, 3)) \ 2
        Case 5, 6
            Volume(CH) = (CLng(TL(CH, 1)) + TL(CH, 2) + TL(CH, 3)) \ 3
        Case 7
            Volume(CH) = (CLng(TL(CH, 0)) + TL(CH, 1) + TL(CH, 2) + TL(CH, 3)) \ 4
        End Select
        
        'Const PI = 3.14159265358979
        ''Const Phase = PI / (MIDI_VOLUME_MAX * 2)
        ''MIDIVolume(CH) = MIDI_VOLUME_MAX * (1 - (Sin(MIDIVolume(CH) * Phase)))
        'MIDIVolume(CH) = &H80 * (1# - Sin(Volume(CH) / &H80 * (PI / 2)))
        'If MIDIVolume(CH) = &H80 Then
        '    MIDIVolume(CH) = &H7F
        'End If
        MIDIVolume(CH) = DB2MidiVol(YM3812_Vol2DB(Volume(CH)) / 4)
        
        If TempByt <> MIDIVolume(CH) Then
        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, MIDIVolume(CH)
        End If

'    Case YM2612_KS_AR
    
'    Case YM2612_DR
    
'    Case YM2612_SR
    
'    Case YM2612_SL_RR

'    Case YM2612_SSG_EG
    
    Case &HA4 To &HA6
        CH = (Register Xor &HA4) + Port
        
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        
        Block(CH) = (Data And YM2612_Block) / 8
        FNum_MSB(CH) = (Data And 7)
    Case &HA0 To &HA2
        CH = (Register Xor &HA0) + Port
        
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        
        FNum_LSB(CH) = Data
        
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = ((FNum_MSB(CH) * 256) + FNum_LSB(CH))
        
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_YM2612(FNum_2(CH), Block(CH))
                    
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = Note(Hz_2(CH))
        
        If NoteOn_2(CH) = 1 Then
            If Note_2(CH) <> Note_1(CH) Then
                DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH)
            End If
        End If
        
'    Case YM2612_CH3_SPECIAL_FNum_MSB To (YM2612_CH3_SPECIAL_FNum_MSB + 2)
    
'    Case YM2612_CH3_SPECIAL_BLOCK_FNum_LSB To (YM2612_CH3_SPECIAL_BLOCK_FNum_LSB + 2)
    
    Case YM2612_FB_CONNECTION To (YM2612_FB_CONNECTION + 2)
        CH = (Register Xor YM2612_FB_CONNECTION) + Port
        Connection(CH) = (Data And YM2612_CONNECTION)
    
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        If YM2612_PROG_DISABLED(CH) = True Then Exit Sub
        
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, Data And &H7F
        'MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, (Data And &HF8) / &H8
    
    Case YM2612_L_R To (YM2612_L_R + 2)
        CH = (Register Xor YM2612_L_R) + Port
        
        If YM2612_CH_DISABLED(CH) = 1 Then Exit Sub
        If YM2612_PAN_DISABLED(CH) = 1 Then Exit Sub
        
        If CH = &H5 And DAC_EN Then
            MIDIPan(CH) = &HFF
        End If
        Select Case (Data And YM2612_BOTH_L_R)
        Case YM2612_L
            TempByt = MIDI_PAN_LEFT
        Case YM2612_R
            TempByt = MIDI_PAN_RIGHT
        Case YM2612_BOTH_L_R, 0
            TempByt = MIDI_PAN_CENTER
        End Select
        If MIDIPan(CH) <> TempByt Then
            MIDIPan(CH) = TempByt
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
        End If
        
        TempSng = (Data And &H7) / &H7
        TempByt = TempSng * TempSng * &H7F
        If MIDIMod(CH) <> TempByt Then
            MIDIMod(CH) = TempByt
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_MODULATOR_WHEEL, MIDIMod(CH)
        End If
    
        If YM2612_DAC_DISABLED = 1 Then Exit Sub
        
        'If CH = 5 And DAC_EN = 1 Then
        '    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CHN_DAC, MIDI_PAN, MIDIPan(CH)
        '    MIDI_Event_Write MIDI_NOTE_OFF, CHN_DAC, 35, 0
        '    MIDI_Event_Write MIDI_NOTE_ON, CHN_DAC, 35, MIDI_VOLUME_MAX * 0.8
        'End If

    Case Else
        Exit Sub
        Debug.Print "Register " & Hex$(Register) & ": ";
        Select Case Register
        Case YM2612_TEST
            Debug.Print "TEST - LSI Test Data"
        Case YM2612_LFO_EN_LFO_FREQ
            Debug.Print "LFO_EN_LFO_FREQ"
        Case YM2612_TIMER_A_MSB
            Debug.Print "TIMER_A_MSB"
        Case YM2612_TIMER_A_LSB
            Debug.Print "TIMER_A_LSB"
        Case YM2612_TIMER_B
            Debug.Print "TIMER_B"
        Case YM2612_CH3_MODE_RESET_ENABLE_LOAD
            Debug.Print "CH3_MODE_RESET_ENABLE_LOAD"
        Case YM2612_SLOT_CH
            Debug.Print "SLOT_CH - Key On/Off"
        Case YM2612_DAC
            Debug.Print "DAC - DAC Data"
        Case YM2612_DAC_DATA
            Debug.Print "DAC_DATA"
        Case YM2612_DAC_EN
            Debug.Print "DAC_EN - DAC Data"
        Case YM2612_DT_MULTI
            Debug.Print "DT_MULTI - Detune/Multiple"
        Case YM2612_TL
            Debug.Print "TL - Total Level"
        Case YM2612_KS_AR
            Debug.Print "KS_AR - Key Scale/Attack Rate"
        Case YM2612_DR
            Debug.Print "DR - Decay Rate"
        Case YM2612_SR
            Debug.Print "SR - Sustain Rate"
        Case YM2612_SL_RR
            Debug.Print "SL_RR - Sustain Level/Release Rate"
        Case YM2612_SSG_EG
            Debug.Print "SSG_EG - SSG-Type Envelope Control"
        Case YM2612_FNum_LSB
            Debug.Print "FNum_LSB"
        Case YM2612_Block_FNum_MSB
            Debug.Print "Block_FNum_MSB"
        Case YM2612_CH3_SPECIAL_FNum_MSB
            Debug.Print "CH3_SPECIAL_FNum_MSB"
        Case YM2612_CH3_SPECIAL_BLOCK_FNum_LSB
            Debug.Print "CH3_SPECIAL_BLOCK_FNum_LSB"
        Case YM2612_CH3_SPECIAL_FNum_LSB
            Debug.Print "CH3_SPECIAL_FNum_LSB"
        Case YM2612_FB_CONNECTION
            Debug.Print "FB_CONNECTION - Self-Feedback/Connection"
        Case YM2612_L_R
            Debug.Print "L_R - Pan Select"
        Case Else
            Debug.Print "Unknown"
        End Select
        'Stop
    End Select
    
    Exit Sub
ErrHandler:
    Dim strPrompt As String, lngResult As Long
    strPrompt = "Error #" & Err.Number _
    & vbCrLf & "'" & Err.Description & "'" _
    & vbCrLf & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbYesNo + vbCritical, "YM2612_Command_Handle")
    If lngResult = vbYes Then End
End Sub

Private Sub FMOPN_ADPCM_Write(ByVal Register As Byte, ByVal Data As Byte)

    Dim CH As Byte
    Dim TempByt As Byte
    Dim Volume As Integer
    Dim VolMul As Byte
    Dim VolShift As Byte
    Static TL As Byte
    Static IL(5) As Byte
    Static InsVol(5) As Byte
    Static NoteOn(5) As Byte
    Static VolMax As Byte
    
    Select Case Register
    Case &H0    ' DM, --, C5, C4, C3, C2, C1, C0
        If (Data And &H80) = &H0 Then
            ' Key On
            For CH = &H0 To &H5
                If Data And (2 ^ CH) Then
                    If NoteOn(CH) Then
                        MIDI_Event_Write MIDI_NOTE_OFF, &H9, ADPCM_DN(CH), &H0
                    End If
                    MIDI_Event_Write MIDI_NOTE_ON, &H9, ADPCM_DN(CH), InsVol(CH)
                    NoteOn(CH) = 1
                Else
                    If NoteOn(CH) Then
                        MIDI_Event_Write MIDI_NOTE_OFF, &H9, ADPCM_DN(CH), &H0
                    End If
                    NoteOn(CH) = 0
                End If
            Next CH
        Else
            ' All Keys Off
            For CH = &H0 To &H5
                If NoteOn(CH) Then
                    MIDI_Event_Write MIDI_NOTE_OFF, &H9, ADPCM_DN(CH), &H0
                End If
                NoteOn(CH) = 0
            Next CH
        End If
    Case &H1    ' Bit 0-5 = Total Level
        TL = (Not Data) And &H3F
        If VolMax = 0 Then VolMax = &HFF
        'TempByt = (Not Data) And &H3F
        'For CH = &H0 To &H5
        '    Volume = TL + IL(CH)
        '    If Volume >= &H3F Then
        '        VolMul = &H0
        '        VolShift = &H0
        '    Else
        '        VolMul = &HF - (Volume And &H7)
        '        VolShift = &H1 + ((Volume And &H38) / &H8)
        '    End If
        '    'Volume = (AdPcm_Acc * VolMul) / 2 ^ VolShift
        '    Volume = &H100 * VolMul / 2 ^ VolShift
        'Next CH
    Case Else
        CH = Register And &H7
        If CH >= &H6 Then Exit Sub
        
        Select Case Register And &H38
        Case &H8    ' Bit 7 = L, Bit 6 = R, Bit 4-0 = Instrument Level
            IL(CH) = (Not Data) And &H3F
            Volume = TL + IL(CH)
            If Volume < VolMax Then VolMax = Volume
            If Volume >= &H3F Then
                VolMul = &H0
                VolShift = &H0
            Else
                VolMul = &HF - (Volume And &H7)
                VolShift = &H1 + ((Volume And &H38) / &H8)
            End If
            
            Select Case (Register And &HC0) / &H40
            Case &H1
                TempByt = MIDI_PAN_RIGHT
            Case &H2
                TempByt = MIDI_PAN_LEFT
            Case &H0, &H3
                TempByt = MIDI_PAN_CENTER
            End Select
            'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
            
            'Volume = (AdPcm_Acc * VolMul) / 2 ^ VolShift
            Volume = &H100& * VolMul / 2 ^ VolShift
            If Volume = &H80 Then Volume = &H7F
            If Volume >= &H100 Then Volume = Volume And &HFF Or &H80
            If Volume = &H0 Then Volume = &H1
            InsVol(CH) = Volume
            'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, Volume
        Case &H10, &H18 ' Start Address
            If (Register And &H38) = &H18 Then
                Debug.Print Hex(Data)
                'Stop
            End If
        Case &H20, &H28 ' End Address
        End Select
    End Select

End Sub

Private Sub YM_ADPCM_Write(ByVal Register As Byte, ByVal Data As Byte)

    Static InsVol As Byte
    
    Select Case Register And &HF
    Case &H0    ' Control 1: Start, Rec, MemMode, Repeat, SpOff, --, --, Reset
        If Data And &H80 Then
            MIDI_Event_Write MIDI_NOTE_OFF, &H9, &H7F, &H0
            MIDI_Event_Write MIDI_NOTE_ON, &H9, &H7F, InsVol
        Else
            MIDI_Event_Write MIDI_NOTE_OFF, &H9, &H7F, &H0
        End If
    Case &H1    ' Control 2: L, R, -, -, Sample, DA/AD, RAMTYPE, ROM
        Select Case (Data And &HC0) / &H40
        Case &H1
            'MIDIPan(CH) = MIDI_PAN_RIGHT
        Case &H2
            'MIDIPan(CH) = MIDI_PAN_LEFT
        Case &H3, &H0
            'MIDIPan(CH) = MIDI_PAN_CENTER
        End Select
    Case &H2    ' Start Address Low
    Case &H3    ' Start Address High
    Case &H4    ' Stop Address Low
    Case &H5    ' Stop Address High
    Case &H6    ' Prescale Low
    Case &H7    ' Prescale High
    Case &H8    ' ADPCM Data
    Case &H9    ' Delta-N Low
    Case &HA    ' Delta-N High
    Case &HB    ' Volume
        InsVol = Int(Data / &H2)
    Case &HC    ' Flag Control: Extend Status Clear/Mask
    End Select

End Sub
