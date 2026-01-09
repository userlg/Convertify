' Convertify Lab Environment Launcher
' This script launches convertify.exe with the --lab flag
' to automatically process videos in the lab directories

Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this VBS script is located
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Path to convertify.exe (assumes it's in the same directory as this script)
exePath = scriptDir & "\convertify.exe"

' Run convertify with --lab flag
' The --lab flag automatically uses:
'   - W:/4. PREPARAR RESUMEN
'   - W:/8. Base Datos Unica
WshShell.Run """" & exePath & """ --lab", 1, False

Set WshShell = Nothing
