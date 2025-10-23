# Futuristic Antivirus System

A comprehensive, AI-powered antivirus solution featuring real-time monitoring, cloud intelligence, sandboxing, and blockchain-based signature updates.

## Features

- **Signature-based Scanning**: Traditional hash-based malware detection
- **Heuristic Analysis**: Rule-based detection of suspicious patterns
- **AI-Powered Anomaly Detection**: Machine learning for zero-day threat detection
- **Cloud Threat Intelligence**: Real-time global threat sharing
- **Advanced Sandboxing**: Isolated execution environment (Docker-based)
- **Real-time Monitoring**: File system monitoring with watchdog
- **Web-based GUI**: User-friendly dashboard and API
- **Blockchain Integration**: Decentralized signature updates
- **IoT Device Scanning**: Network device protection

## Installation

### Windows (Recommended)

1. Download or clone the repository
2. Run the installer: install_windows.bat
3. The installer will:
   - Check Python installation
   - Install required dependencies
   - Create desktop and Start Menu shortcuts
   - Set up the application for easy use

### Manual Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies: pip install -r requirements.txt
3. Run the application: python main.py [options]

## Usage

### GUI Mode (Recommended)
`ash
python main.py --gui
`
Opens a web interface at http://localhost:5000

### Command Line
`ash
# Scan a file or directory
python main.py --scan /path/to/scan

# Start real-time monitoring
python main.py --monitor /path/to/monitor

# Quarantine a file
python main.py --quarantine /path/to/file

# Show help
python main.py --help
`

### Windows Shortcuts
After installation, use the desktop shortcut or Start Menu entries for easy access.

## Architecture

- main.py: Main entry point and CLI interface
- src/antivirus.py: Core scanning engine
- src/ml_model.py: AI anomaly detection
- src/cloud_intel.py: Cloud threat intelligence
- src/sandbox.py: Sandboxing functionality
- src/gui.py: Web interface and API
- src/monitor.py: Real-time file monitoring

## Configuration

Edit config.json to customize:
- Scan intervals
- Quarantine paths
- API endpoints
- Logging levels

## Requirements

- Python 3.8+
- Windows 10/11 (primary), Linux/MacOS (compatible)
- Internet connection for cloud features
- Docker (optional, for full sandboxing)

## Dependencies

See 
equirements.txt for full list. Key packages:
- scikit-learn: Machine learning
- flask: Web framework
- watchdog: File monitoring
- requests: HTTP client
- docker: Container management
- numpy, pandas: Data processing

## Testing

The system has been tested with:
- Signature-based detection
- Real-time monitoring
- Web GUI functionality
- API endpoints
- Cloud intelligence (mock mode)
- Sandboxing (mock mode)

## License

This project is open-source. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This is a demonstration project. Use at your own risk. Always have multiple layers of security.
