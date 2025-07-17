#!/usr/bin/env python3
"""
Demo script for the new advanced export system
Showcases industrial-level report generation capabilities
"""

import sys
import json
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🏭 CyberSec-AI Advanced Export System Demo")
print("=" * 50)

# Demo sample findings
demo_findings = [
    {
        "title": "Critical SQL Injection",
        "description": "SQL injection vulnerability in user authentication",
        "severity": "Critical",
        "cvss_score": 9.8,
        "risk_level": "Critical",
        "affected_url": "https://demo.com/login",
        "parameter": "username",
        "method": "POST",
        "evidence": "' OR '1'='1 -- -",
        "ai_summary": "Critical SQL injection allowing complete database compromise",
        "remediation": "Implement parameterized queries and input validation",
        "references": ["CWE-89", "OWASP-A03"],
        "cwe_id": "CWE-89",
        "impact": "Critical",
        "confidence": "Confirmed"
    },
    {
        "title": "Cross-Site Scripting (XSS)",
        "description": "Stored XSS in user comments",
        "severity": "High",
        "cvss_score": 7.2,
        "risk_level": "High",
        "affected_url": "https://demo.com/comments",
        "parameter": "comment",
        "method": "POST",
        "evidence": "<script>alert('XSS')</script>",
        "ai_summary": "Stored XSS allowing persistent script execution",
        "remediation": "Implement output encoding and CSP",
        "references": ["CWE-79", "OWASP-A07"],
        "cwe_id": "CWE-79",
        "impact": "High",
        "confidence": "Confirmed"
    },
    {
        "title": "Insecure Authentication",
        "description": "Weak password policy implementation",
        "severity": "Medium",
        "cvss_score": 6.5,
        "risk_level": "Medium",
        "affected_url": "https://demo.com/register",
        "parameter": "password",
        "method": "POST",
        "evidence": "Allows passwords like '123456'",
        "ai_summary": "Weak authentication controls increase breach risk",
        "remediation": "Implement strong password policies and MFA",
        "references": ["CWE-521", "OWASP-A07"],
        "cwe_id": "CWE-521",
        "impact": "Medium",
        "confidence": "Confirmed"
    }
]

try:
    print("📊 Available Export Formats:")
    from exporters import get_export_info
    info = get_export_info()
    
    print(f"  • HTML Templates: {', '.join(info['html_templates'])}")
    print(f"  • PDF Formats: {', '.join(info['pdf_formats'])}")
    print(f"  • Multi Formats: {', '.join(info['multi_formats'])}")
    print(f"  • Compliance: {', '.join(info['compliance_formats'])}")
    print(f"  • Recommended PDF: {info['recommended_pdf_method']}")
    
    print("\n🎯 Generating Demo Reports...")
    
    # Executive Summary
    print("📋 Generating Executive Summary...")
    from exporters import export_executive_summary
    exec_files = export_executive_summary(demo_findings, "demo_executive")
    print(f"  ✅ Generated: {exec_files}")
    
    # Technical Report
    print("🔧 Generating Technical Report...")
    from exporters import export_technical_report
    tech_files = export_technical_report(demo_findings, "demo_technical")
    print(f"  ✅ Generated: {tech_files}")
    
    # Compliance Pack
    print("🛡️ Generating Compliance Pack...")
    from exporters import export_compliance_pack
    compliance_files = export_compliance_pack(demo_findings, "demo_compliance")
    print(f"  ✅ Generated: {compliance_files}")
    
    print("\n🎉 Demo Complete!")
    print("\nGenerated Files:")
    import glob
    for pattern in ["demo_*"]:
        for file_path in glob.glob(pattern):
            size = os.path.getsize(file_path)
            print(f"  📄 {file_path} ({size} bytes)")
    
    print("\n📖 Usage Examples:")
    print("  python main.py full-report -i scan.xml -fmt executive")
    print("  python main.py full-report -i scan.json -fmt compliance")
    print("  python main.py full-report -i scan.xml -fmt all")
    print("  python main.py export -f findings.json -fmt pdf --advanced")
    print("  python main.py export-info")
    
except Exception as e:
    print(f"❌ Demo failed: {str(e)}")
    print("💡 Make sure all export modules are properly installed")
    sys.exit(1)

print("\n🚀 Ready to generate industrial-level security reports!")
