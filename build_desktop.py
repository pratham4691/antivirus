#!/usr/bin/env python3
"""
Build script for creating a standalone Windows executable of the Futuristic Antivirus System.
"""

import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """Build standalone executable using PyInstaller"""
    try:
        # Ensure we're in the project root
        project_root = Path(__file__).parent
        os.chdir(project_root)

        # Create build directory if it doesn't exist
        build_dir = project_root / "build"
        build_dir.mkdir(exist_ok=True)

        # Create dist directory if it doesn't exist
        dist_dir = project_root / "dist"
        dist_dir.mkdir(exist_ok=True)

        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--onefile",  # Single executable file
            "--windowed",  # No console window
            "--name=FuturisticAntivirus",
            "--icon=icon.ico",  # We'll create a default icon if it doesn't exist
            "--add-data=src;src",  # Include src directory
            "--add-data=data;data",  # Include data directory
            "--add-data=templates;templates",  # Include templates
            "--add-data=models;models",  # Include models
            "--hidden-import=psutil",
            "--hidden-import=watchdog",
            "--hidden-import=scikit-learn",
            "--hidden-import=flask",
            "--hidden-import=requests",
            "--hidden-import=joblib",
            "--hidden-import=cryptography",
            "--hidden-import=PyQt6",
            "--hidden-import=PyQt6.QtWidgets",
            "--hidden-import=PyQt6.QtCore",
            "--hidden-import=PyQt6.QtGui",
            "main.py"
        ]

        print("Building standalone executable...")
        print("Command:", " ".join(cmd))

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Build successful!")
            print(f"Executable created at: {dist_dir / 'FuturisticAntivirus.exe'}")

            # Create a simple installer script
            create_installer_script(dist_dir / "FuturisticAntivirus.exe")

        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

    except Exception as e:
        print(f"❌ Build error: {e}")

def create_installer_script(exe_path):
    """Create a simple installer script"""
    installer_script = f"""
@echo off
echo Installing Futuristic Antivirus System...
echo.

REM Create installation directory
if not exist "C:\\Program Files\\Futuristic Antivirus" mkdir "C:\\Program Files\\Futuristic Antivirus"

REM Copy executable
copy "{exe_path}" "C:\\Program Files\\Futuristic Antivirus\\FuturisticAntivirus.exe"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%USERPROFILE%\\Desktop\\Futuristic Antivirus.lnk');$s.TargetPath='C:\\Program Files\\Futuristic Antivirus\\FuturisticAntivirus.exe';$s.Save()"

REM Create Start Menu shortcut
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Futuristic Antivirus" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Futuristic Antivirus"
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Futuristic Antivirus\\Futuristic Antivirus.lnk');$s.TargetPath='C:\\Program Files\\Futuristic Antivirus\\FuturisticAntivirus.exe';$s.Save()"

echo.
echo Installation complete!
echo Desktop shortcut created.
echo Start Menu entry created.
echo.
echo Press any key to exit...
pause >nul
"""

    installer_path = exe_path.parent / "install.bat"
    with open(installer_path, 'w') as f:
        f.write(installer_script)

    print(f"✅ Installer script created at: {installer_path}")

def create_default_icon():
    """Create a default icon if none exists"""
    # This is a simple placeholder - in a real application you'd use a proper icon
    pass

if __name__ == "__main__":
    print("Futuristic Antivirus System - Windows Build Script")
    print("=" * 50)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Check if PyQt6 is installed
    try:
        import PyQt6
        print("✅ PyQt6 found")
    except ImportError:
        print("❌ PyQt6 not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)

    # Build the executable
    build_exe()

    print("\nBuild process complete!")
    print("Run 'dist\\install.bat' to install the application.")
