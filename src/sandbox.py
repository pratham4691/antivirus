import docker
import os
import logging
import time
from datetime import datetime

class Sandbox:
    def __init__(self, image='ubuntu:20.04'):
        try:
            self.client = docker.from_env()
            self.image = image
            self.container = None
            print("Docker sandbox initialized successfully.")
        except Exception as e:
            print(f"Docker not available: {e}")
            print("Using mock sandbox mode. For full sandboxing, install Docker Desktop from https://www.docker.com/products/docker-desktop")
            print("Mock mode provides simulated analysis for demonstration purposes.")
            self.client = None

    def run_in_sandbox(self, file_path, timeout=30):
        if not os.path.isfile(file_path):
            return {"error": "File not found"}

        if self.client is None:
            # Mock sandbox when Docker is not available
            filename = os.path.basename(file_path)
            results = {
                'file': filename,
                'suspicious_activities': ['network_connection_attempt', 'file_modification'],
                'risk_score': 0.8,
                'timestamp': datetime.now().isoformat()
            }
            return results

        try:
            # Create a temporary directory for the file
            temp_dir = '/tmp/sandbox'
            os.makedirs(temp_dir, exist_ok=True)

            # Copy file to temp dir (in real implementation, use secure copy)
            filename = os.path.basename(file_path)
            temp_file = os.path.join(temp_dir, filename)

            # For demo, we'll simulate behavior analysis
            # In real implementation, mount the file and run it in container
            container = self.client.containers.run(
                self.image,
                command=['sleep', str(timeout)],
                volumes={temp_dir: {'bind': '/sandbox', 'mode': 'ro'}},
                detach=True,
                remove=True
            )

            # Simulate monitoring (in real impl, monitor syscalls, network, etc.)
            time.sleep(5)  # Simulate execution time

            # Mock analysis results
            results = {
                'file': filename,
                'suspicious_activities': ['network_connection_attempt', 'file_modification'],
                'risk_score': 0.8,
                'timestamp': datetime.now().isoformat()
            }

            container.stop()
            return results

        except Exception as e:
            logging.error(f"Sandbox execution failed: {e}")
            return {"error": str(e)}

    def analyze_behavior(self, results):
        # Analyze sandbox results for malicious behavior
        suspicious_patterns = [
            'network_connection_attempt',
            'registry_modification',
            'file_deletion',
            'process_injection'
        ]

        risk_score = results.get('risk_score', 0)
        activities = results.get('suspicious_activities', [])

        for activity in activities:
            if activity in suspicious_patterns:
                risk_score += 0.2

        return risk_score > 0.5  # Threshold for malicious

if __name__ == "__main__":
    sandbox = Sandbox()
    # Mock test
    results = sandbox.run_in_sandbox("dummy_file.exe")
    print(f"Sandbox results: {results}")
    malicious = sandbox.analyze_behavior(results)
    print(f"Malicious: {malicious}")
