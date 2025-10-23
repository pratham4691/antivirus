#!/usr/bin/env python3
"""
Simple Desktop Application for Futuristic Antivirus System
A minimal desktop GUI using tkinter for better compatibility.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import time
import psutil
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from src.antivirus import AntivirusEngine
    AV_AVAILABLE = True
except ImportError:
    AV_AVAILABLE = False
    print("Warning: Antivirus engine not available")

class SimpleAntivirusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Futuristic Antivirus System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')

        # Initialize antivirus engine
        self.av_engine = AntivirusEngine() if AV_AVAILABLE else None

        # System monitoring variables
        self.cpu_var = tk.StringVar(value="--%")
        self.mem_var = tk.StringVar(value="--%")
        self.disk_var = tk.StringVar(value="--%")
        self.uptime_var = tk.StringVar(value="-- hours")

        # Threat variables
        self.quarantined_var = tk.StringVar(value="--")
        self.scans_var = tk.StringVar(value="--")
        self.threats_var = tk.StringVar(value="--")
        self.threat_level_var = tk.StringVar(value="LOW")

        self.create_widgets()
        self.start_monitoring()

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg='#667eea', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🛡️ Futuristic Antivirus System",
                              font=('Arial', 24, 'bold'), bg='#667eea', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        status_label = tk.Label(header_frame, text="System Protected",
                               font=('Arial', 16, 'bold'), bg='#667eea', fg='#4CAF50')
        status_label.pack(side=tk.RIGHT, padx=20, pady=20)

        # Content area
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_frame = tk.Frame(content_frame, bg='#1a1a2e', width=600)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # System Performance Card
        self.create_system_card(left_frame)

        # Threat Overview Card
        self.create_threat_card(left_frame)

        # Activity Timeline Card
        self.create_activity_card(left_frame)

        # Right panel
        right_frame = tk.Frame(content_frame, bg='#1a1a2e')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scan Card
        self.create_scan_card(right_frame)

        # Logs Card
        self.create_logs_card(right_frame)

    def create_system_card(self, parent):
        card = tk.LabelFrame(parent, text="System Performance", bg='#2a2a4e', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', bd=2)
        card.pack(fill=tk.X, pady=(0, 20), padx=10)

        # CPU
        cpu_frame = tk.Frame(card, bg='#2a2a4e')
        cpu_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(cpu_frame, text="CPU Usage:", bg='#2a2a4e', fg='white').pack(side=tk.LEFT)
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(cpu_frame, textvariable=self.cpu_var, fg='#667eea', bg='#2a2a4e',
                font=('Arial', 14, 'bold')).pack(side=tk.RIGHT)

        # Memory
        mem_frame = tk.Frame(card, bg='#2a2a4e')
        mem_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(mem_frame, text="Memory Usage:", bg='#2a2a4e', fg='white').pack(side=tk.LEFT)
        self.mem_progress = ttk.Progressbar(mem_frame, length=200, mode='determinate')
        self.mem_progress.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(mem_frame, textvariable=self.mem_var, fg='#764ba2', bg='#2a2a4e',
                font=('Arial', 14, 'bold')).pack(side=tk.RIGHT)

        # Disk
        disk_frame = tk.Frame(card, bg='#2a2a4e')
        disk_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(disk_frame, text="Disk Usage:", bg='#2a2a4e', fg='white').pack(side=tk.LEFT)
        self.disk_progress = ttk.Progressbar(disk_frame, length=200, mode='determinate')
        self.disk_progress.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(disk_frame, textvariable=self.disk_var, fg='#f093fb', bg='#2a2a4e',
                font=('Arial', 14, 'bold')).pack(side=tk.RIGHT)

        # Uptime
        uptime_frame = tk.Frame(card, bg='#2a2a4e')
        uptime_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(uptime_frame, text="System Uptime:", bg='#2a2a4e', fg='white').pack(side=tk.LEFT)
        tk.Label(uptime_frame, textvariable=self.uptime_var, fg='white', bg='#2a2a4e',
                font=('Arial', 14, 'bold')).pack(side=tk.RIGHT)

    def create_threat_card(self, parent):
        card = tk.LabelFrame(parent, text="Threat Overview", bg='#2a2a4e', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', bd=2)
        card.pack(fill=tk.X, pady=(0, 20), padx=10)

        # Grid layout for threat stats
        grid_frame = tk.Frame(card, bg='#2a2a4e')
        grid_frame.pack(fill=tk.X, padx=20, pady=10)

        # Row 1: Quarantined Files
        tk.Label(grid_frame, text="Quarantined Files:", bg='#2a2a4e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        tk.Label(grid_frame, textvariable=self.quarantined_var, fg='#ff6b6b', bg='#2a2a4e',
                font=('Arial', 18, 'bold')).grid(row=0, column=1, sticky='e', pady=5)

        # Row 2: Recent Scans
        tk.Label(grid_frame, text="Recent Scans:", bg='#2a2a4e', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        tk.Label(grid_frame, textvariable=self.scans_var, fg='#4CAF50', bg='#2a2a4e',
                font=('Arial', 18, 'bold')).grid(row=1, column=1, sticky='e', pady=5)

        # Row 3: Recent Threats
        tk.Label(grid_frame, text="Recent Threats:", bg='#2a2a4e', fg='white').grid(row=2, column=0, sticky='w', pady=5)
        tk.Label(grid_frame, textvariable=self.threats_var, fg='#FF9800', bg='#2a2a4e',
                font=('Arial', 18, 'bold')).grid(row=2, column=1, sticky='e', pady=5)

        # Row 4: Threat Level
        tk.Label(grid_frame, text="Threat Level:", bg='#2a2a4e', fg='white').grid(row=3, column=0, sticky='w', pady=5)
        threat_level_label = tk.Label(grid_frame, textvariable=self.threat_level_var, bg='#4CAF50',
                                    fg='white', font=('Arial', 18, 'bold'), padx=15, pady=5)
        threat_level_label.grid(row=3, column=1, sticky='e', pady=5)

    def create_activity_card(self, parent):
        card = tk.LabelFrame(parent, text="Activity Timeline", bg='#2a2a4e', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', bd=2)
        card.pack(fill=tk.BOTH, expand=True, padx=10)

        # Activity list
        self.activity_listbox = tk.Listbox(card, bg='#3a3a5e', fg='white', selectbackground='#667eea',
                                         font=('Consolas', 10), relief='flat', bd=0)
        scrollbar = tk.Scrollbar(card, orient=tk.VERTICAL, command=self.activity_listbox.yview)
        self.activity_listbox.configure(yscrollcommand=scrollbar.set)

        self.activity_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Add sample activities
        activities = [
            "2 hours ago - Scheduled scan completed (0 threats)",
            "4 hours ago - File quarantined: test_malware.txt",
            "6 hours ago - Real-time monitoring started",
            "1 day ago - Signatures updated (150 new)",
            "2 days ago - System scan completed (1 threat found)"
        ]
        for activity in activities:
            self.activity_listbox.insert(tk.END, activity)

    def create_scan_card(self, parent):
        card = tk.LabelFrame(parent, text="Quick Scan", bg='#2a2a4e', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', bd=2)
        card.pack(fill=tk.X, pady=(0, 20))

        # Path input
        path_frame = tk.Frame(card, bg='#2a2a4e')
        path_frame.pack(fill=tk.X, padx=20, pady=10)
        tk.Label(path_frame, text="Scan Path:", bg='#2a2a4e', fg='white').pack(side=tk.LEFT)
        self.scan_path_var = tk.StringVar()
        self.scan_path_entry = tk.Entry(path_frame, textvariable=self.scan_path_var, bg='#4a4a6e', fg='white',
                                      insertbackground='white', relief='flat', bd=2)
        self.scan_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        tk.Button(path_frame, text="Browse", command=self.browse_path, bg='#667eea', fg='white',
                 relief='flat', bd=0, padx=15).pack(side=tk.RIGHT)

        # Scan button
        self.scan_button = tk.Button(card, text="🔍 Start Scan", command=self.start_scan,
                                   bg='#667eea', fg='white', font=('Arial', 12, 'bold'),
                                   relief='flat', bd=0, padx=20, pady=10)
        self.scan_button.pack(pady=10)

        # Progress
        self.scan_progress_var = tk.StringVar(value="Ready to scan")
        tk.Label(card, textvariable=self.scan_progress_var, bg='#2a2a4e', fg='#ccc').pack(pady=(0, 10))

        # Results
        results_frame = tk.Frame(card, bg='#2a2a4e')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.scan_results = scrolledtext.ScrolledText(results_frame, bg='#3a3a5e', fg='white',
                                                    insertbackground='white', relief='flat', bd=0,
                                                    font=('Consolas', 10), height=8)
        self.scan_results.pack(fill=tk.BOTH, expand=True)

    def create_logs_card(self, parent):
        card = tk.LabelFrame(parent, text="Recent Logs", bg='#2a2a4e', fg='white',
                           font=('Arial', 12, 'bold'), relief='flat', bd=2)
        card.pack(fill=tk.BOTH, expand=True)

        # Refresh button
        tk.Button(card, text="🔄 Refresh Logs", command=self.load_logs,
                 bg='#667eea', fg='white', relief='flat', bd=0, padx=15, pady=5).pack(pady=10)

        # Logs text
        self.logs_text = scrolledtext.ScrolledText(card, bg='#3a3a5e', fg='white',
                                                 insertbackground='white', relief='flat', bd=0,
                                                 font=('Consolas', 9))
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.load_logs()

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.scan_path_var.set(path)

    def start_scan(self):
        path = self.scan_path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please enter a path to scan")
            return

        if not os.path.exists(path):
            messagebox.showerror("Error", "Path does not exist")
            return

        if not AV_AVAILABLE or not self.av_engine:
            messagebox.showerror("Error", "Antivirus engine not available")
            return

        self.scan_button.config(state='disabled', text='🔄 Scanning...')
        self.scan_progress_var.set("Initializing scan...")
        self.scan_results.delete(1.0, tk.END)

        # Start scan in separate thread
        scan_thread = threading.Thread(target=self.perform_scan, args=(path,))
        scan_thread.daemon = True
        scan_thread.start()

    def perform_scan(self, path):
        try:
            self.scan_progress_var.set("Starting scan...")
            infected = self.av_engine.run_scan(path)
            self.scan_progress_var.set(f"Scan completed. Found {len(infected)} threats.")

            if infected:
                result_text = f"Scan completed. Found {len(infected)} infected file(s):\n\n"
                for file in infected:
                    result_text += f"⚠️  {file}\n"
            else:
                result_text = "✅ Scan completed. No threats found."

            self.scan_results.insert(tk.END, result_text)
        except Exception as e:
            self.scan_results.insert(tk.END, f"Scan error: {str(e)}")
        finally:
            self.scan_button.config(state='normal', text='🔍 Start Scan')

    def load_logs(self):
        log_file = 'logs/antivirus.log'
        self.logs_text.delete(1.0, tk.END)

        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = f.readlines()
                self.logs_text.insert(tk.END, ''.join(logs[-50:]))
            except Exception as e:
                self.logs_text.insert(tk.END, f"Error loading logs: {e}")
        else:
            self.logs_text.insert(tk.END, "No log file found")

    def start_monitoring(self):
        # Start system monitoring thread
        monitor_thread = threading.Thread(target=self.system_monitor_loop, daemon=True)
        monitor_thread.start()

        # Start threat monitoring thread
        threat_thread = threading.Thread(target=self.threat_monitor_loop, daemon=True)
        threat_thread.start()

    def system_monitor_loop(self):
        while True:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                self.cpu_var.set(f"{cpu_percent}%")
                self.mem_var.set(f"{memory.percent}%")
                self.disk_var.set(f"{disk.percent}%")
                self.uptime_var.set(f"{int(time.time() - psutil.boot_time()) // 3600} hours")

                self.cpu_progress['value'] = cpu_percent
                self.mem_progress['value'] = memory.percent
                self.disk_progress['value'] = disk.percent

            except Exception as e:
                print(f"System monitoring error: {e}")
            time.sleep(30)

    def threat_monitor_loop(self):
        while True:
            try:
                quarantine_dir = 'quarantine'
                quarantined_count = len(os.listdir(quarantine_dir)) if os.path.exists(quarantine_dir) else 0

                log_file = 'logs/antivirus.log'
                recent_scans = 0
                recent_threats = 0

                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        logs = f.readlines()
                        for log in logs[-100:]:
                            if 'Scan completed' in log:
                                recent_scans += 1
                            if 'Threat detected' in log:
                                recent_threats += 1

                self.quarantined_var.set(str(quarantined_count))
                self.scans_var.set(str(recent_scans))
                self.threats_var.set(str(recent_threats))

                threat_level = 'Low' if recent_threats < 5 else 'Medium' if recent_threats < 15 else 'High'
                self.threat_level_var.set(threat_level.upper())

            except Exception as e:
                print(f"Threat monitoring error: {e}")
            time.sleep(60)

def main():
    root = tk.Tk()
    app = SimpleAntivirusGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
