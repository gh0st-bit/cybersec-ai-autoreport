#!/usr/bin/env python3
"""
CyberSec-AI AutoReport Demo Test
Demonstrates all functionality of the tool
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Exit code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Error running command: {e}")
        return False

def main():
    """Run comprehensive demo test"""
    print("[SHIELD] CyberSec-AI AutoReport - Comprehensive Demo Test")
    print("=" * 60)
    
    # Get Python executable path
    python_exe = '"C:/Users/27668/OneDrive - Riphah International University/Documents/CYB-8-1 AI-Reporting_tool/.venv/Scripts/python.exe"'
    
    tests = [
        # 1. Test CLI Help
        (f"{python_exe} main.py --help", "Testing CLI Help"),
        
        # 2. Test Parsers
        (f"{python_exe} main.py parse --input data/sample_inputs/nmap_sample.xml --type nmap --output test_nmap_parsed.json", "Testing Nmap Parser"),
        (f"{python_exe} main.py parse --input data/sample_inputs/burp_sample.xml --type burp --output test_burp_parsed.json", "Testing Burp Parser"),
        (f"{python_exe} main.py parse --input data/sample_inputs/nuclei_sample.json --type nuclei --output test_nuclei_parsed.json", "Testing Nuclei Parser"),
        
        # 3. Test AI Enhancement
        (f"{python_exe} main.py enhance --file test_nmap_parsed.json --output test_enhanced.json", "Testing AI Enhancement"),
        
        # 4. Test Export
        (f"{python_exe} main.py export --file test_enhanced.json --format html --output test_export.html", "Testing HTML Export"),
        
        # 5. Test Full Report Generation
        (f"{python_exe} main.py full-report --input data/sample_inputs/nmap_sample.xml --type nmap --format html", "Testing Full Report Pipeline"),
        
        # 6. Test Tools
        (f"{python_exe} main.py tools list", "Testing Tools Listing"),
    ]
    
    passed = 0
    failed = 0
    
    for cmd, description in tests:
        success = run_command(cmd, description)
        if success:
            passed += 1
            print("[OK] PASSED")
        else:
            failed += 1
            print("[ERROR] FAILED")
    
    # Summary
    print(f"\n{'='*60}")
    print("[STATS] TEST SUMMARY")
    print(f"{'='*60}")
    print(f"[OK] Passed: {passed}")
    print(f"[ERROR] Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("[SUCCESS] All tests passed! CyberSec-AI AutoReport is fully functional!")
    else:
        print("[WARNING] Some tests failed. Check the logs above for details.")
    
    # Show generated files
    print(f"\n[FILES] Generated Files:")
    report_files = list(Path("reports").glob("*.html")) if Path("reports").exists() else []
    for file in sorted(report_files):
        print(f"  [FILE] {file}")

if __name__ == "__main__":
    main()
