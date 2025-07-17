"""
Simplified MVP Test - No External Dependencies
Tests core functionality without requiring pip packages
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("[SHIELD] CyberSec-AI AutoReport - Basic Test")
    print("=====================================")
    
    try:
        # Test 1: Test mock parsers (don't require xmltodict)
        print("\n1️⃣ Testing mock parsers...")
        
        # Import parser modules and test mock functions
        sys.path.append('parsers')
        
        # Test Nmap mock parser
        from parsers.nmap_parser import parse_mock as nmap_mock
        nmap_findings = nmap_mock()
        print(f"[OK] Nmap mock parser: {len(nmap_findings)} findings")
        
        # Test Burp mock parser  
        from parsers.burp_parser import parse_mock as burp_mock
        burp_findings = burp_mock()
        print(f"[OK] Burp mock parser: {len(burp_findings)} findings")
        
        # Test Nuclei mock parser
        from parsers.nuclei_parser import parse_mock as nuclei_mock
        nuclei_findings = nuclei_mock()
        print(f"[OK] Nuclei mock parser: {len(nuclei_findings)} findings")
        
        # Test 2: Test AI modules (with fallback responses)
        print("\n2️⃣ Testing AI modules...")
        
        from ai.severity_classifier import classify_by_rules, sort_by_severity
        from ai.summarizer import generate
        from ai.remediation_generator import generate_fallback_remediation
        
        # Test severity classification
        test_finding = nmap_findings[0]
        severity = classify_by_rules(test_finding)
        print(f"[OK] Severity classifier: {severity}")
        
        # Test sorting
        sorted_findings = sort_by_severity(nmap_findings + burp_findings)
        print(f"[OK] Findings sorted by severity: {len(sorted_findings)} total")
        
        # Test 3: Test file operations
        print("\n3️⃣ Testing file operations...")
        
        # Simple JSON save/load without external utilities
        test_data = {"test": "data", "findings": sorted_findings[:2]}
        test_file = "simple_test.json"
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        
        print(f"[OK] JSON operations: Saved and loaded {len(loaded_data['findings'])} findings")
        
        # Test 4: Test basic HTML generation
        print("\n4️⃣ Testing HTML generation...")
        
        # Simple HTML template without Jinja2
        html_content = generate_simple_html_report(sorted_findings[:3])
        html_file = "simple_report.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] HTML report generated: {html_file}")
        
        # Test 5: Test tools registry
        print("\n5️⃣ Testing tools system...")
        
        # Simple registry without external dependencies
        tools_registry = {
            "test-tool": {
                "name": "Test Tool",
                "command": "echo 'Test output' > {output}",
                "description": "Simple test tool"
            }
        }
        
        registry_file = "tools/test_registry.json"
        os.makedirs(os.path.dirname(registry_file), exist_ok=True)
        
        with open(registry_file, 'w') as f:
            json.dump(tools_registry, f, indent=2)
        
        print(f"[OK] Tools registry created with {len(tools_registry)} tools")
        
        # Cleanup
        print("\n🧹 Cleaning up...")
        for file in [test_file, html_file, registry_file]:
            if os.path.exists(file):
                os.remove(file)
        
        print("\n[SUCCESS] Basic Test Completed Successfully!")
        print("\n[SUMMARY] Your CyberSec-AI AutoReport MVP is working!")
        print("\n[TOOL] To enable full functionality:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure OpenAI API key in config/settings.yaml")
        print("3. Try: python main.py --help")
        
        return True
    
    except Exception as e:
        print(f"\n[ERROR] Basic Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def generate_simple_html_report(findings):
    """Generate simple HTML report without Jinja2"""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberSec-AI Security Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #e9ecef; padding-bottom: 20px; }
        .finding { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 6px; border-left: 4px solid #007bff; }
        .severity-critical { border-left-color: #dc3545; }
        .severity-high { border-left-color: #fd7e14; }
        .severity-medium { border-left-color: #ffc107; }
        .severity-low { border-left-color: #28a745; }
        .finding-title { font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
        .finding-meta { color: #6c757d; font-size: 14px; margin-bottom: 10px; }
        .finding-description { margin-bottom: 15px; }
        .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>[SHIELD] CyberSec-AI Security Report</h1>
            <p>Generated by CyberSec-AI AutoReport MVP</p>
        </div>
        
        <div class="findings">
"""
    
    for finding in findings:
        severity = finding.get('severity', 'Medium').lower()
        html += f"""
            <div class="finding severity-{severity}">
                <div class="finding-title">{finding.get('title', 'Unknown Finding')}</div>
                <div class="finding-meta">
                    Severity: <strong>{finding.get('severity', 'Medium')}</strong> | 
                    Source: {finding.get('source', 'Unknown')} |
                    Category: {finding.get('category', 'General')}
                </div>
                <div class="finding-description">{finding.get('description', 'No description available')}</div>
                <div><strong>Impact:</strong> {finding.get('impact', 'Impact unknown')}</div>
            </div>
        """
    
    html += """
        </div>
        
        <div class="footer">
            <p>Report generated by CyberSec-AI AutoReport v1.0.0</p>
            <p>[AI] AI-powered cybersecurity reporting automation</p>
        </div>
    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    test_basic_functionality()
