@echo off
echo Creating desktop shortcut for Futuristic Antivirus...

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Futuristic Antivirus.lnk'); $Shortcut.TargetPath = 'python.exe'; $Shortcut.Arguments = 'simple_desktop.py'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'python.exe'; $Shortcut.Description = 'Futuristic Antivirus System - Desktop Application'; $Shortcut.Save()"

echo Desktop shortcut created successfully!
echo You can now double-click the "Futuristic Antivirus" shortcut on your desktop to launch the application.
pause
