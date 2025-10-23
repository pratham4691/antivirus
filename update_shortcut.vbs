Set sh = CreateObject("WScript.Shell")
Set lnk = sh.CreateShortcut("C:\Users\PRO\Desktop\Futuristic Antivirus.lnk")
lnk.TargetPath = "C:\Users\PRO\AppData\Local\Programs\Python\Python314\python.exe"
lnk.Arguments = "C:\Users\PRO\Desktop\skanda_a\main.py"
lnk.Save()
