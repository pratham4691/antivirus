from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "hashlib", "logging", "json", "time", "threading", "requests", "watchdog", "flask", "numpy", "pandas", "joblib", "cryptography", "scikit-learn", "docker"],
    "excludes": [],
    "include_files": ["data/", "models/", "logs/", "templates/", "config.json"]
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="FuturisticAntivirus",
    version="1.0",
    description="Futuristic Antivirus System",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
