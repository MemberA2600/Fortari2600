VERSION 5.00
Begin VB.Form frmOptions 
   BorderStyle     =   4  'Festes Werkzeugfenster
   Caption         =   "Options"
   ClientHeight    =   6975
   ClientLeft      =   45
   ClientTop       =   315
   ClientWidth     =   8175
   ControlBox      =   0   'False
   LinkTopic       =   "frmOptions"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   6975
   ScaleWidth      =   8175
   ShowInTaskbar   =   0   'False
   StartUpPosition =   1  'Fenstermitte
   Begin VB.Frame fraOptions 
      Height          =   6015
      Index           =   0
      Left            =   120
      TabIndex        =   7
      Top             =   360
      Width           =   6855
      Begin VB.Frame fraTempo 
         Caption         =   "MIDI Tempo Modification"
         Height          =   1095
         Left            =   120
         TabIndex        =   216
         Top             =   3720
         Width           =   3975
         Begin VB.TextBox txtTempoDiv 
            Alignment       =   1  'Rechts
            Height          =   285
            Left            =   2280
            MaxLength       =   5
            TabIndex        =   223
            Text            =   "256"
            Top             =   600
            Width           =   615
         End
         Begin VB.TextBox txtTempoMult 
            Alignment       =   1  'Rechts
            Height          =   285
            Left            =   1440
            MaxLength       =   5
            TabIndex        =   221
            Text            =   "256"
            Top             =   600
            Width           =   615
         End
         Begin VB.OptionButton optTempoMod 
            Caption         =   "Multiply with"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   220
            Top             =   600
            Value           =   -1  'True
            Width           =   1215
         End
         Begin VB.OptionButton optTempoMod 
            Caption         =   "Convert with"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   219
            Top             =   240
            Width           =   1215
         End
         Begin VB.TextBox txtBPM 
            Alignment       =   1  'Rechts
            Height          =   285
            Left            =   1440
            MaxLength       =   9
            TabIndex        =   217
            Text            =   "120"
            Top             =   210
            Width           =   735
         End
         Begin VB.Label LabelTempoDiv 
            Alignment       =   2  'Zentriert
            Caption         =   "/"
            Height          =   255
            Left            =   2040
            TabIndex        =   222
            Top             =   645
            Width           =   255
         End
         Begin VB.Label LabelBPM 
            Caption         =   "BPM"
            Height          =   255
            Left            =   2280
            TabIndex        =   218
            Top             =   255
            Width           =   615
         End
      End
      Begin VB.Frame fraVGMLoop 
         Caption         =   "Looping VGMs"
         Height          =   615
         Left            =   120
         TabIndex        =   212
         Top             =   3000
         Width           =   3975
         Begin VB.TextBox txtLoopTimes 
            Alignment       =   1  'Rechts
            Height          =   285
            Left            =   600
            MaxLength       =   3
            TabIndex        =   213
            Text            =   "1"
            Top             =   210
            Width           =   495
         End
         Begin VB.Label LabelLoop 
            Caption         =   "Loop"
            Height          =   255
            Left            =   120
            TabIndex        =   215
            Top             =   255
            Width           =   495
         End
         Begin VB.Label LabelLoopTime 
            Caption         =   "times"
            Height          =   255
            Left            =   1200
            TabIndex        =   214
            Top             =   255
            Width           =   615
         End
      End
      Begin VB.Frame fraDualChipHandle 
         Caption         =   "Dual Chip Handling"
         Height          =   975
         Left            =   120
         TabIndex        =   206
         Top             =   1920
         Width           =   3975
         Begin VB.OptionButton optDualChipHandle 
            Caption         =   "Disable 1nd Chip"
            Enabled         =   0   'False
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   209
            Top             =   600
            Width           =   1575
         End
         Begin VB.OptionButton optDualChipHandle 
            Caption         =   "Handle both as one"
            Height          =   255
            Index           =   1
            Left            =   1800
            TabIndex        =   208
            Top             =   240
            Width           =   1695
         End
         Begin VB.OptionButton optDualChipHandle 
            Caption         =   "Disable 2nd Chip"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   207
            Top             =   240
            Value           =   -1  'True
            Width           =   1575
         End
      End
      Begin VB.Frame fraConversionAccuracy 
         Caption         =   "Conversion Accuracy (Ticks per Quarter)"
         Height          =   975
         Left            =   120
         TabIndex        =   148
         Top             =   840
         Width           =   3975
         Begin VB.OptionButton optConversionAccuracy 
            Caption         =   "Sample (22050)"
            Height          =   255
            Index           =   3
            Left            =   1800
            TabIndex        =   152
            Top             =   600
            Width           =   1455
         End
         Begin VB.OptionButton optConversionAccuracy 
            Caption         =   "High (2205)"
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   151
            Top             =   600
            Width           =   1455
         End
         Begin VB.OptionButton optConversionAccuracy 
            Caption         =   "Good (480)"
            Height          =   255
            Index           =   1
            Left            =   1800
            TabIndex        =   150
            Top             =   240
            Width           =   1455
         End
         Begin VB.OptionButton optConversionAccuracy 
            Caption         =   "Frame (30)"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   149
            Top             =   240
            Value           =   -1  'True
            Width           =   1455
         End
      End
      Begin VB.CommandButton cmdDefaults_General 
         Caption         =   "&Defaults"
         Height          =   375
         Left            =   5760
         TabIndex        =   144
         Top             =   5520
         Width           =   975
      End
      Begin VB.Frame fraPitchWheelSensitivity 
         Caption         =   "Pitchwheel Sensitivity (+/- Semitones)"
         Height          =   615
         Left            =   120
         TabIndex        =   9
         Top             =   120
         Width           =   4095
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "64*"
            Height          =   255
            Index           =   5
            Left            =   3360
            TabIndex        =   15
            Top             =   240
            Width           =   615
         End
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "48*"
            Height          =   255
            Index           =   4
            Left            =   2760
            TabIndex        =   14
            Top             =   240
            Width           =   615
         End
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "24"
            Height          =   255
            Index           =   3
            Left            =   2160
            TabIndex        =   13
            Top             =   240
            Width           =   495
         End
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "12"
            Height          =   255
            Index           =   2
            Left            =   1680
            TabIndex        =   12
            Top             =   240
            Width           =   495
         End
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "4"
            Height          =   255
            Index           =   1
            Left            =   1200
            TabIndex        =   11
            Top             =   240
            Width           =   375
         End
         Begin VB.OptionButton optPitchWheelSensitivity 
            Caption         =   "2 (default)"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   10
            Top             =   240
            Value           =   -1  'True
            Width           =   1095
         End
      End
      Begin VB.Label Label3 
         Caption         =   $"frmOptions.frx":0000
         Height          =   420
         Left            =   120
         TabIndex        =   211
         Top             =   5520
         Width           =   5535
      End
   End
   Begin VB.OptionButton optOptions 
      Caption         =   "YM2151"
      Height          =   255
      Index           =   4
      Left            =   3960
      Style           =   1  'Grafisch
      TabIndex        =   6
      Top             =   120
      Width           =   975
   End
   Begin VB.OptionButton optOptions 
      Caption         =   "YM2612"
      Height          =   255
      Index           =   3
      Left            =   3000
      Style           =   1  'Grafisch
      TabIndex        =   5
      Top             =   120
      Width           =   975
   End
   Begin VB.OptionButton optOptions 
      Caption         =   "YM2413"
      Height          =   255
      Index           =   2
      Left            =   2040
      Style           =   1  'Grafisch
      TabIndex        =   4
      Top             =   120
      Width           =   975
   End
   Begin VB.OptionButton optOptions 
      Caption         =   "PSG"
      Height          =   255
      Index           =   1
      Left            =   1080
      Style           =   1  'Grafisch
      TabIndex        =   3
      Top             =   120
      Width           =   975
   End
   Begin VB.OptionButton optOptions 
      Caption         =   "General"
      Height          =   255
      Index           =   0
      Left            =   120
      Style           =   1  'Grafisch
      TabIndex        =   2
      Top             =   120
      Width           =   975
   End
   Begin VB.Frame fraOptions 
      Height          =   6015
      Index           =   1
      Left            =   360
      TabIndex        =   8
      Top             =   360
      Width           =   6855
      Begin VB.Frame fraVolDepNotes 
         Caption         =   "Volume-dependent Note On/Off"
         Height          =   975
         Left            =   120
         TabIndex        =   153
         Top             =   1800
         Width           =   3975
         Begin VB.OptionButton optVoldepNotes 
            Caption         =   "Yes"
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   156
            Top             =   600
            Width           =   1455
         End
         Begin VB.OptionButton optVoldepNotes 
            Caption         =   "only Vol = 0 / Vol > 0"
            Height          =   255
            Index           =   1
            Left            =   1800
            TabIndex        =   155
            Top             =   240
            Width           =   2055
         End
         Begin VB.OptionButton optVoldepNotes 
            Caption         =   "No"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   154
            Top             =   240
            Value           =   -1  'True
            Width           =   1455
         End
      End
      Begin VB.CommandButton cmdDefaults_PSG 
         Caption         =   "&Defaults"
         Height          =   375
         Left            =   5760
         TabIndex        =   147
         Top             =   5520
         Width           =   975
      End
      Begin VB.Frame fraPSG 
         Caption         =   "PSG"
         Height          =   1575
         Left            =   120
         TabIndex        =   93
         Top             =   120
         Width           =   2535
         Begin VB.CheckBox chkPSG_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   100
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   99
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   98
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_NOISE_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Left            =   2040
            Style           =   1  'Grafisch
            TabIndex        =   97
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Enabled         =   0   'False
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   96
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Enabled         =   0   'False
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   95
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkPSG_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Enabled         =   0   'False
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   94
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.Line Line1 
            Index           =   8
            X1              =   120
            X2              =   2400
            Y1              =   720
            Y2              =   720
         End
         Begin VB.Label Label1 
            Caption         =   "Enabled"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   106
            Top             =   840
            Width           =   735
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 0 "
            Height          =   495
            Index           =   4
            Left            =   840
            TabIndex        =   105
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 1 "
            Height          =   495
            Index           =   5
            Left            =   1200
            TabIndex        =   104
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 2 "
            Height          =   495
            Index           =   6
            Left            =   1560
            TabIndex        =   103
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "Noise"
            Height          =   255
            Index           =   7
            Left            =   1920
            TabIndex        =   102
            Top             =   345
            Width           =   495
         End
         Begin VB.Label Label1 
            Caption         =   "Volume"
            Enabled         =   0   'False
            Height          =   255
            Index           =   3
            Left            =   120
            TabIndex        =   101
            Top             =   1200
            Width           =   615
         End
      End
   End
   Begin VB.CommandButton cmdResetAll 
      Caption         =   "&Reset All"
      Height          =   375
      Left            =   4920
      TabIndex        =   1
      Top             =   6480
      Width           =   975
   End
   Begin VB.CommandButton cmdOK 
      Caption         =   "&OK"
      Default         =   -1  'True
      Height          =   375
      Left            =   6000
      TabIndex        =   0
      Top             =   6480
      Width           =   975
   End
   Begin VB.Frame fraOptions 
      Height          =   6015
      Index           =   2
      Left            =   600
      TabIndex        =   17
      Top             =   360
      Width           =   6855
      Begin VB.CheckBox chkoptimizedVGM 
         Caption         =   "optimized VGMs"
         Height          =   255
         Left            =   5040
         TabIndex        =   210
         Top             =   1800
         Width           =   1575
      End
      Begin VB.CommandButton cmdDefaults_YM2413 
         Caption         =   "&Defaults"
         Height          =   375
         Left            =   5760
         TabIndex        =   145
         Top             =   5520
         Width           =   975
      End
      Begin VB.Frame fraYM2413 
         Caption         =   "YM2413"
         Height          =   1935
         Left            =   120
         TabIndex        =   18
         Top             =   120
         Width           =   4815
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   46
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   45
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   44
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   43
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   42
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   41
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   40
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   39
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   8
            Left            =   3720
            Style           =   1  'Grafisch
            TabIndex        =   38
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PERCUSSION_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Left            =   4200
            Style           =   1  'Grafisch
            TabIndex        =   37
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   36
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   35
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   34
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   33
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   32
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   31
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   30
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   29
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   8
            Left            =   3720
            Style           =   1  'Grafisch
            TabIndex        =   28
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   27
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   26
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   25
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   24
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   23
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   22
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   21
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   20
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2413_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   8
            Left            =   3720
            Style           =   1  'Grafisch
            TabIndex        =   19
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.Line Line1 
            Index           =   1
            X1              =   120
            X2              =   4680
            Y1              =   720
            Y2              =   720
         End
         Begin VB.Label Label1 
            Caption         =   "Enabled"
            Height          =   255
            Index           =   9
            Left            =   120
            TabIndex        =   59
            Top             =   840
            Width           =   735
         End
         Begin VB.Label Label1 
            Caption         =   "Volume"
            Height          =   255
            Index           =   10
            Left            =   120
            TabIndex        =   58
            Top             =   1200
            Width           =   735
         End
         Begin VB.Label Label1 
            Caption         =   "Program"
            Height          =   255
            Index           =   11
            Left            =   120
            TabIndex        =   57
            Top             =   1560
            Width           =   615
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 0 "
            Height          =   495
            Index           =   12
            Left            =   840
            TabIndex        =   56
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 1 "
            Height          =   495
            Index           =   13
            Left            =   1200
            TabIndex        =   55
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 2 "
            Height          =   495
            Index           =   14
            Left            =   1560
            TabIndex        =   54
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 3 "
            Height          =   495
            Index           =   15
            Left            =   1920
            TabIndex        =   53
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 4 "
            Height          =   495
            Index           =   16
            Left            =   2280
            TabIndex        =   52
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 5 "
            Height          =   495
            Index           =   17
            Left            =   2640
            TabIndex        =   51
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 6 "
            Height          =   495
            Index           =   18
            Left            =   3000
            TabIndex        =   50
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 7 "
            Height          =   495
            Index           =   19
            Left            =   3360
            TabIndex        =   49
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 8 "
            Height          =   495
            Index           =   20
            Left            =   3720
            TabIndex        =   48
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "Drums"
            Height          =   255
            Index           =   21
            Left            =   4080
            TabIndex        =   47
            Top             =   345
            Width           =   495
         End
      End
      Begin VB.Frame FraYM2413_MIDI_Patch 
         Caption         =   "Patch Changes"
         Height          =   3255
         Index           =   1
         Left            =   120
         TabIndex        =   60
         Top             =   2160
         Width           =   6615
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   15
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   76
            Top             =   2760
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   14
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   75
            Top             =   2400
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   13
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   74
            Top             =   2040
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   12
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   73
            Top             =   1680
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   11
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   72
            Top             =   1320
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   10
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   71
            Top             =   960
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   9
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   70
            Top             =   600
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   8
            Left            =   4320
            Style           =   2  'Dropdown-Liste
            TabIndex        =   69
            Top             =   240
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   7
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   68
            Top             =   2760
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   6
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   67
            Top             =   2400
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   5
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   66
            Top             =   2040
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   4
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   65
            Top             =   1680
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   3
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   64
            Top             =   1320
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   2
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   63
            Top             =   960
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   1
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   62
            Top             =   600
            Width           =   2175
         End
         Begin VB.ComboBox cboYM2413_MIDI_Patch 
            Height          =   315
            Index           =   0
            Left            =   840
            Style           =   2  'Dropdown-Liste
            TabIndex        =   61
            Top             =   240
            Width           =   2175
         End
         Begin VB.Label Label1 
            Caption         =   "Electric Guitar"
            Height          =   255
            Index           =   46
            Left            =   3240
            TabIndex        =   92
            Top             =   2760
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Acoustic Bass"
            Height          =   255
            Index           =   45
            Left            =   3240
            TabIndex        =   91
            Top             =   2400
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Synth Bass"
            Height          =   255
            Index           =   44
            Left            =   3240
            TabIndex        =   90
            Top             =   2040
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Vibes"
            Height          =   255
            Index           =   43
            Left            =   3240
            TabIndex        =   89
            Top             =   1680
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Harpsichord"
            Height          =   255
            Index           =   42
            Left            =   3240
            TabIndex        =   88
            Top             =   1320
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Synthesizer"
            Height          =   255
            Index           =   41
            Left            =   3240
            TabIndex        =   87
            Top             =   960
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Horn"
            Height          =   255
            Index           =   40
            Left            =   3240
            TabIndex        =   86
            Top             =   600
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Organ"
            Height          =   255
            Index           =   39
            Left            =   3240
            TabIndex        =   85
            Top             =   240
            Width           =   1095
         End
         Begin VB.Label Label1 
            Caption         =   "Trumpet"
            Height          =   255
            Index           =   38
            Left            =   120
            TabIndex        =   84
            Top             =   2760
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Oboe"
            Height          =   255
            Index           =   37
            Left            =   120
            TabIndex        =   83
            Top             =   2400
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Clarinet"
            Height          =   255
            Index           =   36
            Left            =   120
            TabIndex        =   82
            Top             =   2040
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Flute"
            Height          =   255
            Index           =   35
            Left            =   120
            TabIndex        =   81
            Top             =   1680
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Piano"
            Height          =   255
            Index           =   34
            Left            =   120
            TabIndex        =   80
            Top             =   1320
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Guitar"
            Height          =   255
            Index           =   33
            Left            =   120
            TabIndex        =   79
            Top             =   960
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Violin"
            Height          =   255
            Index           =   8
            Left            =   120
            TabIndex        =   78
            Top             =   600
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Original"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   77
            Top             =   240
            Width           =   615
         End
      End
      Begin VB.Label Label1 
         Caption         =   "Note: Options also affect YM3812, YM3526, Y8950 and YMF262 chips."
         Height          =   255
         Index           =   29
         Left            =   240
         TabIndex        =   157
         Top             =   5580
         Width           =   5295
      End
   End
   Begin VB.Frame fraOptions 
      Height          =   6015
      Index           =   3
      Left            =   840
      TabIndex        =   16
      Top             =   360
      Width           =   6855
      Begin VB.CommandButton cmdDefaults_YM2612 
         Caption         =   "&Defaults"
         Height          =   375
         Left            =   5760
         TabIndex        =   146
         Top             =   5520
         Width           =   975
      End
      Begin VB.Frame fraYM2612 
         Caption         =   "YM2612"
         Height          =   2295
         Left            =   120
         TabIndex        =   107
         Top             =   120
         Width           =   3615
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   132
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   131
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   130
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   129
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   128
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   127
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_DAC_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Left            =   3120
            Style           =   1  'Grafisch
            TabIndex        =   126
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   125
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   124
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   123
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   122
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   121
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   120
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   119
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   118
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   117
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   116
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   115
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   114
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   113
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   112
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   111
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   110
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   109
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2612_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   108
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 3 "
            Height          =   375
            Index           =   22
            Left            =   1920
            TabIndex        =   143
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 2 "
            Height          =   375
            Index           =   23
            Left            =   1560
            TabIndex        =   142
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 1 "
            Height          =   375
            Index           =   24
            Left            =   1200
            TabIndex        =   141
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 0 "
            Height          =   375
            Index           =   25
            Left            =   840
            TabIndex        =   140
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Caption         =   "Program"
            Height          =   255
            Index           =   26
            Left            =   120
            TabIndex        =   139
            Top             =   1560
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Volume"
            Height          =   255
            Index           =   27
            Left            =   120
            TabIndex        =   138
            Top             =   1200
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Enabled"
            Height          =   255
            Index           =   28
            Left            =   120
            TabIndex        =   137
            Top             =   840
            Width           =   615
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 4 "
            Height          =   375
            Index           =   30
            Left            =   2280
            TabIndex        =   136
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 5 "
            Height          =   375
            Index           =   31
            Left            =   2640
            TabIndex        =   135
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "DAC"
            Height          =   255
            Index           =   32
            Left            =   3000
            TabIndex        =   134
            Top             =   345
            Width           =   495
         End
         Begin VB.Label Label1 
            Caption         =   "Pan"
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   133
            Top             =   1920
            Width           =   615
         End
         Begin VB.Line Line1 
            Index           =   0
            X1              =   120
            X2              =   3480
            Y1              =   720
            Y2              =   720
         End
      End
      Begin VB.Label Label1 
         Caption         =   "Note: Options also affect YM2203, YM2608 and YM2610/B chips."
         Height          =   255
         Index           =   47
         Left            =   240
         TabIndex        =   158
         Top             =   5580
         Width           =   5295
      End
   End
   Begin VB.Frame fraOptions 
      Height          =   6015
      Index           =   4
      Left            =   1080
      TabIndex        =   159
      Top             =   360
      Width           =   6855
      Begin VB.Frame fraYM2151 
         Caption         =   "YM2151"
         Height          =   2295
         Left            =   120
         TabIndex        =   161
         Top             =   120
         Width           =   3735
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   205
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   204
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   202
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   201
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   200
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   199
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   198
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PAN_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   197
            Top             =   1920
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   185
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   184
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   183
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   182
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   181
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   180
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   179
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_PROG_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   178
            Top             =   1560
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   177
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   176
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   175
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   174
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   173
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   172
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   171
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_VOL_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   170
            Top             =   1200
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   7
            Left            =   3360
            Style           =   1  'Grafisch
            TabIndex        =   169
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   6
            Left            =   3000
            Style           =   1  'Grafisch
            TabIndex        =   168
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   5
            Left            =   2640
            Style           =   1  'Grafisch
            TabIndex        =   167
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   4
            Left            =   2280
            Style           =   1  'Grafisch
            TabIndex        =   166
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   3
            Left            =   1920
            Style           =   1  'Grafisch
            TabIndex        =   165
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   2
            Left            =   1560
            Style           =   1  'Grafisch
            TabIndex        =   164
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   1
            Left            =   1200
            Style           =   1  'Grafisch
            TabIndex        =   163
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.CheckBox chkYM2151_CH_DISABLED 
            Alignment       =   1  'Rechts ausgerichtet
            BackColor       =   &H000000FF&
            Height          =   255
            Index           =   0
            Left            =   840
            Style           =   1  'Grafisch
            TabIndex        =   162
            Top             =   840
            Value           =   1  'Aktiviert
            Width           =   255
         End
         Begin VB.Label Label1 
            Caption         =   "Pan"
            Height          =   255
            Index           =   69
            Left            =   120
            TabIndex        =   203
            Top             =   1920
            Width           =   615
         End
         Begin VB.Line Line1 
            Index           =   2
            X1              =   120
            X2              =   3600
            Y1              =   720
            Y2              =   720
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 7 "
            Height          =   495
            Index           =   58
            Left            =   3360
            TabIndex        =   196
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 6 "
            Height          =   495
            Index           =   57
            Left            =   3000
            TabIndex        =   195
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 5 "
            Height          =   495
            Index           =   56
            Left            =   2640
            TabIndex        =   194
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 4 "
            Height          =   495
            Index           =   55
            Left            =   2280
            TabIndex        =   193
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 3 "
            Height          =   495
            Index           =   54
            Left            =   1920
            TabIndex        =   192
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 2 "
            Height          =   495
            Index           =   53
            Left            =   1560
            TabIndex        =   191
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 1 "
            Height          =   495
            Index           =   52
            Left            =   1200
            TabIndex        =   190
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Alignment       =   2  'Zentriert
            Caption         =   "CH 0 "
            Height          =   495
            Index           =   51
            Left            =   840
            TabIndex        =   189
            Top             =   240
            Width           =   255
         End
         Begin VB.Label Label1 
            Caption         =   "Program"
            Height          =   255
            Index           =   50
            Left            =   120
            TabIndex        =   188
            Top             =   1560
            Width           =   615
         End
         Begin VB.Label Label1 
            Caption         =   "Volume"
            Height          =   255
            Index           =   49
            Left            =   120
            TabIndex        =   187
            Top             =   1200
            Width           =   735
         End
         Begin VB.Label Label1 
            Caption         =   "Enabled"
            Height          =   255
            Index           =   48
            Left            =   120
            TabIndex        =   186
            Top             =   840
            Width           =   735
         End
      End
      Begin VB.CommandButton cmdDefaults_YM2151 
         Caption         =   "&Defaults"
         Height          =   375
         Left            =   5760
         TabIndex        =   160
         Top             =   5520
         Width           =   975
      End
   End
End
Attribute VB_Name = "frmOptions"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Dim MIDIPatchName(127) As String
Dim ForegroundTab As Integer

Private Sub MIDIPatchNames_Assign()
    MIDIPatchName(0) = "Acoustic Grand Piano"
    MIDIPatchName(1) = "Bright Acoustic Piano"
    MIDIPatchName(2) = "Electric Grand Piano"
    MIDIPatchName(3) = "Honky Tonk Piano"
    MIDIPatchName(4) = "Rhodes Piano"
    MIDIPatchName(5) = "Chorused Piano"
    MIDIPatchName(6) = "Harpsichord"
    MIDIPatchName(7) = "Clavinet"
    MIDIPatchName(8) = "Celesta"
    MIDIPatchName(9) = "Glockenspiel"
    MIDIPatchName(10) = "Music Box"
    MIDIPatchName(11) = "Vibraphone"
    MIDIPatchName(12) = "Marimba"
    MIDIPatchName(13) = "Xylophone"
    MIDIPatchName(14) = "Tubular Bells"
    MIDIPatchName(15) = "Dulcimer"
    MIDIPatchName(16) = "Hammond Organ"
    MIDIPatchName(17) = "Percussive Organ"
    MIDIPatchName(18) = "Rock Organ"
    MIDIPatchName(19) = "Church Organ"
    MIDIPatchName(20) = "Reed Organ"
    MIDIPatchName(21) = "Accordion"
    MIDIPatchName(22) = "Harmonica"
    MIDIPatchName(23) = "Tango Accordion"
    MIDIPatchName(24) = "Acoustic Guitar (Nylon)"
    MIDIPatchName(25) = "Acoustic Guitar (Steel)"
    MIDIPatchName(26) = "Electric Guitar (Jazz)"
    MIDIPatchName(27) = "Electric Guitar (Clean)"
    MIDIPatchName(28) = "Electric Guitar (Muted)"
    MIDIPatchName(29) = "Overdriven Guitar"
    MIDIPatchName(30) = "Distortion Guitar"
    MIDIPatchName(31) = "Guitar Harmonics"
    MIDIPatchName(32) = "Acoustic Bass"
    MIDIPatchName(33) = "Electric Bass Finger"
    MIDIPatchName(34) = "Electric Bass Pick"
    MIDIPatchName(35) = "Fretless Bass"
    MIDIPatchName(36) = "Slap Bass 1"
    MIDIPatchName(37) = "Slap Bass 2"
    MIDIPatchName(38) = "Synth Bass 1"
    MIDIPatchName(39) = "Synth Bass 2"
    MIDIPatchName(40) = "Violin"
    MIDIPatchName(41) = "Viola"
    MIDIPatchName(42) = "Cello"
    MIDIPatchName(43) = "Contrabass"
    MIDIPatchName(44) = "Tremolo Strings"
    MIDIPatchName(45) = "Pizzicato Strings"
    MIDIPatchName(46) = "Orchestral Harp"
    MIDIPatchName(47) = "Timpani"
    MIDIPatchName(48) = "String Ensemble 1"
    MIDIPatchName(49) = "String Ensemble 2"
    MIDIPatchName(50) = "Synth Strings 1"
    MIDIPatchName(51) = "Synth Strings 2"
    MIDIPatchName(52) = "Choir Ahhs"
    MIDIPatchName(53) = "Voice Oohs"
    MIDIPatchName(54) = "Synth Voice"
    MIDIPatchName(55) = "Orchestra Hit"
    MIDIPatchName(56) = "Trumpet"
    MIDIPatchName(57) = "Trombone"
    MIDIPatchName(58) = "Tuba"
    MIDIPatchName(59) = "Muted Trumpet"
    MIDIPatchName(60) = "French Horn"
    MIDIPatchName(61) = "Brass Section"
    MIDIPatchName(62) = "Synth Brass 1"
    MIDIPatchName(63) = "Synth Brass 2"
    MIDIPatchName(64) = "Soprano Sax"
    MIDIPatchName(65) = "Alto Sax"
    MIDIPatchName(66) = "Tenor Sax"
    MIDIPatchName(67) = "Baritone Sax"
    MIDIPatchName(68) = "Oboe"
    MIDIPatchName(69) = "English Horn"
    MIDIPatchName(70) = "Bassoon"
    MIDIPatchName(71) = "Clarinet"
    MIDIPatchName(72) = "Piccolo"
    MIDIPatchName(73) = "Flute"
    MIDIPatchName(74) = "Recorder"
    MIDIPatchName(75) = "Pan Flute"
    MIDIPatchName(76) = "Bottle Blow"
    MIDIPatchName(77) = "Shakuhachi"
    MIDIPatchName(78) = "Whistle"
    MIDIPatchName(79) = "Ocarina"
    MIDIPatchName(80) = "Lead 1 (Square)"
    MIDIPatchName(81) = "Lead 2 (Sawtooth)"
    MIDIPatchName(82) = "Lead 3 (Calliope)"
    MIDIPatchName(83) = "Lead 4 (Chiff)"
    MIDIPatchName(84) = "Lead 5 (Changarang)"
    MIDIPatchName(85) = "Lead 6 (Voice)"
    MIDIPatchName(86) = "Lead 7 (Fifths)"
    MIDIPatchName(87) = "Lead 8 (Bass & Lead)"
    MIDIPatchName(88) = "Pad 1 (New Age)"
    MIDIPatchName(89) = "Pad 2 (Warm)"
    MIDIPatchName(90) = "Pad 3 (Polysynth)"
    MIDIPatchName(91) = "Pad 4 (Choir)"
    MIDIPatchName(92) = "Pad 5 (Bowed)"
    MIDIPatchName(93) = "Pad 6 (Metallic)"
    MIDIPatchName(94) = "Pad 7 (Halo)"
    MIDIPatchName(95) = "Pad 8 (Sweep)"
    MIDIPatchName(96) = "FX 1 (Rain)"
    MIDIPatchName(97) = "FX 2 (Soundtrack)"
    MIDIPatchName(98) = "FX 3 (Crystal)"
    MIDIPatchName(99) = "FX 4 (Atmosphere)"
    MIDIPatchName(100) = "FX 5 (Brightness)"
    MIDIPatchName(101) = "FX 6 (Goblins)"
    MIDIPatchName(102) = "FX 7 (Echoes)"
    MIDIPatchName(103) = "FX 8 (Sci fi)"
    MIDIPatchName(104) = "Sitar"
    MIDIPatchName(105) = "Banjo"
    MIDIPatchName(106) = "Shamisen"
    MIDIPatchName(107) = "Koto"
    MIDIPatchName(108) = "Kalimba"
    MIDIPatchName(109) = "Bagpipe"
    MIDIPatchName(110) = "Fiddle"
    MIDIPatchName(111) = "Shanai"
    MIDIPatchName(112) = "Tinkle Bell"
    MIDIPatchName(113) = "Agogo"
    MIDIPatchName(114) = "Steel Drums"
    MIDIPatchName(115) = "Woodblock"
    MIDIPatchName(116) = "Taiko Drum"
    MIDIPatchName(117) = "Melodic Tom"
    MIDIPatchName(118) = "Synth Drum"
    MIDIPatchName(119) = "Reverse Cymbal"
    MIDIPatchName(120) = "Guitar Fret Noise"
    MIDIPatchName(121) = "Breath Noise"
    MIDIPatchName(122) = "Seashore"
    MIDIPatchName(123) = "Bird Tweet"
    MIDIPatchName(124) = "Telephone Ring"
    MIDIPatchName(125) = "Helicopter"
    MIDIPatchName(126) = "Applause"
    MIDIPatchName(127) = "Gunshot"
End Sub
Public Sub Options_Set_All()
    Options_Set_General
    Options_Set_PSG
    Options_Set_YM2413
    Options_Set_YM2612
End Sub
Public Function Options_Set_Defaults_All()
    Options_Set_Defaults_General
    Options_Set_Defaults_PSG
    Options_Set_Defaults_YM2413
    Options_Set_Defaults_YM2612
    Options_Set_Defaults_YM2151
End Function

Public Sub Options_Set_Defaults_General()
    optPitchWheelSensitivity(0).Value = True
'    optPitchWheelSensitivity(1).Value = False
'    optPitchWheelSensitivity(2).Value = False
'    optPitchWheelSensitivity(3).Value = False
'    optPitchWheelSensitivity(4).Value = False
'    optPitchWheelSensitivity(5).Value = False
    optConversionAccuracy(1).Value = True
    optDualChipHandle(1).Value = True
    txtLoopTimes.Text = Format$(2)
    Call txtLoopTimes_Change
    optTempoMod(0).Value = True
    txtBPM.Text = Format$(120)
    txtTempoMult.Text = Format$(256)
    txtTempoDiv.Text = Format$(256)
End Sub
Public Sub Options_Set_Defaults_PSG()
    Dim i As Integer
    For i = 0 To 2
        chkPSG_CH_DISABLED(i).Value = vbUnchecked
        chkPSG_VOL_DISABLED(i).Value = vbUnchecked
    Next
    chkPSG_NOISE_DISABLED.Value = vbUnchecked
    optVoldepNotes(2).Value = True
End Sub
Public Sub Options_Set_Defaults_YM2413()
    Dim i As Integer
    For i = 0 To 8
        chkYM2413_CH_DISABLED(i).Value = vbUnchecked
        chkYM2413_VOL_DISABLED(i).Value = vbUnchecked
        chkYM2413_PROG_DISABLED(i).Value = vbUnchecked
    Next
    chkYM2413_PERCUSSION_DISABLED.Value = vbUnchecked
    chkoptimizedVGM.Value = vbUnchecked
    
    cboYM2413_MIDI_Patch(0).ListIndex = MIDI_PATCH_Ocarina 'Original
    cboYM2413_MIDI_Patch(1).ListIndex = MIDI_PATCH_Synth_Strings_1 'Violin
    cboYM2413_MIDI_Patch(2).ListIndex = MIDI_PATCH_Acoustic_Guitar_Nylon 'Guitar
    cboYM2413_MIDI_Patch(3).ListIndex = MIDI_PATCH_Acoustic_Grand_Piano 'Piano
    cboYM2413_MIDI_Patch(4).ListIndex = MIDI_PATCH_Flute 'Flute
    cboYM2413_MIDI_Patch(5).ListIndex = MIDI_PATCH_Clarinet 'Clarinet
    cboYM2413_MIDI_Patch(6).ListIndex = MIDI_PATCH_Oboe 'Oboe
    cboYM2413_MIDI_Patch(7).ListIndex = MIDI_PATCH_Trumpet 'Trumpet
    cboYM2413_MIDI_Patch(8).ListIndex = MIDI_PATCH_Hammond_Organ 'Organ
    cboYM2413_MIDI_Patch(9).ListIndex = MIDI_PATCH_French_Horn 'Horn
    cboYM2413_MIDI_Patch(10).ListIndex = MIDI_PATCH_Pad_3_Polysynth 'Synthesizer
    cboYM2413_MIDI_Patch(11).ListIndex = MIDI_PATCH_Harpsichord 'Harpsichord
    cboYM2413_MIDI_Patch(12).ListIndex = MIDI_PATCH_Vibraphone 'Vibes
    cboYM2413_MIDI_Patch(13).ListIndex = MIDI_PATCH_Synth_Bass_2 'Synth Bass
    cboYM2413_MIDI_Patch(14).ListIndex = MIDI_PATCH_Acoustic_Bass 'Acoustic Bass
    cboYM2413_MIDI_Patch(15).ListIndex = MIDI_PATCH_Electric_Guitar_Jazz ' Electric Guitar
End Sub
Public Sub Options_Set_Defaults_YM2612()
    Dim i As Integer
    For i = 0 To 5
        chkYM2612_CH_DISABLED(i).Value = vbUnchecked
        chkYM2612_VOL_DISABLED(i).Value = vbUnchecked
        chkYM2612_PROG_DISABLED(i).Value = vbUnchecked
        chkYM2612_PAN_DISABLED(i).Value = vbUnchecked
    Next
    chkYM2612_DAC_DISABLED.Value = vbUnchecked
End Sub
Public Sub Options_Set_Defaults_YM2151()
    Dim i As Integer
    For i = 0 To 7
        chkYM2151_CH_DISABLED(i).Value = vbUnchecked
        chkYM2151_VOL_DISABLED(i).Value = vbUnchecked
        chkYM2151_PROG_DISABLED(i).Value = vbUnchecked
        chkYM2151_PAN_DISABLED(i).Value = vbUnchecked
    Next i
End Sub
Public Sub Options_Set_General()
    Dim intOptIndex As Integer
    
    On Error Resume Next
    
    For intOptIndex = 0 To (optPitchWheelSensitivity.Count - 1)
        If optPitchWheelSensitivity(intOptIndex).Value = True Then Exit For
    Next intOptIndex
    ' Values 8, 16, 32 changed to 12, 24, 48 to fit octaves
    ' Warning! The maximum range of Pitch Depth is 24,
    ' but some devices also support higher values.
    PITCHWHEEL_SENSITIVITY = Choose(intOptIndex + 1, 2, 4, 12, 24, 48, 64)
    PITCHWHEEL_STEPS = 8192 / PITCHWHEEL_SENSITIVITY
    
    ' New: Set the conversion accuracy
    For intOptIndex = 0 To optConversionAccuracy.Count - 1
        If optConversionAccuracy(intOptIndex).Value = True Then Exit For
    Next intOptIndex
    CNV_ACCURACY = Choose(intOptIndex + 1, &H0, &H10, &H80, &HFF)
    For intOptIndex = 0 To optDualChipHandle.Count - 1
        If optDualChipHandle(intOptIndex).Value = True Then Exit For
    Next intOptIndex
    DUAL_CHIPS = intOptIndex
    
    ' New: Tempo Modifier
    VGM_LOOPS = Val(txtLoopTimes.Text)
    For intOptIndex = 0 To optDualChipHandle.Count - 1
        If optTempoMod(intOptIndex).Value = True Then Exit For
    Next intOptIndex
    TEMPO_MOD = intOptIndex
    TEMPO_BPM = Val(txtBPM.Text)
    TEMPO_MULT = Val(txtTempoMult.Text)
    TEMPO_DIV = Val(txtTempoDiv.Text)
    
End Sub
Public Sub Options_Set_PSG()
    Dim i As Integer
    For i = 0 To 2
        PSG_CH_DISABLED(i) = IIf(chkPSG_CH_DISABLED(i).Value = vbChecked, 1, 0)
        PSG_VOL_DISABLED(i) = IIf(chkPSG_VOL_DISABLED(i).Value = vbChecked, 1, 0)
    Next
    PSG_NOISE_DISABLED = IIf(chkPSG_NOISE_DISABLED.Value = vbChecked, 1, 0)
    ' New: Volume-dependent notes
    For i = 0 To optConversionAccuracy.Count - 1
        If optVoldepNotes(i).Value = True Then Exit For
    Next i
    PSG_VOLDEP_NOTES = i
End Sub
Public Sub Options_Set_YM2413()
    Dim i As Integer
    For i = 0 To 8
        YM2413_CH_DISABLED(i) = IIf(chkYM2413_CH_DISABLED(i).Value = vbChecked, 1, 0)
        YM2413_VOL_DISABLED(i) = IIf(chkYM2413_VOL_DISABLED(i).Value = vbChecked, 1, 0)
        YM2413_PROG_DISABLED(i) = IIf(chkYM2413_PROG_DISABLED(i).Value = vbChecked, 1, 0)
    Next
    YM2413_PERCUSSION_DISABLED = IIf(chkYM2413_PERCUSSION_DISABLED.Value = vbChecked, 1, 0)
    YM2413_OPTIMIZED_VGMS = IIf(chkoptimizedVGM.Value = vbChecked, 1, 0)
    For i = 0 To 15
        YM2413_MIDI_PATCH(i) = cboYM2413_MIDI_Patch(i).ListIndex
    Next
End Sub
Public Sub Options_Set_YM2612()
    Dim i As Integer
    For i = 0 To 5
        YM2612_CH_DISABLED(i) = IIf(chkYM2612_CH_DISABLED(i).Value = vbChecked, 1, 0)
        YM2612_VOL_DISABLED(i) = IIf(chkYM2612_VOL_DISABLED(i).Value = vbChecked, 1, 0)
        YM2612_PROG_DISABLED(i) = IIf(chkYM2612_PROG_DISABLED(i).Value = vbChecked, 1, 0)
        YM2612_PAN_DISABLED(i) = IIf(chkYM2612_PAN_DISABLED(i).Value = vbChecked, 1, 0)
    Next
    YM2612_DAC_DISABLED = IIf(chkYM2612_DAC_DISABLED.Value = vbChecked, 1, 0)
End Sub
Public Sub Options_Set_YM2151()
    Dim i As Integer
    For i = 0 To 7
        YM2151_CH_DISABLED(i) = IIf(chkYM2151_CH_DISABLED(i).Value = vbChecked, 1, 0)
        YM2151_VOL_DISABLED(i) = IIf(chkYM2151_VOL_DISABLED(i).Value = vbChecked, 1, 0)
        YM2151_PROG_DISABLED(i) = IIf(chkYM2151_PROG_DISABLED(i).Value = vbChecked, 1, 0)
        YM2151_PAN_DISABLED(i) = IIf(chkYM2151_PAN_DISABLED(i).Value = vbChecked, 1, 0)
    Next i
End Sub

Private Sub chkPSG_CH_DISABLED_Click(Index As Integer)
    With chkPSG_CH_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkPSG_NOISE_DISABLED_Click()
    With chkPSG_NOISE_DISABLED
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub


Private Sub chkPSG_VOL_DISABLED_Click(Index As Integer)
    With chkPSG_VOL_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub


Private Sub chkYM2413_CH_DISABLED_Click(Index As Integer)
    With chkYM2413_CH_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub


Private Sub chkYM2413_PERCUSSION_DISABLED_Click()
    With chkYM2413_PERCUSSION_DISABLED
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2413_PROG_DISABLED_Click(Index As Integer)
    With chkYM2413_PROG_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2413_VOL_DISABLED_Click(Index As Integer)
    With chkYM2413_VOL_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub


Private Sub chkYM2612_CH_DISABLED_Click(Index As Integer)
    With chkYM2612_CH_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2612_DAC_DISABLED_Click()
    With chkYM2612_DAC_DISABLED
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub


Private Sub chkYM2612_PAN_DISABLED_Click(Index As Integer)
    With chkYM2612_PAN_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2612_PROG_DISABLED_Click(Index As Integer)
    With chkYM2612_PROG_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2612_VOL_DISABLED_Click(Index As Integer)
    With chkYM2612_VOL_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2151_CH_DISABLED_Click(Index As Integer)
    With chkYM2151_CH_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2151_VOL_DISABLED_Click(Index As Integer)
    With chkYM2151_VOL_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2151_PROG_DISABLED_Click(Index As Integer)
    With chkYM2151_PROG_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub chkYM2151_PAN_DISABLED_Click(Index As Integer)
    With chkYM2151_PAN_DISABLED(Index)
        .BackColor = IIf(.Value = vbChecked, &HFF&, &HFF00&)
    End With
End Sub

Private Sub cmdDefaults_General_Click()
    Options_Set_Defaults_General
End Sub

Private Sub cmdDefaults_PSG_Click()
    Options_Set_Defaults_PSG
End Sub

Private Sub cmdDefaults_YM2413_Click()
    Options_Set_Defaults_YM2413
End Sub

Private Sub cmdDefaults_YM2612_Click()
    Options_Set_Defaults_YM2612
End Sub

Private Sub cmdDefaults_YM2151_Click()
    Options_Set_Defaults_YM2151
End Sub

Private Sub cmdOK_Click()
    Options_Set_All
    Me.Hide
End Sub

Private Sub cmdResetAll_Click()
    Options_Set_Defaults_All
End Sub


Private Sub Form_Load()
    Dim i As Integer, j As Integer
    
    With cmdOK
        Me.Width = .Left + .Width + 240
        Me.Height = .Top + .Height + 480
    End With
    
    With fraOptions(0)
        For i = 1 To (fraOptions.Count - 1)
            fraOptions(i).Move .Left, .Top, .Width, .Height
            'fraOptions(i).ZOrder vbSendToBack
            fraOptions(i).Visible = False   ' Disable Tab-Key
        Next
        .Visible = True
        ForegroundTab = .Index
    End With

    MIDIPatchNames_Assign

    For i = 0 To cboYM2413_MIDI_Patch.Count - 1
        ' Disabling AutoRedraw really speeds the whole thing up (~10 - 15%)
        Call Control_AutoRedraw(cboYM2413_MIDI_Patch(i), False)
        With cboYM2413_MIDI_Patch(i)
            For j = 0 To 127
                .AddItem MIDIPatchName(j)
            Next
            .ListIndex = 0
        End With
        Call Control_AutoRedraw(cboYM2413_MIDI_Patch(i), True)
    Next

    Options_Set_Defaults_All

End Sub

Private Sub optOptions_Click(Index As Integer)
    'fraOptions(Index).ZOrder vbBringToFront
    fraOptions(ForegroundTab).Visible = False
    fraOptions(Index).Visible = True
    ForegroundTab = Index
End Sub

Private Sub txtLoopTimes_Change()

    Dim TempInt As Integer
    
    On Error Resume Next
    TempInt = CInt(txtLoopTimes.Text)
    LabelLoopTime.Caption = "time" & IIf(TempInt = 1, "", "s")

End Sub

Private Sub txtLoopTimes_KeyPress(KeyAscii As Integer)

    If KeyAscii >= &H20 And KeyAscii < &H30 Or KeyAscii > &H39 Then
        KeyAscii = &H0
        Beep
    End If

End Sub

Private Sub txtBPM_KeyPress(KeyAscii As Integer)

    If KeyAscii = &H2C Then KeyAscii = &H2E
    If KeyAscii >= &H20 And KeyAscii < &H30 And KeyAscii <> &H2E Or KeyAscii > &H39 Then
        KeyAscii = &H0
        Beep
    End If

End Sub

Private Sub txtTempoMult_KeyPress(KeyAscii As Integer)

    If KeyAscii >= &H20 And KeyAscii < &H30 Or KeyAscii > &H39 Then
        KeyAscii = &H0
        Beep
    End If

End Sub

Private Sub txtTempoDiv_KeyPress(KeyAscii As Integer)

    If KeyAscii >= &H20 And KeyAscii < &H30 Or KeyAscii > &H39 Then
        KeyAscii = &H0
        Beep
    End If

End Sub

Private Sub optTempoMod_Click(Index As Integer)

    Select Case Index
    Case 0
        txtBPM.Enabled = True
        LabelBPM.Enabled = True
        txtTempoMult.Enabled = False
        LabelTempoDiv.Enabled = False
        txtTempoDiv.Enabled = False
    Case 1
        txtBPM.Enabled = False
        LabelBPM.Enabled = False
        txtTempoMult.Enabled = True
        LabelTempoDiv.Enabled = True
        txtTempoDiv.Enabled = True
    End Select

End Sub

Private Sub Control_AutoRedraw(ByRef Ctrl As Object, ByVal AutoRedraw As Boolean)

    If Not AutoRedraw Then
        Call SendMessage(Ctrl.hWnd, WM_SETREDRAW, &H0, &H0)
    Else
        Call SendMessage(Ctrl.hWnd, WM_SETREDRAW, &H1, &H0)
        Ctrl.Refresh
    End If

End Sub
