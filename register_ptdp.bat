@echo off
REM register_ptdp.bat
REM Windows Registry Script untuk associate .ptdp files
REM Run as Administrator!

echo.
echo ========================================
echo  PTDP File Association Registration
echo ========================================
echo.
echo This will register .ptdp file extension
echo with PTDP Viewer on your system.
echo.
echo Press Ctrl+C to cancel or
pause

REM Get current directory
set "APP_PATH=%~dp0PTDP-Viewer.exe"

echo.
echo Installing file association...
echo.

REM Create file association
reg add "HKEY_CLASSES_ROOT\.ptdp" /ve /d "PTDPFile" /f
reg add "HKEY_CLASSES_ROOT\.ptdp" /v "Content Type" /d "application/x-ptdp" /f

REM Set default icon
reg add "HKEY_CLASSES_ROOT\PTDPFile\DefaultIcon" /ve /d "\"%APP_PATH%\",0" /f

REM Set description
reg add "HKEY_CLASSES_ROOT\PTDPFile" /ve /d "Protected Digital Product File" /f

REM Set friendly name
reg add "HKEY_CLASSES_ROOT\PTDPFile" /v "FriendlyTypeName" /d "PTDP Protected File" /f

REM Set open command
reg add "HKEY_CLASSES_ROOT\PTDPFile\shell\open\command" /ve /d "\"\"%APP_PATH%\"\" \"\"%%1\"\"" /f

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo You can now double-click .ptdp files
echo to open them with PTDP Viewer.
echo.
pause
