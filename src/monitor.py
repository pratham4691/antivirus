import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .antivirus import AntivirusEngine

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, av_engine):
        self.av_engine = av_engine

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"New file detected: {event.src_path}")
            if self.av_engine.scan_file(event.src_path):
                logging.warning(f"Threat detected in new file: {event.src_path}")
                # Could add alert/notification here

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            # Optional: re-scan modified files

class RealTimeMonitor:
    def __init__(self, paths_to_monitor):
        self.paths = paths_to_monitor
        self.av_engine = AntivirusEngine()
        self.observer = Observer()

    def start_monitoring(self):
        event_handler = FileMonitorHandler(self.av_engine)
        for path in self.paths:
            self.observer.schedule(event_handler, path, recursive=True)
            logging.info(f"Monitoring started for: {path}")

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    # Example usage
    monitor = RealTimeMonitor(["C:\\Users\\PRO\\Desktop\\test_folder"])  # Replace with actual paths
    monitor.start_monitoring()
