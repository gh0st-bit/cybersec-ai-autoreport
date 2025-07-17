#!/bin/bash
# Enhanced Tool Installation Script for CyberSec-AI AutoReport
# Automatically installs missing security tools

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           CyberSec-AI AutoReport - Tool Installer              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install via package manager
install_package() {
    local package=$1
    local description=$2
    
    echo -e "${GREEN}[INSTALL]${NC} Installing $package ($description)..."
    
    # Try different package managers
    if command_exists apt-get; then
        sudo apt-get update -qq
        sudo apt-get install -y "$package"
    elif command_exists yum; then
        sudo yum install -y "$package"
    elif command_exists dnf; then
        sudo dnf install -y "$package"
    elif command_exists pacman; then
        sudo pacman -S --noconfirm "$package"
    elif command_exists brew; then
        brew install "$package"
    else
        echo -e "${RED}[ERROR]${NC} No supported package manager found"
        return 1
    fi
}

# Function to install Go-based tools
install_go_tool() {
    local tool_url=$1
    local tool_name=$2
    
    echo -e "${GREEN}[INSTALL]${NC} Installing $tool_name via Go..."
    
    if command_exists go; then
        go install -v "$tool_url"
        
        # Add GOPATH/bin to PATH if not already there
        if [[ ":$PATH:" != *":$HOME/go/bin:"* ]]; then
            echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
            export PATH=$PATH:$HOME/go/bin
        fi
    else
        echo -e "${YELLOW}[WARNING]${NC} Go not installed. Installing Go first..."
        install_package golang-go "Go programming language"
        go install -v "$tool_url"
    fi
}

# Function to install Python-based tools
install_python_tool() {
    local tool_name=$1
    local pip_package=$2
    
    echo -e "${GREEN}[INSTALL]${NC} Installing $tool_name via pip..."
    
    if command_exists pip3; then
        pip3 install --user "$pip_package"
    elif command_exists pip; then
        pip install --user "$pip_package"
    else
        echo -e "${YELLOW}[WARNING]${NC} pip not found. Installing python3-pip first..."
        install_package python3-pip "Python package manager"
        pip3 install --user "$pip_package"
    fi
}

# Check and install core tools
echo -e "${GREEN}[INFO]${NC} Checking for security tools..."

# Core tools with installation methods
declare -A tools=(
    ["nmap"]="package:nmap:Network discovery and security auditing"
    ["nuclei"]="go:github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest:Fast vulnerability scanner"
    ["nikto"]="package:nikto:Web server scanner"
    ["gobuster"]="go:github.com/OJ/gobuster/v3@latest:Directory/file brute-forcer"
    ["sqlmap"]="package:sqlmap:SQL injection testing tool"
    ["dirsearch"]="python:dirsearch:Directory brute-forcer"
    ["subfinder"]="go:github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest:Subdomain discovery tool"
    ["httpx"]="go:github.com/projectdiscovery/httpx/cmd/httpx@latest:HTTP toolkit"
)

# Check which tools are missing
missing_tools=()
available_tools=()

for tool in "${!tools[@]}"; do
    if command_exists "$tool"; then
        available_tools+=("$tool")
        echo -e "  ✅ $tool - Available"
    else
        missing_tools+=("$tool")
        echo -e "  ❌ $tool - Missing"
    fi
done

echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Available tools: ${#available_tools[@]}"
echo -e "  Missing tools: ${#missing_tools[@]}"

if [ ${#missing_tools[@]} -eq 0 ]; then
    echo -e "${GREEN}[SUCCESS]${NC} All tools are already installed!"
    exit 0
fi

# Ask user if they want to install missing tools
echo ""
echo -e "${YELLOW}[QUESTION]${NC} Do you want to install missing tools? (y/n)"
read -r response

if [[ "$response" != "y" && "$response" != "Y" ]]; then
    echo -e "${YELLOW}[INFO]${NC} Skipping tool installation"
    exit 0
fi

# Install missing tools
echo -e "${GREEN}[INFO]${NC} Installing missing tools..."

for tool in "${missing_tools[@]}"; do
    install_info="${tools[$tool]}"
    IFS=':' read -r method package description <<< "$install_info"
    
    echo ""
    echo -e "${BLUE}Installing $tool${NC}"
    echo -e "  Description: $description"
    
    case "$method" in
        "package")
            install_package "$package" "$description"
            ;;
        "go")
            install_go_tool "$package" "$tool"
            ;;
        "python")
            install_python_tool "$tool" "$package"
            ;;
        *)
            echo -e "${RED}[ERROR]${NC} Unknown installation method: $method"
            continue
            ;;
    esac
    
    # Verify installation
    if command_exists "$tool"; then
        echo -e "${GREEN}[SUCCESS]${NC} $tool installed successfully"
    else
        echo -e "${RED}[ERROR]${NC} $tool installation failed"
    fi
done

# Update tool registry
echo ""
echo -e "${GREEN}[INFO]${NC} Updating tool registry..."
if [ -f "tools/runner_enhanced.py" ]; then
    python3 tools/runner_enhanced.py
else
    echo -e "${YELLOW}[WARNING]${NC} Enhanced runner not found, using basic runner"
    python3 -c "
from tools.runner import list_tools
tools = list_tools()
print('Registered tools:')
for name, info in tools.items():
    print(f'  - {name}: {info.get(\"description\", \"No description\")}')
"
fi

# Final verification
echo ""
echo -e "${GREEN}[INFO]${NC} Final verification..."
all_installed=true

for tool in "${missing_tools[@]}"; do
    if command_exists "$tool"; then
        echo -e "  ✅ $tool - Now available"
    else
        echo -e "  ❌ $tool - Still missing"
        all_installed=false
    fi
done

if $all_installed; then
    echo ""
    echo -e "${GREEN}[SUCCESS]${NC} All tools installed successfully!"
    echo -e "${BLUE}[INFO]${NC} You can now use all security tools with CyberSec-AI AutoReport"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Run: python3 tools/runner_enhanced.py (to verify tool registration)"
    echo "2. Test: ./interactive.py (to test the enhanced interactive mode)"
    echo "3. Scan: python3 main.py full-report --input target.com --type auto"
else
    echo ""
    echo -e "${YELLOW}[WARNING]${NC} Some tools could not be installed automatically"
    echo -e "${BLUE}[INFO]${NC} Please install missing tools manually:"
    
    for tool in "${missing_tools[@]}"; do
        if ! command_exists "$tool"; then
            install_info="${tools[$tool]}"
            IFS=':' read -r method package description <<< "$install_info"
            
            case "$method" in
                "package")
                    echo "  $tool: sudo apt-get install $package"
                    ;;
                "go")
                    echo "  $tool: go install -v $package"
                    ;;
                "python")
                    echo "  $tool: pip3 install --user $package"
                    ;;
            esac
        fi
    done
fi

echo ""
echo -e "${BLUE}[INFO]${NC} Tool installation complete!"
