from flask import Flask, render_template, request, jsonify
import os
import psutil
import time
from datetime import datetime, timedelta
from .antivirus import AntivirusEngine
import json

# Configure Flask to look for templates in the parent directory
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)
av_engine = AntivirusEngine()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan', methods=['POST'])
def scan():
    path = request.json.get('path')
    if not path:
        return jsonify({'error': 'No path provided'}), 400

    # Check if path exists
    if not os.path.exists(path):
        return jsonify({'error': 'Path does not exist'}), 400

    try:
        infected = av_engine.run_scan(path)
        return jsonify({
            'scanned_path': path,
            'infected_files': infected,
            'total_infected': len(infected)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/system_stats')
def system_stats():
    # Get system statistics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    stats = {
        'cpu_usage': cpu_percent,
        'memory_usage': memory.percent,
        'memory_used': round(memory.used / (1024**3), 2),  # GB
        'memory_total': round(memory.total / (1024**3), 2),  # GB
        'disk_usage': disk.percent,
        'disk_used': round(disk.used / (1024**3), 2),  # GB
        'disk_total': round(disk.total / (1024**3), 2),  # GB
        'uptime': int(time.time() - psutil.boot_time())
    }
    return jsonify(stats)

@app.route('/threat_stats')
def threat_stats():
    # Mock threat statistics
    quarantine_dir = 'quarantine'
    quarantined_count = len(os.listdir(quarantine_dir)) if os.path.exists(quarantine_dir) else 0

    # Get recent scan history from logs
    log_file = 'logs/antivirus.log'
    recent_scans = 0
    recent_threats = 0

    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.readlines()
            # Count scans and threats in last 24 hours
            cutoff = datetime.now() - timedelta(hours=24)
            for log in logs[-100:]:  # Check last 100 entries
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
    return jsonify(stats)

@app.route('/activity_timeline')
def activity_timeline():
    # Mock activity timeline data
    activities = [
        {'time': '2 hours ago', 'action': 'Scheduled scan completed', 'details': '0 threats found'},
        {'time': '4 hours ago', 'action': 'File quarantined', 'details': 'test_malware.txt'},
        {'time': '6 hours ago', 'action': 'Real-time monitoring started', 'details': 'Desktop folder'},
        {'time': '1 day ago', 'action': 'Signatures updated', 'details': '150 new signatures'},
        {'time': '2 days ago', 'action': 'System scan completed', 'details': '1 threat found and quarantined'}
    ]
    return jsonify({'activities': activities})

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
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(1)  # Wait for server to start
        webbrowser.open('http://localhost:5000')

    # Start browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=5000)
