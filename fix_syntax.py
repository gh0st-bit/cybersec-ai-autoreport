#!/usr/bin/env python3
"""
Quick IndentationError Fix for CyberSec-AI AutoReport
This script checks and fixes Python syntax errors
"""

import ast
import sys
import os
import subprocess
from pathlib import Path

def check_python_syntax(filepath):
    """Check if a Python file has valid syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def fix_common_issues():
    """Fix common Python syntax issues"""
    files_to_check = ['main.py', 'interactive.py', 'auto_detect.py']
    
    print("🔍 Checking Python files for syntax errors...")
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"  Checking {filename}...")
            is_valid, error = check_python_syntax(filename)
            
            if is_valid:
                print(f"    ✅ {filename} - OK")
            else:
                print(f"    ❌ {filename} - ERROR: {error}")
                
                # Try to fix by recompiling
                try:
                    result = subprocess.run(['python3', '-m', 'py_compile', filename], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"    ✅ {filename} - Fixed!")
                    else:
                        print(f"    ❌ {filename} - Cannot fix: {result.stderr}")
                except Exception as e:
                    print(f"    ❌ {filename} - Cannot fix: {e}")
        else:
            print(f"  ⚠️  {filename} - Not found")

def test_imports():
    """Test if key modules can be imported"""
    print("\n🧪 Testing module imports...")
    
    modules_to_test = [
        ('main', 'main.py'),
        ('interactive', 'interactive.py'),
        ('parsers.nmap_parser', 'parsers/nmap_parser.py'),
        ('exporters.html_generator', 'exporters/html_generator.py'),
        ('tools.runner', 'tools/runner.py')
    ]
    
    for module_name, file_path in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name} - Import OK")
        except ImportError as e:
            print(f"  ❌ {module_name} - Import failed: {e}")
        except SyntaxError as e:
            print(f"  ❌ {module_name} - Syntax error: {e}")
        except Exception as e:
            print(f"  ❌ {module_name} - Error: {e}")

def main():
    """Main function"""
    print("🛠️  CyberSec-AI AutoReport - Syntax Fix Tool")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ main.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Fix common issues
    fix_common_issues()
    
    # Test imports
    test_imports()
    
    # Test CLI
    print("\n🎯 Testing CLI functionality...")
    try:
        result = subprocess.run(['python3', 'main.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("  ✅ CLI - Working correctly")
        else:
            print(f"  ❌ CLI - Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("  ❌ CLI - Timeout")
    except Exception as e:
        print(f"  ❌ CLI - Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Diagnosis complete!")
    print("\n💡 If you're still getting IndentationError:")
    print("1. Make sure you're using Python 3.8+")
    print("2. Check that your terminal encoding is UTF-8")
    print("3. Try running: python3 -c 'import main; print(\"OK\")'")
    print("4. If issues persist, delete and re-clone the repository")

if __name__ == "__main__":
    main()
