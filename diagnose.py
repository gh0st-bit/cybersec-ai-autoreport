#!/usr/bin/env python3
"""
CyberSec-AI AutoReport - Diagnostic Tool
Diagnoses common issues and provides fixes
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print section header"""
    print(f"\n--- {title} ---")

def check_python_version():
    """Check Python version"""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_dependencies():
    """Check Python dependencies"""
    print_section("Python Dependencies Check")
    
    required_packages = [
        'openai', 'jinja2', 'weasyprint', 'xmltodict', 
        'click', 'pyyaml', 'fastapi', 'uvicorn', 
        'python-multipart', 'aiofiles', 'python-docx'
    ]
    
    missing = []
    working = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            working.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n📦 Missing packages: {', '.join(missing)}")
        print("Fix: pip install " + " ".join(missing))
        return False
    else:
        print("✅ All Python dependencies are installed")
        return True

def check_system_dependencies():
    """Check system dependencies for PDF generation"""
    print_section("System Dependencies Check")
    
    # Check WeasyPrint
    print("WeasyPrint PDF generation:")
    try:
        from weasyprint import HTML
        # Test basic HTML to PDF conversion
        test_html = "<html><body><h1>Test</h1></body></html>"
        HTML(string=test_html).write_pdf("/tmp/test.pdf")
        os.remove("/tmp/test.pdf")
        print("✅ WeasyPrint is working")
        weasyprint_ok = True
    except Exception as e:
        print(f"❌ WeasyPrint failed: {e}")
        weasyprint_ok = False
    
    # Check wkhtmltopdf
    print("wkhtmltopdf PDF generation:")
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ wkhtmltopdf is available")
            print(f"   Version: {result.stdout.split()[1]}")
            wkhtmltopdf_ok = True
        else:
            print("❌ wkhtmltopdf failed")
            wkhtmltopdf_ok = False
    except Exception as e:
        print(f"❌ wkhtmltopdf not found: {e}")
        wkhtmltopdf_ok = False
    
    # Check Chrome headless
    print("Chrome headless PDF generation:")
    chrome_commands = ['google-chrome', 'chromium-browser', 'chromium']
    chrome_ok = False
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {cmd} is available")
                print(f"   Version: {result.stdout.strip()}")
                chrome_ok = True
                break
        except:
            continue
    
    if not chrome_ok:
        print("❌ Chrome/Chromium not found")
    
    # Summary
    if weasyprint_ok:
        print("✅ PDF generation is working (WeasyPrint)")
        return True
    elif wkhtmltopdf_ok:
        print("⚠️  PDF generation available (wkhtmltopdf fallback)")
        return True
    elif chrome_ok:
        print("⚠️  PDF generation available (Chrome headless fallback)")
        return True
    else:
        print("❌ No PDF generation methods available")
        return False

def check_openai_config():
    """Check OpenAI configuration"""
    print_section("OpenAI Configuration Check")
    
    try:
        import yaml
        config_path = Path("config/settings.yaml")
        
        if not config_path.exists():
            print("❌ Configuration file not found")
            return False
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        api_key = config.get('openai', {}).get('api_key', '')
        
        if not api_key or api_key == 'your_openai_api_key_here':
            print("❌ OpenAI API key not configured")
            return False
        
        # Test API key
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Simple test
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            
            print("✅ OpenAI API key is working")
            print(f"   Model: {config.get('openai', {}).get('model', 'gpt-3.5-turbo')}")
            return True
            
        except Exception as e:
            print(f"❌ OpenAI API test failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

def check_file_structure():
    """Check project file structure"""
    print_section("Project Structure Check")
    
    required_dirs = [
        'config', 'templates', 'parsers', 'exporters', 
        'ai', 'tools', 'utils', 'data', 'outputs', 'reports'
    ]
    
    required_files = [
        'main.py', 'interactive.py', 'auto_detect.py',
        'requirements.txt', 'setup.sh', 'install.sh'
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
            print(f"❌ Missing directory: {dir_name}")
        else:
            print(f"✅ {dir_name}/")
    
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
            print(f"❌ Missing file: {file_name}")
        else:
            print(f"✅ {file_name}")
    
    if missing_dirs or missing_files:
        print("\n📁 Missing components detected")
        print("Fix: Re-run installation script or clone fresh repository")
        return False
    else:
        print("✅ Project structure is complete")
        return True

def check_permissions():
    """Check file permissions"""
    print_section("File Permissions Check")
    
    executable_files = ['interactive.py', 'setup.sh', 'install.sh']
    
    for file_name in executable_files:
        if Path(file_name).exists():
            if os.access(file_name, os.X_OK):
                print(f"✅ {file_name} is executable")
            else:
                print(f"❌ {file_name} is not executable")
                print(f"   Fix: chmod +x {file_name}")
        else:
            print(f"❌ {file_name} not found")
    
    # Check write permissions for output directories
    output_dirs = ['outputs', 'reports', 'config']
    for dir_name in output_dirs:
        if Path(dir_name).exists():
            if os.access(dir_name, os.W_OK):
                print(f"✅ {dir_name}/ is writable")
            else:
                print(f"❌ {dir_name}/ is not writable")
                return False
    
    return True

def run_basic_test():
    """Run basic functionality test"""
    print_section("Basic Functionality Test")
    
    try:
        # Test parsing
        print("Testing parser...")
        from parsers import nmap_parser
        
        # Test AI components
        print("Testing AI components...")
        from ai import summarizer, severity_classifier
        
        # Test exporters
        print("Testing exporters...")
        from exporters import html_generator, pdf_exporter
        
        print("✅ All core components load successfully")
        
        # Test sample data
        sample_file = Path("data/sample_inputs/nmap_sample.xml")
        if sample_file.exists():
            print("Testing with sample data...")
            findings = nmap_parser.parse(str(sample_file))
            print(f"✅ Sample parsing successful: {len(findings)} findings")
            return True
        else:
            print("⚠️  Sample data not found, skipping parse test")
            return True
            
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def provide_fixes():
    """Provide common fixes"""
    print_section("Common Fixes")
    
    print("🔧 Quick Fixes:")
    print("1. Install missing dependencies:")
    print("   pip install -r requirements.txt")
    print()
    
    print("2. Install system dependencies for PDF:")
    print("   ./install_dependencies.sh")
    print()
    
    print("3. Fix file permissions:")
    print("   chmod +x interactive.py setup.sh install.sh")
    print()
    
    print("4. Configure OpenAI API key:")
    print("   ./interactive.py")
    print("   Choose: Quick actions -> Configure OpenAI API key")
    print()
    
    print("5. Test PDF generation:")
    print("   python3 -c 'from exporters.pdf_exporter import test_pdf_export; test_pdf_export()'")
    print()
    
    print("6. Reinstall from scratch:")
    print("   rm -rf cybersec-ai-autoreport")
    print("   curl -fsSL https://raw.githubusercontent.com/gh0st-bit/cybersec-ai-autoreport/main/install.sh | bash")

def main():
    """Main diagnostic function"""
    print_header("CyberSec-AI AutoReport - Diagnostic Tool")
    
    print("🔍 Running comprehensive system check...")
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Dependencies", check_dependencies),
        ("System Dependencies", check_system_dependencies),
        ("OpenAI Configuration", check_openai_config),
        ("Project Structure", check_file_structure),
        ("File Permissions", check_permissions),
        ("Basic Functionality", run_basic_test)
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results[name] = False
    
    # Summary
    print_section("Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Checks passed: {passed}/{total}")
    print()
    
    if passed == total:
        print("🎉 All checks passed! Your system is ready.")
        print("Run: ./interactive.py to get started")
    else:
        print("⚠️  Some issues found. See details above.")
        provide_fixes()
        
        # Critical issues
        if not results.get("Python Version", False):
            print("\n🚨 CRITICAL: Python version incompatible")
        elif not results.get("Python Dependencies", False):
            print("\n🚨 CRITICAL: Missing Python dependencies")
        elif not results.get("Project Structure", False):
            print("\n🚨 CRITICAL: Project structure incomplete")
        else:
            print("\n💡 Non-critical issues found - tool may still work with limitations")

if __name__ == "__main__":
    main()
