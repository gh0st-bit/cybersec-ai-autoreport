"""
Advanced Exporters Module

This module provides comprehensive functionality for exporting security findings 
to various formats including HTML, PDF, JSON, CSV, XML, SARIF, STIX, and more.

Features:
- Industrial-level HTML reports with professional styling
- Advanced PDF generation with multiple methods and formats
- Multi-format export for compliance (SARIF, STIX, MITRE, NIST)
- Executive, technical, and compliance report formats
- Chart generation and visualizations
- Watermarking and branding support
"""

# Legacy imports for backward compatibility
from .html_generator import export as export_html
from .pdf_exporter import export as export_pdf

# Advanced exporters
from .html_generator_advanced import AdvancedHTMLGenerator, export_advanced as export_html_advanced
from .pdf_exporter_advanced import AdvancedPDFExporter, export_advanced as export_pdf_advanced
from .multi_format_exporter import MultiFormatExporter, export_to_multiple_formats

# Convenience functions
def export_all_formats(findings, base_path, config=None):
    """Export to all supported formats"""
    exported_files = []
    
    try:
        # HTML Advanced
        html_generator = AdvancedHTMLGenerator()
        html_path = html_generator.export(findings, f"{base_path}.html", report_config=config)
        exported_files.append(html_path)
        
        # PDF Advanced
        pdf_exporter = AdvancedPDFExporter()
        pdf_path = pdf_exporter.export(html_path, f"{base_path}.pdf", format_type='executive')
        exported_files.append(pdf_path)
        
        # Multi-format exports
        multi_exporter = MultiFormatExporter()
        formats = ['json', 'csv', 'xml', 'sarif', 'markdown']
        
        for format_type in formats:
            try:
                file_ext = 'xlsx' if format_type == 'excel' else format_type
                output_path = f"{base_path}.{file_ext}"
                exported_file = multi_exporter.export(findings, output_path, format_type, config)
                exported_files.append(exported_file)
            except Exception as e:
                print(f"[WARNING] Failed to export {format_type}: {str(e)}")
        
        return exported_files
    
    except Exception as e:
        print(f"[ERROR] Failed to export all formats: {str(e)}")
        return exported_files

def export_compliance_pack(findings, base_path, config=None):
    """Export compliance-focused report pack"""
    exported_files = []
    
    try:
        # HTML Professional Report
        html_generator = AdvancedHTMLGenerator()
        html_path = html_generator.export(
            findings, 
            f"{base_path}_compliance.html", 
            report_config=config,
            template_name="industrial_report.html"
        )
        exported_files.append(html_path)
        
        # PDF Compliance Format
        pdf_exporter = AdvancedPDFExporter()
        pdf_path = pdf_exporter.export(
            html_path, 
            f"{base_path}_compliance.pdf", 
            format_type='compliance'
        )
        exported_files.append(pdf_path)
        
        # Compliance formats
        multi_exporter = MultiFormatExporter()
        compliance_formats = ['sarif', 'stix', 'mitre', 'nist', 'junit']
        
        for format_type in compliance_formats:
            try:
                output_path = f"{base_path}_compliance.{format_type}"
                exported_file = multi_exporter.export(findings, output_path, format_type, config)
                exported_files.append(exported_file)
            except Exception as e:
                print(f"[WARNING] Failed to export {format_type}: {str(e)}")
        
        return exported_files
    
    except Exception as e:
        print(f"[ERROR] Failed to export compliance pack: {str(e)}")
        return exported_files

def export_executive_summary(findings, base_path, config=None):
    """Export executive-focused summary"""
    try:
        # Executive HTML
        html_generator = AdvancedHTMLGenerator()
        html_path = html_generator.export(
            findings, 
            f"{base_path}_executive.html", 
            report_config=config,
            executive_dashboard=True,
            charts=True
        )
        
        # Executive PDF
        pdf_exporter = AdvancedPDFExporter()
        pdf_path = pdf_exporter.export(
            html_path, 
            f"{base_path}_executive.pdf", 
            format_type='executive',
            include_charts=True
        )
        
        return [html_path, pdf_path]
    
    except Exception as e:
        print(f"[ERROR] Failed to export executive summary: {str(e)}")
        return []

def export_technical_report(findings, base_path, config=None):
    """Export technical-focused report"""
    try:
        # Technical HTML
        html_generator = AdvancedHTMLGenerator()
        html_path = html_generator.export(
            findings, 
            f"{base_path}_technical.html", 
            report_config=config,
            template_name="industrial_report.html"
        )
        
        # Technical PDF
        pdf_exporter = AdvancedPDFExporter()
        pdf_path = pdf_exporter.export(
            html_path, 
            f"{base_path}_technical.pdf", 
            format_type='technical'
        )
        
        # Technical formats
        multi_exporter = MultiFormatExporter()
        json_path = multi_exporter.export(findings, f"{base_path}_technical.json", "json", config)
        csv_path = multi_exporter.export(findings, f"{base_path}_technical.csv", "csv", config)
        
        return [html_path, pdf_path, json_path, csv_path]
    
    except Exception as e:
        print(f"[ERROR] Failed to export technical report: {str(e)}")
        return []

def get_export_info():
    """Get information about available export formats and methods"""
    html_generator = AdvancedHTMLGenerator()
    pdf_exporter = AdvancedPDFExporter()
    multi_exporter = MultiFormatExporter()
    
    return {
        'html_templates': ['industrial_report.html', 'default.html.j2'],
        'pdf_formats': list(pdf_exporter.pdf_styles.keys()),
        'pdf_methods': pdf_exporter.list_available_methods(),
        'multi_formats': multi_exporter.get_supported_formats(),
        'compliance_formats': ['sarif', 'stix', 'mitre', 'nist', 'junit'],
        'recommended_pdf_method': pdf_exporter.select_best_method()
    }

__all__ = [
    # Legacy exports
    'export_html', 'export_pdf',
    
    # Advanced exports
    'export_html_advanced', 'export_pdf_advanced',
    'AdvancedHTMLGenerator', 'AdvancedPDFExporter', 'MultiFormatExporter',
    
    # Convenience functions
    'export_all_formats', 'export_compliance_pack', 
    'export_executive_summary', 'export_technical_report',
    'export_to_multiple_formats', 'get_export_info'
]
