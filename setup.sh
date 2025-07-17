#!/bin/bash
# CyberSec-AI AutoReport - Smart Setup Script for Linux
# This script automates the entire setup process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}   CyberSec-AI AutoReport Setup${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

print_header

# 1. Check Python version
print_status "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_status "Python version: $PYTHON_VERSION"

# 2. Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# 3. Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# 4. Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# 5. Install requirements
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# 6. Create necessary directories
print_status "Creating project directories..."
mkdir -p outputs reports data/sample_inputs tools

# 7. Configure settings
print_status "Setting up configuration..."
if [ ! -f "config/settings.yaml" ]; then
    cp config/settings.yaml.template config/settings.yaml
    print_status "Configuration template copied"
fi

# 8. Interactive OpenAI API key setup
echo
read -p "Do you want to configure OpenAI API key now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Please enter your OpenAI API key (or press Enter to skip):"
    read -s API_KEY
    if [ ! -z "$API_KEY" ]; then
        # Update the settings file with the API key
        sed -i "s/your_openai_api_key_here/$API_KEY/" config/settings.yaml
        print_status "OpenAI API key configured"
    else
        print_warning "OpenAI API key skipped. Tool will use mock responses."
    fi
else
    print_warning "OpenAI API key not configured. Tool will use mock responses."
fi

# 9. Test installation
print_status "Testing installation..."
python main.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status "Installation test passed"
else
    print_error "Installation test failed"
    exit 1
fi

# 10. Create quick start script
print_status "Creating quick start script..."
cat > quick_start.sh << 'EOF'
#!/bin/bash
# Quick Start Script for CyberSec-AI AutoReport

# Activate virtual environment
source venv/bin/activate

# Function to run interactive mode
interactive_mode() {
    echo "=== CyberSec-AI AutoReport - Interactive Mode ==="
    echo
    echo "Available scan types:"
    echo "1) Nmap XML"
    echo "2) Burp Suite JSON/XML"
    echo "3) Nuclei JSON"
    echo "4) Run built-in tools"
    echo "5) Exit"
    echo
    
    read -p "Select option (1-5): " choice
    
    case $choice in
        1)
            read -p "Enter path to Nmap XML file: " input_file
            if [ -f "$input_file" ]; then
                python main.py full-report --input "$input_file" --type nmap --format html
            else
                echo "File not found: $input_file"
            fi
            ;;
        2)
            read -p "Enter path to Burp Suite file: " input_file
            if [ -f "$input_file" ]; then
                python main.py full-report --input "$input_file" --type burp --format html
            else
                echo "File not found: $input_file"
            fi
            ;;
        3)
            read -p "Enter path to Nuclei JSON file: " input_file
            if [ -f "$input_file" ]; then
                python main.py full-report --input "$input_file" --type nuclei --format html
            else
                echo "File not found: $input_file"
            fi
            ;;
        4)
            python main.py tools list
            echo
            read -p "Enter tool name to run: " tool_name
            read -p "Enter input (target/file): " input_target
            python main.py tools run --name "$tool_name" --input "$input_target"
            ;;
        5)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
}

# Check if arguments provided
if [ $# -eq 0 ]; then
    interactive_mode
else
    # Run with provided arguments
    python main.py "$@"
fi
EOF

chmod +x quick_start.sh

print_status "Setup completed successfully!"
echo
echo -e "${GREEN}Quick Start Options:${NC}"
echo "1. Interactive mode:    ./quick_start.sh"
echo "2. Direct command:      ./quick_start.sh full-report --input scan.xml --type nmap"
echo "3. Manual command:      source venv/bin/activate && python main.py --help"
echo
echo -e "${YELLOW}Example Usage:${NC}"
echo "./quick_start.sh full-report --input /path/to/nmap_scan.xml --type nmap --format html"
echo
echo -e "${BLUE}Configuration:${NC}"
echo "Edit config/settings.yaml to update OpenAI API key and other settings"
echo
deactivate 2>/dev/null || true
