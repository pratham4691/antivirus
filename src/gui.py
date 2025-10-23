from flask import Flask, render_template, request, jsonify
import os
from .antivirus import AntivirusEngine
import json

app = Flask(__name__)
av_engine = AntivirusEngine()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan', methods=['POST'])
def scan():
    path = request.json.get('path')
    if not path:
        return jsonify({'error': 'No path provided'}), 400

    infected = av_engine.run_scan(path)
    return jsonify({
        'scanned_path': path,
        'infected_files': infected,
        'total_infected': len(infected)
    })

@app.route('/logs')
def get_logs():
    log_file = 'logs/antivirus.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.readlines()
        return jsonify({'logs': logs[-50:]})  # Last 50 log entries
    return jsonify({'logs': []})

@app.route('/quarantine')
def quarantine_list():
    quarantine_dir = 'quarantine'
    if os.path.exists(quarantine_dir):
        files = os.listdir(quarantine_dir)
        return jsonify({'quarantined_files': files})
    return jsonify({'quarantined_files': []})

@app.route('/update_signatures', methods=['POST'])
def update_signatures():
    # Mock signature update
    new_signatures = request.json.get('signatures', [])
    with open('data/signatures.txt', 'a') as f:
        for sig in new_signatures:
            f.write(sig + '\n')
    av_engine.signatures.update(new_signatures)
    return jsonify({'message': 'Signatures updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
