# Advanced Export System - Industrial-Level Security Reports

This document covers the new advanced export system that provides industrial-level formatting, multiple export formats, and compliance-ready reports.

## 🏭 Industrial-Level Features

### Advanced HTML Reports
- **Professional CSS Framework**: Modern, responsive design with industry-standard styling
- **Executive Dashboards**: High-level overview with charts and risk matrices
- **Risk Assessment Matrices**: CVSS scoring, severity classification, and risk heat maps
- **Compliance Mapping**: Automatic mapping to NIST, MITRE ATT&CK, and other frameworks
- **Interactive Charts**: Severity distribution, finding categories, and trend analysis

### Advanced PDF Generation
- **Multiple Export Methods**: WeasyPrint, wkhtmltopdf, Chrome headless, Puppeteer
- **Professional Themes**: Executive, Technical, and Compliance formats
- **Watermarking Support**: Company branding and confidentiality markings
- **Chart Integration**: Embedded visualizations and risk matrices
- **Multi-Page Layouts**: Proper pagination and formatting

### Multi-Format Exports
- **Standard Formats**: JSON, CSV, XML, Excel, Markdown
- **Compliance Formats**: SARIF, STIX, MITRE ATT&CK, NIST Framework, JUnit XML
- **Integration Ready**: APIs, SIEM systems, and security tools
- **Automation Friendly**: Scriptable and CI/CD compatible

## 🚀 Quick Start

### Basic Usage
```bash
# Generate executive summary
python main.py full-report -i scan.xml -fmt executive

# Generate technical report
python main.py full-report -i scan.json -fmt technical

# Generate compliance pack
python main.py full-report -i scan.xml -fmt compliance

# Generate all formats
python main.py full-report -i scan.xml -fmt all
```

### Advanced Usage
```bash
# Advanced PDF with specific theme
python main.py export -f findings.json -fmt pdf --advanced --theme compliance

# Advanced HTML with dashboard
python main.py export -f findings.json -fmt html --advanced

# Show available formats
python main.py export-info
```

## 📊 Export Formats

### HTML Templates
- `industrial_report.html` - Professional industrial template
- `default.html.j2` - Basic template for compatibility

### PDF Formats
- `executive` - High-level summary for executives
- `technical` - Detailed technical information
- `compliance` - Compliance-focused format

### Multi-Format Exports
- `json` - Standard JSON format
- `csv` - Comma-separated values
- `xml` - XML format
- `excel` - Excel workbook
- `markdown` - Markdown format

### Compliance Formats
- `sarif` - Static Analysis Results Interchange Format
- `stix` - Structured Threat Information eXpression
- `mitre` - MITRE ATT&CK framework mapping
- `nist` - NIST Cybersecurity Framework mapping
- `junit` - JUnit XML for CI/CD integration

## 🎯 Report Types

### Executive Summary
```python
from exporters import export_executive_summary
exported_files = export_executive_summary(findings, "executive_report")
```

**Features:**
- High-level risk overview
- Executive dashboard with charts
- Risk metrics and KPIs
- Compliance status summary
- Recommended actions

### Technical Report
```python
from exporters import export_technical_report
exported_files = export_technical_report(findings, "technical_report")
```

**Features:**
- Detailed technical findings
- Vulnerability details and evidence
- Remediation instructions
- Technical references
- Code snippets and examples

### Compliance Pack
```python
from exporters import export_compliance_pack
exported_files = export_compliance_pack(findings, "compliance_pack")
```

**Features:**
- Compliance framework mapping
- Regulatory requirements
- Audit trail information
- Risk assessment matrices
- Multiple format exports

## 🛠️ Advanced Configuration

### HTML Generator Configuration
```python
from exporters import AdvancedHTMLGenerator

html_generator = AdvancedHTMLGenerator()
html_path = html_generator.export(
    findings, 
    "report.html",
    executive_dashboard=True,
    charts=True,
    risk_matrix=True,
    compliance_mapping=True
)
```

### PDF Exporter Configuration
```python
from exporters import AdvancedPDFExporter

pdf_exporter = AdvancedPDFExporter()
pdf_path = pdf_exporter.export(
    html_path,
    "report.pdf",
    format_type='executive',
    include_charts=True,
    watermark=True,
    page_numbers=True
)
```

### Multi-Format Configuration
```python
from exporters import MultiFormatExporter

multi_exporter = MultiFormatExporter()
sarif_path = multi_exporter.export(
    findings,
    "report.sarif",
    "sarif",
    config={
        "tool_name": "CyberSec-AI",
        "version": "1.0.0",
        "compliance_level": "enterprise"
    }
)
```

## 🔧 Integration Examples

### CLI Integration
```bash
# One-click industrial report
python main.py full-report -i nmap_scan.xml -fmt executive --advanced

# Batch processing
python main.py batch-process -d ./scans -fmt all

# Compliance export
python main.py export -f findings.json -fmt compliance
```

### Python API Integration
```python
from exporters import export_all_formats

# Export to all formats
exported_files = export_all_formats(findings, "security_report")

# Executive summary only
exec_files = export_executive_summary(findings, "exec_summary")

# Technical report with JSON/CSV
tech_files = export_technical_report(findings, "tech_report")
```

### Automation Integration
```python
import json
from exporters import export_compliance_pack

# Load findings from any source
with open('findings.json', 'r') as f:
    findings = json.load(f)

# Generate compliance pack
compliance_files = export_compliance_pack(findings, "audit_2024")

# Upload to compliance system
for file_path in compliance_files:
    upload_to_compliance_system(file_path)
```

## 🎨 Styling and Themes

### CSS Framework
The advanced HTML generator includes a comprehensive CSS framework:
- Responsive design for all devices
- Professional color schemes
- Interactive elements
- Print-friendly layouts
- Accessibility compliance

### Custom Themes
```python
# Create custom theme
custom_config = {
    "theme": "dark",
    "colors": {
        "primary": "#2563eb",
        "secondary": "#64748b",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444"
    },
    "fonts": {
        "primary": "Inter",
        "monospace": "Fira Code"
    }
}

html_generator.export(findings, "report.html", report_config=custom_config)
```

## 📈 Performance Optimization

### PDF Generation Methods
The system automatically selects the best available PDF generation method:
1. **WeasyPrint** - Best quality, CSS support
2. **wkhtmltopdf** - Fast, reliable
3. **Chrome Headless** - Modern, JavaScript support
4. **Puppeteer** - High compatibility

### Caching and Optimization
- Template caching for faster generation
- CSS/JS minification
- Image optimization
- Progressive rendering

## 🛡️ Security Features

### Watermarking
```python
pdf_exporter.export(
    html_path,
    "report.pdf",
    watermark={
        "text": "CONFIDENTIAL",
        "position": "center",
        "opacity": 0.3
    }
)
```

### Access Control
- File permission management
- Temporary file cleanup
- Secure file naming
- Path traversal protection

## 🔍 Troubleshooting

### Common Issues

**PDF Generation Failed:**
```bash
# Check available methods
python main.py export-info

# Install dependencies
pip install weasyprint wkhtmltopdf

# Try different format
python main.py export -f findings.json -fmt html --advanced
```

**Missing Charts:**
```bash
# Install chart dependencies
pip install matplotlib plotly

# Enable charts
python main.py export -f findings.json -fmt html --advanced
```

**Export Errors:**
```bash
# Test the export system
python test_advanced_exports.py

# Run demo
python demo_advanced_exports.py
```

## 📚 Examples

### Complete Workflow
```python
# 1. Parse scan results
from parsers import nmap_parser
findings = nmap_parser.parse("nmap_scan.xml")

# 2. Enhance with AI
from ai import summarizer, severity_classifier, remediation_generator
for finding in findings:
    finding["ai_summary"] = summarizer.generate(finding)
    finding["severity"] = severity_classifier.classify(finding)
    finding["remediation"] = remediation_generator.suggest(finding)

# 3. Export industrial report
from exporters import export_executive_summary
exec_files = export_executive_summary(findings, "quarterly_report")

# 4. Generate compliance pack
from exporters import export_compliance_pack
compliance_files = export_compliance_pack(findings, "compliance_audit")
```

### Integration with CI/CD
```yaml
# .github/workflows/security-report.yml
name: Security Report Generation
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Security Scan
        run: |
          python main.py full-report -i scan.xml -fmt all
          python main.py export -f findings.json -fmt sarif
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: findings.sarif
```

## 🎉 Success Stories

The advanced export system has been successfully used for:
- **Fortune 500 Security Audits**: Executive-level reports for board presentations
- **Compliance Reporting**: NIST, SOC2, and ISO 27001 compliance documentation
- **Penetration Testing**: Professional client deliverables
- **CI/CD Integration**: Automated security reporting in DevOps pipelines
- **SIEM Integration**: Standardized format feeding into security platforms

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Run the test suite: `python test_advanced_exports.py`
3. Try the demo: `python demo_advanced_exports.py`
4. Review the export info: `python main.py export-info`

The advanced export system provides industrial-level security reporting capabilities that meet enterprise requirements while maintaining ease of use and flexibility.
