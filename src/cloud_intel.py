import requests
import json
import logging
from datetime import datetime, timedelta

class CloudThreatIntel:
    def __init__(self, api_url='https://api.threatintel.example.com', api_key='your_api_key'):
        self.api_url = api_url
        self.api_key = api_key
        self.threats = set()
        self.last_update = None

    def fetch_threats(self):
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(f"{self.api_url}/threats", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.threats = set(data.get('threats', []))
                self.last_update = datetime.now()
                logging.info(f"Fetched {len(self.threats)} threats from cloud")
                return True
            else:
                logging.error(f"Failed to fetch threats: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Error fetching threats: {e}")
            return False

    def is_threat(self, hash_value):
        if not self.threats:
            self.fetch_threats()
        return hash_value in self.threats

    def report_threat(self, hash_value, details):
        try:
            headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
            payload = {
                'hash': hash_value,
                'details': details,
                'timestamp': datetime.now().isoformat()
            }
            response = requests.post(f"{self.api_url}/report", json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                logging.info(f"Reported threat: {hash_value}")
                return True
            else:
                logging.error(f"Failed to report threat: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Error reporting threat: {e}")
            return False

    def get_global_stats(self):
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get(f"{self.api_url}/stats", headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to get stats: {response.status_code}")
                return {}
        except Exception as e:
            logging.error(f"Error getting stats: {e}")
            return {}

if __name__ == "__main__":
    # Mock usage
    intel = CloudThreatIntel()
    intel.fetch_threats()
    print(f"Threats loaded: {len(intel.threats)}")
