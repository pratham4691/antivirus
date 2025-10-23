#!/usr/bin/env python3
"""
Futuristic Antivirus System - Desktop GUI Application
A standalone Windows desktop application with modern UI.
"""

import sys
import os
import psutil
import time
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QTextEdit, QListWidget,
    QGridLayout, QFrame, QScrollArea, QGroupBox, QSplitter,
    QSystemTrayIcon, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QPainter, QLinearGradient
from .antivirus import AntivirusEngine

class SystemMonitorThread(QThread):
    stats_updated = pyqtSignal(dict)

    def run(self):
        while True:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')

                stats = {
                    'cpu_usage': cpu_percent,
                    'memory_usage': memory.percent,
                    'memory_used': round(memory.used / (1024**3), 2),
                    'memory_total': round(memory.total / (1024**3), 2),
                    'disk_usage': disk.percent,
                    'disk_used': round(disk.used / (1024**3), 2),
                    'disk_total': round(disk.total / (1024**3), 2),
                    'uptime': int(time.time() - psutil.boot_time())
                }
                self.stats_updated.emit(stats)
                self.sleep(30)  # Update every 30 seconds
            except Exception as e:
                print(f"System monitoring error: {e}")
                self.sleep(30)

class ThreatStatsThread(QThread):
    stats_updated = pyqtSignal(dict)

    def run(self):
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

                stats = {
                    'total_quarantined': quarantined_count,
                    'recent_scans': recent_scans,
                    'recent_threats': recent_threats,
                    'threat_level': 'Low' if recent_threats < 5 else 'Medium' if recent_threats < 15 else 'High'
                }
                self.stats_updated.emit(stats)
                self.sleep(60)  # Update every minute
            except Exception as e:
                print(f"Threat stats error: {e}")
                self.sleep(60)

class ScanWorker(QThread):
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)

    def __init__(self, path, av_engine):
        super().__init__()
        self.path = path
        self.av_engine = av_engine

    def run(self):
        try:
            self.progress.emit("Starting scan...")
            infected = self.av_engine.run_scan(self.path)
            self.progress.emit(f"Scan completed. Found {len(infected)} threats.")
            self.finished.emit(infected)
        except Exception as e:
            self.progress.emit(f"Scan error: {str(e)}")
            self.finished.emit([])

class ModernCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)

        # Modern styling
        self.setStyleSheet("""
            ModernCard {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 5px;
            }
        """)

        layout = QVBoxLayout(self)
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #fff;
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #667eea;
                }
            """)
            layout.addWidget(title_label)

class FuturisticAntivirusGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.av_engine = AntivirusEngine()
        self.system_monitor = SystemMonitorThread()
        self.threat_monitor = ThreatStatsThread()
        self.scan_worker = None

        self.init_ui()
        self.setup_system_tray()
        self.start_monitoring()

    def init_ui(self):
        self.setWindowTitle("Futuristic Antivirus System")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0c0c0c, stop:0.5 #1a1a2e, stop:1 #16213e);
                color: #e0e0e0;
            }
        """)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - System Stats & Threat Overview
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)

        # Right panel - Activity & Controls
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)

        content_splitter.setSizes([700, 700])
        main_layout.addWidget(content_splitter)

        # Status bar
        self.statusBar().showMessage("Ready")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: rgba(255, 255, 255, 0.05);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: #e0e0e0;
            }
        """)

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 20px;
                margin: 10px;
                padding: 20px;
            }
        """)
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)

        title = QLabel("🛡️ Futuristic Antivirus System")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                text-shadow: 0 0 20px rgba(255,255,255,0.5);
            }
        """)
        layout.addWidget(title)

        layout.addStretch()

        status_label = QLabel("System Protected")
        status_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(status_label)

        return header

    def create_left_panel(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        container = QWidget()
        layout = QVBoxLayout(container)

        # System Performance Card
        system_card = ModernCard("System Performance")
        self.create_system_stats(system_card)
        layout.addWidget(system_card)

        # Threat Overview Card
        threat_card = ModernCard("Threat Overview")
        self.create_threat_overview(threat_card)
        layout.addWidget(threat_card)

        # Activity Timeline Card
        activity_card = ModernCard("Activity Timeline")
        self.create_activity_timeline(activity_card)
        layout.addWidget(activity_card)

        layout.addStretch()
        scroll_area.setWidget(container)
        return scroll_area

    def create_right_panel(self):
        container = QWidget()
        layout = QVBoxLayout(container)

        # Quick Scan Card
        scan_card = ModernCard("Quick Scan")
        self.create_scan_interface(scan_card)
        layout.addWidget(scan_card)

        # Logs Card
        logs_card = ModernCard("Recent Logs")
        self.create_logs_interface(logs_card)
        layout.addWidget(logs_card)

        # Quarantine Card
        quarantine_card = ModernCard("Quarantine")
        self.create_quarantine_interface(quarantine_card)
        layout.addWidget(quarantine_card)

        return container

    def create_system_stats(self, parent):
        grid = QGridLayout()

        # CPU
        cpu_label = QLabel("CPU Usage")
        cpu_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setStyleSheet(self.get_progress_style("#667eea"))
        self.cpu_value = QLabel("--%")
        self.cpu_value.setStyleSheet("color: #667eea; font-size: 18px; font-weight: bold;")

        # Memory
        mem_label = QLabel("Memory Usage")
        mem_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self.mem_progress = QProgressBar()
        self.mem_progress.setStyleSheet(self.get_progress_style("#764ba2"))
        self.mem_value = QLabel("--%")
        self.mem_value.setStyleSheet("color: #764ba2; font-size: 18px; font-weight: bold;")

        # Disk
        disk_label = QLabel("Disk Usage")
        disk_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self.disk_progress = QProgressBar()
        self.disk_progress.setStyleSheet(self.get_progress_style("#f093fb"))
        self.disk_value = QLabel("--%")
        self.disk_value.setStyleSheet("color: #f093fb; font-size: 18px; font-weight: bold;")

        # Uptime
        uptime_label = QLabel("System Uptime")
        uptime_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self.uptime_value = QLabel("-- hours")
        self.uptime_value.setStyleSheet("color: #e0e0e0; font-size: 18px; font-weight: bold;")

        grid.addWidget(cpu_label, 0, 0)
        grid.addWidget(self.cpu_progress, 0, 1)
        grid.addWidget(self.cpu_value, 0, 2)

        grid.addWidget(mem_label, 1, 0)
        grid.addWidget(self.mem_progress, 1, 1)
        grid.addWidget(self.mem_value, 1, 2)

        grid.addWidget(disk_label, 2, 0)
        grid.addWidget(self.disk_progress, 2, 1)
        grid.addWidget(self.disk_value, 2, 2)

        grid.addWidget(uptime_label, 3, 0)
        grid.addWidget(self.uptime_value, 3, 1, 1, 2)

        parent.layout().addLayout(grid)

    def create_threat_overview(self, parent):
        grid = QGridLayout()

        # Threat stats
        quarantined_label = QLabel("Quarantined Files")
        quarantined_label.setStyleSheet("color: #ccc;")
        self.quarantined_value = QLabel("--")
        self.quarantined_value.setStyleSheet("color: #ff6b6b; font-size: 24px; font-weight: bold;")

        scans_label = QLabel("Recent Scans")
        scans_label.setStyleSheet("color: #ccc;")
        self.scans_value = QLabel("--")
        self.scans_value.setStyleSheet("color: #4CAF50; font-size: 24px; font-weight: bold;")

        threats_label = QLabel("Recent Threats")
        threats_label.setStyleSheet("color: #ccc;")
        self.threats_value = QLabel("--")
        self.threats_value.setStyleSheet("color: #FF9800; font-size: 24px; font-weight: bold;")

        level_label = QLabel("Threat Level")
        level_label.setStyleSheet("color: #ccc;")
        self.threat_level = QLabel("LOW")
        self.threat_level.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 24px;
                font-weight: bold;
                padding: 5px 15px;
                border-radius: 15px;
                background: rgba(76, 175, 80, 0.2);
            }
        """)

        grid.addWidget(quarantined_label, 0, 0)
        grid.addWidget(self.quarantined_value, 0, 1)
        grid.addWidget(scans_label, 1, 0)
        grid.addWidget(self.scans_value, 1, 1)
        grid.addWidget(threats_label, 2, 0)
        grid.addWidget(self.threats_value, 2, 1)
        grid.addWidget(level_label, 3, 0)
        grid.addWidget(self.threat_level, 3, 1)

        parent.layout().addLayout(grid)

    def create_activity_timeline(self, parent):
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #e0e0e0;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.02);
                margin: 2px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.08);
            }
        """)

        # Add sample activities
        activities = [
            "2 hours ago - Scheduled scan completed (0 threats)",
            "4 hours ago - File quarantined: test_malware.txt",
            "6 hours ago - Real-time monitoring started",
            "1 day ago - Signatures updated (150 new)",
            "2 days ago - System scan completed (1 threat found)"
        ]

        for activity in activities:
            self.activity_list.addItem(activity)

        parent.layout().addWidget(self.activity_list)

    def create_scan_interface(self, parent):
        layout = QVBoxLayout()

        # Path input
        from PyQt6.QtWidgets import QLineEdit
        self.scan_path = QLineEdit()
        self.scan_path.setPlaceholderText("Enter path to scan (e.g., C:\\Users\\...)")
        self.scan_path.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
            }
        """)
        layout.addWidget(self.scan_path)

        # Scan button
        self.scan_button = QPushButton("🔍 Start Scan")
        self.scan_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a6fd8, stop:1 #6a4191);
            }
            QPushButton:pressed {
                transform: translateY(2px);
            }
        """)
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        # Progress and results
        self.scan_progress = QLabel("Ready to scan")
        self.scan_progress.setStyleSheet("color: #ccc; margin: 10px 0;")
        layout.addWidget(self.scan_progress)

        self.scan_results = QTextEdit()
        self.scan_results.setReadOnly(True)
        self.scan_results.setMaximumHeight(150)
        self.scan_results.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #e0e0e0;
                padding: 10px;
            }
        """)
        layout.addWidget(self.scan_results)

        parent.layout().addLayout(layout)

    def create_logs_interface(self, parent):
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #e0e0e0;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
        """)

        refresh_btn = QPushButton("🔄 Refresh Logs")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        refresh_btn.clicked.connect(self.load_logs)

        parent.layout().addWidget(refresh_btn)
        parent.layout().addWidget(self.logs_text)
        self.load_logs()

    def create_quarantine_interface(self, parent):
        self.quarantine_list = QListWidget()
        self.quarantine_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #e0e0e0;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.02);
                margin: 2px;
                border-radius: 5px;
            }
        """)

        refresh_btn = QPushButton("🔄 Refresh Quarantine")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        refresh_btn.clicked.connect(self.load_quarantine)

        parent.layout().addWidget(refresh_btn)
        parent.layout().addWidget(self.quarantine_list)
        self.load_quarantine()

    def get_progress_style(self, color):
        return f"""
            QProgressBar {{
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                text-align: center;
                background: rgba(255, 255, 255, 0.05);
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 4px;
            }}
        """

    def setup_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        hide_action = tray_menu.addAction("Hide")
        hide_action.triggered.connect(self.hide)
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def start_monitoring(self):
        self.system_monitor.stats_updated.connect(self.update_system_stats)
        self.system_monitor.start()

        self.threat_monitor.stats_updated.connect(self.update_threat_stats)
        self.threat_monitor.start()

    def update_system_stats(self, stats):
        self.cpu_value.setText(f"{stats['cpu_usage']}%")
        self.cpu_progress.setValue(int(stats['cpu_usage']))

        self.mem_value.setText(f"{stats['memory_usage']}%")
        self.mem_progress.setValue(int(stats['memory_usage']))

        self.disk_value.setText(f"{stats['disk_usage']}%")
        self.disk_progress.setValue(int(stats['disk_usage']))

        self.uptime_value.setText(f"{stats['uptime'] // 3600} hours")

    def update_threat_stats(self, stats):
        self.quarantined_value.setText(str(stats['total_quarantined']))
        self.scans_value.setText(str(stats['recent_scans']))
        self.threats_value.setText(str(stats['recent_threats']))

        level = stats['threat_level']
        self.threat_level.setText(level.upper())

        # Update threat level styling
        if level == 'Low':
            self.threat_level.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 15px;
                    background: rgba(76, 175, 80, 0.2);
                }
            """)
        elif level == 'Medium':
            self.threat_level.setStyleSheet("""
                QLabel {
                    color: #FF9800;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 15px;
                    background: rgba(255, 152, 0, 0.2);
                }
            """)
        else:  # High
            self.threat_level.setStyleSheet("""
                QLabel {
                    color: #F44336;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 15px;
                    background: rgba(244, 67, 54, 0.2);
                }
            """)

    def start_scan(self):
        path = self.scan_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Error", "Please enter a path to scan")
            return

        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Path does not exist")
            return

        self.scan_button.setEnabled(False)
        self.scan_button.setText("🔄 Scanning...")
        self.scan_progress.setText("Initializing scan...")
        self.scan_results.clear()

        self.scan_worker = ScanWorker(path, self.av_engine)
        self.scan_worker.progress.connect(self.scan_progress.setText)
        self.scan_worker.finished.connect(self.scan_finished)
        self.scan_worker.start()

    def scan_finished(self, infected_files):
        self.scan_button.setEnabled(True)
        self.scan_button.setText("🔍 Start Scan")

        if infected_files:
            result_text = f"Scan completed. Found {len(infected_files)} infected file(s):\n\n"
            for file in infected_files:
                result_text += f"⚠️  {file}\n"
        else:
            result_text = "✅ Scan completed. No threats found."

        self.scan_results.setText(result_text)
        self.statusBar().showMessage(f"Scan completed: {len(infected_files)} threats found")

    def load_logs(self):
        log_file = 'logs/antivirus.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = f.readlines()
            self.logs_text.setText(''.join(logs[-50:]))
        else:
            self.logs_text.setText("No log file found")

    def load_quarantine(self):
        quarantine_dir = 'quarantine'
        self.quarantine_list.clear()

        if os.path.exists(quarantine_dir):
            files = os.listdir(quarantine_dir)
            if files:
                for file in files:
                    self.quarantine_list.addItem(f"🗂️  {file}")
            else:
                self.quarantine_list.addItem("No quarantined files")
        else:
            self.quarantine_list.addItem("Quarantine directory not found")

    def closeEvent(self, event):
        # Hide to tray instead of closing
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Futuristic Antivirus",
            "Application minimized to system tray",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Dark theme palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(12, 12, 12))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.Base, QColor(26, 26, 46))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(22, 33, 62))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.Text, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.Button, QColor(26, 26, 46))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(224, 224, 224))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(102, 126, 234))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(102, 126, 234))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    window = FuturisticAntivirusGUI()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
