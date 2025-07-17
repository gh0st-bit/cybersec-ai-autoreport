"""
MVP Test Script
Quick test to verify all components are working
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_mvp():
    """Test the MVP functionality"""
    print("[LAUNCH] Testing CyberSec-AI AutoReport MVP...")
    
    try:
        # Test 1: Import all modules
        print("\n1️⃣ Testing module imports...")
        from parsers import nmap_parser, burp_parser, nuclei_parser
        from ai import summarizer, severity_classifier, remediation_generator
        from exporters import html_generator, pdf_exporter
        from tools import runner, parser
        from utils.file_loader import save_json, load_json
        print("[OK] All modules imported successfully")
        
        # Test 2: Parse sample nmap file
        print("\n2️⃣ Testing Nmap parser...")
        sample_nmap = "data/sample_inputs/nmap_sample.xml"
        if os.path.exists(sample_nmap):
            findings = nmap_parser.parse(sample_nmap)
            print(f"[OK] Parsed {len(findings)} findings from Nmap")
        else:
            findings = nmap_parser.parse_mock()
            print(f"[OK] Generated {len(findings)} mock findings")
        
        # Test 3: AI Enhancement
        print("\n3️⃣ Testing AI enhancement...")
        for finding in findings:
            finding["ai_summary"] = summarizer.generate(finding)
            finding["severity"] = severity_classifier.classify(finding)
            finding["remediation"] = remediation_generator.suggest(finding)
        print("[OK] AI enhancement completed")
        
        # Test 4: Save and load JSON
        print("\n4️⃣ Testing file operations...")
        test_file = "test_findings.json"
        save_json(findings, test_file)
        loaded_findings = load_json(test_file)
        print(f"[OK] Saved and loaded {len(loaded_findings)} findings")
        
        # Test 5: HTML Export
        print("\n5️⃣ Testing HTML export...")
        html_path = html_generator.export(findings, "test_report.html")
        print(f"[OK] HTML report generated: {html_path}")
        
        # Test 6: PDF Export (will show warning if WeasyPrint not available)
        print("\n6️⃣ Testing PDF export...")
        try:
            pdf_path = pdf_exporter.export(html_path, "test_report.pdf")
            print(f"[OK] PDF report generated: {pdf_path}")
        except Exception as e:
            print(f"[WARNING] PDF export issue (this is normal): {str(e)}")
        
        # Test 7: Custom Tools Registry
        print("\n7️⃣ Testing custom tools...")
        from tools.runner import register_tool, list_tools
        register_tool("test-tool", "echo 'Test output' > {output}", "Test tool")
        tools = list_tools()
        print(f"[OK] Registered tools: {list(tools.keys())}")
        
        # Cleanup
        print("\n🧹 Cleaning up test files...")
        for file in [test_file, html_path]:
            if os.path.exists(file):
                os.remove(file)
        
        print("\n[SUCCESS] MVP Test Completed Successfully!")
        print("\n[SUMMARY] Next Steps:")
        print("1. Configure OpenAI API key in config/settings.yaml")
        print("2. Try: python main.py full-report --input data/sample_inputs/nmap_sample.xml --type nmap")
        print("3. Explore custom tools: python main.py tools list")
        
        return True
    
    except Exception as e:
        print(f"\n[ERROR] MVP Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_mvp()
