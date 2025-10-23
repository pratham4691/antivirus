@echo off
echo ============================================
echo Futuristic Antivirus System - Windows Installer
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing required Python packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Futuristic Antivirus.lnk'); $Shortcut.TargetPath = '%~dp0run_antivirus.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,4'; $Shortcut.Save()"

REM Create start menu entry
echo Creating Start Menu entry...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Futuristic Antivirus" (
    mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Futuristic Antivirus"
)
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Futuristic Antivirus\Futuristic Antivirus.lnk'); $Shortcut.TargetPath = '%~dp0run_antivirus.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,4'; $Shortcut.Save()"

REM Create additional shortcuts for different modes
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Futuristic Antivirus\GUI Mode.lnk'); $Shortcut.TargetPath = '%~dp0run_antivirus.bat'; $Shortcut.Arguments = '--gui'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,13'; $Shortcut.Save()"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Futuristic Antivirus\Monitor Mode.lnk'); $Shortcut.TargetPath = '%~dp0run_antivirus.bat'; $Shortcut.Arguments = '--monitor \"%USERPROFILE%\Desktop\"'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'shell32.dll,22'; $Shortcut.Save()"

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo Shortcuts created:
echo - Desktop: Futuristic Antivirus
echo - Start Menu: Futuristic Antivirus (with sub-options)
echo.
echo You can now run the antivirus using:
echo - The desktop shortcut
echo - Start Menu shortcuts
echo - Command line: run_antivirus.bat [options]
echo.
echo Available options:
echo   --scan PATH    : Scan a specific file or directory
echo   --monitor PATH : Start real-time monitoring
echo   --gui          : Start web-based GUI
echo   --help         : Show help
echo.
pause
