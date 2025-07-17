# CyberSec-AI AutoReport - Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Issue 1: PDF Generation Not Working

**Symptoms:**
- Reports claim PDF generation but files are not created
- WeasyPrint errors or silent failures
- Only HTML reports are generated

**Solutions:**

1. **Install System Dependencies (Linux):**
   ```bash
   ./install_dependencies.sh
   ```

2. **Manual Installation (Ubuntu/Debian):**
   ```bash
   sudo apt-get install -y \
     libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev \
     libffi-dev shared-mime-info libxml2-dev libxslt1-dev
   ```

3. **Test PDF Generation:**
   ```bash
   python3 -c "from exporters.pdf_exporter import test_pdf_export; test_pdf_export()"
   ```

4. **Alternative PDF Methods:**
   - **wkhtmltopdf:** `sudo apt-get install wkhtmltopdf`
   - **Chrome headless:** `sudo apt-get install chromium-browser`
   - **Browser printing:** Open HTML report → Print → Save as PDF

### Issue 2: OpenAI API Configuration Problems

**Symptoms:**
- "Using mock responses" despite configuring API key
- API key not being recognized

**Solutions:**

1. **Check Configuration:**
   ```bash
   ./diagnose.py
   ```

2. **Reconfigure API Key:**
   ```bash
   ./interactive.py
   # Choose: Quick actions → Configure OpenAI API key
   ```

3. **Manual Configuration:**
   Edit `config/settings.yaml`:
   ```yaml
   openai:
     api_key: "sk-your-actual-api-key-here"
     model: "gpt-3.5-turbo"
   ```

4. **Test API Key:**
   ```bash
   python3 -c "from ai.openai_client import ai_client; ai_client.reload_config()"
   ```

### Issue 3: Browser Opening Failures

**Symptoms:**
- Graphics errors when opening reports
- "No such file or directory" errors
- Reports don't open in browser

**Solutions:**

1. **Install Browser Utils:**
   ```bash
   sudo apt-get install xdg-utils
   ```

2. **Manual Browser Opening:**
   ```bash
   firefox reports/latest_report.html
   # or
   chromium-browser reports/latest_report.html
   ```

3. **Check Display Environment:**
   ```bash
   echo $DISPLAY
   # If empty, you're in a headless environment
   ```

### Issue 4: File Path Errors

**Symptoms:**
- "No such file or directory" errors
- Empty path errors

**Solutions:**

1. **Check File Permissions:**
   ```bash
   ./quick_fix.py
   # Choose: File Permissions
   ```

2. **Verify File Structure:**
   ```bash
   ./diagnose.py
   ```

3. **Reset Installation:**
   ```bash
   rm -rf cybersec-ai-autoreport
   curl -fsSL https://raw.githubusercontent.com/gh0st-bit/cybersec-ai-autoreport/main/install.sh | bash
   ```

## 🛠️ Diagnostic Tools

### 1. Complete System Check
```bash
./diagnose.py
```
Checks all system components and provides detailed fix recommendations.

### 2. Quick Fix Tool
```bash
./quick_fix.py
```
Provides automated fixes for common issues.

### 3. System Dependencies Installer
```bash
./install_dependencies.sh
```
Installs all required system libraries for PDF generation.

## 📊 Testing Your Installation

### 1. Basic Functionality Test
```bash
python main.py --help
```

### 2. PDF Generation Test
```bash
python3 -c "from exporters.pdf_exporter import test_pdf_export; test_pdf_export()"
```

### 3. OpenAI API Test
```bash
python3 -c "from ai.openai_client import ai_client; print(ai_client.chat_completion('Hello', max_tokens=5))"
```

### 4. End-to-End Test
```bash
python main.py full-report --input data/sample_inputs/nmap_sample.xml --type nmap --format pdf
```

## 🔍 Advanced Troubleshooting

### Enable Debug Mode
Set environment variable for verbose output:
```bash
export DEBUG=1
./interactive.py
```

### Check Log Files
```bash
tail -f outputs/*.log
```

### Verify Dependencies
```bash
pip list | grep -E "(openai|weasyprint|jinja2|click)"
```

### Check System Dependencies
```bash
ldconfig -p | grep -E "(cairo|pango|gdk-pixbuf)"
```

## 📋 System Requirements

### Minimum Requirements
- Python 3.8+
- 2GB RAM
- 500MB disk space
- Internet connection (for OpenAI API)

### Recommended Requirements
- Python 3.10+
- 4GB RAM
- 1GB disk space
- Linux/macOS (Windows support via WSL)

### Supported Distributions
- Ubuntu 20.04+ / Debian 11+
- CentOS 8+ / RHEL 8+
- Arch Linux
- macOS 10.15+
- Windows 10+ (via WSL2)

## 🚨 Known Issues

### 1. WeasyPrint on ARM Systems
**Issue:** WeasyPrint may fail on ARM-based systems (Apple M1, Raspberry Pi)
**Workaround:** Use Chrome headless fallback or wkhtmltopdf

### 2. Large Scan Files
**Issue:** Memory issues with very large scan files (>100MB)
**Workaround:** Split scan files or increase system memory

### 3. Network Proxies
**Issue:** OpenAI API calls may fail behind corporate proxies
**Workaround:** Configure proxy settings in environment variables

### 4. SELinux/AppArmor
**Issue:** Security policies may block file operations
**Workaround:** Temporarily disable or configure appropriate policies

## 📞 Getting Help

### 1. Check Documentation
- [Main README](README.md)
- [Installation Guide](INSTALL.md)
- [API Documentation](API.md)

### 2. Run Diagnostics
```bash
./diagnose.py > system_report.txt
```

### 3. Report Issues
- GitHub Issues: https://github.com/gh0st-bit/cybersec-ai-autoreport/issues
- Include system report from diagnostics
- Provide minimal reproduction steps

### 4. Community Support
- Discussions: https://github.com/gh0st-bit/cybersec-ai-autoreport/discussions
- Wiki: https://github.com/gh0st-bit/cybersec-ai-autoreport/wiki

## 🎯 Quick Recovery Commands

### Full Reset
```bash
rm -rf cybersec-ai-autoreport
curl -fsSL https://raw.githubusercontent.com/gh0st-bit/cybersec-ai-autoreport/main/install.sh | bash
```

### Repair Installation
```bash
./quick_fix.py
./diagnose.py
```

### Update to Latest
```bash
git pull origin main
pip install -r requirements.txt
```

### Emergency HTML-only Mode
```bash
python main.py full-report --input scan.xml --type nmap --format html
```

---

💡 **Tip:** Always run `./diagnose.py` first when encountering issues - it provides comprehensive system analysis and specific fix recommendations.
