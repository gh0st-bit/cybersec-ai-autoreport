#!/usr/bin/env python3
"""
CyberSec-AI AutoReport - Quick Fix Utility
Automated fixes for common issues
"""

import os
import sys
import json
import stat
import subprocess
import platform
from pathlib import Path

def fix_file_permissions():
    """Fix file permissions for the project"""
    print("[FIX] Fixing file permissions...")
    
    try:
        # Get current directory
        project_dir = Path(__file__).parent
        
        # Files that need execute permissions
        executable_files = [
            'main.py',
            'interactive.py',
            'install_dependencies.sh',
            'diagnose.py',
            'quick_fix.py'
        ]
        
        for file_name in executable_files:
            file_path = project_dir / file_name
            if file_path.exists():
                # Make file executable
                current_mode = file_path.stat().st_mode
                file_path.chmod(current_mode | stat.S_IEXEC)
                print(f"  ✓ Made {file_name} executable")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error fixing permissions: {e}")
        return False

def fix_directory_structure():
    """Ensure all required directories exist"""
    print("[FIX] Checking directory structure...")
    
    try:
        project_dir = Path(__file__).parent
        
        # Required directories
        required_dirs = [
            'parsers',
            'exporters',
            'ai',
            'tools',
            'utils',
            'templates',
            'output',
            'samples'
        ]
        
        for dir_name in required_dirs:
            dir_path = project_dir / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ Created directory: {dir_name}")
            else:
                print(f"  ✓ Directory exists: {dir_name}")
                
        return True
        
    except Exception as e:
        print(f"  ✗ Error creating directories: {e}")
        return False

def fix_config_file():
    """Create or fix configuration files"""
    print("[FIX] Checking configuration files...")
    
    try:
        project_dir = Path(__file__).parent
        
        # Create config.json if it doesn't exist
        config_path = project_dir / 'config.json'
        if not config_path.exists():
            default_config = {
                "openai": {
                    "api_key": "",
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000
                },
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
                },
                "output": {
                    "directory": "output",
                    "filename_format": "security_report_{timestamp}",
                    "include_timestamp": True
                }
            }
            
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"  ✓ Created config.json")
        else:
            print(f"  ✓ Config file exists: config.json")
            
        # Create .env.example
        env_example_path = project_dir / '.env.example'
        if not env_example_path.exists():
            env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000

# PDF Configuration
PDF_ENGINE=weasyprint
PDF_PAGE_SIZE=A4

# Output Configuration
OUTPUT_DIR=output
"""
            with open(env_example_path, 'w') as f:
                f.write(env_content)
            print(f"  ✓ Created .env.example")
        else:
            print(f"  ✓ Environment example exists: .env.example")
            
        return True
        
    except Exception as e:
        print(f"  ✗ Error creating config files: {e}")
        return False

def fix_dependencies():
    """Install missing Python dependencies"""
    print("[FIX] Checking Python dependencies...")
    
    try:
        # Required packages
        required_packages = [
            'click',
            'requests',
            'beautifulsoup4',
            'lxml',
            'jinja2',
            'python-dotenv',
            'colorama',
            'tqdm'
        ]
        
        # Optional packages
        optional_packages = [
            'openai',
            'pyyaml',
            'weasyprint',
            'markdown'
        ]
        
        missing_packages = []
        
        # Check required packages
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"  ✓ {package} is installed")
            except ImportError:
                missing_packages.append(package)
                print(f"  ✗ {package} is missing")
        
        # Check optional packages
        for package in optional_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"  ✓ {package} is installed (optional)")
            except ImportError:
                print(f"  ⚠ {package} is missing (optional)")
        
        # Install missing packages
        if missing_packages:
            print(f"[FIX] Installing missing packages: {', '.join(missing_packages)}")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("  ✓ Missing packages installed")
            
        return True
        
    except Exception as e:
        print(f"  ✗ Error installing dependencies: {e}")
        return False

def fix_pdf_dependencies():
    """Install PDF generation dependencies"""
    print("[FIX] Checking PDF dependencies...")
    
    try:
        # Check WeasyPrint
        try:
            import weasyprint
            print("  ✓ WeasyPrint is available")
        except ImportError:
            print("  ⚠ WeasyPrint not available, trying to install...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'weasyprint'])
                print("  ✓ WeasyPrint installed")
            except subprocess.CalledProcessError:
                print("  ✗ WeasyPrint installation failed")
        
        # Check system dependencies based on OS
        system = platform.system().lower()
        
        if system == 'linux':
            print("  ℹ For Linux systems, you may need to install:")
            print("    sudo apt-get install python3-dev python3-cffi libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev")
        elif system == 'darwin':
            print("  ℹ For macOS, you may need to install:")
            print("    brew install cairo pango gdk-pixbuf libffi")
        elif system == 'windows':
            print("  ℹ For Windows, install GTK+ from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error checking PDF dependencies: {e}")
        return False

def fix_sample_data():
    """Create sample data files for testing"""
    print("[FIX] Creating sample data files...")
    
    try:
        project_dir = Path(__file__).parent
        samples_dir = project_dir / 'samples'
        samples_dir.mkdir(exist_ok=True)
        
        # Sample Nmap XML
        nmap_sample = samples_dir / 'sample_nmap.xml'
        if not nmap_sample.exists():
            nmap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<nmaprun>
    <host>
        <address addr="192.168.1.1" addrtype="ipv4"/>
        <ports>
            <port protocol="tcp" portid="80">
                <state state="open"/>
                <service name="http" product="Apache" version="2.4.41"/>
            </port>
            <port protocol="tcp" portid="443">
                <state state="open"/>
                <service name="https" product="Apache" version="2.4.41"/>
            </port>
        </ports>
    </host>
</nmaprun>'''
            with open(nmap_sample, 'w') as f:
                f.write(nmap_xml)
            print(f"  ✓ Created sample Nmap XML")
        
        # Sample Burp JSON
        burp_sample = samples_dir / 'sample_burp.json'
        if not burp_sample.exists():
            burp_json = {
                "issues": [
                    {
                        "issue_name": "SQL Injection",
                        "issue_type": "1048576",
                        "severity": "High",
                        "confidence": "Certain",
                        "url": "https://example.com/login",
                        "description": "SQL injection vulnerability detected"
                    }
                ]
            }
            with open(burp_sample, 'w') as f:
                json.dump(burp_json, f, indent=2)
            print(f"  ✓ Created sample Burp JSON")
        
        # Sample Nuclei JSON
        nuclei_sample = samples_dir / 'sample_nuclei.json'
        if not nuclei_sample.exists():
            nuclei_json = [
                {
                    "template": "apache-version-detect",
                    "template-url": "https://templates.nuclei.sh/apache-version-detect",
                    "info": {
                        "name": "Apache Version Detection",
                        "author": "pdteam",
                        "severity": "info"
                    },
                    "type": "http",
                    "host": "https://example.com",
                    "matched-at": "https://example.com/",
                    "extracted-results": ["Apache/2.4.41"]
                }
            ]
            with open(nuclei_sample, 'w') as f:
                json.dump(nuclei_json, f, indent=2)
            print(f"  ✓ Created sample Nuclei JSON")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error creating sample data: {e}")
        return False

def run_basic_test():
    """Run basic functionality test"""
    print("[FIX] Running basic functionality test...")
    
    try:
        # Test imports
        print("  Testing imports...")
        
        # Test main CLI
        try:
            from main import cli
            print("  ✓ Main CLI imports successfully")
        except Exception as e:
            print(f"  ✗ Main CLI import failed: {e}")
            return False
        
        # Test interactive mode
        try:
            from interactive import InteractiveCLI
            print("  ✓ Interactive CLI imports successfully")
        except Exception as e:
            print(f"  ✗ Interactive CLI import failed: {e}")
            return False
        
        # Test parsers
        try:
            from parsers import nmap_parser, burp_parser, nuclei_parser
            print("  ✓ Parsers import successfully")
        except Exception as e:
            print(f"  ✗ Parsers import failed: {e}")
            return False
        
        # Test exporters
        try:
            from exporters import html_generator, pdf_exporter
            print("  ✓ Exporters import successfully")
        except Exception as e:
            print(f"  ✗ Exporters import failed: {e}")
            return False
        
        print("  ✓ All basic tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Basic test failed: {e}")
        return False

def main():
    """Main function to run all fixes"""
    print("🔧 CyberSec-AI AutoReport - Quick Fix Utility")
    print("=" * 50)
    
    fixes = [
        ("File Permissions", fix_file_permissions),
        ("Directory Structure", fix_directory_structure),
        ("Configuration Files", fix_config_file),
        ("Python Dependencies", fix_dependencies),
        ("PDF Dependencies", fix_pdf_dependencies),
        ("Sample Data", fix_sample_data),
        ("Basic Test", run_basic_test)
    ]
    
    results = []
    
    for name, fix_func in fixes:
        print(f"\n[{name}]")
        try:
            success = fix_func()
            results.append((name, success))
            if success:
                print(f"✅ {name} completed successfully")
            else:
                print(f"❌ {name} failed")
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print(f"\nOverall: {success_count}/{total_count} fixes completed successfully")
    
    if success_count == total_count:
        print("\n🎉 All fixes completed! Your system should be ready to use.")
        print("\nNext steps:")
        print("1. Set your OpenAI API key in config.json or .env file")
        print("2. Test with: python main.py --help")
        print("3. Try interactive mode: python main.py interactive")
    else:
        print("\n⚠️  Some fixes failed. Please check the errors above.")
        print("You may need to:")
        print("1. Install system dependencies manually")
        print("2. Check file permissions")
        print("3. Run with administrator/root privileges")

if __name__ == "__main__":
    main()
