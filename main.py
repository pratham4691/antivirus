#!/usr/bin/env python3
"""
Futuristic Antivirus System - Main Entry Point
A comprehensive antivirus solution with AI, cloud intelligence, sandboxing, and real-time monitoring.
"""

import argparse
import sys
import os
from src.antivirus import AntivirusEngine
from src.monitor import RealTimeMonitor
from src.gui import app

def main():
    parser = argparse.ArgumentParser(description="Futuristic Antivirus System")
    parser.add_argument('--scan', help='Scan a file or directory')
    parser.add_argument('--monitor', help='Start real-time monitoring for a directory')
    parser.add_argument('--gui', action='store_true', help='Start the web GUI')
    parser.add_argument('--quarantine', help='Quarantine a specific file')

    args = parser.parse_args()

    if args.scan:
        av = AntivirusEngine()
        if os.path.isfile(args.scan):
            result = av.scan_file(args.scan)
            print(f"Scan result for {args.scan}: {'Threat detected' if result else 'Clean'}")
        elif os.path.isdir(args.scan):
            infected = av.run_scan(args.scan)
            print(f"Scan completed. Infected files: {len(infected)}")
            for file in infected:
                print(f"  - {file}")
        else:
            print(f"Path not found: {args.scan}")

    elif args.monitor:
        if os.path.isdir(args.monitor):
            monitor = RealTimeMonitor([args.monitor])
            print(f"Starting real-time monitoring for {args.monitor}")
            monitor.start_monitoring()
        else:
            print(f"Directory not found: {args.monitor}")

    elif args.gui:
        print("Starting web GUI on http://localhost:5000")
        app.run(debug=True)

    elif args.quarantine:
        av = AntivirusEngine()
        av.quarantine_file(args.quarantine)
        print(f"Quarantined: {args.quarantine}")

    else:
        print("Futuristic Antivirus System")
        print("Usage:")
        print("  python main.py --scan <path>          # Scan file or directory")
        print("  python main.py --monitor <directory>  # Start real-time monitoring")
        print("  python main.py --gui                   # Start web interface")
        print("  python main.py --quarantine <file>    # Quarantine a file")

if __name__ == "__main__":
    main()
