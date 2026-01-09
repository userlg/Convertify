' Convertify Production Script with Full Environment Setup
' This version ensures proper execution context for network paths

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the script's directory
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Set working directory explicitly
objShell.CurrentDirectory = scriptDir

' Build command with explicit path
exePath = scriptDir & "\convertify.exe"
command = """" & exePath & """ convert --lab"

' Execute with proper settings
' 0 = Hidden window
' True = Wait for completion
' This ensures the process completes fully before VBS exits
objShell.Run command, 0, True

Set objShell = Nothing
Set objFSO = Nothing