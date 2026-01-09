# Convertify VBS Scripts Guide

## Production Script: `convertify.vbs`

**Purpose:** Silent execution for automated workflows

```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "C:\services\convertify.exe convert --lab", 0, False
```

**Characteristics:**

- `0` = Hidden window (no console visible)
- `False` = Asynchronous (doesn't wait for completion)
- Best for: Scheduled tasks, automated workflows

---

## Debug Script: `convertify_debug.vbs`

**Purpose:** Troubleshooting and diagnostics

```vbscript
Set objShell = CreateObject("WScript.Shell")
objShell.Run "C:\services\convertify.exe convert --lab", 1, True
MsgBox "Conversion process completed. Check the console output for any errors.", vbInformation, "Convertify Debug"
```

**Characteristics:**

- `1` = Visible window (normal size)
- `True` = Synchronous (waits for completion)
- Shows completion message box
- Best for: Diagnosing issues, seeing real-time progress

---

## How to Use Debug Script

1. **Copy to production environment:**

   ```
   C:\services\
   ├── convertify.exe
   ├── convertify.vbs          (production - silent)
   └── convertify_debug.vbs    (debug - visible)
   ```

2. **Run debug version:**

   - Double-click `convertify_debug.vbs`
   - Watch the console window for errors
   - See which directory is being processed
   - Check for any error messages

3. **Common issues to look for:**

   - ❌ "No AVI files found" - Directory is empty or path is wrong
   - ❌ "Permission denied" - Need admin rights
   - ❌ "Path not found" - Directory doesn't exist
   - ❌ Stops after first directory - Check logs for errors

4. **Check logs:**
   - Location: `C:\services\logs\convertify.log` (hidden folder)
   - To view hidden folders: File Explorer → View → Hidden items
   - Look for errors related to second directory

---

## Troubleshooting Second Directory Issue

### Possible Causes:

1. **Permission Issues**

   - Second directory might have different permissions
   - Solution: Run as administrator

2. **Path Issues**

   - Spaces in path name might cause problems
   - Solution: Check if path exists and is accessible

3. **File Lock Issues**

   - Files in second directory might be in use
   - Solution: Check if files are locked by another process

4. **Early Exit**
   - Error in first directory might stop processing
   - Solution: Check logs for errors

### Debug Steps:

1. Run `convertify_debug.vbs` to see console output
2. Check `C:\services\logs\convertify.log` for detailed errors
3. Manually test second directory:
   ```bash
   cd C:\services
   .\convertify.exe convert --dir "Z:/8. Base Datos Unica"
   ```
4. Verify directory exists and has AVI files:
   ```bash
   dir "Z:\8. Base Datos Unica\*.avi"
   ```

---

## Switching Between Modes

**For Production (Silent):**
Use `convertify.vbs`

**For Debugging (Visible):**
Use `convertify_debug.vbs`

**To Make Production Visible Temporarily:**
Edit `convertify.vbs` and change:

```vbscript
objShell.Run "C:\services\convertify.exe convert --lab", 1, True
```

Then change back to `0, False` when done debugging.
