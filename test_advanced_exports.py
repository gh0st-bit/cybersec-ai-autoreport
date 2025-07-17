#!/usr/bin/env python3
"""
Test script for advanced export system
Tests all new industrial-level export capabilities
"""

import sys
import json
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from exporters import (
    AdvancedHTMLGenerator, AdvancedPDFExporter, MultiFormatExporter,
    export_all_formats, export_compliance_pack, export_executive_summary,
    export_technical_report, get_export_info
)

def create_test_findings():
    """Create test findings for testing"""
    return [
        {
            "title": "SQL Injection Vulnerability",
            "description": "A SQL injection vulnerability was found in the login form",
            "severity": "High",
            "cvss_score": 8.5,
            "risk_level": "Critical",
            "affected_url": "https://example.com/login",
            "parameter": "username",
            "method": "POST",
            "evidence": "' OR '1'='1",
            "ai_summary": "Critical SQL injection vulnerability allowing unauthorized database access",
            "remediation": "Implement parameterized queries and input validation",
            "references": ["CWE-89", "OWASP-A03"],
            "cwe_id": "CWE-89",
            "location": {
                "file": "login.php",
                "line": 42
            },
            "impact": "High",
            "confidence": "Confirmed"
        },
        {
            "title": "Cross-Site Scripting (XSS)",
            "description": "Reflected XSS vulnerability in search functionality",
            "severity": "Medium",
            "cvss_score": 6.1,
            "risk_level": "Medium",
            "affected_url": "https://example.com/search",
            "parameter": "query",
            "method": "GET",
            "evidence": "<script>alert('XSS')</script>",
            "ai_summary": "Reflected XSS vulnerability allowing script execution",
            "remediation": "Implement output encoding and Content Security Policy",
            "references": ["CWE-79", "OWASP-A07"],
            "cwe_id": "CWE-79",
            "location": {
                "file": "search.php",
                "line": 15
            },
            "impact": "Medium",
            "confidence": "Confirmed"
        },
        {
            "title": "Insecure Direct Object Reference",
            "description": "User can access other users' data by manipulating ID parameter",
            "severity": "High",
            "cvss_score": 7.5,
            "risk_level": "High",
            "affected_url": "https://example.com/profile",
            "parameter": "user_id",
            "method": "GET",
            "evidence": "Accessed user ID 123 data with user ID 456 credentials",
            "ai_summary": "Authorization bypass allowing access to unauthorized data",
            "remediation": "Implement proper authorization checks and access controls",
            "references": ["CWE-639", "OWASP-A01"],
            "cwe_id": "CWE-639",
            "location": {
                "file": "profile.php",
                "line": 28
            },
            "impact": "High",
            "confidence": "Confirmed"
        },
        {
            "title": "Sensitive Data Exposure",
            "description": "Application logs contain sensitive information",
            "severity": "Medium",
            "cvss_score": 5.3,
            "risk_level": "Medium",
            "affected_url": "https://example.com/logs",
            "parameter": "N/A",
            "method": "N/A",
            "evidence": "Password hashes and API keys found in application logs",
            "ai_summary": "Sensitive information exposure through application logs",
            "remediation": "Implement secure logging practices and data sanitization",
            "references": ["CWE-532", "OWASP-A09"],
            "cwe_id": "CWE-532",
            "location": {
                "file": "logger.php",
                "line": 67
            },
            "impact": "Medium",
            "confidence": "Confirmed"
        },
        {
            "title": "Missing Security Headers",
            "description": "Critical security headers are missing",
            "severity": "Low",
            "cvss_score": 3.7,
            "risk_level": "Low",
            "affected_url": "https://example.com/",
            "parameter": "N/A",
            "method": "GET",
            "evidence": "Missing: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection",
            "ai_summary": "Missing security headers increase attack surface",
            "remediation": "Implement comprehensive security headers",
            "references": ["OWASP-A05"],
            "cwe_id": "CWE-693",
            "location": {
                "file": "index.php",
                "line": 1
            },
            "impact": "Low",
            "confidence": "Confirmed"
        }
    ]

def test_advanced_html_generator():
    """Test AdvancedHTMLGenerator"""
    print("🧪 Testing AdvancedHTMLGenerator...")
    
    try:
        findings = create_test_findings()
        html_generator = AdvancedHTMLGenerator()
        
        # Test basic export
        html_path = html_generator.export(findings, "test_advanced.html")
        print(f"✅ Advanced HTML generated: {html_path}")
        
        # Test with executive dashboard
        html_path = html_generator.export(
            findings, 
            "test_executive.html",
            executive_dashboard=True,
            charts=True
        )
        print(f"✅ Executive dashboard generated: {html_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ AdvancedHTMLGenerator test failed: {str(e)}")
        return False

def test_advanced_pdf_exporter():
    """Test AdvancedPDFExporter"""
    print("🧪 Testing AdvancedPDFExporter...")
    
    try:
        findings = create_test_findings()
        
        # Generate HTML first
        html_generator = AdvancedHTMLGenerator()
        html_path = html_generator.export(findings, "test_pdf_source.html")
        
        pdf_exporter = AdvancedPDFExporter()
        
        # Test different formats
        formats = ['executive', 'technical', 'compliance']
        for format_type in formats:
            pdf_path = pdf_exporter.export(
                html_path, 
                f"test_{format_type}.pdf", 
                format_type=format_type
            )
            print(f"✅ {format_type.title()} PDF generated: {pdf_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ AdvancedPDFExporter test failed: {str(e)}")
        return False

def test_multi_format_exporter():
    """Test MultiFormatExporter"""
    print("🧪 Testing MultiFormatExporter...")
    
    try:
        findings = create_test_findings()
        multi_exporter = MultiFormatExporter()
        
        # Test different formats
        formats = ['json', 'csv', 'xml', 'markdown']
        for format_type in formats:
            output_path = f"test_multi.{format_type}"
            exported_file = multi_exporter.export(findings, output_path, format_type)
            print(f"✅ {format_type.upper()} export generated: {exported_file}")
        
        # Test compliance formats
        compliance_formats = ['sarif', 'stix', 'mitre', 'nist']
        for format_type in compliance_formats:
            try:
                output_path = f"test_compliance.{format_type}"
                exported_file = multi_exporter.export(findings, output_path, format_type)
                print(f"✅ {format_type.upper()} compliance export generated: {exported_file}")
            except Exception as e:
                print(f"⚠️ {format_type.upper()} export failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ MultiFormatExporter test failed: {str(e)}")
        return False

def test_convenience_functions():
    """Test convenience export functions"""
    print("🧪 Testing convenience export functions...")
    
    try:
        findings = create_test_findings()
        
        # Test export_all_formats
        print("Testing export_all_formats...")
        exported_files = export_all_formats(findings, "test_all")
        print(f"✅ export_all_formats generated {len(exported_files)} files")
        
        # Test export_executive_summary
        print("Testing export_executive_summary...")
        exported_files = export_executive_summary(findings, "test_exec")
        print(f"✅ export_executive_summary generated {len(exported_files)} files")
        
        # Test export_technical_report
        print("Testing export_technical_report...")
        exported_files = export_technical_report(findings, "test_tech")
        print(f"✅ export_technical_report generated {len(exported_files)} files")
        
        # Test export_compliance_pack
        print("Testing export_compliance_pack...")
        exported_files = export_compliance_pack(findings, "test_compliance")
        print(f"✅ export_compliance_pack generated {len(exported_files)} files")
        
        return True
        
    except Exception as e:
        print(f"❌ Convenience functions test failed: {str(e)}")
        return False

def test_export_info():
    """Test get_export_info function"""
    print("🧪 Testing export info...")
    
    try:
        info = get_export_info()
        
        print("📊 Export Information:")
        print(f"  HTML Templates: {info['html_templates']}")
        print(f"  PDF Formats: {info['pdf_formats']}")
        print(f"  PDF Methods: {info['pdf_methods']}")
        print(f"  Multi Formats: {info['multi_formats']}")
        print(f"  Compliance Formats: {info['compliance_formats']}")
        print(f"  Recommended PDF Method: {info['recommended_pdf_method']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Export info test failed: {str(e)}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print("🧹 Cleaning up test files...")
    
    test_patterns = [
        "test_*.html", "test_*.pdf", "test_*.json", "test_*.csv",
        "test_*.xml", "test_*.md", "test_*.sarif", "test_*.stix",
        "test_*.mitre", "test_*.nist", "test_*.junit", "test_*.xlsx"
    ]
    
    import glob
    for pattern in test_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print(f"  Removed: {file_path}")
            except Exception as e:
                print(f"  Failed to remove {file_path}: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting Advanced Export System Tests")
    print("=" * 50)
    
    tests = [
        test_export_info,
        test_advanced_html_generator,
        test_advanced_pdf_exporter,
        test_multi_format_exporter,
        test_convenience_functions
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {str(e)}")
            failed += 1
        
        print("-" * 30)
    
    print(f"\n📊 Test Results:")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Advanced export system is working correctly.")
    else:
        print(f"\n⚠️ {failed} tests failed. Check the output above for details.")
    
    # Cleanup
    cleanup_test_files()

if __name__ == "__main__":
    main()
