Attribute VB_Name = "basMIDI"
Option Explicit

Public Type BigEndianInteger
    MSB As Byte
    LSB As Byte
End Type

Public Type BigEndianLong
    MSB As Byte
    Byte3 As Byte
    Byte2 As Byte
    LSB As Byte
End Type

Public Type MidiHeaderData
    MThd As String * 4
    HeaderLen As BigEndianLong
    MidiFormat As BigEndianInteger
    NumTracks As BigEndianInteger
    NumTicks As BigEndianInteger
End Type

Public Type DACHeaderData
    RIFF As String * 4
    HeaderLen As Long
    WAVEfmt As String * 8
    HeaderSize As Long
    Tag As Integer
    Channels As Integer
    SampleRate As Long
    BytespSecond As Long
    BytespSample As Integer
    SampelBits As Integer
    Data As String * 4
    DataLen As Long
End Type

Public MidiHeader As MidiHeaderData

Private Type MidiTrackHeaderData
    MTrk As String * 4
    TrackLen As BigEndianLong
End Type

Public MidiTrackHeader As MidiTrackHeaderData

Private MID_TrackSize As Long
Public MID_Trackdata() As Byte
Public MidFilePos As Long
Public DeltaTime As Long

'MIDI Command Constants
Public Const MIDI_NOTE_OFF = &H80
Public Const MIDI_NOTE_ON = &H90
Public Const MIDI_NOTE_AFTERTOUCH = &HA0
Public Const MIDI_CONTROLLER_CHANGE = &HB0
Public Const MIDI_PROGRAM_CHANGE = &HC0
Public Const MIDI_CHANNEL_AFTERTOUCH = &HD0
Public Const MIDI_PITCHWHEEL = &HE0
Public Const MIDI_META_EVENT = &HFF

Public Enum MIDICommand
     mcNoteOff = &H80
     mcNoteOn = &H90
     mcNoteAftertouch = &HA0
     mcControllerChange = &HB0
     mcProgramChange = &HC0
     mcChannelAftertouch = &HD0
     mcPitchWheel = &HE0
     mcMetaEvent = &HFF
End Enum

'MIDI Controller Numbers
Public Const MIDI_MODULATOR_WHEEL = &H1
Public Const MIDI_DATA_ENTRY_MSB = &H6
Public Const MIDI_VOLUME = &H7
Public Const MIDI_PAN = &HA
Public Const MIDI_SUSTAIN = &H40
Public Const MIDI_SOFT = &H43
Public Const MIDI_LEGATO_PEDAL = &H44
Public Const MIDI_HOLD2_PEDAL = &H45
Public Const MIDI_SOUND_TIMBRE = &H47
Public Const MIDI_SOUND_RELEASE_TIME = &H48
Public Const MIDI_SOUND_ATTACK_TIME = &H49
Public Const MIDI_SOUND_BRIGHTNESS = &H4A
Public Const MIDI_NRPN_LSB = &H62
Public Const MIDI_NRPN_MSB = &H63
Public Const MIDI_RPN_LSB = &H64
Public Const MIDI_RPN_MSB = &H65
Public Const MIDI_ALL_SOUNDS_OFF = &H78
Public Const MIDI_RESET_ALL_CONTROLLERS = &H79
Public Const MIDI_ALL_NOTES_OFF = &H7B

Public Enum MIDIControllers
    mcModulatorWheel = 1
    mcDataEntry = 6
    mcVolume = 7
    mcPan = 10
    mcSustain = 64
    mcLegatoPedal = 68
    mcHold2Pedal = 69
    mcSoundTimbre = 71
    mcSoundReleaseTime = 72
    mcSoundAttackTime = 73
    mcSoundBrightness = 74
    mcRPNFine = 100
    mcRPNCoarse = 101
    mcAllControllersOff = 123
    mcAllNotesOff = 123
End Enum

'Meta Event Constants
Public Const META_TEXT = &H1
Public Const META_COPYRIGHT = &H2
Public Const META_TRACK_NAME = &H3
Public Const META_INSTRUMENT_NAME = &H4
Public Const META_LYRIC = &H5
Public Const META_MARKER = &H6
Public Const META_CUE_POINT = &H6
Public Const META_TRACK_END = &H2F
Public Const META_TEMPO = &H51
Public Const META_SMPTE_OFS = &H54
Public Const META_MEASURE = &H58
Public Const META_KEY_SIGNATURE = &H59

' Loop-Strings (compatible with WinAmp)
Public Const TEXT_LOOP_START = "loopStart"
Public Const TEXT_LOOP_END = "loopEnd"
' When I tested the Space Harrier BIOS-VGM, I found a bug in Winamp.
' If the MIDI has the text "loopStart", looping works correctly (jump to 0:13)
' If the text has another case (like "LoopStart" or "Loopstart") or even a
' space ("Loop Start") it jumps to 2:34. I can't say why.

Public Enum MIDIMetaEvent
    mmeTrackEnd = &H2F
End Enum

'RPNs
Public Const RPN_PITCH_BEND_RANGE_M = &H0
Public Const RPN_PITCH_BEND_RANGE_L = &H0

' NRPNs
Public Const NRPN_DRUM_PITCH_COARSE = &H18
Public Const NRPN_DRUM_PITCH_FINE = &H19
Public Const NRPN_DRUM_VOLUME = &H1A
Public Const NRPN_DRUM_PAN = &H1C

Public Enum MIDIRPN
    mrPitchBendRange = 0
End Enum

''AWE32/SBLive! NRPNs
'Public Const NRPN_ENV1_DELAY = 16260
'Public Const NRPN_ENV1_ATTACK = 16261
'Public Const NRPN_ENV1_HOLD = 16262
'Public Const NRPN_ENV1_DECAY = 16263
'Public Const NRPN_ENV1_SUSTAIN = 16264
'Public Const NRPN_ENV1_RELEASE = 16265

'Public Enum MIDINRPN
'    mnEnv1DDelay = 16260
'    mnEnv1Attack = 16261
'    mnEnv1Hold = 16262
'    mnEnvDecay = 16263
'    mnEnvSustain = 16264
'    mnEnvRelease = 16265
'End Enum

' MIDI Controller Values
Public Const MIDI_VOLUME_MIN = &H0
Public Const MIDI_VOLUME_MAX = &H7F

Public Const MIDI_PAN_LEFT = &H0
Public Const MIDI_PAN_RIGHT = &H7F
Public Const MIDI_PAN_CENTER = &H40

Public Const MIDI_PITCHWHEEL_DOWN_ONE_SEMITONE = &H0
Public Const MIDI_PITCHWHEEL_DOWN_TWO_SEMITONES = &H1000
Public Const MIDI_PITCHWHEEL_DOWN_HALF_SEMITIONE = &H1800
Public Const MIDI_PITCHWHEEL_MIN = &H0
Public Const MIDI_PITCHWHEEL_CENTER = &H2000
Public Const MIDI_PITCHWHEEL_MAX = &H3FFF
Public Const MIDI_PITCHWHEEL_UP_HALF_SEMITIONE = &H2800
Public Const MIDI_PITCHWHEEL_UP_ONE_SEMITONE = &H3000
Public Const MIDI_PITCHWHEEL_UP_TWO_SEMITONES = &H3FFF

Public Enum MIDIControllerValue
    'Volume
    mcvVolumeMin = &H0
    mcvVolumeMax = &H7F
    'Pan
    mcvPanLeft = &H0
    mcvPanRight = &H7F
    mcvPanCenter = &H40
    'PitchWheel
    mcvPitchWheelCenter = &H2000
End Enum

'General MIDI Patch Names
Public Const MIDI_PATCH_Acoustic_Grand_Piano = 0
Public Const MIDI_PATCH_Bright_Acoustic_Piano = 1
Public Const MIDI_PATCH_Electric_Grand_Piano = 2
Public Const MIDI_PATCH_Honky_Tonk_Piano = 3
Public Const MIDI_PATCH_Rhodes_Piano = 4
Public Const MIDI_PATCH_Chorused_Piano = 5
Public Const MIDI_PATCH_Harpsichord = 6
Public Const MIDI_PATCH_Clavinet = 7
Public Const MIDI_PATCH_Celesta = 8
Public Const MIDI_PATCH_Glockenspiel = 9
Public Const MIDI_PATCH_Music_Box = 10
Public Const MIDI_PATCH_Vibraphone = 11
Public Const MIDI_PATCH_Marimba = 12
Public Const MIDI_PATCH_Xylophone = 13
Public Const MIDI_PATCH_Tubular_Bells = 14
Public Const MIDI_PATCH_Dulcimer = 15
Public Const MIDI_PATCH_Hammond_Organ = 16
Public Const MIDI_PATCH_Percussive_Organ = 17
Public Const MIDI_PATCH_Rock_Organ = 18
Public Const MIDI_PATCH_Church_Organ = 19
Public Const MIDI_PATCH_Reed_Organ = 20
Public Const MIDI_PATCH_Accordion = 21
Public Const MIDI_PATCH_Harmonica = 22
Public Const MIDI_PATCH_Tango_Accordion = 23
Public Const MIDI_PATCH_Acoustic_Guitar_Nylon = 24
Public Const MIDI_PATCH_Acoustic_Guitar_Steel = 25
Public Const MIDI_PATCH_Electric_Guitar_Jazz = 26
Public Const MIDI_PATCH_Electric_Guitar_Clean = 27
Public Const MIDI_PATCH_Electric_Guitar_Muted = 28
Public Const MIDI_PATCH_Overdriven_Guitar = 29
Public Const MIDI_PATCH_Distortion_Guitar = 30
Public Const MIDI_PATCH_Guitar_Harmonics = 31
Public Const MIDI_PATCH_Acoustic_Bass = 32
Public Const MIDI_PATCH_Electric_Bass_Finger = 33
Public Const MIDI_PATCH_Electric_Bass_Pick = 34
Public Const MIDI_PATCH_Fretless_Bass = 35
Public Const MIDI_PATCH_Slap_Bass_1 = 36
Public Const MIDI_PATCH_Slap_Bass_2 = 37
Public Const MIDI_PATCH_Synth_Bass_1 = 38
Public Const MIDI_PATCH_Synth_Bass_2 = 39
Public Const MIDI_PATCH_Violin = 40
Public Const MIDI_PATCH_Viola = 41
Public Const MIDI_PATCH_Cello = 42
Public Const MIDI_PATCH_Contrabass = 43
Public Const MIDI_PATCH_Tremolo_Strings = 44
Public Const MIDI_PATCH_Pizzicato_Strings = 45
Public Const MIDI_PATCH_Orchestral_Harp = 46
Public Const MIDI_PATCH_Timpani = 47
Public Const MIDI_PATCH_String_Ensemble_1 = 48
Public Const MIDI_PATCH_String_Ensemble_2 = 49
Public Const MIDI_PATCH_Synth_Strings_1 = 50
Public Const MIDI_PATCH_Synth_Strings_2 = 51
Public Const MIDI_PATCH_Choir_Ahhs = 52
Public Const MIDI_PATCH_Voice_Oohs = 53
Public Const MIDI_PATCH_Synth_Voice = 54
Public Const MIDI_PATCH_Orchestra_Hit = 55
Public Const MIDI_PATCH_Trumpet = 56
Public Const MIDI_PATCH_Trombone = 57
Public Const MIDI_PATCH_Tuba = 58
Public Const MIDI_PATCH_Muted_Trumpet = 59
Public Const MIDI_PATCH_French_Horn = 60
Public Const MIDI_PATCH_Brass_Section = 61
Public Const MIDI_PATCH_Synth_Brass_1 = 62
Public Const MIDI_PATCH_Synth_Brass_2 = 63
Public Const MIDI_PATCH_Soprano_Sax = 64
Public Const MIDI_PATCH_Alto_Sax = 65
Public Const MIDI_PATCH_Tenor_Sax = 66
Public Const MIDI_PATCH_Baritone_Sax = 67
Public Const MIDI_PATCH_Oboe = 68
Public Const MIDI_PATCH_English_Horn = 69
Public Const MIDI_PATCH_Bassoon = 70
Public Const MIDI_PATCH_Clarinet = 71
Public Const MIDI_PATCH_Piccolo = 72
Public Const MIDI_PATCH_Flute = 73
Public Const MIDI_PATCH_Recorder = 74
Public Const MIDI_PATCH_Pan_Flute = 75
Public Const MIDI_PATCH_Bottle_Blow = 76
Public Const MIDI_PATCH_Shakuhachi = 77
Public Const MIDI_PATCH_Whistle = 78
Public Const MIDI_PATCH_Ocarina = 79
Public Const MIDI_PATCH_Lead_1_Square = 80
Public Const MIDI_PATCH_Lead_2_Sawtooth = 81
Public Const MIDI_PATCH_Lead_3_Calliope = 82
Public Const MIDI_PATCH_Lead_4_Chiff = 83
Public Const MIDI_PATCH_Lead_5_Changarang = 84
Public Const MIDI_PATCH_Lead_6_Voice = 85
Public Const MIDI_PATCH_Lead_7_Fifths = 86
Public Const MIDI_PATCH_Lead_8_Bass_Lead = 87
Public Const MIDI_PATCH_Pad_1_New_Age = 88
Public Const MIDI_PATCH_Pad_2_Warm = 89
Public Const MIDI_PATCH_Pad_3_Polysynth = 90
Public Const MIDI_PATCH_Pad_4_Choir = 91
Public Const MIDI_PATCH_Pad_5_Bowed = 92
Public Const MIDI_PATCH_Pad_6_Metallic = 93
Public Const MIDI_PATCH_Pad_7_Halo = 94
Public Const MIDI_PATCH_Pad_8_Sweep = 95
Public Const MIDI_PATCH_FX_1_Rain = 96
Public Const MIDI_PATCH_FX_2_Soundtrack = 97
Public Const MIDI_PATCH_FX_3_Crystal = 98
Public Const MIDI_PATCH_FX_4_Atmosphere = 99
Public Const MIDI_PATCH_FX_5_Brightness = 100
Public Const MIDI_PATCH_FX_6_Goblins = 101
Public Const MIDI_PATCH_FX_7_Echoes = 102
Public Const MIDI_PATCH_FX_8_Sci_fi = 103
Public Const MIDI_PATCH_Sitar = 104
Public Const MIDI_PATCH_Banjo = 105
Public Const MIDI_PATCH_Shamisen = 106
Public Const MIDI_PATCH_Koto = 107
Public Const MIDI_PATCH_Kalimba = 108
Public Const MIDI_PATCH_Bagpipe = 109
Public Const MIDI_PATCH_Fiddle = 110
Public Const MIDI_PATCH_Shanai = 111
Public Const MIDI_PATCH_Tinkle_Bell = 112
Public Const MIDI_PATCH_Agogo = 113
Public Const MIDI_PATCH_Steel_Drums = 114
Public Const MIDI_PATCH_Woodblock = 115
Public Const MIDI_PATCH_Taiko_Drum = 116
Public Const MIDI_PATCH_Melodic_Tom = 117
Public Const MIDI_PATCH_Synth_Drum = 118
Public Const MIDI_PATCH_Reverse_Cymbal = 119
Public Const MIDI_PATCH_Guitar_Fret_Noise = 120
Public Const MIDI_PATCH_Breath_Noise = 121
Public Const MIDI_PATCH_Seashore = 122
Public Const MIDI_PATCH_Bird_Tweet = 123
Public Const MIDI_PATCH_Telephone_Ring = 124
Public Const MIDI_PATCH_Helicopter = 125
Public Const MIDI_PATCH_Applause = 126
Public Const MIDI_PATCH_Gunshot = 127

Public Enum MidiProgramNumber
    mpnAcousticGrandPiano = 0
    mpnBrightAcousticPiano = 1
    mpnElectricGrandPiano = 2
    mpnHonkyTonkPiano = 3
    mpnRhodesPiano = 4
    mpnChorusedPiano = 5
    mpnHarpsichord = 6
    mpnClavinet = 7
    mpnCelesta = 8
    mpnGlockenspiel = 9
    mpnMusicBox = 10
    mpnVibraphone = 11
    mpnMarimba = 12
    mpnXylophone = 13
    mpnTubularBells = 14
    mpnDulcimer = 15
    mpnHammondOrgan = 16
    mpnPercussiveOrgan = 17
    mpnRockOrgan = 18
    mpnChurchOrgan = 19
    mpnReedOrgan = 20
    mpnAccordion = 21
    mpnHarmonica = 22
    mpnTangoAccordion = 23
    mpnAcousticGuitarNylon = 24
    mpnAcousticGuitarSteel = 25
    mpnElectricGuitarJazz = 26
    mpnElectricGuitarClean = 27
    mpnElectricGuitarMuted = 28
    mpnOverdrivenGuitar = 29
    mpnDistortionGuitar = 30
    mpnGuitarHarmonics = 31
    mpnAcousticBass = 32
    mpnElectricBassFinger = 33
    mpnElectricBassPick = 34
    mpnFretlessBass = 35
    mpnSlapBass1 = 36
    mpnSlapBass2 = 37
    mpnSynthBass1 = 38
    mpnSynthBass2 = 39
    mpnViolin = 40
    mpnViola = 41
    mpnCello = 42
    mpnContrabass = 43
    mpnTremoloStrings = 44
    mpnPizzicatoStrings = 45
    mpnOrchestralHarp = 46
    mpnTimpani = 47
    mpnStringEnsemble1 = 48
    mpnStringEnsemble2 = 49
    mpnSynthStrings1 = 50
    mpnSynthStrings2 = 51
    mpnChoirAhhs = 52
    mpnVoiceOohs = 53
    mpnSynthVoice = 54
    mpnOrchestraHit = 55
    mpnTrumpet = 56
    mpnTrombone = 57
    mpnTuba = 58
    mpnMutedTrumpet = 59
    mpnFrenchHorn = 60
    mpnBrassSection = 61
    mpnSynthBrass1 = 62
    mpnSynthBrass2 = 63
    mpnSopranoSax = 64
    mpnAltoSax = 65
    mpnTenorSax = 66
    mpnBaritoneSax = 67
    mpnOboe = 68
    mpnEnglishHorn = 69
    mpnBassoon = 70
    mpnClarinet = 71
    mpnPiccolo = 72
    mpnFlute = 73
    mpnRecorder = 74
    mpnPanFlute = 75
    mpnBottleBlow = 76
    mpnShakuhachi = 77
    mpnWhistle = 78
    mpnOcarina = 79
    mpnLead1Square = 80
    mpnLead2Sawtooth = 81
    mpnLead3Calliope = 82
    mpnLead4Chiff = 83
    mpnLead5Changarang = 84
    mpnLead6Voice = 85
    mpnLead7Fifths = 86
    mpnLead8BassLead = 87
    mpnPad1NewAge = 88
    mpnPad2Warm = 89
    mpnPad3Polysynth = 90
    mpnPad4Choir = 91
    mpnPad5Bowed = 92
    mpnPad6Metallic = 93
    mpnPad7Halo = 94
    mpnPad8Sweep = 95
    mpnFX1Rain = 96
    mpnFX2Soundtrack = 97
    mpnFX3Crystal = 98
    mpnFX4Atmosphere = 99
    mpnFX5Brightness = 100
    mpnFX6Goblins = 101
    mpnFX7Echoes = 102
    mpnFX8Scifi = 103
    mpnSitar = 104
    mpnBanjo = 105
    mpnShamisen = 106
    mpnKoto = 107
    mpnKalimba = 108
    mpnBagpipe = 109
    mpnFiddle = 110
    mpnShanai = 111
    mpnTinkleBell = 112
    mpnAgogo = 113
    mpnSteelDrums = 114
    mpnWoodblock = 115
    mpnTaikoDrum = 116
    mpnMelodicTom = 117
    mpnSynthDrum = 118
    mpnReverseCymbal = 119
    mpnGuitarFretNoise = 120
    mpnBreathNoise = 121
    mpnSeashore = 122
    mpnBirdTweet = 123
    mpnTelephoneRing = 124
    mpnHelicopter = 125
    mpnApplause = 126
    mpnGunshot = 127
End Enum

'General MIDI Drum Kits
Public Enum MIDIDrumKit
    mdkStandard = 0
    mdkStandard2 = 1
    mdkRoom = 8
    mdkPower = 16
    mdkElectronic = 24
    mdkAnalog = 25
    mdkJazz = 32
    mdkBrush = 40
    mdkOrchestral = 48
    mdkSFX = 56
End Enum

Private TickspQuarter As Integer
Private DeltaFact As Single
Private WrittenDelayPos As Long
Private CurSamplePos As Long

Private Function CBEInt(ByVal intInt As Integer) As BigEndianInteger
    Dim intMSB As Integer, intLSB As Integer
    
    intMSB = Fix(intInt / &H100) And &HFF
    intLSB = (intInt And &HFF)
    
    With CBEInt
        .MSB = CByte(intMSB)
        .LSB = CByte(intLSB)
    End With

End Function

Public Sub MID_File_Init()

    Select Case CNV_ACCURACY
    Case &H0
        TickspQuarter = 30
    Case &H10
        TickspQuarter = 480
    Case &H80
        TickspQuarter = 2205
    Case &HFF
        TickspQuarter = 22050
    Case Else
        TickspQuarter = 22050
    End Select
    DeltaFact = 22050 / TickspQuarter
    If TEMPO_MOD = &H0 Then
        DeltaFact = DeltaFact * 120 / TEMPO_BPM
    ElseIf TEMPO_MOD = &H1 Then
        DeltaFact = DeltaFact * TEMPO_MULT / TEMPO_DIV
    End If
    WrittenDelayPos = &H0
    CurSamplePos = &H0
    MID_TrackSize = &H0
    Erase MID_Trackdata()

End Sub

Public Sub MID_File_Write(strFilename As String)
    Dim lngMThd As Long, lngHeaderLen As Long, _
    intMidiFormat As Integer, intNumTracks As Integer, _
    intNumTicks As Integer, lngTrackLen As Long
    
    On Error GoTo File_Error
    
    ' Track End marker
    MIDI_Event_Write MIDI_META_EVENT, META_TRACK_END, 0
    
    ' MIDI File Header (Format 0)
    With MidiHeader
        .MThd = "MThd"
        .HeaderLen.LSB = 6
        .MidiFormat.LSB = 0
        .NumTracks.LSB = 1
        intNumTicks = TickspQuarter
        .NumTicks = CBEInt(intNumTicks)
    End With
    
    ' MIDI Track Header
    With MidiTrackHeader
        .MTrk = "MTrk"
        lngTrackLen = MidFilePos
        .TrackLen = CBELng(lngTrackLen)
    End With
    
    If Dir(strFilename) <> "" Then
        Open strFilename For Binary As #1: Close
        Kill (strFilename)
    End If

    ReDim Preserve MID_Trackdata(&H0 To MidFilePos - 1)
    Open strFilename For Binary As 1
        Put 1, , MidiHeader
        Put 1, , MidiTrackHeader
        Put 1, , MID_Trackdata
    Close
    
    Exit Sub

File_Error:
    Select Case Err.Number
    Dim strPrompt As String, intReturn As Integer
    Case 75 'Path/File Access Error
        strPrompt = "The .MID file you are attempting to save is currently in use by another program or process." _
        & vbCrLf & "Please close the file, and select 'OK' to continue, or select 'Cancel' to, well, cancel."
        intReturn = MsgBox(strPrompt, vbExclamation + vbOKCancel, Err.Description)
        Select Case intReturn
        Case vbOK
            Err.Clear
            Resume
        Case vbCancel
            MsgBox ".MID Save canceled", vbCritical
            Exit Sub
        End Select
    Case Else
        strPrompt = "Error #" & Err.Number _
        & vbCrLf & "'" & Err.Description & "'"
        MsgBox strPrompt
    End Select

End Sub

Private Function ValueToMIDI(ByVal Value As Long, ByRef RetArr() As Byte) As Long

    Dim DataString As String
    Dim TempVal As Byte
    Dim TempDelay As Long
    
    DataString = ""
    TempVal = Value And &H7F
    TempDelay = Int(Value / &H80)
    DataString = Chr$(TempVal)
    
    Do While TempDelay > 0
        TempVal = TempDelay And &H7F
        TempDelay = Int(TempDelay / &H80)
        DataString = Chr$(TempVal Or &H80) & DataString
    Loop
    
    RetArr() = StrConv(DataString, vbFromUnicode)
    ValueToMIDI = Len(DataString)

End Function

Private Sub MIDI_Resize(ByVal NewSize As Long)

    ' Makes sure that the Array has at least NewSize Bytes
    If MID_TrackSize < NewSize Then
        MID_TrackSize = MID_TrackSize + &H10000
        ReDim Preserve MID_Trackdata(MID_TrackSize - 1) As Byte
    End If

End Sub

Public Function MIDI_Event_Write(Optional ByVal Param1 As Variant, Optional ByVal Param2 As Variant, Optional ByVal Param3 As Variant, Optional ByVal Param4 As Variant, Optional ByVal Param5 As Variant) As Byte

    Dim DeltaVal As Long
    Dim DeltaArr() As Byte
    Dim DeltaLen As Long
    Dim TempLng As Long
    
    On Error GoTo MIDIErr
    
    CurSamplePos = CurSamplePos + DeltaTime
    DeltaTime = 0
    TempLng = Int(CurSamplePos / DeltaFact + 0.5)
    DeltaVal = TempLng - WrittenDelayPos
    WrittenDelayPos = WrittenDelayPos + DeltaVal
    
    If DeltaVal >= &H80 Then
        ' New Delay-Calculation
        DeltaLen = ValueToMIDI(DeltaVal, DeltaArr())
        'ReDim Preserve MID_Trackdata(MidFilePos + DeltaLen - 2) As Byte
        Call MIDI_Resize(MidFilePos + DeltaLen - 1)
        For TempLng = &H0 To DeltaLen - 2
            MID_Trackdata(MidFilePos) = DeltaArr(TempLng)
            MidFilePos = MidFilePos + 1
        Next TempLng
        DeltaVal = DeltaArr(DeltaLen - 1)
    End If
    
    Dim Command As Byte, Channel As Byte
    Dim Note As Byte, Velocity As Byte
    
    Command = CByte(Param1)

    Select Case Command
    Case MIDI_NOTE_OFF
        Channel = CByte(Param2)
        Note = CByte(Param3)
        Velocity = CByte(Param4)
        
        'ReDim Preserve MID_Trackdata(MidFilePos + 3) As Byte
        Call MIDI_Resize(MidFilePos + 4)
        
        MID_Trackdata(MidFilePos) = DeltaVal
        MID_Trackdata(MidFilePos + 1) = (Command Or Channel)
        MID_Trackdata(MidFilePos + 2) = Note
        MID_Trackdata(MidFilePos + 3) = Velocity
        
        MidFilePos = MidFilePos + 4
    
    Case MIDI_NOTE_ON:
        Channel = CByte(Param2)
        Note = CByte(Param3)
        Velocity = CByte(Param4)
        
        'ReDim Preserve MID_Trackdata(MidFilePos + 3) As Byte
        Call MIDI_Resize(MidFilePos + 4)
        
        MID_Trackdata(MidFilePos) = DeltaVal
        MID_Trackdata(MidFilePos + 1) = (Command Or Channel)
        MID_Trackdata(MidFilePos + 2) = Note
        MID_Trackdata(MidFilePos + 3) = Velocity
        
        MidFilePos = MidFilePos + 4
    
    
    Case MIDI_CONTROLLER_CHANGE:
        Dim Controller As Byte, ControllerValue As Byte
        
        Channel = CByte(Param2)
        Controller = CByte(Param3)
        ControllerValue = CByte(Param4)
        
        'ReDim Preserve MID_Trackdata(MidFilePos + 3) As Byte
        Call MIDI_Resize(MidFilePos + 4)
        
        MID_Trackdata(MidFilePos) = DeltaVal
        MID_Trackdata(MidFilePos + 1) = (Command Or Channel)
        MID_Trackdata(MidFilePos + 2) = Controller
        MID_Trackdata(MidFilePos + 3) = ControllerValue
        
        MidFilePos = MidFilePos + 4
    
    Case MIDI_PROGRAM_CHANGE:
        Dim Program As Byte
        
        Channel = CByte(Param2)
        Program = CByte(Param3)
                
        'ReDim Preserve MID_Trackdata(MidFilePos + 2) As Byte
        Call MIDI_Resize(MidFilePos + 3)
        
        MID_Trackdata(MidFilePos) = DeltaVal
        MID_Trackdata(MidFilePos + 1) = (Command Or Channel)
        MID_Trackdata(MidFilePos + 2) = Program
        
        MidFilePos = MidFilePos + 3
    
    Case MIDI_PITCHWHEEL:
        Dim PitchWheel As Integer
        
        Channel = CByte(Param2)
        PitchWheel = CInt(Param3)
        
        Dim beintPitchWheel As BigEndianInteger
        'beintPitchWheel = CIntToMidiPitchWheel(PitchWheel)
        Dim intMSB As Integer, intLSB As Integer
        intMSB = Fix(PitchWheel / &H80) And &H7F
        intLSB = (PitchWheel And &H7F)
        With beintPitchWheel
            .MSB = CByte(intMSB)
            .LSB = CByte(intLSB)
        End With
        
        'ReDim Preserve MID_Trackdata(MidFilePos + 3) As Byte
        Call MIDI_Resize(MidFilePos + 4)
        
        MID_Trackdata(MidFilePos) = DeltaVal
        MID_Trackdata(MidFilePos + 1) = (Command Or Channel)
        MID_Trackdata(MidFilePos + 2) = beintPitchWheel.LSB
        MID_Trackdata(MidFilePos + 3) = beintPitchWheel.MSB
        
        MidFilePos = MidFilePos + 4
    
    Case MIDI_META_EVENT:
        Dim EventType As Byte
        
        EventType = CByte(Param2)
        
        Select Case EventType
        Case META_TRACK_END:
            Dim TrackEndMarker As Byte
            
            TrackEndMarker = CByte(Param3)
            
            'ReDim Preserve MID_Trackdata(MidFilePos + 3) As Byte
            Call MIDI_Resize(MidFilePos + 4)
            
            MID_Trackdata(MidFilePos) = DeltaVal
            MID_Trackdata(MidFilePos + 1) = Command
            MID_Trackdata(MidFilePos + 2) = EventType
            MID_Trackdata(MidFilePos + 3) = TrackEndMarker
            
            MidFilePos = MidFilePos + 4
        
        Case META_TEMPO:
            TempLng = CLng(Param3)
            
            'ReDim Preserve MID_Trackdata(MidFilePos + 6) As Byte
            Call MIDI_Resize(MidFilePos + 7)
            
            MID_Trackdata(MidFilePos) = DeltaVal
            MID_Trackdata(MidFilePos + 1) = Command
            MID_Trackdata(MidFilePos + 2) = EventType
            MID_Trackdata(MidFilePos + 3) = &H3 ' Event Length
            MID_Trackdata(MidFilePos + 4) = Int(TempLng / &H10000) And &HFF
            MID_Trackdata(MidFilePos + 5) = Int(TempLng / &H100&) And &HFF
            MID_Trackdata(MidFilePos + 6) = Int(TempLng / &H1&) And &HFF
            
            MidFilePos = MidFilePos + 7
        
        Case Else
            Dim MetaStr As String
            
            MetaStr = CStr(Param3)
            DeltaLen = Len(MetaStr)
            DeltaArr() = StrConv(MetaStr, vbFromUnicode)
            If DeltaLen > &H7F Then
                ' I'm too lazy to insert the delay-calculation a second time
                DeltaLen = &H7F
            End If
            
            'ReDim Preserve MID_Trackdata(MidFilePos + 4 + DeltaLen) As Byte
            Call MIDI_Resize(MidFilePos + 5 + DeltaLen)
            
            MID_Trackdata(MidFilePos) = DeltaVal
            MID_Trackdata(MidFilePos + 1) = Command
            MID_Trackdata(MidFilePos + 2) = EventType
            MID_Trackdata(MidFilePos + 3) = DeltaLen
            For TempLng = &H0 To DeltaLen - 1
                MID_Trackdata(MidFilePos + 4 + TempLng) = DeltaArr(TempLng)
            Next TempLng
            
            MidFilePos = MidFilePos + 4 + DeltaLen
        End Select
    
    End Select
    
    Exit Function

MIDIErr:

    'Stop
    'Resume
    
    Exit Function

End Function
Private Function CLELng(BELng As BigEndianLong) As Long
    
    With BELng
        CLELng = (.MSB * &H1000000) + (.Byte3 * &H10000) + (.Byte2 * &H100) + .LSB
    End With

End Function
Private Function CLEInt(BEInt As BigEndianInteger) As Integer
    
    With BEInt
        CLEInt = (.MSB * &H100) + .LSB
    End With

End Function
Private Function CBELng(ByVal lngLong As Long) As BigEndianLong
    Dim lngMSB As Long, lngByte3 As Long, intByte2 As Integer, intLSB As Integer
    
    lngMSB = Fix(lngLong / &H1000000) And &HFF
    lngByte3 = Fix(lngLong / &H10000) And &HFF
    intByte2 = Fix(lngLong / &H100) And &HFF
    intLSB = Fix(lngLong And &HFF)
    
    With CBELng
        .MSB = CByte(lngMSB)
        .Byte3 = CByte(lngByte3)
        .Byte2 = CByte(intByte2)
        .LSB = CByte(intLSB)
    End With

End Function

Private Function CBELngR(ByVal lngLong As Long) As BigEndianLong
    Dim DataByte(3) As Byte
    
    DataByte(0) = Int(lngLong / &H1000000)
    DataByte(1) = Int(lngLong / &H10000) Mod &H100
    DataByte(2) = Int(lngLong / &H100) Mod &H100
    DataByte(3) = lngLong Mod &H100
    
    With CBELngR
        .MSB = DataByte(3)
        .Byte3 = DataByte(2)
        .Byte2 = DataByte(1)
        .LSB = DataByte(0)
    End With

End Function

' Added possibility to extract DAC-Data to a WAVE-File
Public Sub DAC_WriteOpen()

    On Error GoTo File_Error
    
    Dim DAC_Header As DACHeaderData
    Dim DataBytes As Long
    
    With DAC_Header
        .RIFF = "RIFF"
        .WAVEfmt = "WAVEfmt "
        .HeaderSize = &H10
        .Tag = &H1
        .Channels = &H1
        .SampleRate = 44100
        .BytespSecond = 44100
        .BytespSample = &H1
        .SampelBits = &H8
        .Data = "data"
        .DataLen = -1
        .HeaderLen = -1
    End With
    
    Open Environ("Temp") & "\DAC.wav" For Binary Access Read Write As #2
        Put 2, 1, DAC_Header
        DataBytes = Seek(2) - 1
        Put #2, &H4 + 1, DataBytes
        Seek #2, DataBytes + 1
    
    Exit Sub

File_Error:
    Select Case Err.Number
    Dim strPrompt As String, intReturn As Integer
    Case 75 'Path/File Access Error
        strPrompt = "The DAC.wav file is currently in use by another program or process." _
        & vbCrLf & "Please close the file, and select 'OK' to continue, or select 'Cancel' to, well, cancel."
        intReturn = MsgBox(strPrompt, vbExclamation + vbOKCancel, Err.Description)
        Select Case intReturn
        Case vbOK
            Err.Clear
            Resume
        Case vbCancel
            MsgBox ".MID Save canceled", vbCritical
            Exit Sub
        End Select
    Case Else
        strPrompt = "Error #" & Err.Number _
        & vbCrLf & "'" & Err.Description & "'"
        MsgBox strPrompt
    End Select

End Sub

Public Sub DAC_WriteClose()

    Dim DataBase As Long
    Dim CurPos As Long
    Dim DataLen As Long
    Dim HeadDataLen As Long
    
    CurPos = Seek(2) - 1
    Get #2, &H4 + 1, DataBase
    
    DataLen = CurPos - DataBase
    HeadDataLen = CurPos - &H8
    
    Put #2, DataBase - &H4 + 1, DataLen
    Put #2, &H4 + 1, HeadDataLen
    
    Close #2

End Sub

Public Sub DAC_Write()

    On Error GoTo File_Error
    
    Dim DAC_Header As DACHeaderData
    Dim DataByte(3) As Byte
    Dim DataBytes As Long
    Static DACNumber As Integer
    
    With DAC_Header
        .RIFF = "RIFF"
        .WAVEfmt = "WAVEfmt "
        .HeaderSize = &H10
        .Tag = &H1
        .Channels = &H1
        .SampleRate = &H2800
        .BytespSecond = &H2800
        .BytespSample = &H1
        .SampelBits = &H8
        .Data = "data"
        .DataLen = DAC_Pos
        .HeaderLen = DAC_Pos + &H24
    End With
    
    Open Environ("Temp") & "\DAC" & Format(DACNumber, "000") & ".wav" For Binary Access Write As #2
        Put 2, , DAC_Header
        Put 2, , DAC_Data()
    Close #2
    ReDim DAC_Data(0)
    DAC_Pos = 0
    DACNumber = DACNumber + 1
    
    Exit Sub

File_Error:
    Select Case Err.Number
    Dim strPrompt As String, intReturn As Integer
    Case 75 'Path/File Access Error
        strPrompt = "The DAC.wav file is currently in use by another program or process." _
        & vbCrLf & "Please close the file, and select 'OK' to continue, or select 'Cancel' to, well, cancel."
        intReturn = MsgBox(strPrompt, vbExclamation + vbOKCancel, Err.Description)
        Select Case intReturn
        Case vbOK
            Err.Clear
            Resume
        Case vbCancel
            MsgBox ".MID Save canceled", vbCritical
            Exit Sub
        End Select
    Case Else
        strPrompt = "Error #" & Err.Number _
        & vbCrLf & "'" & Err.Description & "'"
        MsgBox strPrompt
    End Select

End Sub

Public Function DB2MidiVol(ByVal DB As Single) As Byte

    Dim TempSng As Single
    
    TempSng = 10# ^ (DB / 40#)
    DB2MidiVol = TempSng * &H7F

End Function

Public Function Lin2DB(ByVal LinearVal As Single) As Single

    If LinearVal > 0! Then
        Lin2DB = Log(LinearVal) / Log(2) * 6
    Else
        Lin2DB = -400   ' results in volume 0
    End If

End Function
