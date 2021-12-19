VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "VGM"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private Type VGM_HEADER
    strVGM As String * &H4
    lngEOFOffset As Long
    lngVersion As Long
    lngHzPSG As Long
    lngHz2413 As Long
    lngGD3Offset As Long
    lngTotalSamples As Long
    lngLoopOffset As Long
    lngLoopSamples As Long
    lngRate As Long
    shtPSG_Feedback As Integer
    bytPSG_STWidth As Byte
    bytReserved1 As Byte
    lngHz2612 As Long
    lngHz2151 As Long
    lngDataOffset As Long
    lngHzSPCM As Long
    lngSPCMIntf As Long
    lngHzRF5C68 As Long
    lngHz2203 As Long
    lngHz2608 As Long
    lngHz2610 As Long
    lngHz3812 As Long
    lngHz3526 As Long
    lngHz8950 As Long
    lngHz262 As Long
    lngHz278B As Long
    lngHz271 As Long
    lngHz280B As Long
    lngHzRF5C164 As Long
    lngHzPWM As Long
    lngHzAY8910 As Long
    lngHzAYType As Byte
    lngHzAYFlags As Byte
    lngHzAYFlags2203 As Byte
    lngHzAYFlags2608 As Byte
    strReserved As String * &H4
End Type

Private Type GD3_TAG
    strGD3 As String * &H4
    lngVersion As Long
    lngTagLength As Long
    strTrackNameE As String
    strTrackNameJ As String
    strGameNameE As String
    strGameNameJ As String
    strSystemNameE As String
    strSystemNameJ As String
    strAuthorNameE As String
    strAuthorNameJ As String
    strReleaseDate As String
    strCreator As String
    strNotes As String
End Type

Dim vhFileHeader As VGM_HEADER

Dim mstrFullPathName As String, mstrPathname As String, _
mstrFilename As String, mstrFileExt As String

Dim lngFileLen As Long, bytFileData() As Byte, bytGYMFileData() As Byte
Dim DataBankLen As Long, DataBank() As Byte
Dim DataBlockCount As Long, DataBlockPos(&H0 To &HFF) As Long
Dim gtGD3Tag As GD3_TAG

Private Function ConvertGYMtoVGM() As Long
'    Dim lngGYMFilePos As Long, lngVGMFilePos As Long
'    Dim bytSwitch As Byte
'    Dim bytPort As Byte, bytRegister As Byte, bytData As Byte, bytPSGMSB As Byte, bytPSGLSB As Byte
'
'    ' GYM Command Constants
'    Const DELAY_166ms = 0
'    Const YM2612_PORT0 = 1
'    Const YM2612_PORT1 = 2
'    Const YM2612_PSG = 3
'
'    ' VGM Command Constants
'    Const GG_STEREO = &H4F
'    Const PSG = &H50
'    Const YM2413 = &H51
'    Const YM2612_P0 = &H52
'    Const YM2612_P1 = &H53
'    Const YM2151 = &H54
'    Const WAIT_N_SAMPLES = &H61
'    Const WAIT_735_SAMPLES = &H62
'    Const WAIT_882_SAMPLES = &H63
'    Const END_OF_SOUND_DATA = &H66
'
'    On Error GoTo ErrHandler
'
'    Do
'        bytSwitch = bytGYMFileData(lngGYMFilePos)
'        Select Case bytSwitch
'        Case DELAY_166ms
'            ReDim Preserve bytVGMData(lngVGMFilePos)
'            bytVGMData(lngVGMFilePos) = WAIT_735_SAMPLES
'            lngGYMFilePos = lngGYMFilePos + 1
'        Case YM2612_PORT0, YM2612_PORT1
'            bytPort = Switch(bytSwitch = YM2612_PORT0, YM2612_P0, _
'            bytSwitch = YM2612_PORT1, YM2612_P1)
'            bytRegister = bytGYMFileData(lngGYMFilePos + 1)
'            bytData = bytGYMFileData(lngGYMFilePos + 2)
'            lngGYMFilePos = lngGYMFilePos + 3
'            ReDim Preserve bytVGMData(lngVGMFilePos + 2)
'            bytVGMData(lngVGMFilePos) = bytPort
'            bytVGMData(lngVGMFilePos + 1) = bytRegister
'            bytVGMData(lngVGMFilePos + 2) = bytData
'            lngVGMFilePos = lngVGMFilePos + 3
'        Case 3
'            bytPort = PSG
'            bytPSGMSB = bytGYMFileData(lngGYMFilePos + 1)
'            lngGYMFilePos = lngGYMFilePos + 2
'            ReDim Preserve bytVGMData(lngVGMFilePos + 1)
'            bytVGMData(lngVGMFilePos) = bytPort
'            bytVGMData(lngVGMFilePos + 1) = bytPSGMSB
'            lngVGMFilePos = lngVGMFilePos + 2
'        Case Else
'            lngGYMFilePos = lngGYMFilePos + 1
'        End Select
'
'    Loop Until lngGYMFilePos >= UBound(bytGYMFileData)
'
'    ConvertGYMtoVGM = 0
'    Exit Function
'
'ErrHandler:
'    ConvertGYMtoVGM = 255
End Function
Public Function ConvertToMID() As Long
    Dim lngReturn As Long
    Select Case mstrFileExt
    Case "vgm", "vgz"
        lngReturn = ConvertVGMtoMID
    Case "gym"
        lngReturn = ConvertGYMtoMID
    End Select
End Function
Private Function ConvertGYMtoMID() As Long
    Dim lngFilePos As Long
    Dim bytSwitch As Byte
    Dim bytPort As Byte, bytRegister As Byte, bytData As Byte, bytPSGMSB As Byte, bytPSGLSB As Byte

    ' GYM Command Constants
    Const DELAY_166ms = 0
    Const YM2612_PORT0 = 1
    Const YM2612_PORT1 = 2
    Const YM2612_PSG = 3
    
    On Error GoTo ErrHandler
    
    Conversion_Status_Current = 0
    Conversion_Status_Total = UBound(bytGYMFileData)

    Erase MID_Trackdata
    ReDim MID_Trackdata(0) As Byte
    MidFilePos = 0
    DeltaTime = 0

    ClockPSG = vhFileHeader.lngHzPSG
    Clock2612 = vhFileHeader.lngHz2612
    MID_Data_Init True
    
    'DAC_Pos = 0
    'ReDim DAC_Data(0)
    'Dim DelayTime As Long
    Dim Ttime As Single
    Dim TempVal As Long
    Ttime = 0#
    T6W28_PSG = False

    Do
        bytSwitch = bytGYMFileData(lngFilePos)
        Select Case bytSwitch
        Case DELAY_166ms
            DeltaTime = DeltaTime + 735
            For TempVal = &H0 To &H2
                PSG_NoteDelay(TempVal) = PSG_NoteDelay(TempVal) + 735
            Next TempVal
            lngFilePos = lngFilePos + 1
            
            'DelayTime = DelayTime + 1
            'If DelayTime > 1 And DAC_Pos > 0 Then
            '    Call DAC_Write
            'End If
        Case YM2612_PORT0, YM2612_PORT1
            bytPort = Switch(bytSwitch = YM2612_PORT0, 0, _
                        bytSwitch = YM2612_PORT1, 3)
            bytData = bytGYMFileData(lngFilePos + 2)
            'If bytRegister <> YM2612_DAC Then _
                '
                YM2612Command_Handle bytPort, bytRegister, bytData
            lngFilePos = lngFilePos + 3
            'If bytRegister = YM2612_DAC Then
            '    ReDim Preserve DAC_Data(DAC_Pos)
            '    DAC_Data(DAC_Pos) = bytData
            '    DAC_Pos = DAC_Pos + 1
            '    DelayTime = 0
            'End If
        Case YM2612_PSG
            bytPort = 10
            bytPSGMSB = bytGYMFileData(lngFilePos + 1)
            Select Case (bytPSGMSB And 240)
            Case PSG_TONE_1, PSG_TONE_2, PSG_TONE_3
                bytPSGLSB = bytGYMFileData(lngFilePos + 3)
                lngFilePos = lngFilePos + 4
            Case Else
                lngFilePos = lngFilePos + 2
            End Select
            PSGCommand_Handle bytPSGMSB, bytPSGLSB
        Case Else
            lngFilePos = lngFilePos + 1
        End Select
    
        Conversion_Status_Current = lngFilePos
        
        If Ttime < Timer Then
            Call frmMain.tmrConversionStatus_Timer
            DoEvents
            Ttime = Timer + 0.5
        End If
        
    'Loop Until lngFilePos >= UBound(bytGYMFileData) / 8
    Loop Until lngFilePos >= UBound(bytGYMFileData)

    ConvertGYMtoMID = 0
    Exit Function

ErrHandler:
    ConvertGYMtoMID = 255
End Function

Private Function ConvertVGMtoMID() As Long

    Dim lngFilePos As Long
    Dim bytCommand As Byte, bytPort As Byte, bytRegister As Byte, bytData As Byte
    Dim dblWait As Long
    Dim DETimer As Single
    Dim LastDataNote As Byte
    Dim DataBankPos As Long
    Dim TempLng As Long
    Dim LastPSGCmd(&H0 To &H1) As Byte
    Dim LoopAvb As Boolean  ' Loop available
    Dim StopVGM As Boolean
    Dim LoopPos As Long
    Dim DACWrt As Boolean
    Dim CurChip As Byte
    Dim CurLoop As Integer

    ' VGM Command Constants
    Const GG_STEREO = &H4F
    Const PSG = &H50
    Const YM2413 = &H51
    Const YM2612_P0 = &H52
    Const YM2612_P1 = &H53
    Const YM2151 = &H54
    Const YM2203 = &H55
    Const YM2608_P0 = &H56
    Const YM2608_P1 = &H57
    Const YM2610_P0 = &H58
    Const YM2610_P1 = &H59
    Const YM3812 = &H5A
    Const YM3526 = &H5B
    Const Y8950 = &H5C
    Const YMF262_P0 = &H5E
    Const YMF262_P1 = &H5F
    Const RF5C68_REG = &HB0
    Const SPCM_MEM = &HC0
    Const RF5C68_MEM = &HC1
    Const DATABNK_SEEK = &HE0
    Const AY8910 = &HA0
    
    Const WAIT_N_SAMPLES = &H61
    Const WAIT_735_SAMPLES = &H62
    Const WAIT_882_SAMPLES = &H63
    Const END_OF_SOUND_DATA = &H66
    Const DATA_BLOCK = &H67

    On Error GoTo ErrHandler

    Conversion_Status_Current = &H0
    Conversion_Status_Total = vhFileHeader.lngEOFOffset - vhFileHeader.lngDataOffset
    DataBankLen = &H0
    DataBlockCount = &H0

    Call PSGCommand_Handle(&H0, &H0)
    If vhFileHeader.lngLoopOffset > 0 Then
        LoopAvb = True
        LoopPos = vhFileHeader.lngLoopOffset
    Else
        LoopAvb = False
    End If
    
    DETimer = Timer
    'Call DAC_WriteOpen
    LastPSGCmd(&H0) = &H0
    LastPSGCmd(&H1) = &H0
    DACWrt = False
    DAC_DataByte = &H80
    LastDataNote = &HFF
    
    ClockPSG = vhFileHeader.lngHzPSG And &H3FFFFFFF
    Clock2413 = vhFileHeader.lngHz2413 And &H3FFFFFFF
    Clock2612 = vhFileHeader.lngHz2612 And &H3FFFFFFF
    Clock2151 = vhFileHeader.lngHz2151 And &H3FFFFFFF
    fsam2413 = Clock2413 / 72
    fsam2612 = Clock2612 / 72
    ClockAY = vhFileHeader.lngHzAY8910
    T6W28_PSG = False
    If (vhFileHeader.lngHzPSG And &HC0000000) = &HC0000000 Then
        T6W28_PSG = True
    End If
    If vhFileHeader.lngHz278B Then
        Call LoadOPL4InstrumentSet
    End If
    
    Erase MID_Trackdata
    ReDim MID_Trackdata(0) As Byte
    MidFilePos = 0
    DeltaTime = 0
    Call SegaPCM_Init
    Call WriteMidiTag
    Call MID_Data_Init(CBool(ClockPSG) Or CBool(ClockAY))
    
    lngFilePos = vhFileHeader.lngDataOffset
    StopVGM = False
    CurLoop = &H0
    Do
        dblWait = 0
        CurChip = &H0
        bytCommand = bytFileData(lngFilePos)
        
        If DUAL_CHIPS > &H0 Then
            Select Case bytCommand
            Case &H30
                CurChip = &H1
                bytCommand = bytCommand + &H20
            Case &H3F
                CurChip = &H1
                bytCommand = bytCommand + &H10
            Case &HA1 To &HAC
                CurChip = &H1
                bytCommand = bytCommand - &H50
            End Select
        End If
        
        Select Case bytCommand
        Case GG_STEREO
            PSG_NUM = CurChip
            bytData = bytFileData(lngFilePos + 1)
            Call GGStereo_Handle(bytData)
            lngFilePos = lngFilePos + 2
        Case PSG
            PSG_NUM = CurChip
            bytData = bytFileData(lngFilePos + 1)
            If bytData And &H80 Then
                Select Case (bytData And PSG_CHANNEL_SELECT)
                Case PSG_TONE_1, PSG_TONE_2, PSG_TONE_3
                    ' skip and wait for data command
                Case Else
                    ' Volume Changes use LSB
                    PSGCommand_Handle bytData, bytData
                End Select
                LastPSGCmd(PSG_NUM) = bytData
            Else
                ' do data write
                PSGCommand_Handle LastPSGCmd(PSG_NUM), bytData
            End If
            lngFilePos = lngFilePos + 2
        Case YM2413
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            YM2413Command_Handle bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case YM2612_P0, YM2612_P1, YM2203 To YM2610_P1
            'If bytCommand = YM2612_P0 Then
            '    bytPort = 0
            'ElseIf bytCommand = YM2612_P1 Then
            '    bytPort = 3
            'End If
            bytPort = IIf(bytCommand = &H55, &H0, bytCommand And &H1) * &H3
            Select Case bytCommand
            Case YM2612_P0, YM2612_P1
                OPNType = OPN_TYPE_YM2612
                bytPort = bytCommand And &H1
                fsam2612 = (vhFileHeader.lngHz2612 And &H3FFFFFFF) / 72
            Case YM2203
                OPNType = OPN_TYPE_YM2203
                bytPort = &H0
                fsam2612 = (vhFileHeader.lngHz2203 And &H3FFFFFFF) / 72
            Case YM2608_P0, YM2608_P1
                OPNType = OPN_TYPE_YM2608
                bytPort = bytCommand And &H1
                fsam2612 = (vhFileHeader.lngHz2608 And &H3FFFFFFF) / 72
            Case YM2610_P0, YM2610_P1
                OPNType = OPN_TYPE_YM2610
                bytPort = bytCommand And &H1
                fsam2612 = (vhFileHeader.lngHz2610 And &H3FFFFFFF) / 72
            End Select
            
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            YM2612Command_Handle bytPort * &H3, bytRegister, bytData
            If bytRegister = YM2612_DAC Then
                DAC_DataByte = bytData
                DACWrt = True
            End If
            lngFilePos = lngFilePos + 3
        Case YM2151
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            YM2151Command_Handle bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case YM3812 To Y8950
            Select Case bytCommand
            Case YM3812
                OPLType = OPL_TYPE_YM3812
                fsam3812 = (vhFileHeader.lngHz3812 And &H3FFFFFFF) / 72
            Case YM3526
                OPLType = OPL_TYPE_YM3526
                fsam3812 = (vhFileHeader.lngHz3526 And &H3FFFFFFF) / 72
            Case Y8950
                OPLType = OPL_TYPE_Y8950
                fsam3812 = (vhFileHeader.lngHz8950 And &H3FFFFFFF) / 72
            End Select
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            YM3812Command_Handle bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case YMF262_P0 To YMF262_P1
            OPLType = OPL_TYPE_YMF262
            fsam3812 = (vhFileHeader.lngHz262 And &H3FFFFFFF) / 288
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            YM3812Command_Handle (bytCommand And &H1) * &H100 Or bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case &HD0
            bytPort = bytFileData(lngFilePos + 1)
            bytRegister = bytFileData(lngFilePos + 2)
            bytData = bytFileData(lngFilePos + 3)
            YMF278Command_Handle bytPort, bytRegister, bytData
            lngFilePos = lngFilePos + 4
        Case &HB3
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            GameBoyCommand_Handle bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case &HB4
            If ClockPSG = 0 Then ClockPSG = 1
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            NesApuCommand_Handle bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case WAIT_N_SAMPLES
            dblWait = bytFileData(lngFilePos + 2) * &H100&
            dblWait = dblWait Or bytFileData(lngFilePos + 1)
            lngFilePos = lngFilePos + 3
        Case WAIT_735_SAMPLES
            dblWait = 735
            lngFilePos = lngFilePos + 1
        Case WAIT_882_SAMPLES
            dblWait = 882
            lngFilePos = lngFilePos + 1
        Case END_OF_SOUND_DATA
            StopVGM = True
        Case DATA_BLOCK
            bytRegister = bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 2)
            dblWait = bytFileData(lngFilePos + 3) * &H1& Or _
                        bytFileData(lngFilePos + 4) * &H100& Or _
                        bytFileData(lngFilePos + 5) * &H10000 Or _
                        bytFileData(lngFilePos + 6) * &H1000000
            lngFilePos = lngFilePos + 7
            
            If bytData = &H0 Then
                ReDim Preserve DataBank(&H0 To DataBankLen + dblWait - 1)
                
                For TempLng = &H0 To dblWait - 1
                    DataBank(DataBankLen + TempLng) = bytFileData(lngFilePos + TempLng)
                Next TempLng
                DataBankLen = DataBankLen + dblWait
            End If
            lngFilePos = lngFilePos + dblWait
            dblWait = 0
        Case &H70 To &H7F
            dblWait = (bytCommand And &HF) + 1
            lngFilePos = lngFilePos + 1
        Case &H80 To &H8F
            dblWait = bytCommand And &HF
            bytPort = &H0
            bytRegister = &H2A
            bytData = DataBank(DataBankPos)
            YM2612Command_Handle bytPort, bytRegister, bytData
            DAC_DataByte = bytData
            DACWrt = True
            DataBankPos = DataBankPos + 1
            lngFilePos = lngFilePos + 1
        Case AY8910
            bytPort = bytFileData(lngFilePos + 1) \ &H80
            bytRegister = bytFileData(lngFilePos + 1) And &HF
            bytData = bytFileData(lngFilePos + 2)
            AYCommand_Handle bytPort, bytRegister, bytData
            lngFilePos = lngFilePos + 3
        Case RF5C68_REG ' RF5C68 Register Write
            lngFilePos = lngFilePos + 3
        Case SPCM_MEM   ' SegaPCM Memory Write
            dblWait = bytFileData(lngFilePos + 2) * &H100& Or bytFileData(lngFilePos + 1)
            bytData = bytFileData(lngFilePos + 3)
            Call SegaPCM_Mem_Write(dblWait, bytData)
            
            dblWait = 0
            lngFilePos = lngFilePos + 4
        Case RF5C68_MEM ' RF5C68 Memory Write
            lngFilePos = lngFilePos + 4
        Case DATABNK_SEEK
            DataBankPos = bytFileData(lngFilePos + 1) * &H1& Or _
                        bytFileData(lngFilePos + 2) * &H100& Or _
                        bytFileData(lngFilePos + 3) * &H10000 Or _
                        bytFileData(lngFilePos + 4) * &H1000000
            
            For TempLng = &H0 To DataBlockCount - 1
                If DataBlockPos(TempLng) = DataBankPos Then
                    Exit For
                End If
            Next TempLng
            
            If TempLng >= DataBlockCount Then
                DataBlockPos(DataBlockCount) = DataBankPos
                DataBlockCount = DataBlockCount + &H1
            End If
            
            lngFilePos = lngFilePos + 5
        Case &H30 To &H4E
            lngFilePos = lngFilePos + 2
        Case &H55 To &H5F
            lngFilePos = lngFilePos + 3
        Case &HA0 To &HBF
            lngFilePos = lngFilePos + 3
        Case &HC0 To &HDF
            lngFilePos = lngFilePos + 4
        Case &HE1 To &HFF
            lngFilePos = lngFilePos + 5
        Case &H90   ' DAC Stream Setup
            lngFilePos = lngFilePos + 5
        Case &H91   ' Set Stream Data
            lngFilePos = lngFilePos + 5
        Case &H92   ' Set Stream Frequency
            lngFilePos = lngFilePos + 6
        Case &H93   ' Start Stream
            DataBankPos = bytFileData(lngFilePos + 2) * &H1& Or _
                        bytFileData(lngFilePos + 3) * &H100& Or _
                        bytFileData(lngFilePos + 4) * &H10000 Or _
                        bytFileData(lngFilePos + 5) * &H1000000
            
            For TempLng = &H0 To DataBlockCount - 1
                If DataBlockPos(TempLng) = DataBankPos Then
                    Exit For
                End If
            Next TempLng
            
            If TempLng >= DataBlockCount Then
                DataBlockPos(DataBlockCount) = DataBankPos
                DataBlockCount = DataBlockCount + &H1
            End If
            DACWrt = True
            
            lngFilePos = lngFilePos + 11
        Case &H94   ' Stop Stream
            If LastDataNote < &H80 Then
                MIDI_Event_Write MIDI_NOTE_OFF, &HF, LastDataNote, &H0
            End If
            LastDataNote = &HFF
            lngFilePos = lngFilePos + 2
        Case &H95   ' Start Stream (fast call)
            TempLng = bytFileData(lngFilePos + 2) And &H7F
            If LastDataNote < &H80 Then
                MIDI_Event_Write MIDI_NOTE_OFF, &HF, LastDataNote, &H0
            End If
            MIDI_Event_Write MIDI_NOTE_ON, &HF, TempLng, &H7F
            LastDataNote = TempLng
            
            lngFilePos = lngFilePos + 5
        Case Else
            lngFilePos = lngFilePos + 1
            Stop
        End Select
        DeltaTime = DeltaTime + dblWait
        
        If LoopAvb Then
            If StopVGM Then
                CurLoop = CurLoop + &H1
                If CurLoop < VGM_LOOPS Then
                    MIDI_Event_Write MIDI_META_EVENT, META_MARKER, TEXT_LOOP_END
                    StopVGM = False
                    lngFilePos = LoopPos
                End If
            End If
            If lngFilePos = LoopPos Then
                MIDI_Event_Write MIDI_META_EVENT, META_MARKER, TEXT_LOOP_START
                'Call SegaPCM_Dump
            End If
        End If
        
        If ClockPSG Then
            For TempLng = &H0 To &H7
                PSG_NoteDelay(TempLng) = PSG_NoteDelay(TempLng) + dblWait
            Next TempLng
        End If
        
        'If YM2612_DAC_DISABLED = 1 Then DACWrt = False
        'If Clock2612 Then
            'For TempLng = &H0 To dblWait - 1
            '    Put #2, , DAC_DataByte
            'Next TempLng
        'End If
        If DACWrt Then
            For TempLng = &H0 To DataBlockCount - 1
                If DataBlockPos(TempLng) = DataBankPos - 1 Then
                    If LastDataNote < &H80 Then
                        MIDI_Event_Write MIDI_NOTE_OFF, &HF, LastDataNote, &H0
                    End If
                    MIDI_Event_Write MIDI_NOTE_ON, &HF, TempLng, &H7F
                    LastDataNote = TempLng
                End If
            Next TempLng
            DACWrt = False
        End If
        
        If Timer >= DETimer Then
            ' Calling DoEvents too often causes huge slowdowns
            Call frmMain.tmrConversionStatus_Timer
            Conversion_Status_Current = lngFilePos - vhFileHeader.lngDataOffset
            DoEvents
            DETimer = Timer + 0.2
        End If
    
    Loop Until lngFilePos >= vhFileHeader.lngEOFOffset Or StopVGM
    
    If LoopAvb Then
        MIDI_Event_Write MIDI_META_EVENT, META_MARKER, TEXT_LOOP_END
    End If
    'Call SegaPCM_Dump
    'Call DAC_WriteClose
    
    If ClockPSG Then
        bytPort = IIf(vhFileHeader.lngHzPSG And &H40000000, &H1, &H0)
        For PSG_NUM = &H0 To bytPort
            For bytCommand = &H0 To &H3
                bytData = &H80 Or (bytCommand * &H20) Or &H0
                PSGCommand_Handle bytData, &H0
            Next bytCommand
        Next PSG_NUM
    End If
    If Clock2413 And False Then
        ' TODO ...
        For bytCommand = &H0 To &H7
            bytRegister = &H0
            bytData = &H0
            YM2413Command_Handle bytRegister, bytData
        Next bytCommand
    End If
    If Clock2612 And False Then
        ' TODO ...
        For bytCommand = &H0 To &H5
            bytPort = Fix(bytCommand / &H3)
            bytRegister = &H0 Or (bytCommand Mod &H3)
            bytData = &H0
            YM2612Command_Handle bytPort, bytRegister, bytData
        Next bytCommand
    End If
    If Clock2151 Then
        For bytCommand = &H0 To &H7
            bytRegister = &H8
            bytData = &H0 Or bytCommand
            YM2151Command_Handle bytRegister, bytData
        Next bytCommand
    End If
    
    ConvertVGMtoMID = 0
    Exit Function

ErrHandler:
    ConvertVGMtoMID = 255
    Resume
End Function

Private Sub WriteMidiTag()

    ' Tag Writing with Multiple Language Support
    ' (though I think, MIDI can't handle Japanese letters, because it uses 8-bit-Chars)
    
    ' Language Modes:   00 - English only
    '                   01 - Japanese only
    '                   02 - both, English is preferred
    '                   03 - both, Japanese is preferred
    ' Language Values:  01 - English available
    '                   02 - Japanese available
    Const LANG_MODE = &H2
    
    Dim StrLng As Byte
    Dim UseLng As Byte
    Dim WrtStr As String
    Dim MidiStr As String
    
    With gtGD3Tag
        If .lngVersion = &H0 Then Exit Sub
        
        StrLng = IIf(.strTrackNameE = "", &H0, &H1) Or IIf(.strTrackNameJ = "", &H0, &H2)
        UseLng = SelectTagLanguage(StrLng, LANG_MODE)
        If UseLng = &H0 Then
            WrtStr = .strTrackNameE
        ElseIf UseLng = &H1 Then
            WrtStr = .strTrackNameJ
        ElseIf UseLng = &HFF Then
            WrtStr = "Unknown Song"
        End If
        MidiStr = WrtStr
        
        StrLng = IIf(.strGameNameE = "", &H0, &H1) Or IIf(.strGameNameJ = "", &H0, &H2)
        UseLng = SelectTagLanguage(StrLng, LANG_MODE)
        If UseLng = &H0 Then
            WrtStr = .strGameNameE
        ElseIf UseLng = &H1 Then
            WrtStr = .strGameNameJ
        ElseIf UseLng = &HFF Then
            WrtStr = "Unknown Game"
        End If
        MidiStr = MidiStr & " (" & WrtStr
        
        StrLng = IIf(.strSystemNameE = "", &H0, &H1) Or IIf(.strSystemNameJ = "", &H0, &H2)
        UseLng = SelectTagLanguage(StrLng, LANG_MODE)
        If UseLng = &H0 Then
            WrtStr = .strSystemNameE
        ElseIf UseLng = &H1 Then
            WrtStr = .strSystemNameJ
        ElseIf UseLng = &HFF Then
            WrtStr = "Unknown System"
        End If
        MidiStr = MidiStr & " - " & WrtStr & ")"
        MIDI_Event_Write MIDI_META_EVENT, META_TRACK_NAME, MidiStr
        
        StrLng = IIf(.strAuthorNameE = "", &H0, &H1) Or IIf(.strAuthorNameJ = "", &H0, &H2)
        UseLng = SelectTagLanguage(StrLng, LANG_MODE)
        If UseLng = &H0 Then
            WrtStr = .strAuthorNameE
        ElseIf UseLng = &H1 Then
            WrtStr = .strAuthorNameJ
        End If
        If UseLng < &HFF Then
            MidiStr = "By " & WrtStr
            MIDI_Event_Write MIDI_META_EVENT, META_TEXT, MidiStr
        End If
        
        If .strReleaseDate <> "" Then
            MidiStr = "© Sega " & .strReleaseDate
            MIDI_Event_Write MIDI_META_EVENT, META_TEXT, MidiStr
        End If
        
        MidiStr = "Converted from a VGM by " & .strCreator
        MIDI_Event_Write MIDI_META_EVENT, META_TEXT, MidiStr
        
        MidiStr = "Notes: " & Replace$(.strNotes, Chr$(&HA), Chr$(&HD) & Chr$(&HA))
        MIDI_Event_Write MIDI_META_EVENT, META_TEXT, MidiStr
    End With

End Sub

Private Function SelectTagLanguage(ByVal AvbLang As Byte, ByVal LangMode As Byte) As Byte

    If AvbLang = &H0 Then
        SelectTagLanguage = &HFF
        Exit Function
    End If
    
    Select Case LangMode
    Case &H0, &H1
        SelectTagLanguage = LangMode
    Case &H2
        If CBool(AvbLang And &H1) Then
            SelectTagLanguage = &H0
        Else
            SelectTagLanguage = &H1
        End If
    Case &H3
        If CBool(AvbLang And &H2) Then
            SelectTagLanguage = &H1
        Else
            SelectTagLanguage = &H0
        End If
    End Select

End Function

Property Get FileExt() As String
    FileExt = mstrFileExt
End Property

Property Get Filename() As String
    Filename = mstrFilename
End Property

Property Let Filename(strFilename As String)
    mstrFilename = strFilename
End Property


Property Get FullPathname() As String
    FullPathname = mstrFullPathName
End Property

Property Get GD3Offset() As Long
    GD3Offset = vhFileHeader.lngGD3Offset
End Property


Private Function GetFileExt(strFilename As String) As String
    GetFileExt = Switch(InStr(1, LCase(strFilename), ".vgm"), "vgm", _
    InStr(1, strFilename, ".vgz") <> 0, "vgz", _
    InStr(1, strFilename, ".vgm.gz") <> 0, "vgz", _
    InStr(1, strFilename, ".gym") <> 0, "gym")
End Function
Private Function GetFilename(strFilename As String) As String
    Dim lngSearchLen As Long
    Do
        lngSearchLen = lngSearchLen + 1
    Loop Until InStr(1, Right(strFilename, lngSearchLen), "\") = 1
    GetFilename = Right(strFilename, lngSearchLen - 1)
End Function
Private Function GetFullPathname(strFilename As String) As String
'    Dim lngMatchPos As Long, strTestChar As String * 1
'    strTestChar = Chr(0)
'    lngMatchPos = InStr(1, strFilename, strTestChar)
'    GetFullPathname = Left(strFilename, lngMatchPos - 1)
    GetFullPathname = strFilename
End Function

Private Function GetGYMFileData(strFilename As String) As Long
    On Error GoTo ErrHandler
    Open strFilename For Binary As 1
        lngFileLen = LOF(1)
        ReDim bytGYMFileData(lngFileLen - 1)
        Get 1, 1, bytGYMFileData
    Close
    
    With vhFileHeader
        .lngEOFOffset = lngFileLen
        .lngVersion = 1
        .lngHzPSG = 3579545
        .lngHz2413 = 0
        .lngGD3Offset = 0
        .lngTotalSamples = 0
        .lngLoopOffset = 0
        .lngLoopSamples = 0
        .lngRate = 60
        .shtPSG_Feedback = &H9
        .bytPSG_STWidth = 16
        .lngHz2612 = 3579545
        .lngHz2151 = 0
        .lngDataOffset = &H0
    End With
    
    GetGYMFileData = 0
    Exit Function

ErrHandler:
    GetGYMFileData = 255
End Function
Private Function GetHeaderData(strFilename As String) As Long
    On Error GoTo ErrHandler
    
    Open strFilename For Binary As 1
        Get 1, 1, vhFileHeader
    Close
    If vhFileHeader.strVGM <> "Vgm " Then GoTo ErrHandler
    
    With vhFileHeader
        ' correct the header for old files and calculate absolute offsets
        .lngEOFOffset = &H4 + .lngEOFOffset
        If .lngGD3Offset > &H0 Then
            .lngGD3Offset = &H14 + .lngGD3Offset
        End If
        If .lngLoopOffset > &H0 Then
            .lngLoopOffset = .lngLoopOffset + &H1C
        End If
        If .lngVersion < &H101 Then
            .lngRate = &H0
        End If
        If .lngVersion < &H110 Then
            .shtPSG_Feedback = &H9
            .bytPSG_STWidth = 16
            .lngHz2612 = .lngHz2413
            .lngHz2151 = .lngHz2413
        End If
        If .lngVersion < &H150 Or .lngDataOffset = &H0 Then
            .lngDataOffset = &HC
        End If
        If .lngVersion < &H151 Or .lngDataOffset <= &HC Then
            .lngHzSPCM = &H0
            .lngSPCMIntf = &H0
            .lngHzRF5C68 = &H0
            .lngHz2203 = &H0
            .lngHz2608 = &H0
            .lngHz2610 = &H0
            .lngHz3812 = &H0
            .lngHz3526 = &H0
            .lngHz8950 = &H0
            .lngHz262 = &H0
            .lngHz278B = &H0
            .lngHz271 = &H0
            .lngHz280B = &H0
            .lngHzRF5C164 = &H0
            .lngHzPWM = &H0
            .lngHzAY8910 = &H0
            .lngHzAYType = &H0
            .lngHzAYFlags = &H0
            .lngHzAYFlags2203 = &H0
            .lngHzAYFlags2608 = &H0
        End If
        .lngDataOffset = &H34 + .lngDataOffset
    End With
    GetHeaderData = 0
    
    Exit Function
    
ErrHandler:
    GetHeaderData = 255
End Function
Private Function GetPathname(strFilename As String) As String
    Dim lngSearchLen As Long
    Do
        lngSearchLen = lngSearchLen + 1
    Loop Until InStr(1, Right(strFilename, lngSearchLen), "\") = 1
    GetPathname = Left(strFilename, Len(strFilename) - lngSearchLen)
End Function

Property Get Hz2413() As Long
    Hz2413 = vhFileHeader.lngHz2413
End Property

Property Get HzPSG() As Long
    HzPSG = vhFileHeader.lngHzPSG
End Property

Property Get Hz2612() As Long
    Hz2612 = vhFileHeader.lngHz2612
End Property

Property Get Hz2151() As Long
    Hz2151 = vhFileHeader.lngHz2151
End Property

Property Get LoopOffset() As Long
    LoopOffset = vhFileHeader.lngLoopOffset
End Property

Property Get LoopSamples() As Long
    LoopSamples = vhFileHeader.lngLoopSamples
End Property

Property Get Offset() As Long
    Offset = vhFileHeader.lngEOFOffset
End Property


Public Function OpenFile(strFilename As String) As Long
    Dim lngReturn As Long
    Dim CmdStr As String
    mstrFullPathName = GetFullPathname(strFilename)
    mstrPathname = GetPathname(mstrFullPathName)
    mstrFilename = GetFilename(mstrFullPathName)
    mstrFileExt = GetFileExt(mstrFilename)
        
    Select Case mstrFileExt
    Case "vgm", "vgz"
        If mstrFileExt = "vgz" Then
            FileCopy mstrFullPathName, App.Path & "\temp.vgm.gz"
            ChDrive App.Path
            ChDir App.Path
            Shell "gzip.exe -d -f -q temp.vgm.gz", vbMinimizedNoFocus
            mstrFullPathName = App.Path & "\temp.vgm"
            ' Sleeping should speed up the decompression
            Do Until Dir(mstrFullPathName) <> "": Sleep 1: DoEvents: Loop
            Do Until FileLen(mstrFullPathName) > 0: Sleep 1: DoEvents: Loop
        End If
        lngReturn = GetHeaderData(mstrFullPathName)
        If lngReturn = 255 Then GoTo ErrHandler
        lngReturn = GetFileData(mstrFullPathName)
        If lngReturn = 255 Then GoTo ErrHandler
        If mstrFileExt = "vgz" Then
            On Error Resume Next
            Do Until Dir(mstrFullPathName) = "": Kill mstrFullPathName: Sleep 1: DoEvents: Loop
            mstrFullPathName = GetFullPathname(strFilename)
            On Error GoTo 0
        End If
        lngReturn = ReadGD3Tag()
        If lngReturn = 255 Then
            vhFileHeader.lngGD3Offset = &H0
            lngReturn = ReadGD3Tag()
        End If
    Case "gym"
        lngReturn = GetGYMFileData(mstrFullPathName)
        If lngReturn = 255 Then GoTo ErrHandler
'        lngReturn = ConvertGYMtoVGM
'        If lngReturn = 255 Then GoTo ErrHandler
    End Select
    
    OpenFile = 0
    Exit Function

ErrHandler:
    OpenFile = 255
End Function
Property Get Pathname() As String
    Pathname = mstrPathname
End Property

Property Get Rate() As Long
    Rate = vhFileHeader.lngRate
End Property

Private Function GetFileData(strFilename As String) As Long
    On Error GoTo ErrHandler
    Open strFilename For Binary As 1
        lngFileLen = LOF(1)
        ReDim bytFileData(&H0 To lngFileLen - 1)
        Get 1, 1, bytFileData
    Close 1
    If lngFileLen < vhFileHeader.lngEOFOffset Then
        vhFileHeader.lngEOFOffset = lngFileLen
    End If
    GetFileData = 0
    Exit Function

ErrHandler:
    GetFileData = 255
End Function
Property Get TotalSamples() As Long
    TotalSamples = vhFileHeader.lngTotalSamples
End Property

Property Get Version() As Long
    Version = vhFileHeader.lngVersion
End Property

Private Function ReadGD3Tag() As Byte

    If vhFileHeader.lngGD3Offset = &H0 Then
        With gtGD3Tag
            .strGD3 = String$(&H4, &H0)
            .lngVersion = &H0
            .lngTagLength = &H0
            .strTrackNameE = ""
            .strTrackNameJ = ""
            .strGameNameE = ""
            .strGameNameJ = ""
            .strSystemNameE = ""
            .strSystemNameJ = ""
            .strAuthorNameE = ""
            .strAuthorNameJ = ""
            .strReleaseDate = ""
            .strCreator = ""
            .strNotes = ""
        End With
        ReadGD3Tag = &H0
        Exit Function
    End If
    
    Dim CurPos As Long
    Dim StrArr() As Byte
    Dim StrLen As Long
    
    On Error GoTo ErrHandler
    
    With gtGD3Tag
        CurPos = vhFileHeader.lngGD3Offset
        If CurPos + &H4 > vhFileHeader.lngEOFOffset Then GoTo ErrHandler
        
        ReDim StrArr(&H0 To &H3)
        Call CopyMemory(StrArr(&H0), bytFileData(CurPos), &H4)
        .strGD3 = StrConv(StrArr, vbUnicode)
        If .strGD3 <> "Gd3 " Then GoTo ErrHandler
        
        Call CopyMemory(.lngVersion, bytFileData(CurPos + &H4), &H4)
        Call CopyMemory(.lngTagLength, bytFileData(CurPos + &H8), &H4)
        CurPos = CurPos + &HC
        
        StrLen = GetUnicodeStr(CurPos, .strTrackNameE)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strTrackNameJ)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strGameNameE)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strGameNameJ)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strSystemNameE)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strSystemNameJ)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strAuthorNameE)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strAuthorNameJ)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strReleaseDate)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strCreator)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
        StrLen = GetUnicodeStr(CurPos, .strNotes)
        If StrLen < &H0 Then GoTo ErrHandler
        CurPos = CurPos + StrLen * &H2 + &H2
    End With
    
    ReadGD3Tag = &H0
    Exit Function

ErrHandler:

    ReadGD3Tag = &HFF
    Exit Function

End Function

Private Function GetUnicodeStr(ByVal StartPos As Long, ByRef RetString As String) As Long

    Dim StrLen As Long
    Dim StrArr() As Byte
    Dim CurChr As Integer
    
    On Error GoTo ErrHandler
    
    StrLen = &H0
    Do
        Call CopyMemory(CurChr, bytFileData(StartPos + StrLen * &H2), &H2)
        StrLen = StrLen + &H1
    Loop Until CurChr = &H0
    
    StrLen = StrLen - &H1
    If StrLen > &H0 Then
        ReDim StrArr(&H0 To StrLen * &H2 - &H1)
        Call CopyMemory(StrArr(&H0), bytFileData(StartPos), StrLen * &H2)
        RetString = StrArr()    ' VB uses Unicode Strings
    Else
        RetString = ""
    End If
    
    GetUnicodeStr = StrLen
    Exit Function

ErrHandler:

    GetUnicodeStr = -1
    Exit Function

End Function
