Attribute VB_Name = "basYMF278"
Option Explicit

Private Type OPL4_TONE
    Ins As Byte
    Pitch As Integer
    KeyScl As Byte
End Type

Private Const XG_MODE As Boolean = False

Private OPL4ToneCount As Integer
Private OPL4Tones() As OPL4_TONE

Public Sub LoadOPL4InstrumentSet()

    Const INSSET_SIG = "INSSET"
    Dim TempStr As String
    
    Open App.Path & "\" & "yrw801.ins" For Binary Access Read As #1
        TempStr = String$(Len(INSSET_SIG), &H0)
        Get #1, 1, TempStr
        If TempStr <> INSSET_SIG Then
            Close #1
            Exit Sub
        End If
        Get #1, , OPL4ToneCount
        ReDim OPL4Tones(&H0 To OPL4ToneCount - 1)
        Get #1, , OPL4Tones()
    Close #1

End Sub

Private Function Note_YMF278(ByVal Tone As Integer, _
                            ByVal FNum As Long, ByVal Oct As Integer) As Double

    Dim TempSng As Single
    Dim Pitch As Single
    Dim Octave As Integer
    Dim Note As Double
    
    If Oct = -8 And FNum = 0 Then
        Note_YMF278 = &HFF
        Exit Function
    End If
    
    ' Note2FNum from Linux' OPL4 Driver
    'pitch = (note - 60) * voice->sound->key_scaling / 100 + 60;
    'pitch = pitch << 7;    -- 1 Halftone = 128 pitch --
    'pitch += voice->sound->pitch_offset;
    'octave = pitch / 0x600 - 8;
    'fnum = pitch2fnum(pitch % 0x600);
    
    Pitch = Log(1 + FNum / 1024) / Log(2)
    Octave = Oct + 8
    'If OPL4Tones(Tone).Pitch = &H1000 Then Stop
    Pitch = Pitch - OPL4Tones(Tone).Pitch / &H600
    ' Formula from YMF278B Manual:             1024 + F_NUMBER
    ' F(c) = 1200 x (Octave - 1) + 1200 x log2 ---------------
    ' 1 octave = 1200c                               1024
    Note = Octave * 12 + Pitch * 12
    'If OPL4Tones(Tone).KeyScl > 0 And OPL4Tones(Tone).KeyScl <> 100 Then
    '    Note = (Note - 60) * 100 / OPL4Tones(Tone).KeyScl + 60
    'End If
    
    Note_YMF278 = Note

End Function

Private Function ChannelSelect(ByVal SNum As Byte, ByVal ToneIns As Byte, _
                                ByRef DrumMode As Boolean) As Byte

    Dim SelChn As Byte
    
    If XG_MODE Then
        SelChn = SNum And &HF
        DrumMode = False
    Else
        If Not CBool(ToneIns And &H80) Then
            SelChn = SNum And &HF
            If SelChn = CHN_DAC Then
                SelChn = &HF
            End If
            'If SNum <= &H4 Then SelChn = &H8
            DrumMode = False
        Else
            SelChn = CHN_DAC
            DrumMode = True
        End If
    End If
    
    ChannelSelect = SelChn

End Function

Public Sub YMF278Command_Handle(ByVal Port As Byte, ByVal Register As Byte, _
                                ByVal Data As Byte)

    Static FNum_MSB(0 To 23) As Byte, FNum_LSB(0 To 23) As Byte
    Static ToneWave(0 To 23) As Integer, ToneIns(0 To 23) As Byte
    Static Oct(0 To 23) As Integer, _
            FNum_O(0 To 23) As Long, FNum_N(0 To 23) As Long, _
            Note_O(0 To 23) As Double, Note_N(0 To 23) As Double, _
            NoteOn_O(0 To 23) As Byte, NoteOn_N(0 To 23) As Byte
    Static MIDINote(0 To 23) As Byte, MIDIWheel(0 To 23) As Integer
    Static SlotVolume(0 To 23) As Byte, SlotPan(0 To 23) As Byte
    Static DamperOn_O(0 To 23) As Byte, DamperOn_N(0 To 23) As Byte
    Static Vib(0 To 23) As Byte
    Static MIDIVolume(&H0 To &HF) As Byte, MIDIPan(&H0 To &HF) As Byte, _
            MIDIIns(&H0 To &HF) As Byte, _
            DrumPan(&H0 To &HF, &H0 To &H7F) As Byte, _
            DrumPitch(&H0 To &HF, &H0 To &H7F) As Byte, _
            DrumNRPN_M(&H0 To &HF) As Byte, DrumNRPN_L(&H0 To &HF) As Byte
            
    Dim SNum As Byte    ' Slot Number
    Dim CH As Byte
    Dim DrumMode As Boolean
    Dim OldVal As Byte
    Dim TempByt As Byte
    
    'On Error GoTo ConvErr
    
    If Port < &H2 Then
        Call YM3812Command_Handle(Port * &H100 Or Register, Data)
        If Port = &H1 And Register = &H5 Then
            Erase FNum_MSB(), FNum_LSB()
            Erase ToneWave(), ToneIns()
            Erase Oct(), FNum_O(), FNum_N(), Note_O(), Note_N(), _
                    NoteOn_O(), NoteOn_N()
            Erase MIDINote(), MIDIWheel()
            Erase SlotVolume(), SlotPan()
            Erase MIDIVolume(), MIDIPan(), DrumPan()
            Erase DamperOn_O(), DamperOn_N()
            Erase Vib()
            
            For SNum = 0 To 23
                Note_O(SNum) = &HFF
                MIDINote(SNum) = &HFF
                ToneIns(SNum) = &HFF
                SlotVolume(SNum) = &HFF
                SlotPan(SNum) = &HFF
                Vib(SNum) = &HFF
            Next SNum
            For CH = &H0 To &HF
                MIDIIns(CH) = &HFF
                MIDINote(CH) = &HFF
                MIDIWheel(CH) = &H8000
                MIDIVolume(CH) = &HFF
                MIDIPan(CH) = &HFF
                For TempByt = &H0 To &H7F
                    DrumPan(CH, TempByt) = &HFF
                    DrumPitch(CH, TempByt) = &HFF
                Next TempByt
                DrumNRPN_M(CH) = &HFF
                DrumNRPN_L(CH) = &HFF
            Next CH
        End If
        Exit Sub
    End If
    
    If Register >= &H8 And Register <= &HF7 Then
    
    SNum = (Register - &H8) Mod 24
    CH = ChannelSelect(SNum, ToneIns(SNum), DrumMode)
    
    Select Case Int((Register - &H8) / 24)
    Case &H0    ' Reg &H8 - &H1F
        'loadTime = time + LOAD_DELAY;
        '
        'slot.wave = (slot.wave And &H100) Or data;
        ToneWave(SNum) = (ToneWave(SNum) And &H100) Or Data
        ToneIns(SNum) = OPL4Tones(ToneWave(SNum)).Ins
        
        OldVal = CH
        CH = ChannelSelect(SNum, ToneIns(SNum), DrumMode)
        If CH <> OldVal And NoteOn_O(SNum) Then
            DoNoteOn Note_O(SNum), &HFF, CH, _
                    MIDINote(SNum), MIDIWheel(SNum), &HFF, TempByt
            NoteOn_O(SNum) = 0
        End If
        
        OldVal = MIDIIns(CH)
        MIDIIns(CH) = IIf(ToneIns(SNum) And &H80, &H80, ToneIns(SNum) And &H7F)
        
        If MIDIIns(CH) <> OldVal Then
        
        If XG_MODE Then
            If (MIDIIns(CH) And &H80) <> (OldVal And &H80) Then
                TempByt = IIf(MIDIIns(CH) And &H80, &H7F, &H0)
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, &H0, TempByt
            End If
            If Not CBool((MIDIIns(CH) And &H80) And (OldVal And &H80)) Then
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, MIDIIns(CH) And &H7F
            End If
        Else
            If Not CBool(MIDIIns(CH) And &H80) Then
                MIDI_Event_Write MIDI_PROGRAM_CHANGE, CH, MIDIIns(CH) And &H7F
            End If
        End If
        'If CH < 8 And MIDIIns(CH) = &H77 Then Stop
        
        End If
        'int base = (slot.wave < 384 Or !wavetblhdr) ?
        '           (slot.wave * 12) :
        '           (wavetblhdr * &H80000 + ((slot.wave - 384) * 12));
        'byte buf[12];
        'for (int i = 0; i < 12; ++i) {
        '    buf[i] = readMem(base + i);
        '}
        'slot.bits = (buf[0] And &HC0) >> 6;
        'slot.set_lfo((buf[7] >> 3) And 7);
        'slot.vib  = buf[7] And 7;
        'slot.AR   = buf[8] >> 4;
        'slot.D1R  = buf[8] And &HF;
        'slot.DL   = dl_tab[buf[9] >> 4];
        'slot.D2R  = buf[9] And &HF;
        'slot.RC   = buf[10] >> 4;
        'slot.RR   = buf[10] And &HF;
        'slot.AM   = buf[11] And 7;
        'slot.startaddr = buf[2] Or (buf[1] << 8) Or
        '                 ((buf[0] And &H3F) << 16);
        'slot.loopaddr = buf[4] + (buf[3] << 8);
        'slot.endaddr  = (((buf[6] + (buf[5] << 8)) ^ &HFFFF) + 1);
        'if ((regs[Register + 4] And &H080)) {
        '     keyOnHelper(slot);
        '}
    Case &H1    ' Reg &H20 - &H37
        'slot.wave = (slot.wave And &HFF) Or ((data And &H1) << 8);
        ToneWave(SNum) = (ToneWave(SNum) And &HFF) Or (Data And &H1) * &H100
        'slot.FN = (slot.FN And &H380) Or (data >> 1);
        FNum_LSB(SNum) = Int(Data / &H2)
        ' usually, FNum MSB is sent after FNum LSB
    Case &H2    ' Reg &H38 - &H4F
        'slot.FN = (slot.FN And &H07F) Or ((Data And &H07) << 7)
        FNum_MSB(SNum) = Data And &H7
        'slot.PRVB = ((data And &H08) >> 3)
        'slot.OCT =  ((data And &HF0) >> 4)
        Oct(SNum) = (Data And &HF0) / &H10
        'int oct = slot.OCT;
        If CBool(Oct(SNum) And &H8) Then
            Oct(SNum) = Oct(SNum) Or -8
        End If
        
        FNum_O(SNum) = FNum_N(SNum)
        FNum_N(SNum) = (FNum_MSB(SNum) * &H80) Or FNum_LSB(SNum)
        
        Note_O(SNum) = Note_N(SNum)
        
        Note_N(SNum) = Note_YMF278(ToneWave(SNum), FNum_N(SNum), Oct(SNum))
        If CBool(ToneIns(SNum) And &H80) Then
            TempByt = ToneIns(SNum) And &H7F
            OldVal = DrumPitch(CH, TempByt)
            DrumPitch(CH, TempByt) = Note_N(SNum)
            If DrumPitch(CH, TempByt) <> OldVal Then
                If DrumNRPN_M(CH) <> NRPN_DRUM_PITCH_COARSE Or _
                    DrumNRPN_L(CH) <> TempByt Then
                    DrumNRPN_M(CH) = NRPN_DRUM_PITCH_COARSE
                    DrumNRPN_L(CH) = TempByt
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                    MIDI_NRPN_MSB, DrumNRPN_M(CH)
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                    MIDI_NRPN_LSB, DrumNRPN_L(CH)
                End If
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                MIDI_DATA_ENTRY_MSB, DrumPitch(CH, TempByt)
            End If
            
            Note_N(SNum) = ToneIns(SNum) And &H7F
        End If
        
        If NoteOn_N(SNum) Then
            DoNoteOn Note_O(SNum), Note_N(SNum), CH, MIDINote(SNum), MIDIWheel(SNum)
        End If
    Case &H3    ' Reg &H50 - &H67
        OldVal = SlotVolume(SNum)
        SlotVolume(SNum) = &H7F - Int(Data / &H2)
        If SlotVolume(SNum) = &H0 And NoteOn_N(SNum) = 0 Then
            SlotVolume(SNum) = OldVal
        End If
        'LD = Data And &H1
        
        'If LD Then
        '    ' directly change volume
        'Else
        '    ' interpolate volume
        'End If
        
        If Not DrumMode Then
            OldVal = MIDIVolume(CH)
            MIDIVolume(CH) = SlotVolume(SNum)
            
            If MIDIVolume(CH) <> OldVal Then
                MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_VOLUME, _
                                MIDIVolume(CH)
            End If
        End If
    Case &H4    ' Reg &H68 - &H7F
        If Data And &H80 Then
            OldVal = SlotPan(SNum)
            TempByt = Data And &HF
            If TempByt < &H8 Then
                SlotPan(SNum) = &H40 - TempByt / &H7 * &H40
            ElseIf TempByt > &H8 Then
                SlotPan(SNum) = &H40 + (&H10 - TempByt) / &H7 * &H40
                If SlotPan(SNum) = &H80 Then SlotPan(SNum) = &H7F
            Else
                SlotPan(SNum) = &H40
            End If
            
            If Not DrumMode Then
                OldVal = MIDIPan(CH)
                MIDIPan(CH) = SlotPan(SNum)
                If MIDIPan(CH) <> OldVal Then
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_PAN, _
                                    MIDIPan(CH)
                End If
            Else
                TempByt = ToneIns(SNum) And &H7F
                OldVal = DrumPan(CH, TempByt)
                DrumPan(CH, TempByt) = SlotPan(SNum)
                If DrumPan(CH, TempByt) <> OldVal Then
                    If DrumNRPN_M(CH) <> NRPN_DRUM_PAN Or _
                        DrumNRPN_L(CH) <> TempByt Then
                        DrumNRPN_M(CH) = NRPN_DRUM_PAN
                        DrumNRPN_L(CH) = TempByt
                        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                        MIDI_NRPN_MSB, DrumNRPN_M(CH)
                        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                        MIDI_NRPN_LSB, DrumNRPN_L(CH)
                    End If
                    MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                    MIDI_DATA_ENTRY_MSB, DrumPan(CH, TempByt)
                End If
            End If
        End If

        If (Data And &H20) Then
            ' LFO reset
        Else
            ' LFO activate
        End If
        
        DamperOn_N(SNum) = (Data And &H40) / &H40
        NoteOn_N(SNum) = (Data And &H80) / &H80
        
        If DamperOn_N(SNum) <> DamperOn_O(SNum) Then
            ' Damping increases Decay rate
            'MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_SOFT, _
                            CBool(DamperOn_N(SNum)) And &H7F
            DamperOn_O(SNum) = DamperOn_N(SNum)
        End If
        If NoteOn_N(SNum) <> NoteOn_O(SNum) Then
            If Not DrumMode Then
                TempByt = &H7F
            Else
                TempByt = SlotVolume(SNum)
            End If
            If NoteOn_N(SNum) Then
                DoNoteOn Note_O(SNum), Note_N(SNum), CH, _
                        MIDINote(SNum), MIDIWheel(SNum), &HFF, TempByt
            Else
                DoNoteOn Note_O(SNum), &HFF, CH, _
                        MIDINote(SNum), MIDIWheel(SNum), &HFF, TempByt
            End If
            NoteOn_O(SNum) = NoteOn_N(SNum)
        End If
    Case &H5    ' Reg &H80 - &H97
        OldVal = Vib(SNum)
        Vib(SNum) = (Data And &H7) * &H10
        If Not DrumMode And Vib(SNum) <> OldVal Then
            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, MIDI_MODULATOR_WHEEL, _
                            Vib(SNum)
        End If
        'slot.set_lfo(Int(Data / &H8) And &H7)
    Case &H6    ' Reg &H98 - &HAF
        'slot.AR = Int(Data / &H10)
        'slot.D1R = Data And &HF
        If ToneIns(SNum) = &H77 Then    ' Reverse Cymbal
            TempByt = Int(Data / &H10)
            If TempByt >= &HE Then
                ' -> Crash Cymbal
                If NoteOn_O(SNum) Then
                    DoNoteOn Note_O(SNum), &HFF, CH, _
                            MIDINote(SNum), MIDIWheel(SNum), &HFF, TempByt
                    NoteOn_O(SNum) = 0
                End If
                
                ToneWave(SNum) = &H180
                ToneIns(SNum) = OPL4Tones(ToneWave(SNum)).Ins
                CH = ChannelSelect(SNum, ToneIns(SNum), DrumMode)
                If CBool(ToneIns(SNum) And &H80) Then
                    TempByt = ToneIns(SNum) And &H7F
                    OldVal = DrumPitch(CH, TempByt)
                    DrumPitch(CH, TempByt) = Note_N(SNum)
                    If DrumPitch(CH, TempByt) <> OldVal Then
                        If DrumNRPN_M(CH) <> NRPN_DRUM_PITCH_COARSE Or _
                            DrumNRPN_L(CH) <> TempByt Then
                            DrumNRPN_M(CH) = NRPN_DRUM_PITCH_COARSE
                            DrumNRPN_L(CH) = TempByt
                            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                            MIDI_NRPN_MSB, DrumNRPN_M(CH)
                            MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                            MIDI_NRPN_LSB, DrumNRPN_L(CH)
                        End If
                        MIDI_Event_Write MIDI_CONTROLLER_CHANGE, CH, _
                                        MIDI_DATA_ENTRY_MSB, DrumPitch(CH, TempByt)
                    End If
                    
                    Note_N(SNum) = ToneIns(SNum) And &H7F
                End If
            End If
        End If
    Case &H7    ' Reg &HB0 - &HC7
        'slot.DL = dl_tab(Int(Data / &H10))
        'slot.D2R = Data And &HF
    Case &H8    ' Reg &HC8 - &HDF
        'slot.RC = Int(Data / &H10)
        'slot.RR = Data And &HF
    Case &H9    ' Reg &HE0 - &HF7
        'slot.AM = Data And &H7
    End Select
    
    Else
    
    ' All non-slot registers
    Select Case Register
    Case &H0    ' TEST
    Case &H1
    Case &H2
        'wavetblhdr = (Data >> 2) And &H7
        'memmode = Data And 1
    Case &H3
        'memadr = (memadr And &HFFFF&) Or (Data * &H10000)
    Case &H4
        'memadr = (memadr And &HFF00FF) Or (Data * &H100&)
    Case &H5
        'memadr = (memadr And &HFFFF00) Or Data
    Case &H6   ' memory data
        'Call writeMem(memadr, Data)
        'memadr = (memadr + 1) And &HFFFFFF
    Case &HF8
        'fm_l = Data And &H7
        'fm_r = (Data >> 3) And &H7
    Case &HF9
        'pcm_l = Data And &H7
        'pcm_r = (Data >> 3) And &H7
    End Select
    
    End If

    'regs [Register] = Data
    Exit Sub

ConvErr:

    'Stop
    'Resume

End Sub
