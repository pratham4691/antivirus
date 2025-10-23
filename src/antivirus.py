import os
import hashlib
import logging
import shutil
from datetime import datetime
from src.ml_model import AIModel
from src.cloud_intel import CloudThreatIntel
from src.sandbox import Sandbox

class AntivirusEngine:
    def __init__(self, signatures_file='data/signatures.txt', quarantine_dir='quarantine', log_file='logs/antivirus.log'):
        self.signatures_file = signatures_file
        self.quarantine_dir = quarantine_dir
        self.log_file = log_file
        self.signatures = self.load_signatures()
        self.setup_logging()
        self.ai_model = AIModel()
        self.cloud_intel = CloudThreatIntel()
        self.sandbox = Sandbox()

        if not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_signatures(self):
        signatures = set()
        if os.path.exists(self.signatures_file):
            with open(self.signatures_file, 'r') as f:
                for line in f:
                    signatures.add(line.strip())
        return signatures

    def compute_md5(self, file_path):
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error computing MD5 for {file_path}: {e}")
            return None

    def heuristic_check(self, file_path):
        # Basic heuristic: check for suspicious file extensions or patterns
        suspicious_extensions = ['.exe', '.bat', '.scr', '.pif', '.com']
        if any(file_path.lower().endswith(ext) for ext in suspicious_extensions):
            return True
        return False

    def scan_file(self, file_path):
        if not os.path.isfile(file_path):
            return False

        md5_hash = self.compute_md5(file_path)
        if md5_hash and md5_hash in self.signatures:
            logging.warning(f"Malware detected: {file_path} (MD5: {md5_hash})")
            return True

        # Cloud threat intelligence check
        if md5_hash and self.cloud_intel.is_threat(md5_hash):
            logging.warning(f"Cloud threat detected: {file_path} (MD5: {md5_hash})")
            return True

        if self.heuristic_check(file_path):
            logging.warning(f"Suspicious file detected: {file_path}")
            return True

        # AI anomaly detection
        if self.ai_model.predict_anomaly(file_path):
            logging.warning(f"Anomalous file detected by AI: {file_path}")
            return True

        # Advanced sandboxing for suspicious files
        if self.heuristic_check(file_path) or self.ai_model.predict_anomaly(file_path):
            sandbox_results = self.sandbox.run_in_sandbox(file_path)
            if self.sandbox.analyze_behavior(sandbox_results):
                logging.warning(f"Malicious behavior detected in sandbox: {file_path}")
                return True

        return False

    def scan_directory(self, directory):
        infected_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.scan_file(file_path):
                    infected_files.append(file_path)
        return infected_files

    def quarantine_file(self, file_path):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            quarantined_path = os.path.join(self.quarantine_dir, f"{timestamp}_{filename}")
            shutil.move(file_path, quarantined_path)
            logging.info(f"Quarantined: {file_path} -> {quarantined_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to quarantine {file_path}: {e}")
            return False

    def run_scan(self, path):
        if os.path.isfile(path):
            infected = [path] if self.scan_file(path) else []
        elif os.path.isdir(path):
            infected = self.scan_directory(path)
        else:
            logging.error(f"Invalid path: {path}")
            return []

        for infected_file in infected:
            self.quarantine_file(infected_file)

        return infected

if __name__ == "__main__":
    av = AntivirusEngine()
    # Example usage
    infected = av.run_scan("C:\\Users\\PRO\\Desktop\\test_folder")  # Replace with actual path
    print(f"Scan complete. Infected files: {len(infected)}")
