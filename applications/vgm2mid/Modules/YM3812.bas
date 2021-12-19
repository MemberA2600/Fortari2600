Attribute VB_Name = "basYM3812"
Option Explicit

' OPL Module for YM3812, YM3526, Y8950 and YMF262, based on YM2413 (OPLL) Module

' YM3812/YMF262 Register Constants
Private Const YM3812_REG_TEST_WAVESEL_EN = &H1
Private Const YM3812_REG_CSW_NOTESEL = &H8
Private Const YM3812_REG_MOD_VIB_EG_KS_MULT = &H20
Private Const YM3812_REG_KSL_TL = &H40
Private Const YM3812_REG_AR_DR = &H60
Private Const YM3812_REG_SL_RR = &H80
Private Const YM3812_REG_FNum_LSB = &HA0
Private Const YM3812_REG_KEY_BLOCK_FNum_MSB = &HB0
Private Const YM3812_REG_RHYTHM = &HBD
Private Const YM3812_FB_CONNECTION_PAN = &HC0
Private Const YM3812_WAVESEL = &HE0
Private Const YMF262_4OP_EN = &H104
Private Const YMF262_OPL3_EN = &H105

Private Const YM3812_REG_KEY = &H20
Private Const YM3812_REG_BLOCK = &H1C
Private Const YM3812_REG_FNum_MSB = &H3

Private Const YM3812_REG_RHYTHM_MODE = &H20
Private Const YM3812_REG_BD = &H10
Private Const YM3812_REG_SD = &H8
Private Const YM3812_REG_TOM = &H4
Private Const YM3812_REG_TCT = &H2
Private Const YM3812_REG_HH = &H1

Public Function Hz_YM3812(ByVal FNum As Double, Optional Block As Byte) As Double

    If Block = 0 And FNum = 0 Then
        Hz_YM3812 = 0
    Else
        Hz_YM3812 = FNum * fsam3812 * 2 ^ (Block - 20)
    End If

End Function

'Private Function OPL_TL2Vol(ByVal TotalLevel As Byte) As Byte
'
'    'Dim TempSng As Single
'
'    ' I don't think that MIDI's Volume is linear
'    'TempSng = 1 / 2 ^ ((&H3F - TotalLevel) / 8)
'    'OPL_TL2Vol = TempSng
'    OPL_TL2Vol = (&H3F - TotalLevel) * &H2
'
'End Function

Public Sub YM3812Command_Handle(ByVal Register As Integer, ByVal Data As Byte)

    Static CH As Byte, OP As Byte
    Static FNum_MSB(8) As Byte
    Static KEY_ON(8) As Byte, Block(8) As Byte, FNum_LSB(8) As Byte, FNum_1(8) As Long, FNum_2(8) As Long, Hz_1(8) As Double, Hz_2(8) As Double, Note_1(8) As Double, Note_2(8) As Double
    Static Instrument(8) As Byte, Volume(8) As Byte, BD_VOL As Byte, HH_VOL As Byte, SD_VOL As Byte, TOM_VOL As Byte, TCT_VOL As Byte
    Static MIDINote(8) As Byte, MIDIWheel(8) As Integer, MIDIVolume(8) As Byte, MIDIPan(8) As Byte, NoteOn_1(8) As Byte, NoteOn_2(8) As Byte, Percussion_On(5) As Byte
    Static OPL3Mode As Byte
    Dim TempByt As Byte
    
    On Error GoTo ErrHandler
    
    If Variables_Clear_YM2413 = 1 Then
        CH = 0
        Erase FNum_MSB
        Erase KEY_ON:  Erase Block: Erase FNum_LSB: Erase FNum_1: Erase FNum_2: Erase Hz_1: Erase Hz_2: Erase Note_1: Erase Note_2
        Erase Instrument: Erase Volume: BD_VOL = &H7F: HH_VOL = &H7F: SD_VOL = &H7F: TOM_VOL = &H7F: TCT_VOL = &H7F
        Erase MIDINote: Erase MIDIWheel: Erase MIDIVolume: Erase NoteOn_1: Erase NoteOn_2: Erase Percussion_On
        For CH = &H0 To &H8
            MIDINote(CH) = &HFF
            MIDIWheel(CH) = &H8000
            MIDIVolume(CH) = &HFF
            MIDIPan(CH) = &HFF
        Next CH
        OPL3Mode = &H0
        Variables_Clear_YM2413 = 0
    End If
    
    Select Case Register
    Case YM3812_REG_TEST_WAVESEL_EN
    
        'WaveselEnable = (Data And &H20) / &H20
    
    Case YMF262_4OP_EN
    
    Case YMF262_OPL3_EN
    
        OPL3Mode = Data And &H1
    
    Case YM3812_REG_CSW_NOTESEL
        
    Case YM3812_REG_MOD_VIB_EG_KS_MULT To YM3812_REG_MOD_VIB_EG_KS_MULT + &H15
    
        If (Register And &H7) > &H5 Then Exit Sub
        
        OP = Int((Register And &H7) / &H3)
        CH = ((Register And &H18) / &H8 * &H3) + ((Register And &H7) Mod &H3)
        If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        If OP = &H0 Then Exit Sub
        
        TempByt = (Data And &HFE) / &H2
        
        If YM2413_VOL_DISABLED(CH) = 1 Then Exit Sub
        
        MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, TempByt
    
    Case YM3812_REG_KSL_TL To YM3812_REG_KSL_TL + &H17
        
        If (Register And &H7) > &H5 Then Exit Sub
        
        OP = Int((Register And &H7) / &H3)
        CH = ((Register And &H18) / &H8 * &H3) + ((Register And &H7) Mod &H3)
        If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        
        Select Case CH
        Case &H6
            If OP = &H1 Then
                'BD_VOL = OPL_TL2Vol(Data And &H3F)
                BD_VOL = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
            End If
        Case &H7
            If OP = &H0 Then
                'HH_VOL = OPL_TL2Vol(Data And &H3F)
                HH_VOL = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
            ElseIf OP = &H1 Then
                'SD_VOL = OPL_TL2Vol(Data And &H3F)
                SD_VOL = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
            End If
        Case &H8
            If OP = &H0 Then
                'TOM_VOL = OPL_TL2Vol(Data And &H3F)
                TOM_VOL = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
            ElseIf OP = &H1 Then
                'TCT_VOL = OPL_TL2Vol(Data And &H3F)
                TCT_VOL = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
            End If
        End Select
        If OP = &H0 Then Exit Sub
        
        'TempByt = OPL_TL2Vol(Data And &H3F)
        TempByt = DB2MidiVol(YM3812_Vol2DB(Data And &H3F))
        
        If YM2413_VOL_DISABLED(CH) = 1 Then Exit Sub
        
        If Volume(CH) <> TempByt Then
            Volume(CH) = TempByt
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, Volume(CH)
        End If
    
    Case YM3812_REG_FNum_LSB To YM3812_REG_FNum_LSB + &H8, _
        YM3812_REG_KEY_BLOCK_FNum_MSB To YM3812_REG_KEY_BLOCK_FNum_MSB + &H8
        CH = Register And &HF
        
        If CH > &H8 Then Exit Sub
        If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        
        If (Register And &HF0) = YM3812_REG_FNum_LSB Then
            FNum_LSB(CH) = Data
            'Exit Sub
        ElseIf (Register And &HF0) = YM3812_REG_KEY_BLOCK_FNum_MSB Then
            KEY_ON(CH) = (Data And YM3812_REG_KEY) / YM3812_REG_KEY
            Block(CH) = (Data And YM3812_REG_BLOCK) / &H4
            FNum_MSB(CH) = Data And YM3812_REG_FNum_MSB
        End If
        
        FNum_1(CH) = FNum_2(CH)
        FNum_2(CH) = (FNum_MSB(CH) * 256) + FNum_LSB(CH)
        
        Hz_1(CH) = Hz_2(CH)
        Hz_2(CH) = Hz_YM3812(FNum_2(CH), Block(CH))
        
        Note_1(CH) = Note_2(CH)
        Note_2(CH) = Note(Hz_2(CH))
        
        NoteOn_1(CH) = NoteOn_2(CH)
        If (Register And &HF0) = YM3812_REG_KEY_BLOCK_FNum_MSB Then
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
            Else 'If (Register And &HF0) = YM3812_REG_KEY_BLOCK_FNum_MSB And _
                    Note_1(CH) <> Note_2(CH) Then
                DoNoteOn Note_1(CH), Note_2(CH), CH, MIDINote(CH), MIDIWheel(CH)
            End If
        End If
    
    Case YM3812_REG_RHYTHM
        
        If YM2413_PERCUSSION_DISABLED = 1 Then Exit Sub
        
        CH = CHN_DAC
        
        If (Data And YM3812_REG_BD) = 0 Then
            If Percussion_On(0) = 1 Then MIDI_Event_Write MIDI_NOTE_OFF, CH, 35, &H0
            Percussion_On(0) = 0
        Else
            If Percussion_On(0) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 35, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 35, BD_VOL
                Percussion_On(0) = 1
            End If
        End If
        If (Data And YM3812_REG_SD) = 0 Then
            If Percussion_On(1) = 1 Then MIDI_Event_Write MIDI_NOTE_OFF, CH, 38, &H0
            Percussion_On(1) = 0
        Else
            If Percussion_On(1) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 38, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 38, SD_VOL
                Percussion_On(1) = 1
            End If
        End If
        If (Data And YM3812_REG_TOM) = 0 Then
            If Percussion_On(2) = 1 Then MIDI_Event_Write MIDI_NOTE_OFF, CH, 45, &H0
            Percussion_On(2) = 0
        Else
            If Percussion_On(2) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 45, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 45, TOM_VOL
                Percussion_On(2) = 1
            End If
        End If
        ' Cymbal mustn't be "Open Hi-Hat", because it's often used with the Hi-Hat
        If (Data And YM3812_REG_TCT) = 0 Then
            If Percussion_On(3) = 1 Then MIDI_Event_Write MIDI_NOTE_OFF, CH, 51, &H0
            Percussion_On(3) = 0
        Else
            If Percussion_On(3) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 51, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 51, TCT_VOL
                Percussion_On(3) = 1
            End If
        End If
        If (Data And YM3812_REG_HH) = 0 Then
            If Percussion_On(4) = 1 Then MIDI_Event_Write MIDI_NOTE_OFF, CH, 42, &H0
            Percussion_On(4) = 0
        Else
            If Percussion_On(4) = 0 Then
                'MIDI_Event_Write MIDI_NOTE_OFF, CH, 42, &H0
                MIDI_Event_Write MIDI_NOTE_ON, CH, 42, HH_VOL
                Percussion_On(4) = 1
            End If
        End If
        
    Case YM3812_FB_CONNECTION_PAN To YM3812_FB_CONNECTION_PAN + &H8
        CH = Register And &HF
        
        If YM2413_CH_DISABLED(CH) = 1 Then Exit Sub
        If YM2413_VOL_DISABLED(CH) = 1 Then Exit Sub
        If OPLType <> OPL_TYPE_YMF262 Then Exit Sub ' Skip Pan-Ctrl for non-OPL3
        
        If OPL3Mode Then
            Select Case (Data And &H30) / &H10
            Case &H0    ' should actually be complete silence
                TempByt = MIDI_PAN_CENTER
            Case &H1
                TempByt = MIDI_PAN_LEFT
            Case &H2
                TempByt = MIDI_PAN_CENTER
            Case &H3
                TempByt = MIDI_PAN_RIGHT
            End Select
        Else
            TempByt = MIDI_PAN_CENTER
        End If
        
        'If TempByt <> MIDIPan(CH) Then
            MIDIPan(CH) = TempByt
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, MIDIPan(CH)
        'End If
    
    End Select

    Exit Sub

ErrHandler:

    Dim strPrompt As String, lngResult As VbMsgBoxResult
    
    strPrompt = "Error #" & Err.Number & vbNewLine & "'" & Err.Description & "'" & _
                vbNewLine & "Terminate Program?"
    lngResult = MsgBox(strPrompt, vbCritical Or vbYesNo, "YM3812_Command_Handle")
    If lngResult = vbYes Then End
    
    Exit Sub

End Sub

Public Function YM3812_Vol2DB(ByVal TL As Byte) As Single

    YM3812_Vol2DB = -TL * 4 / 3

End Function

