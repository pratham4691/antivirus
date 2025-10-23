Set sh = CreateObject("WScript.Shell")
Set lnk = sh.CreateShortcut("C:\Users\PRO\Desktop\Futuristic Antivirus.lnk")
WScript.Echo lnk.TargetPath
WScript.Echo lnk.Arguments
