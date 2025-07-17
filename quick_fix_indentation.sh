#!/bin/bash
# Quick Fix Script for CyberSec-AI AutoReport Issues

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 CyberSec-AI AutoReport                         ║"
echo "║                    Quick Fix Script                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}[ERROR]${NC} main.py not found. Please run this script from the cybersec-ai-autoreport directory."
    exit 1
fi

echo -e "${GREEN}[INFO]${NC} Fixing Python file indentation issues..."

# Fix main.py indentation issues
python3 -c "
import ast
import sys

# Test if main.py compiles
try:
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Try to parse the file
    ast.parse(content)
    print('✓ main.py syntax is valid')
except SyntaxError as e:
    print(f'✗ main.py has syntax error: {e}')
    print(f'  Line {e.lineno}: {e.text.strip() if e.text else \"(unknown)\"}')
    sys.exit(1)
except Exception as e:
    print(f'✗ main.py has other issues: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} main.py has syntax errors. Recreating from template..."
    
    # Backup the corrupted file
    cp main.py main.py.backup
    
    # Create a clean main.py
    cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
CyberSec-AI AutoReport - Main CLI Entry Point
AI-powered cybersecurity report automation tool
"""

import click
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from parsers import nmap_parser, burp_parser, nuclei_parser
from exporters import html_generator, pdf_exporter
from ai import summarizer, severity_classifier, remediation_generator
from tools.runner import register_tool, execute_tool, list_tools
from tools.parser import parse_output
from utils.file_loader import save_json, load_json

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """[SHIELD] CyberSec-AI AutoReport - Automated Security Reporting Tool"""
    pass

@cli.command()
@click.option('--input', '-i', required=True, help='Path to scan file')
@click.option('--type', '-t', required=True, 
              type=click.Choice(['nmap', 'burp', 'nuclei']), 
              help='Type of scan file')
@click.option('--output', '-o', default='parsed.json', help='Output file path')
def parse(input, type, output):
    """Parse scan files (Nmap XML, Burp JSON, Nuclei JSON)"""
    click.echo(f"[FINDINGS] Parsing {type} scan file: {input}")
    
    try:
        if type == "nmap":
            findings = nmap_parser.parse(input)
        elif type == "burp":
            findings = burp_parser.parse(input)
        elif type == "nuclei":
            findings = nuclei_parser.parse(input)
        
        save_json(findings, output)
        click.echo(f"[OK] Parsed {len(findings)} findings saved to {output}")
        
    except Exception as e:
        click.echo(f"[ERROR] Error parsing file: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', required=True, help='Parsed JSON file')
@click.option('--output', '-o', default='enhanced.json', help='Output file path')
def enhance(file, output):
    """Enhance findings with AI analysis"""
    click.echo(f"[AI] Enhancing findings with AI: {file}")
    
    try:
        findings = load_json(file)
        
        for i, finding in enumerate(findings):
            click.echo(f"Processing finding {i+1}/{len(findings)}: {finding.get('title', 'Unknown')}")
            
            # Add AI enhancements
            finding["ai_summary"] = summarizer.generate(finding)
            finding["severity"] = severity_classifier.classify(finding)
            finding["remediation"] = remediation_generator.suggest(finding)
        
        save_json(findings, output)
        click.echo(f"[OK] Enhanced findings saved to {output}")
        
    except Exception as e:
        click.echo(f"[ERROR] Error enhancing findings: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', required=True, help='Enhanced JSON file')
@click.option('--format', '-fmt', default='pdf', 
              type=click.Choice(['html', 'pdf']), help='Export format')
@click.option('--output', '-o', help='Output file path')
def export(file, format, output):
    """Export report to HTML or PDF"""
    click.echo(f"[FILE] Exporting report as {format.upper()}: {file}")
    
    try:
        findings = load_json(file)
        
        # Generate HTML first
        html_path = html_generator.export(findings, output_path=output)
        
        if format == "pdf":
            pdf_path = pdf_exporter.export(html_path)
            click.echo(f"[OK] PDF report generated: {pdf_path}")
        else:
            click.echo(f"[OK] HTML report generated: {html_path}")
            
    except Exception as e:
        click.echo(f"[ERROR] Error exporting report: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', required=True, help='Path to scan file')
@click.option('--type', '-t', 
              type=click.Choice(['nmap', 'burp', 'nuclei', 'auto']), 
              default='auto',
              help='Type of scan file (auto-detect by default)')
@click.option('--format', '-fmt', default='html', 
              type=click.Choice(['html', 'pdf']), help='Export format')
def full_report(input, type, format):
    """One-click: Parse → AI Enhance → Export"""
    click.echo("[LAUNCH] Running full report generation pipeline...")
    
    # Auto-detect scan type if needed
    if type == 'auto':
        from auto_detect import ScanAutoDetector
        detector = ScanAutoDetector()
        detected_type = detector.detect_scan_type(input)
        if detected_type:
            type = detected_type
            click.echo(f"[INFO] Auto-detected scan type: {type}")
        else:
            click.echo("[ERROR] Could not auto-detect scan type. Please specify --type")
            sys.exit(1)
    
    # Step 1: Parse
    click.echo("Step 1/3: Parsing scan file...")
    try:
        if type == "nmap":
            findings = nmap_parser.parse(input)
        elif type == "burp":
            findings = burp_parser.parse(input)
        elif type == "nuclei":
            findings = nuclei_parser.parse(input)
        
        click.echo(f"[OK] Parsed {len(findings)} findings")
    except Exception as e:
        click.echo(f"[ERROR] Parsing failed: {str(e)}", err=True)
        sys.exit(1)
    
    # Step 2: AI Enhancement
    click.echo("Step 2/3: AI enhancement...")
    try:
        for i, finding in enumerate(findings):
            click.echo(f"  Processing {i+1}/{len(findings)}: {finding.get('title', 'Unknown')}")
            finding["ai_summary"] = summarizer.generate(finding)
            finding["severity"] = severity_classifier.classify(finding)
            finding["remediation"] = remediation_generator.suggest(finding)
        
        click.echo(f"[OK] Enhanced {len(findings)} findings")
    except Exception as e:
        click.echo(f"[ERROR] AI enhancement failed: {str(e)}", err=True)
        sys.exit(1)
    
    # Step 3: Export Report
    click.echo("Step 3/3: Generating report...")
    try:
        html_path = html_generator.export(findings)
        click.echo(f"[OK] HTML report generated: {html_path}")
        
        if format == "pdf":
            try:
                pdf_path = pdf_exporter.export(html_path)
                click.echo(f"[OK] PDF report generated: {pdf_path}")
                click.echo(f"[SUCCESS] Full report completed: {pdf_path}")
            except Exception as pdf_error:
                click.echo(f"[ERROR] PDF generation failed: {str(pdf_error)}")
                click.echo(f"[INFO] HTML report is still available: {html_path}")
                click.echo("[TIP] Try running: ./install_dependencies.sh")
        else:
            click.echo(f"[SUCCESS] Full report completed: {html_path}")
            
    except Exception as e:
        click.echo(f"[ERROR] Report generation failed: {str(e)}", err=True)
        sys.exit(1)

# Custom Tools Commands
@cli.group()
def tools():
    """Custom tool integration commands"""
    pass

@tools.command()
@click.option('--name', required=True, help='Tool name')
@click.option('--command', required=True, help='Command template with {input} and {output}')
@click.option('--desc', default='', help='Tool description')
def register(name, command, desc):
    """Register a new custom tool"""
    click.echo(f"[TOOL] Registering tool: {name}")
    
    try:
        register_tool(name, command, desc, "file", "file")
        click.echo(f"[OK] Tool '{name}' registered successfully")
    except Exception as e:
        click.echo(f"[ERROR] Registration failed: {str(e)}", err=True)

@tools.command()
@click.option('--name', required=True, help='Tool name')
@click.option('--input', required=True, help='Input file path')
@click.option('--output', help='Output file path (optional)')
def run(name, input, output):
    """Run a registered custom tool"""
    click.echo(f"[EXEC] Running tool: {name}")
    
    try:
        output_file, stdout = execute_tool(name, input, output)
        if output_file:
            click.echo(f"[OK] Tool completed. Output saved to: {output_file}")
            
            # Parse with AI
            summary = parse_output(output_file)
            click.echo(f"[AI] AI Summary:\n{summary}")
        else:
            click.echo("[ERROR] Tool execution failed")
            
    except Exception as e:
        click.echo(f"[ERROR] Tool execution failed: {str(e)}", err=True)

@tools.command()
def list():
    """List all registered tools"""
    click.echo("[TOOL] Registered Tools:")
    
    try:
        tools_list = list_tools()
        for name, tool in tools_list.items():
            click.echo(f"  • {name}: {tool.get('description', 'No description')}")
            click.echo(f"    Command: {tool.get('command', 'N/A')}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to list tools: {str(e)}", err=True)

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to process')
@click.option('--format', '-fmt', default='html', 
              type=click.Choice(['html', 'pdf']), help='Export format')
@click.option('--recursive', '-r', is_flag=True, help='Search recursively')
def batch_process(directory, format, recursive):
    """Process all scan files in a directory"""
    click.echo(f"[LAUNCH] Batch processing directory: {directory}")
    
    try:
        from auto_detect import AutoProcessor
        processor = AutoProcessor()
        
        # Find and process all scan files
        reports = processor.process_directory(directory, format)
        
        if reports:
            click.echo(f"[SUCCESS] Generated {len(reports)} reports:")
            for report in reports:
                click.echo(f"  {report}")
        else:
            click.echo("[WARNING] No scan files found or processed")
            
    except Exception as e:
        click.echo(f"[ERROR] Batch processing failed: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def interactive():
    """Launch interactive mode"""
    click.echo("[LAUNCH] Starting interactive mode...")
    
    try:
        from interactive import InteractiveCLI
        cli_app = InteractiveCLI()
        cli_app.main_menu()
    except Exception as e:
        click.echo(f"[ERROR] Interactive mode failed: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', help='File to analyze')
@click.option('--directory', '-d', default='.', help='Directory to scan')
def auto_detect(file, directory):
    """Auto-detect scan file types"""
    try:
        from auto_detect import ScanAutoDetector
        detector = ScanAutoDetector()
        
        if file:
            # Analyze single file
            file_info = detector.get_file_info(file)
            if file_info:
                click.echo(f"File: {file_info['name']}")
                click.echo(f"Type: {file_info['detected_type']}")
                click.echo(f"Valid: {file_info['is_valid']}")
                click.echo(f"Size: {file_info['size']} bytes")
            else:
                click.echo("[ERROR] File not found")
        else:
            # Scan directory
            scan_files = detector.find_scan_files(directory)
            if scan_files:
                click.echo(f"Found {len(scan_files)} scan files:")
                for file_path, scan_type in scan_files:
                    click.echo(f"  {file_path} -> {scan_type}")
            else:
                click.echo("[INFO] No scan files found")
                
    except Exception as e:
        click.echo(f"[ERROR] Auto-detection failed: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
EOF

    echo -e "${GREEN}[INFO]${NC} main.py has been recreated with proper indentation"
fi

# Fix permissions
echo -e "${GREEN}[INFO]${NC} Setting correct file permissions..."
chmod +x main.py
chmod +x interactive.py
chmod +x setup.sh
chmod +x install.sh
chmod +x auto_detect.py

# Test the files
echo -e "${GREEN}[INFO]${NC} Testing file syntax..."
python3 -m py_compile main.py
python3 -m py_compile interactive.py

echo -e "${GREEN}[SUCCESS]${NC} All files have been fixed!"
echo
echo -e "${YELLOW}What was fixed:${NC}"
echo "✓ Python indentation errors"
echo "✓ File permissions"
echo "✓ Syntax validation"
echo
echo -e "${BLUE}You can now run:${NC}"
echo "  python3 main.py --help"
echo "  ./interactive.py"
echo "  python3 main.py full-report --input scan.xml --type nmap"
echo

# Create a better installation script that keeps user in directory
cat > install_fixed.sh << 'EOF'
#!/bin/bash
# Enhanced Installation Script that keeps user in the right directory

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 CyberSec-AI AutoReport                         ║"
echo "║                Enhanced Installation                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're already in the right directory
if [ -f "main.py" ] && [ -f "interactive.py" ]; then
    echo -e "${GREEN}[INFO]${NC} Already in project directory"
    PROJECT_DIR=$(pwd)
else
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Git is not installed. Please install git first."
        exit 1
    fi

    # Clone repository if not already present
    if [ ! -d "cybersec-ai-autoreport" ]; then
        echo -e "${GREEN}[INFO]${NC} Cloning repository..."
        git clone https://github.com/gh0st-bit/cybersec-ai-autoreport.git
    else
        echo -e "${GREEN}[INFO]${NC} Repository already exists, updating..."
        cd cybersec-ai-autoreport
        git pull origin main
        cd ..
    fi

    PROJECT_DIR="$(pwd)/cybersec-ai-autoreport"
fi

# Run setup from the project directory
cd "$PROJECT_DIR"
echo -e "${GREEN}[INFO]${NC} Running setup from: $(pwd)"

# Make files executable
chmod +x setup.sh
chmod +x interactive.py
chmod +x auto_detect.py
chmod +x main.py

# Run setup
if [ -f "setup.sh" ]; then
    echo -e "${GREEN}[INFO]${NC} Running setup script..."
    ./setup.sh
else
    echo -e "${YELLOW}[WARNING]${NC} setup.sh not found, running basic setup..."
    
    # Basic setup
    echo -e "${GREEN}[INFO]${NC} Installing Python dependencies..."
    pip3 install --user click requests beautifulsoup4 lxml jinja2 colorama tqdm
    
    echo -e "${GREEN}[INFO]${NC} Creating directories..."
    mkdir -p output samples
    
    echo -e "${GREEN}[INFO]${NC} Testing installation..."
    python3 main.py --help > /dev/null 2>&1 && echo -e "${GREEN}[SUCCESS]${NC} Installation test passed"
fi

echo -e "${GREEN}[SUCCESS]${NC} Installation complete!"
echo
echo -e "${YELLOW}Current directory: $(pwd)${NC}"
echo -e "${YELLOW}You are now in the project directory${NC}"
echo
echo -e "${BLUE}Quick Start Commands:${NC}"
echo "  ./interactive.py                           # Interactive mode"
echo "  python3 main.py --help                    # Show help"
echo "  python3 main.py full-report --input scan.xml --type nmap"
echo
echo -e "${GREEN}[INFO]${NC} Ready to use! No need to change directories."

# Create an alias for easy access
echo
echo -e "${BLUE}Tip: Add this to your ~/.bashrc for easy access:${NC}"
echo "alias cybersec-ai='cd $PROJECT_DIR && ./interactive.py'"
EOF

chmod +x install_fixed.sh

echo -e "${GREEN}[INFO]${NC} Created enhanced installation script: install_fixed.sh"
echo -e "${GREEN}[INFO]${NC} This script will keep users in the correct directory after installation"
