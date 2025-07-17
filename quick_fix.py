#!/usr/bin/env python3
"""
CyberSec-AI AutoReport - Quick Fix Tool
Provides automated fixes for common issues
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_section(title):
    """Print section header"""
    print(f"\n--- {title} ---")

def fix_file_permissions():
    """Fix file permissions for executable files"""
    print_section("Fixing File Permissions")
    
    executable_files = [
        'interactive.py',
        'auto_detect.py', 
        'diagnose.py',
        'quick_fix.py',
        'setup.sh',
        'install.sh',
        'install_dependencies.sh'
    ]
    
    fixed_count = 0
    
    for file_name in executable_files:
        if Path(file_name).exists():
            try:
                # Make executable (Linux/Mac)
                if sys.platform != 'win32':
                    subprocess.run(['chmod', '+x', file_name], check=True)
                    print(f"✅ Made {file_name} executable")
                    fixed_count += 1
                else:
                    print(f"ℹ️  {file_name} (Windows - no chmod needed)")
            except Exception as e:
                print(f"❌ Failed to fix {file_name}: {e}")
        else:
            print(f"⚠️  {file_name} not found")
    
    print(f"\n📋 Fixed permissions for {fixed_count} files")
    return fixed_count > 0

def fix_python_dependencies():
    """Fix Python dependencies"""
    print_section("Fixing Python Dependencies")
    
    try:
        # Check if requirements.txt exists
        if not Path('requirements.txt').exists():
            print("❌ requirements.txt not found")
            return False
        
        # Install/update dependencies
        print("📦 Installing/updating Python dependencies...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing Python dependencies: {e}")
        return False

def fix_directory_structure():
    """Fix directory structure"""
    print_section("Fixing Directory Structure")
    
    required_dirs = [
        'config',
        'templates', 
        'parsers',
        'exporters',
        'ai',
        'tools',
        'utils',
        'data',
        'data/sample_inputs',
        'outputs',
        'reports'
    ]
    
    created_count = 0
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created directory: {dir_name}")
                created_count += 1
            except Exception as e:
                print(f"❌ Failed to create {dir_name}: {e}")
        else:
            print(f"✅ Directory exists: {dir_name}")
    
    print(f"\n📋 Created {created_count} directories")
    return created_count > 0

def fix_config_file():
    """Fix configuration file"""
    print_section("Fixing Configuration File")
    
    config_path = Path('config/settings.yaml')
    
    if config_path.exists():
        print("✅ Configuration file exists")
        
        # Check if it needs fixing
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                
            if 'your_openai_api_key_here' in content:
                print("⚠️  OpenAI API key needs configuration")
                print("💡 Run './interactive.py' and choose 'Configure OpenAI API key'")
            else:
                print("✅ Configuration appears to be set up")
                
        except Exception as e:
            print(f"⚠️  Could not read config file: {e}")
            
        return True
        
    else:
        print("❌ Configuration file missing")
        
        # Create default config
        try:
            config_content = '''# CyberSec-AI AutoReport Configuration
openai:
  api_key: "your_openai_api_key_here"
  model: "gpt-3.5-turbo"
  temperature: 0.5
  max_tokens: 1500

report:
  title: "Cybersecurity Assessment Report"
  company: "Your Company Name"
  author: "Security Team"
  template: "default"

paths:
  templates: "templates"
  outputs: "outputs"
  reports: "reports"
  tools_registry: "tools/registry.json"

export:
  formats: ["html", "pdf"]
  default_format: "pdf"

tools:
  timeout: 300
  max_output_size: 10485760
'''
            
            with open(config_path, 'w') as f:
                f.write(config_content)
                
            print("✅ Created default configuration file")
            print("💡 Run './interactive.py' to configure your OpenAI API key")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create config file: {e}")
            return False

def fix_pdf_dependencies():
    """Fix PDF generation dependencies"""
    print_section("Fixing PDF Dependencies")
    
    # Check WeasyPrint
    try:
        from weasyprint import HTML
        print("✅ WeasyPrint is available")
        weasyprint_ok = True
    except ImportError:
        print("❌ WeasyPrint not available")
        weasyprint_ok = False
    except Exception as e:
        print(f"⚠️  WeasyPrint has issues: {e}")
        weasyprint_ok = False
    
    # Check wkhtmltopdf
    wkhtmltopdf_ok = False
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ wkhtmltopdf is available")
            wkhtmltopdf_ok = True
        else:
            print("❌ wkhtmltopdf not working")
    except:
        print("❌ wkhtmltopdf not found")
    
    # Check Chrome
    chrome_ok = False
    chrome_commands = ['google-chrome', 'chromium-browser', 'chromium']
    
    for cmd in chrome_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {cmd} is available")
                chrome_ok = True
                break
        except:
            continue
    
    if not chrome_ok:
        print("❌ Chrome/Chromium not found")
    
    # Provide recommendations
    if not weasyprint_ok and not wkhtmltopdf_ok and not chrome_ok:
        print("\n⚠️  No PDF generation methods available!")
        print("💡 Recommendations:")
        print("   1. Run: ./install_dependencies.sh")
        print("   2. Install WeasyPrint: pip install weasyprint")
        print("   3. Install wkhtmltopdf: sudo apt-get install wkhtmltopdf")
        print("   4. Install Chrome: sudo apt-get install chromium-browser")
        return False
    else:
        print("\n✅ At least one PDF generation method is available")
        return True

def fix_sample_data():
    """Fix sample data"""
    print_section("Fixing Sample Data")
    
    sample_dir = Path('data/sample_inputs')
    sample_file = sample_dir / 'nmap_sample.xml'
    
    if sample_file.exists():
        print("✅ Sample data exists")
        return True
    
    print("❌ Sample data missing")
    
    # Create sample nmap XML
    try:
        sample_content = '''<?xml version="1.0" encoding="UTF-8"?>
<nmaprun scanner="nmap" args="nmap -sV -sC 192.168.1.1" start="1642680000" startstr="Thu Jan 20 12:00:00 2022" version="7.80">
    <host>
        <address addr="192.168.1.1" addrtype="ipv4"/>
        <ports>
            <port protocol="tcp" portid="22">
                <state state="open" reason="syn-ack"/>
                <service name="ssh" version="OpenSSH 7.4"/>
            </port>
            <port protocol="tcp" portid="80">
                <state state="open" reason="syn-ack"/>
                <service name="http" version="nginx 1.16.1"/>
            </port>
            <port protocol="tcp" portid="443">
                <state state="open" reason="syn-ack"/>
                <service name="https" version="nginx 1.16.1"/>
            </port>
        </ports>
    </host>
</nmaprun>'''
        
        with open(sample_file, 'w') as f:
            f.write(sample_content)
            
        print("✅ Created sample nmap data")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def run_basic_test():
    """Run basic functionality test"""
    print_section("Running Basic Test")
    
    try:
        # Test main.py
        result = subprocess.run([sys.executable, 'main.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ main.py is working")
            
            # Test with sample data
            sample_file = Path('data/sample_inputs/nmap_sample.xml')
            if sample_file.exists():
                print("🧪 Testing with sample data...")
                result = subprocess.run([
                    sys.executable, 'main.py', 'full-report',
                    '--input', str(sample_file),
                    '--type', 'nmap',
                    '--format', 'html'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print("✅ Sample report generation successful")
                    return True
                else:
                    print(f"⚠️  Sample report generation failed: {result.stderr}")
                    return False
            else:
                print("⚠️  No sample data for testing")
                return True
                
        else:
            print(f"❌ main.py failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def main():
    """Main fix function"""
    print_header("CyberSec-AI AutoReport - Quick Fix Tool")
    
    print("🔧 This tool will attempt to fix common issues automatically")
    print("⚠️  Some fixes may require sudo privileges")
    print()
    
    if not input("Continue? (y/n): ").lower().startswith('y'):
        print("Aborted.")
        return
    
    fixes = [
        ("File Permissions", fix_file_permissions),
        ("Directory Structure", fix_directory_structure), 
        ("Configuration File", fix_config_file),
        ("Python Dependencies", fix_python_dependencies),
        ("PDF Dependencies", fix_pdf_dependencies),
        ("Sample Data", fix_sample_data),
        ("Basic Functionality", run_basic_test)
    ]
    
    results = {}
    
    for name, fix_func in fixes:
        print_header(f"Fixing: {name}")
        
        try:
            results[name] = fix_func()
        except Exception as e:
            print(f"❌ {name} fix failed: {e}")
            results[name] = False
    
    # Summary
    print_header("Fix Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Fixes applied: {passed}/{total}")
    print()
    
    for name, success in results.items():
        status = "✅ FIXED" if success else "❌ FAILED"
        print(f"{status}: {name}")
    
    print()
    
    if passed == total:
        print("🎉 All fixes applied successfully!")
        print("💡 Try running: ./interactive.py")
    else:
        print("⚠️  Some fixes failed. Manual intervention may be required.")
        print("💡 Run: ./diagnose.py for detailed analysis")
        
        if not results.get("Python Dependencies", False):
            print("\n🚨 Critical: Python dependencies failed")
            print("   Try: pip install -r requirements.txt")
        
        if not results.get("PDF Dependencies", False):
            print("\n🚨 Critical: PDF dependencies failed")
            print("   Try: ./install_dependencies.sh")

if __name__ == "__main__":
    main()
    try:
        subprocess.run(['xdg-open', '--version'], check=True, capture_output=True)
        print("✅ xdg-open is available")
    except:
        print("📦 Installing xdg-utils...")
        try:
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'xdg-utils'], check=True)
            print("✅ xdg-utils installed")
        except:
            print("❌ Failed to install xdg-utils")
            return False
    
    return True

def fix_pdf_generation():
    """Fix PDF generation issues"""
    print("🔧 Fixing PDF generation issues...")
    
    # Check WeasyPrint system dependencies
    system_deps = [
        'libcairo2-dev', 'libpango1.0-dev', 'libgdk-pixbuf2.0-dev',
        'libffi-dev', 'shared-mime-info', 'libxml2-dev', 'libxslt1-dev'
    ]
    
    print("📦 Installing WeasyPrint system dependencies...")
    try:
        cmd = ['sudo', 'apt-get', 'install', '-y'] + system_deps
        subprocess.run(cmd, check=True)
        print("✅ System dependencies installed")
    except:
        print("❌ Failed to install system dependencies")
        return False
    
    # Test WeasyPrint
    try:
        from weasyprint import HTML
        HTML(string="<h1>Test</h1>").write_pdf("/tmp/test.pdf")
        os.remove("/tmp/test.pdf")
        print("✅ WeasyPrint is working")
        return True
    except Exception as e:
        print(f"❌ WeasyPrint still not working: {e}")
        return False

def fix_openai_config():
    """Fix OpenAI configuration"""
    print("🔧 Fixing OpenAI configuration...")
    
    config_path = Path("config/settings.yaml")
    if not config_path.exists():
        print("❌ Config file not found")
        return False
    
    # Read config
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        api_key = config.get('openai', {}).get('api_key', '')
        
        if not api_key or api_key == 'your_openai_api_key_here':
            print("⚠️  OpenAI API key not configured")
            new_key = input("Enter OpenAI API key (or press Enter to skip): ").strip()
            
            if new_key:
                config['openai']['api_key'] = new_key
                with open(config_path, 'w') as f:
                    yaml.safe_dump(config, f, default_flow_style=False)
                print("✅ API key updated")
                return True
            else:
                print("⚠️  Skipping API key configuration")
                return False
        else:
            print("✅ API key is already configured")
            return True
            
    except Exception as e:
        print(f"❌ Config fix failed: {e}")
        return False

def fix_permissions():
    """Fix file permissions"""
    print("🔧 Fixing file permissions...")
    
    executable_files = ['interactive.py', 'setup.sh', 'install.sh', 'diagnose.py']
    
    for file_name in executable_files:
        if Path(file_name).exists():
            try:
                os.chmod(file_name, 0o755)
                print(f"✅ Fixed permissions for {file_name}")
            except:
                print(f"❌ Failed to fix permissions for {file_name}")
        else:
            print(f"⚠️  {file_name} not found")
    
    return True

def main():
    """Main fix function"""
    print("🔧 CyberSec-AI AutoReport - Quick Fix Tool")
    print("=" * 50)
    
    fixes = [
        ("Browser Opening", fix_browser_opening),
        ("PDF Generation", fix_pdf_generation),
        ("OpenAI Configuration", fix_openai_config),
        ("File Permissions", fix_permissions)
    ]
    
    print("Available fixes:")
    for i, (name, _) in enumerate(fixes, 1):
        print(f"{i}. {name}")
    print("0. Run all fixes")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    if choice == '0':
        # Run all fixes
        for name, fix_func in fixes:
            print(f"\n--- {name} ---")
            try:
                fix_func()
            except Exception as e:
                print(f"❌ {name} fix failed: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(fixes):
        # Run specific fix
        name, fix_func = fixes[int(choice) - 1]
        print(f"\n--- {name} ---")
        try:
            fix_func()
        except Exception as e:
            print(f"❌ {name} fix failed: {e}")
    else:
        print("Invalid choice")
    
    print("\n🎯 Quick fix completed!")
    print("Run './diagnose.py' to check system status")

if __name__ == "__main__":
    main()
