import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import hashlib

class AIModel:
    def __init__(self, model_path='models/anomaly_detector.pkl'):
        self.model_path = model_path
        self.model = None

    def extract_features(self, file_path):
        # Extract basic features from file
        features = {}
        try:
            stat = os.stat(file_path)
            features['size'] = stat.st_size
            features['modified_time'] = stat.st_mtime
            features['created_time'] = stat.st_ctime

            # Compute hash for uniqueness
            with open(file_path, 'rb') as f:
                hash_md5 = hashlib.md5(f.read()).hexdigest()
            features['md5_hash'] = int(hash_md5, 16) % 1000000  # Convert to int for ML

            # File extension as numeric
            _, ext = os.path.splitext(file_path)
            features['extension'] = hash(ext) % 1000

        except Exception as e:
            print(f"Error extracting features from {file_path}: {e}")
            return None

        return features

    def train_model(self, benign_files, malicious_files):
        data = []
        labels = []

        for file in benign_files:
            features = self.extract_features(file)
            if features:
                data.append(features)
                labels.append(0)  # 0 for benign

        for file in malicious_files:
            features = self.extract_features(file)
            if features:
                data.append(features)
                labels.append(1)  # 1 for malicious

        if not data:
            print("No data to train on")
            return

        df = pd.DataFrame(data)
        X = df.values
        y = np.array(labels)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        joblib.dump(self.model, self.model_path)

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False

    def predict_anomaly(self, file_path):
        if not self.model:
            if not self.load_model():
                return False

        features = self.extract_features(file_path)
        if not features:
            return False

        df = pd.DataFrame([features])
        prediction = self.model.predict(df.values)
        return prediction[0] == 1  # 1 means malicious/anomalous

if __name__ == "__main__":
    # Example training (replace with actual file paths)
    ai = AIModel()
    benign_files = []  # List of benign file paths
    malicious_files = []  # List of malicious file paths
    if benign_files and malicious_files:
        ai.train_model(benign_files, malicious_files)
    else:
        print("No training data provided. Skipping training.")
