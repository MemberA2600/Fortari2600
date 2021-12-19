Attribute VB_Name = "basWin32API"
Option Explicit

Declare Function GetShortPathName Lib "kernel32" (ByVal lpszLongPath As String, ByVal lpszShortPath As String, ByVal cchBuffer As Long) As Long
Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" _
    (ByRef hpvDest As Any, ByRef hpvSource As Any, ByVal cbCopy As Long)
Declare Function SendMessage Lib "user32" Alias "SendMessageA" _
    (ByVal hWnd As Long, ByVal wMsg As Long, ByVal wParam As Long, _
    ByRef lParam As Any) As Long

Public Const WM_SETREDRAW = &HB



