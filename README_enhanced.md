# 🛡️ CyberSec-AI AutoReport - Enhanced Edition

**AI-Powered Cybersecurity Report Automation Tool**  
*Tested and optimized for Kali Linux 2025*

## 🚀 Quick Start

```bash
# 1. Clone or download the project
git clone <repository-url>
cd cybersec_ai_autoreport

# 2. Run the enhanced installation script
chmod +x install_enhanced.sh
./install_enhanced.sh

# 3. Set your OpenAI API key
nano config.json  # Edit the "api_key" field

# 4. Start using the tool
python3 main.py interactive
```

## 🔥 What's New in This Enhanced Edition

### ✅ **Fixed Issues from Kali Linux 2025 Testing**
- **PDF Generation**: Fixed WeasyPrint issues with multiple fallback methods
- **OpenAI Integration**: Enhanced API key configuration and error handling
- **Browser Opening**: Safe cross-platform browser launching
- **File Corruption**: Resolved IndentationError issues in core files
- **Dependencies**: Improved dependency management and installation

### ✅ **New Features**
- **Interactive Mode**: User-friendly guided interface
- **Auto-Detection**: Automatically detect scan file types
- **Batch Processing**: Process multiple scan files at once
- **Custom Tools**: Integrate your own security tools
- **Diagnostic Tools**: Built-in system diagnostics and fixes
- **Enhanced Reporting**: Beautiful HTML/PDF reports with AI insights

### ✅ **System Improvements**
- **Error Handling**: Comprehensive error handling and recovery
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Fallback Methods**: Multiple PDF generation methods
- **Mock Mode**: Works without OpenAI API key for testing
- **Configuration**: Flexible configuration system

## 📋 System Requirements

### **Kali Linux 2025 (Recommended)**
```bash
# Core requirements
python3 (3.9+)
pip3
git

# System dependencies (auto-installed)
python3-dev
python3-cffi
libcairo2-dev
libpango1.0-dev
libgdk-pixbuf2.0-dev
libffi-dev
```

### **Other Linux Distributions**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev build-essential

# CentOS/RHEL
sudo yum install python3 python3-pip python3-devel gcc

# Arch Linux
sudo pacman -S python python-pip base-devel
```

## 🔧 Installation Methods

### **Method 1: Enhanced Auto-Installation (Recommended)**
```bash
chmod +x install_enhanced.sh
./install_enhanced.sh
```

### **Method 2: Quick Fix Installation**
```bash
python3 quick_fix.py  # Automated fixes
python3 diagnose.py   # System diagnosis
```

### **Method 3: Manual Installation**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install PDF dependencies
pip install weasyprint pyyaml openai

# Create configuration
cp config.json.example config.json
```

## 🎯 Usage Examples

### **Interactive Mode (Beginner-Friendly)**
```bash
python3 main.py interactive
```

### **Command Line Interface**
```bash
# Parse scan files
python3 main.py parse -i scan.xml -t nmap
python3 main.py parse -i burp_scan.json -t burp
python3 main.py parse -i nuclei_output.json -t nuclei

# Generate full report (one command)
python3 main.py full-report -i scan.xml -t nmap --format pdf

# Auto-detect scan type
python3 main.py full-report -i scan.xml -t auto

# Batch process directory
python3 main.py batch-process -d /path/to/scans --format pdf
```

### **Advanced Workflows**
```bash
# Step-by-step processing
python3 main.py parse -i scan.xml -t nmap -o findings.json
python3 main.py enhance -f findings.json -o enhanced.json
python3 main.py export -f enhanced.json --format pdf

# Custom tools integration
python3 main.py tools register --name "custom-scanner" --command "scanner {input} {output}"
python3 main.py tools run --name "custom-scanner" --input target.txt
```

## 🛠️ Configuration

### **OpenAI API Configuration**
```json
{
  "openai": {
    "api_key": "your-api-key-here",
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000
  }
}
```

### **PDF Generation Configuration**
```json
{
  "pdf": {
    "engine": "weasyprint",
    "fallback_engines": ["chrome_headless", "wkhtmltopdf"],
    "page_size": "A4",
    "margins": {
      "top": "20mm",
      "right": "20mm",
      "bottom": "20mm",
      "left": "20mm"
    }
  }
}
```

### **Environment Variables**
```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL="gpt-3.5-turbo"
export PDF_ENGINE="weasyprint"
```

## 🔍 Supported Scan Types

### **Nmap XML**
```bash
# Generate compatible XML
nmap -sS -sV -O target -oX scan.xml

# Parse with tool
python3 main.py parse -i scan.xml -t nmap
```

### **Burp Suite**
```bash
# Export as JSON from Burp Suite
# File > Export > JSON

# Parse with tool
python3 main.py parse -i burp_scan.json -t burp
```

### **Nuclei JSON**
```bash
# Generate JSON output
nuclei -t nuclei-templates/ -u target -json -o nuclei.json

# Parse with tool
python3 main.py parse -i nuclei.json -t nuclei
```

## 📊 Report Features

### **AI-Enhanced Analysis**
- **Vulnerability Summaries**: AI-generated executive summaries
- **Risk Assessment**: Automated severity classification
- **Remediation Suggestions**: Actionable fix recommendations
- **Impact Analysis**: Business impact assessment

### **Report Formats**
- **HTML**: Interactive web reports with charts
- **PDF**: Professional printable reports
- **JSON**: Machine-readable data export
- **CSV**: Spreadsheet-compatible format

### **Customization Options**
- **Templates**: Custom report templates
- **Branding**: Add company logos and colors
- **Filters**: Filter by severity, type, or status
- **Grouping**: Group by host, service, or category

## 🚨 Troubleshooting

### **Common Issues and Solutions**

#### **PDF Generation Fails**
```bash
# Check system dependencies
python3 diagnose.py

# Install PDF dependencies
sudo apt-get install wkhtmltopdf chromium-browser

# Use fallback method
python3 main.py full-report -i scan.xml -t nmap --format html
```

#### **OpenAI API Issues**
```bash
# Check API key
python3 -c "import os; print(os.environ.get('OPENAI_API_KEY', 'Not set'))"

# Test without API key (mock mode)
python3 main.py parse -i samples/sample_nmap.xml -t nmap
```

#### **Import Errors**
```bash
# Run diagnostics
python3 diagnose.py

# Fix common issues
python3 quick_fix.py

# Manual dependency installation
pip install -r requirements.txt
```

#### **File Corruption Issues**
```bash
# Check file integrity
python3 -m py_compile main.py
python3 -m py_compile interactive.py

# Restore from backup
git checkout main.py interactive.py
```

## 🔧 Development Tools

### **Diagnostic Tools**
```bash
# System diagnostics
python3 diagnose.py

# Quick fixes
python3 quick_fix.py

# Dependency check
python3 -c "import sys; print(sys.version)"
```

### **Sample Data**
```bash
# Test with sample data
python3 main.py parse -i samples/sample_nmap.xml -t nmap
python3 main.py parse -i samples/sample_burp.json -t burp
python3 main.py parse -i samples/sample_nuclei.json -t nuclei
```

### **Custom Tool Integration**
```bash
# Register custom tools
python3 main.py tools register --name "nikto" --command "nikto -h {input} -o {output}"

# List registered tools
python3 main.py tools list

# Run custom tool
python3 main.py tools run --name "nikto" --input target.txt
```

## 📁 Project Structure

```
cybersec_ai_autoreport/
├── main.py                    # Main CLI entry point
├── interactive.py             # Interactive mode interface
├── diagnose.py               # System diagnostics
├── quick_fix.py              # Automated fixes
├── install_enhanced.sh       # Enhanced installation script
├── config.json               # Configuration file
├── requirements.txt          # Python dependencies
├── parsers/                  # Scan file parsers
│   ├── nmap_parser.py
│   ├── burp_parser.py
│   └── nuclei_parser.py
├── exporters/                # Report exporters
│   ├── html_generator.py
│   └── pdf_exporter.py
├── ai/                       # AI integration modules
│   ├── summarizer.py
│   ├── severity_classifier.py
│   └── remediation_generator.py
├── tools/                    # Custom tools integration
│   ├── runner.py
│   └── parser.py
├── utils/                    # Utility functions
│   └── file_loader.py
├── templates/                # Report templates
│   └── report_template.html
├── samples/                  # Sample data files
│   ├── sample_nmap.xml
│   ├── sample_burp.json
│   └── sample_nuclei.json
└── output/                   # Generated reports
```

## 🤝 Contributing

### **Bug Reports**
1. Run `python3 diagnose.py` and include output
2. Provide system information (OS, Python version)
3. Include error messages and stack traces
4. Test with sample data if possible

### **Feature Requests**
1. Describe the use case
2. Provide example inputs/outputs
3. Consider backward compatibility
4. Test with existing functionality

### **Code Contributions**
1. Follow existing code style
2. Add comprehensive error handling
3. Include documentation and examples
4. Test on multiple platforms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT API integration
- **WeasyPrint** for PDF generation
- **Click** for CLI framework
- **Kali Linux Team** for testing environment
- **Security Community** for feedback and testing

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and inline help
- **Diagnostics**: Use `python3 diagnose.py` for troubleshooting
- **Quick Fixes**: Use `python3 quick_fix.py` for common issues

---

**Made with ❤️ for the cybersecurity community**

*Tested and optimized for Kali Linux 2025*
