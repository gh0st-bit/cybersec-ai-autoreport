#!/bin/bash
# One-command installation and setup for CyberSec-AI AutoReport

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 CyberSec-AI AutoReport                         ║"
echo "║                 One-Command Setup                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Git is not installed. Please install git first."
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed. Please install Python 3.8+."
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Starting installation..."

# Clone repository if not already present
if [ ! -d "cybersec-ai-autoreport" ]; then
    echo -e "${GREEN}[INFO]${NC} Cloning repository..."
    git clone https://github.com/gh0st-bit/cybersec-ai-autoreport.git
    cd cybersec-ai-autoreport
else
    echo -e "${GREEN}[INFO]${NC} Repository already exists, entering directory..."
    cd cybersec-ai-autoreport
    git pull origin main
fi

# Make setup script executable
chmod +x setup.sh
chmod +x interactive.py
chmod +x auto_detect.py

# Run setup
echo -e "${GREEN}[INFO]${NC} Running setup script..."
./setup.sh

echo -e "${GREEN}[SUCCESS]${NC} Installation complete!"
echo
echo -e "${YELLOW}Current directory: $(pwd)${NC}"
echo -e "${YELLOW}You are now in the project directory!${NC}"
echo
echo -e "${BLUE}Quick Start Commands:${NC}"
echo "  Interactive mode:     ./interactive.py"
echo "  Auto-detect files:    python auto_detect.py"
echo "  Batch process:        python main.py batch-process"
echo "  One-click report:     python main.py full-report --input scan.xml"
echo
echo -e "${BLUE}Examples:${NC}"
echo "  # Interactive mode (recommended for beginners)"
echo "  ./interactive.py"
echo
echo "  # Auto-detect and process all scans in current directory"
echo "  python main.py batch-process"
echo
echo "  # Process specific file with auto-detection"
echo "  python main.py full-report --input /path/to/scan.xml"
echo
echo -e "${GREEN}[INFO]${NC} Run './interactive.py' to get started!"
echo -e "${GREEN}[INFO]${NC} No need to change directories - you're already in the right place!"

# Keep user in the project directory by spawning a new shell
echo -e "${BLUE}[INFO]${NC} Spawning new shell in project directory..."
echo -e "${BLUE}[INFO]${NC} Type 'exit' to return to your previous directory"
exec bash
