' Convertify Debug Script with Full Environment Setup
' Shows console window and waits for completion

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the script's directory
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Set working directory explicitly
objShell.CurrentDirectory = scriptDir

' Build command with explicit path
exePath = scriptDir & "\convertify.exe"
command = """" & exePath & """ convert --lab"

' Log the command being executed
WScript.Echo "Executing: " & command
WScript.Echo "Working Directory: " & scriptDir

' Execute with visible window and wait
' 1 = Normal window (visible)
' True = Wait for completion
objShell.Run command, 1, True

' Show completion message
MsgBox "Conversion process completed." & vbCrLf & vbCrLf & _
       "Check C:\services\logs\convertify.log for details." & vbCrLf & vbCrLf & _
       "Lab directories processed:" & vbCrLf & _
       "  - \\TNAS-Click\Team-design\4. PREPARAR RESUMEN" & vbCrLf & _
       "  - \\TNAS-Click\Team-design\8. Base Datos Unica", _
       vbInformation, "Convertify Debug"

Set objShell = Nothing
Set objFSO = Nothing
