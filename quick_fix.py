#!/usr/bin/env python3
"""
Quick Fix Script for Common Issues
"""

import os
import sys
import subprocess
from pathlib import Path

def fix_browser_opening():
    """Fix browser opening issues on Linux"""
    print("🔧 Fixing browser opening issues...")
    
    # Check if running in headless environment
    if not os.getenv('DISPLAY') and not os.getenv('WAYLAND_DISPLAY'):
        print("⚠️  Running in headless environment - browser opening disabled")
        return False
    
    # Install xdg-utils if missing
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
