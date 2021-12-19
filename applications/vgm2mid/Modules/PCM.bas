Attribute VB_Name = "basPCM"
Option Explicit

Private SegaPCM_RAM(&H0 To &H7FF) As Byte

Public Sub SegaPCM_Init()

    Erase SegaPCM_RAM()

End Sub

Public Sub SegaPCM_Mem_Write(ByVal Offset As Integer, ByVal Data As Byte)

    Dim Channel As Byte
    Dim RelOffset As Integer
    Dim TempByt As Byte
    Dim NoteVol As Byte
    Static ChnAddr(&H0 To &HF) As Long
    Static ChnVolL(&H0 To &HF) As Byte
    Static ChnVolR(&H0 To &HF) As Byte
    Static ChnNote(&H0 To &HF) As Byte
    Static LastPan(&H0 To &HF) As Byte
    
    Offset = Offset And &H7FF
    Channel = Int(Offset / &H8) And &HF
    RelOffset = Offset And (Not &H78)
    SegaPCM_RAM(Offset) = Data
    
    Select Case RelOffset
    Case &H86   ' Channel On/Off
        'OnOff = Data And &H1
        If CBool(Data And &H1) Then
            MIDI_Event_Write MIDI_NOTE_OFF, &H9, ChnNote(Channel), &H0
            ChnNote(Channel) = &H0
        End If
    Case &H4    ' Set Audio Address Low
        ChnAddr(Channel) = (ChnAddr(Channel) And &HFF00&) Or (Data * &H1&)
    Case &H5    ' Set Audio Address High
        ChnAddr(Channel) = (ChnAddr(Channel) And &HFF&) Or (Data * &H100&)
        
        Select Case ChnAddr(Channel)
        Case &H0
            Data = &H0
        Case &H437C
            Data = &H38
        Case &H49DE
            Data = &H1C
        Case &H302F
            Data = &H2A
        Case &H17C0, &H172F
            Data = &H2E
        Case &H90
            Data = &H26
        Case &HF0
            Data = &H2D
        Case &H29AB
            Data = &H24
        Case &H5830
            Data = &H27
        Case &H1C03
            Data = &H30
        Case &H951
            Data = &H2B
        Case &H3BE6
            Data = &H31
        Case &H4DA0
            Data = &H45
        Case &HC1D
            Data = &H28
        Case &H6002
            Data = &H33
        'Case &H6700
        '    Data = &H7F
        Case &H82
            Data = &H60
        Case &H2600
            Data = &H61
        Case &H4A
            Data = &H62
        Case &H5600
            Data = &H63
        Case &H4000
            Data = &H65
        Case &H2D6
            Data = &H67
        Case &H158A
            Data = &H68
        Case &HC04
            Data = &H69
        Case &H1CD0
            Data = &H6A
        Case &H218E
            Data = &H6B
        Case &H1E34
            Data = &H6C
        Case &HE31
            Data = &H6D
        Case &H89B
            Data = &H6E
        Case &H27B
            Data = &H6F
        Case &H4EA
            Data = &H70
        Case &H3600
            Data = &H71
        Case &H1800
            Data = &H72
        Case &H18BA
            Data = &H73
        Case &H173
            Data = &H74
        Case &H204F
            Data = &H75
        Case &HAB
            Data = &H76
        Case &H201D
            Data = &H77
        Case &H20AB
            Data = &H78
        Case &H2000
            Data = &H79
        Case &H2
            Data = &H7A
        Case &H1D
            Data = &H7B
        Case &H2F
            Data = &H7C
        Case &H26AB
            Data = &H7D
        Case &H262F
            Data = &H7E
        Case Else
            'Debug.Print Hex$(ChnAddr(Channel))
            Stop
            Data = &H7F
        End Select
        
        MIDI_Event_Write MIDI_NOTE_OFF, &H9, ChnNote(Channel), &H0
        NoteVol = ChnVolL(Channel) + ChnVolR(Channel)
        If NoteVol > 0 Then
            TempByt = (ChnVolR(Channel) / (NoteVol / 2)) * &H40
        Else
            TempByt = &H40
        End If
        If LastPan(Channel) <> TempByt Then
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, &H9, MIDI_NRPN_MSB, NRPN_DRUM_PAN
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, &H9, MIDI_NRPN_LSB, Data
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, &H9, MIDI_DATA_ENTRY_MSB, TempByt
            LastPan(Channel) = TempByt
        End If
        'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, &H9, &H20, Channel
        If NoteVol = &H0 Then NoteVol = &H1
        'Data = Data - Channel
        If NoteVol <= &H40 Then
            NoteVol = &H40 + NoteVol / 2
        End If
        MIDI_Event_Write MIDI_NOTE_ON, &H9, Data, NoteVol
        'MIDI_Event_Write MIDI_NOTE_OFF, &H9, Data, &H0
        
        ChnNote(Channel) = Data
    Case &H84   ' Set Loop Address Low
    Case &H85   ' Set Loop Address High
    Case &H6    ' Set End Address
    Case &H7    ' Set Sample Delta Time
        MIDI_Event_Write MIDI_PITCHWHEEL, &H9, MIDI_PITCHWHEEL_CENTER + _
                        IIf(Data And &H80, &H80 - Data, Data), &H0
    Case &H2    ' Set Volume L
        ChnVolL(Channel) = Data
        'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, Channel, MIDI_VOLUME, TempByt
    Case &H3    ' Set Volume R
        ChnVolR(Channel) = Data
        'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, Channel, MIDI_VOLUME Or &H20, TempByt
    Case Else   ' Write Offset ##, Data ##
    End Select

End Sub

Public Sub SegaPCM_Dump()

    Open "SegaPCM.dmp" For Binary Access Write As #2
        Put #2, 1, SegaPCM_RAM()
    Close #2

End Sub
