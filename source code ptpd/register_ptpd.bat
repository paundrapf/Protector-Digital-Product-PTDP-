@echo off
REM register_ptpd.bat
REM Windows Registry Script untuk associate .ptpd files
REM Run as Administrator!

echo.
echo ========================================
echo  PTPD File Association Registration
echo ========================================
echo.
echo This will register .ptpd file extension
echo with PTPD Viewer on your system.
echo.
echo Press Ctrl+C to cancel or
pause

REM Get current directory
set "APP_PATH=%~dp0PTPD-Viewer.exe"

echo.
echo Installing file association...
echo.

REM Create file association
reg add "HKEY_CLASSES_ROOT\.ptpd" /ve /d "PTPDFile" /f
reg add "HKEY_CLASSES_ROOT\.ptpd" /v "Content Type" /d "application/x-ptpd" /f

REM Set default icon
reg add "HKEY_CLASSES_ROOT\PTPDFile\DefaultIcon" /ve /d "\"%APP_PATH%\",0" /f

REM Set description
reg add "HKEY_CLASSES_ROOT\PTPDFile" /ve /d "Protected Digital Product File" /f

REM Set friendly name
reg add "HKEY_CLASSES_ROOT\PTPDFile" /v "FriendlyTypeName" /d "PTPD Protected File" /f

REM Set open command
reg add "HKEY_CLASSES_ROOT\PTPDFile\shell\open\command" /ve /d "\"\"%APP_PATH%\"\" \"\"%%1\"\"" /f

echo.
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo You can now double-click .ptpd files
echo to open them with PTPD Viewer.
echo.
pause
