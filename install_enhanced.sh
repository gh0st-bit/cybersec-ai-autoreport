#!/bin/bash
# Enhanced installation script for CyberSec-AI AutoReport
# Compatible with Kali Linux 2025 and other Debian-based systems

echo "🔧 CyberSec-AI AutoReport - Enhanced Installation Script"
echo "======================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_system_deps() {
    echo "[INSTALL] Installing system dependencies..."
    
    # Update package list
    sudo apt-get update -y
    
    # Install Python and pip
    sudo apt-get install -y python3 python3-pip python3-dev python3-venv
    
    # Install build tools
    sudo apt-get install -y build-essential
    
    # Install dependencies for WeasyPrint (PDF generation)
    sudo apt-get install -y \
        python3-cffi \
        libcairo2-dev \
        libpango1.0-dev \
        libgdk-pixbuf2.0-dev \
        libffi-dev \
        shared-mime-info
    
    # Install additional tools
    sudo apt-get install -y \
        curl \
        wget \
        git \
        nmap \
        wkhtmltopdf \
        chromium-browser
    
    echo "✅ System dependencies installed successfully"
}

# Function to create virtual environment
create_venv() {
    echo "[INSTALL] Creating Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✅ Virtual environment created"
    else
        echo "✅ Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    echo "✅ Virtual environment ready"
}

# Function to install Python dependencies
install_python_deps() {
    echo "[INSTALL] Installing Python dependencies..."
    
    # Ensure we're in virtual environment
    if [ -z "$VIRTUAL_ENV" ]; then
        source venv/bin/activate
    fi
    
    # Install required packages
    pip install -r requirements.txt
    
    # Install optional packages with fallback
    echo "[INSTALL] Installing optional packages..."
    
    # Try to install WeasyPrint
    if pip install weasyprint; then
        echo "✅ WeasyPrint installed successfully"
    else
        echo "⚠️  WeasyPrint installation failed, PDF generation will use fallback methods"
    fi
    
    # Install PyYAML
    if pip install pyyaml; then
        echo "✅ PyYAML installed successfully"
    else
        echo "⚠️  PyYAML installation failed, will use environment variables"
    fi
    
    # Install OpenAI
    if pip install openai; then
        echo "✅ OpenAI library installed successfully"
    else
        echo "⚠️  OpenAI installation failed, will use mock responses"
    fi
    
    echo "✅ Python dependencies installed"
}

# Function to set up configuration
setup_config() {
    echo "[INSTALL] Setting up configuration..."
    
    # Create config directory
    mkdir -p ~/.config/cybersec-ai-autoreport
    
    # Create sample configuration
    if [ ! -f "config.json" ]; then
        python3 quick_fix.py
        echo "✅ Configuration files created"
    else
        echo "✅ Configuration already exists"
    fi
    
    # Set up OpenAI API key
    echo ""
    echo "🔑 OpenAI API Key Setup"
    echo "To use AI features, you need to set up your OpenAI API key:"
    echo "1. Get your API key from: https://platform.openai.com/account/api-keys"
    echo "2. Edit config.json and add your key, or"
    echo "3. Set environment variable: export OPENAI_API_KEY='your-key-here'"
    echo ""
}

# Function to run tests
run_tests() {
    echo "[INSTALL] Running system tests..."
    
    # Test main CLI
    if python3 main.py --help >/dev/null 2>&1; then
        echo "✅ Main CLI is working"
    else
        echo "❌ Main CLI test failed"
        return 1
    fi
    
    # Test interactive mode
    if python3 -c "from interactive import InteractiveCLI; print('Interactive CLI OK')" >/dev/null 2>&1; then
        echo "✅ Interactive CLI is working"
    else
        echo "❌ Interactive CLI test failed"
        return 1
    fi
    
    # Test parsers
    if python3 -c "from parsers import nmap_parser, burp_parser, nuclei_parser; print('Parsers OK')" >/dev/null 2>&1; then
        echo "✅ Parsers are working"
    else
        echo "❌ Parsers test failed"
        return 1
    fi
    
    # Test with sample data
    if python3 main.py parse -i samples/sample_nmap.xml -t nmap >/dev/null 2>&1; then
        echo "✅ Sample parsing test passed"
    else
        echo "❌ Sample parsing test failed"
        return 1
    fi
    
    echo "✅ All tests passed"
    return 0
}

# Function to create desktop shortcut
create_shortcuts() {
    echo "[INSTALL] Creating shortcuts..."
    
    # Create launcher script
    cat > cybersec-ai-autoreport.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py interactive
EOF
    
    chmod +x cybersec-ai-autoreport.sh
    
    # Create desktop entry
    if [ -d "$HOME/Desktop" ]; then
        cat > "$HOME/Desktop/CyberSec-AI-AutoReport.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=CyberSec-AI AutoReport
Comment=AI-powered cybersecurity report automation tool
Exec=$(pwd)/cybersec-ai-autoreport.sh
Icon=application-x-executable
Terminal=true
Categories=Security;Network;
EOF
        chmod +x "$HOME/Desktop/CyberSec-AI-AutoReport.desktop"
        echo "✅ Desktop shortcut created"
    fi
    
    echo "✅ Shortcuts created"
}

# Main installation function
main() {
    echo "Starting installation..."
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        echo "⚠️  Don't run this script as root. It will ask for sudo when needed."
        exit 1
    fi
    
    # Check system
    if ! command_exists apt-get; then
        echo "❌ This script is designed for Debian-based systems (like Kali Linux)"
        echo "Please install dependencies manually for your system"
        exit 1
    fi
    
    # Run installation steps
    install_system_deps
    create_venv
    install_python_deps
    setup_config
    
    # Run tests
    if run_tests; then
        create_shortcuts
        
        echo ""
        echo "🎉 Installation completed successfully!"
        echo "======================================="
        echo ""
        echo "Quick Start:"
        echo "1. Set your OpenAI API key in config.json"
        echo "2. Run: ./cybersec-ai-autoreport.sh"
        echo "3. Or run: python3 main.py interactive"
        echo ""
        echo "Command Line Usage:"
        echo "  python3 main.py --help"
        echo "  python3 main.py parse -i scan.xml -t nmap"
        echo "  python3 main.py full-report -i scan.xml -t nmap"
        echo ""
        echo "For diagnostics, run: python3 diagnose.py"
        echo "For quick fixes, run: python3 quick_fix.py"
        echo ""
    else
        echo "❌ Installation completed with errors"
        echo "Run 'python3 diagnose.py' for detailed diagnosis"
        exit 1
    fi
}

# Run main function
main "$@"
