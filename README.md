# STForensicMacOS - MacOS Forensic Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

A modular forensic analysis tool developed for MacOS systems. Equipped with rapid deployment and system imaging capabilities for incident response.

## 🚀 Features

- **🔧 Modular Architecture**: Separate modules for each analysis type
- **⚡ Quick Setup**: Single command installation and execution
- **📊 Two Analysis Modes**: Lite (quick analysis) and Full (complete imaging)
- **📄 Automatic Reporting**: Detailed reports in HTML and JSON formats
- **🔍 Real-time Analysis**: System status and change tracking
- **🔒 Security-Focused**: Read-only operations, data integrity preserved

## 📋 Modules

### 🔍 System Information
- Hardware information (CPU, RAM, Disk)
- Operating system details
- System configuration
- Environment variables

### 📁 Filesystem Analysis
- Filesystem structure
- File hashes (MD5, SHA256)
- Timestamps
- Deleted file recovery (basic)

### 🧠 Memory Analysis
- RAM status and usage
- Kernel modules
- Memory mapping
- Swap status

### 🌐 Network Analysis
- Active connections (IPv4/IPv6)
- Routing table
- DNS information
- Firewall rules

### 📝 Log Analysis
- System logs
- Application logs
- Security logs
- Crash logs

### ⚙️ Process Analysis
- Running processes
- Process details
- System services
- Open files

### 👥 User Analysis
- User accounts
- Group information
- Permission levels
- Session information

### ⏰ Timeline Analysis
- File timeline
- System events
- User activities

## 🛠️ Installation

### Requirements
- macOS 10.15 or higher
- Python 3.8+
- Root/Administrator privileges

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/silexi/stforensicmacos.git
cd stforensicmacos
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Run:**
```bash
sudo python3 main.py --mode lite
```

## 📖 Usage

### Basic Usage

```bash
# Quick analysis (Lite mode)
sudo python3 main.py --mode lite --output ./reports

# Full analysis (Full mode)
sudo python3 main.py --mode full --output ./reports

# Run specific modules
sudo python3 main.py --modules system_info,filesystem,network --output ./reports

# Generate HTML report
sudo python3 main.py --mode lite --output ./reports --format html
```

### Command Line Options

```bash
python3 main.py [OPTIONS]

Options:
  --mode TEXT           Analysis mode: lite or full [default: lite]
  --modules TEXT        Modules to run (comma-separated)
  --output TEXT         Report output directory [default: ./reports]
  --format TEXT         Report format: json, html [default: json]
  --verbose, -v         Verbose output
  --no-hash             Skip hash calculations
  --config TEXT         Configuration file path
  --help                Show this message
```

### Examples

```bash
# Quick system analysis
sudo python3 main.py --mode lite --output ./forensic_reports

# Network analysis only
sudo python3 main.py --modules network --output ./network_analysis

# Full analysis + HTML report
sudo python3 main.py --mode full --output ./full_analysis --format html

# Specific modules with verbose output
sudo python3 main.py --modules system_info,processes,users --verbose --output ./detailed_analysis
```

## 📊 Reports

### JSON Report
Structured data format containing all analysis results.

### HTML Report
Modern, interactive web-based report:
- Module-based tables
- Search and filtering
- Responsive design
- Detailed data viewing

## 🔒 Security

- **Root Privileges**: This tool requires root/administrator privileges
- **Read-Only**: Original data is never modified
- **Hash Verification**: SHA256 hashes for report files
- **Data Integrity**: All operations in read-only mode

## 🏗️ Project Structure

```
stforensicmacos/
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── project_details.json   # Project details
├── roadmap.md            # Development roadmap
├── src/                  # Source code
│   ├── core/             # Core modules
│   │   ├── config.py     # Configuration management
│   │   ├── forensic_engine.py  # Main analysis engine
│   │   └── logger.py     # Logging system
│   ├── modules/          # Forensic modules
│   │   ├── base_module.py
│   │   ├── system_info.py
│   │   ├── filesystem.py
│   │   ├── memory.py
│   │   ├── network.py
│   │   ├── logs.py
│   │   ├── processes.py
│   │   ├── users.py
│   │   └── timeline.py
│   ├── reporters/        # Reporters
│   │   ├── json_reporter.py
│   │   └── html_reporter.py
│   └── utils/            # Helper functions
│       └── helpers.py
├── static/               # Static files
├── templates/            # HTML templates
└── test_reports/         # Test reports
```

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for educational and legal forensic analysis purposes only. Users are responsible for complying with local laws and regulations when using this tool.

## 📞 Contact

- **Project Link**: [https://github.com/silexi/stforensicmacos](https://github.com/silexi/stforensicmacos)
- **Issues**: [GitHub Issues](https://github.com/silexi/stforensicmacos/issues)

## 🙏 Acknowledgments

This project is inspired by the following open source projects:
- [Volatility](https://github.com/volatilityfoundation/volatility)
- [Autopsy](https://github.com/sleuthkit/autopsy)
- [The Sleuth Kit](https://github.com/sleuthkit/sleuthkit)

---

⭐ Don't forget to star this project if you like it! 