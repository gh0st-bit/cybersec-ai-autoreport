#!/usr/bin/env python3
"""
CyberSec-AI AutoReport - Main CLI Entry Point
AI-powered cybersecurity report automation tool
"""

import click
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from parsers import nmap_parser, burp_parser, nuclei_parser
from exporters import (
    html_generator, pdf_exporter,
    AdvancedHTMLGenerator, AdvancedPDFExporter, MultiFormatExporter,
    export_all_formats, export_compliance_pack, export_executive_summary,
    export_technical_report, get_export_info
)
from ai import summarizer, severity_classifier, remediation_generator
from tools.runner import register_tool, execute_tool, list_tools
from tools.parser import parse_output
from utils.file_loader import save_json, load_json

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """[SHIELD] CyberSec-AI AutoReport - Automated Security Reporting Tool"""
    pass

@cli.command()
@click.option('--input', '-i', required=True, help='Path to scan file')
@click.option('--type', '-t', required=True, 
              type=click.Choice(['nmap', 'burp', 'nuclei']), 
              help='Type of scan file')
@click.option('--output', '-o', default='parsed.json', help='Output file path')
def parse(input, type, output):
    """Parse scan files (Nmap XML, Burp JSON, Nuclei JSON)"""
    click.echo(f"[FINDINGS] Parsing {type} scan file: {input}")
    
    try:
        if type == "nmap":
            findings = nmap_parser.parse(input)
        elif type == "burp":
            findings = burp_parser.parse(input)
        elif type == "nuclei":
            findings = nuclei_parser.parse(input)
        
        save_json(findings, output)
        click.echo(f"[OK] Parsed {len(findings)} findings saved to {output}")
        
    except Exception as e:
        click.echo(f"[ERROR] Error parsing file: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', required=True, help='Parsed JSON file')
@click.option('--output', '-o', default='enhanced.json', help='Output file path')
def enhance(file, output):
    """Enhance findings with AI analysis"""
    click.echo(f"[AI] Enhancing findings with AI: {file}")
    
    try:
        findings = load_json(file)
        
        for i, finding in enumerate(findings):
            click.echo(f"Processing finding {i+1}/{len(findings)}: {finding.get('title', 'Unknown')}")
            
            # Add AI enhancements
            finding["ai_summary"] = summarizer.generate(finding)
            finding["severity"] = severity_classifier.classify(finding)
            finding["remediation"] = remediation_generator.suggest(finding)
        
        save_json(findings, output)
        click.echo(f"[OK] Enhanced findings saved to {output}")
        
    except Exception as e:
        click.echo(f"[ERROR] Error enhancing findings: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', required=True, help='Enhanced JSON file')
@click.option('--format', '-fmt', default='pdf', 
              type=click.Choice(['html', 'pdf', 'all', 'compliance', 'executive', 'technical']), 
              help='Export format')
@click.option('--output', '-o', help='Output file path')
@click.option('--theme', '-th', default='executive',
              type=click.Choice(['executive', 'technical', 'compliance']),
              help='Report theme for advanced formats')
@click.option('--advanced', '-adv', is_flag=True, help='Use advanced industrial-level formatting')
def export(file, format, output, theme, advanced):
    """Export report to HTML, PDF, or multiple formats with industrial-level formatting"""
    click.echo(f"[FILE] Exporting report as {format.upper()}: {file}")
    
    try:
        findings = load_json(file)
        
        # Determine base output path
        if not output:
            base_path = os.path.splitext(file)[0]
        else:
            base_path = os.path.splitext(output)[0]
        
        if format == "all":
            # Export all formats
            click.echo("[EXPORT] Generating all formats...")
            exported_files = export_all_formats(findings, base_path)
            click.echo(f"[SUCCESS] Generated {len(exported_files)} files:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "compliance":
            # Export compliance pack
            click.echo("[EXPORT] Generating compliance pack...")
            exported_files = export_compliance_pack(findings, base_path)
            click.echo(f"[SUCCESS] Generated compliance pack ({len(exported_files)} files):")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "executive":
            # Export executive summary
            click.echo("[EXPORT] Generating executive summary...")
            exported_files = export_executive_summary(findings, base_path)
            click.echo(f"[SUCCESS] Generated executive summary:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "technical":
            # Export technical report
            click.echo("[EXPORT] Generating technical report...")
            exported_files = export_technical_report(findings, base_path)
            click.echo(f"[SUCCESS] Generated technical report:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif advanced:
            # Advanced export
            if format == "html":
                html_generator = AdvancedHTMLGenerator()
                html_path = html_generator.export(findings, f"{base_path}.html")
                click.echo(f"[SUCCESS] Advanced HTML report generated: {html_path}")
                
            elif format == "pdf":
                # Generate HTML first, then PDF
                html_generator = AdvancedHTMLGenerator()
                html_path = html_generator.export(findings, f"{base_path}.html")
                
                pdf_exporter = AdvancedPDFExporter()
                pdf_path = pdf_exporter.export(html_path, f"{base_path}.pdf", format_type=theme)
                click.echo(f"[SUCCESS] Advanced PDF report generated: {pdf_path}")
                
        else:
            # Legacy export
            html_path = html_generator.export(findings, output_path=output)
            
            if format == "pdf":
                pdf_path = pdf_exporter.export(html_path)
                click.echo(f"[SUCCESS] PDF report generated: {pdf_path}")
            else:
                click.echo(f"[SUCCESS] HTML report generated: {html_path}")
                
    except Exception as e:
        click.echo(f"[ERROR] Error exporting report: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', required=True, help='Path to scan file')
@click.option('--type', '-t', 
              type=click.Choice(['nmap', 'burp', 'nuclei', 'auto']), 
              default='auto',
              help='Type of scan file (auto-detect by default)')
@click.option('--format', '-fmt', default='executive', 
              type=click.Choice(['html', 'pdf', 'all', 'compliance', 'executive', 'technical']), 
              help='Export format')
@click.option('--theme', '-th', default='executive',
              type=click.Choice(['executive', 'technical', 'compliance']),
              help='Report theme')
@click.option('--advanced', '-adv', is_flag=True, default=True, help='Use advanced industrial-level formatting')
def full_report(input, type, format, theme, advanced):
    """One-click: Parse → AI Enhance → Export with industrial-level formatting"""
    click.echo("[LAUNCH] Running full report generation pipeline...")
    
    # Auto-detect scan type if needed
    if type == 'auto':
        try:
            from auto_detect import ScanAutoDetector
            detector = ScanAutoDetector()
            detected_type = detector.detect_scan_type(input)
            if detected_type:
                type = detected_type
                click.echo(f"[INFO] Auto-detected scan type: {type}")
            else:
                click.echo("[ERROR] Could not auto-detect scan type. Please specify --type")
                sys.exit(1)
        except ImportError:
            click.echo("[WARNING] Auto-detection not available. Please specify --type")
            sys.exit(1)
    
    # Step 1: Parse
    click.echo("Step 1/3: Parsing scan file...")
    try:
        if type == "nmap":
            findings = nmap_parser.parse(input)
        elif type == "burp":
            findings = burp_parser.parse(input)
        elif type == "nuclei":
            findings = nuclei_parser.parse(input)
        
        click.echo(f"[OK] Parsed {len(findings)} findings")
    except Exception as e:
        click.echo(f"[ERROR] Parsing failed: {str(e)}", err=True)
        sys.exit(1)
    
    # Step 2: AI Enhancement
    click.echo("Step 2/3: AI enhancement...")
    try:
        for i, finding in enumerate(findings):
            click.echo(f"  Processing {i+1}/{len(findings)}: {finding.get('title', 'Unknown')}")
            finding["ai_summary"] = summarizer.generate(finding)
            finding["severity"] = severity_classifier.classify(finding)
            finding["remediation"] = remediation_generator.suggest(finding)
        
        click.echo(f"[OK] Enhanced {len(findings)} findings")
    except Exception as e:
        click.echo(f"[ERROR] AI enhancement failed: {str(e)}", err=True)
        sys.exit(1)
    
    # Step 3: Export Report
    click.echo("Step 3/3: Generating industrial-level report...")
    try:
        # Determine base output path
        base_path = os.path.splitext(input)[0]
        
        if format == "all":
            # Export all formats
            click.echo("[EXPORT] Generating all formats...")
            exported_files = export_all_formats(findings, base_path)
            click.echo(f"[SUCCESS] Generated {len(exported_files)} files:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "compliance":
            # Export compliance pack
            click.echo("[EXPORT] Generating compliance pack...")
            exported_files = export_compliance_pack(findings, base_path)
            click.echo(f"[SUCCESS] Generated compliance pack ({len(exported_files)} files):")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "executive":
            # Export executive summary
            click.echo("[EXPORT] Generating executive summary...")
            exported_files = export_executive_summary(findings, base_path)
            click.echo(f"[SUCCESS] Generated executive summary:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif format == "technical":
            # Export technical report
            click.echo("[EXPORT] Generating technical report...")
            exported_files = export_technical_report(findings, base_path)
            click.echo(f"[SUCCESS] Generated technical report:")
            for file_path in exported_files:
                click.echo(f"  ✓ {file_path}")
                
        elif advanced:
            # Advanced export
            if format == "html":
                html_generator = AdvancedHTMLGenerator()
                html_path = html_generator.export(findings, f"{base_path}.html")
                click.echo(f"[SUCCESS] Advanced HTML report generated: {html_path}")
                
            elif format == "pdf":
                # Generate HTML first, then PDF
                html_generator = AdvancedHTMLGenerator()
                html_path = html_generator.export(findings, f"{base_path}.html")
                
                pdf_exporter = AdvancedPDFExporter()
                pdf_path = pdf_exporter.export(html_path, f"{base_path}.pdf", format_type=theme)
                click.echo(f"[SUCCESS] Advanced PDF report generated: {pdf_path}")
                
        else:
            # Legacy export
            html_path = html_generator.export(findings)
            click.echo(f"[OK] HTML report generated: {html_path}")
            
            if format == "pdf":
                try:
                    pdf_path = pdf_exporter.export(html_path)
                    click.echo(f"[OK] PDF report generated: {pdf_path}")
                    click.echo(f"[SUCCESS] Full report completed: {pdf_path}")
                except Exception as pdf_error:
                    click.echo(f"[ERROR] PDF generation failed: {str(pdf_error)}")
                    click.echo(f"[INFO] HTML report is still available: {html_path}")
                    click.echo("[TIP] Try running: ./install_dependencies.sh")
            else:
                click.echo(f"[SUCCESS] Full report completed: {html_path}")
            
    except Exception as e:
        click.echo(f"[ERROR] Report generation failed: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def export_info():
    """Show available export formats and methods"""
    click.echo("[INFO] Available Export Formats and Methods:")
    
    try:
        info = get_export_info()
        
        click.echo("\n📊 HTML Templates:")
        for template in info['html_templates']:
            click.echo(f"  • {template}")
            
        click.echo("\n📄 PDF Formats:")
        for format_type in info['pdf_formats']:
            click.echo(f"  • {format_type}")
            
        click.echo("\n🔧 PDF Generation Methods:")
        for method in info['pdf_methods']:
            click.echo(f"  • {method}")
            
        click.echo(f"\n✅ Recommended PDF Method: {info['recommended_pdf_method']}")
        
        click.echo("\n🌐 Multi-Format Exports:")
        for format_type in info['multi_formats']:
            click.echo(f"  • {format_type}")
            
        click.echo("\n🛡️ Compliance Formats:")
        for format_type in info['compliance_formats']:
            click.echo(f"  • {format_type}")
            
        click.echo("\n📋 Export Commands:")
        click.echo("  • full-report -fmt executive     # Executive summary")
        click.echo("  • full-report -fmt technical     # Technical report")
        click.echo("  • full-report -fmt compliance    # Compliance pack")
        click.echo("  • full-report -fmt all          # All formats")
        click.echo("  • export -fmt html --advanced    # Advanced HTML")
        click.echo("  • export -fmt pdf --advanced     # Advanced PDF")
        
    except Exception as e:
        click.echo(f"[ERROR] Failed to get export info: {str(e)}", err=True)
        sys.exit(1)

# Custom Tools Commands
@cli.group()
def tools():
    """Custom tool integration commands"""
    pass

@tools.command()
@click.option('--name', required=True, help='Tool name')
@click.option('--command', required=True, help='Command template with {input} and {output}')
@click.option('--desc', default='', help='Tool description')
def register(name, command, desc):
    """Register a new custom tool"""
    click.echo(f"[TOOL] Registering tool: {name}")
    
    try:
        register_tool(name, command, desc, "file", "file")
        click.echo(f"[OK] Tool '{name}' registered successfully")
    except Exception as e:
        click.echo(f"[ERROR] Registration failed: {str(e)}", err=True)

@tools.command()
@click.option('--name', required=True, help='Tool name')
@click.option('--input', required=True, help='Input file path')
@click.option('--output', help='Output file path (optional)')
def run(name, input, output):
    """Run a registered custom tool"""
    click.echo(f"[EXEC] Running tool: {name}")
    
    try:
        output_file, stdout = execute_tool(name, input, output)
        if output_file:
            click.echo(f"[OK] Tool completed. Output saved to: {output_file}")
            
            # Parse with AI
            summary = parse_output(output_file)
            click.echo(f"[AI] AI Summary:\n{summary}")
        else:
            click.echo("[ERROR] Tool execution failed")
            
    except Exception as e:
        click.echo(f"[ERROR] Tool execution failed: {str(e)}", err=True)

@tools.command()
def list():
    """List all registered tools"""
    click.echo("[TOOL] Registered Tools:")
    
    try:
        tools_list = list_tools()
        for name, tool in tools_list.items():
            click.echo(f"  • {name}: {tool.get('description', 'No description')}")
            click.echo(f"    Command: {tool.get('command', 'N/A')}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to list tools: {str(e)}", err=True)

@cli.command()
@click.option('--directory', '-d', default='.', help='Directory to process')
@click.option('--format', '-fmt', default='html', 
              type=click.Choice(['html', 'pdf']), help='Export format')
@click.option('--recursive', '-r', is_flag=True, help='Search recursively')
def batch_process(directory, format, recursive):
    """Process all scan files in a directory"""
    click.echo(f"[LAUNCH] Batch processing directory: {directory}")
    
    try:
        from auto_detect import AutoProcessor
        processor = AutoProcessor()
        
        # Find and process all scan files
        reports = processor.process_directory(directory, format)
        
        if reports:
            click.echo(f"[SUCCESS] Generated {len(reports)} reports:")
            for report in reports:
                click.echo(f"  {report}")
        else:
            click.echo("[WARNING] No scan files found or processed")
            
    except Exception as e:
        click.echo(f"[ERROR] Batch processing failed: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def interactive():
    """Launch interactive mode"""
    click.echo("[LAUNCH] Starting interactive mode...")
    
    try:
        from interactive import InteractiveCLI
        cli_app = InteractiveCLI()
        cli_app.main_menu()
    except Exception as e:
        click.echo(f"[ERROR] Interactive mode failed: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--file', '-f', help='File to analyze')
@click.option('--directory', '-d', default='.', help='Directory to scan')
def auto_detect(file, directory):
    """Auto-detect scan file types"""
    try:
        from auto_detect import ScanAutoDetector
        detector = ScanAutoDetector()
        
        if file:
            # Analyze single file
            file_info = detector.get_file_info(file)
            if file_info:
                click.echo(f"File: {file_info['name']}")
                click.echo(f"Type: {file_info['detected_type']}")
                click.echo(f"Valid: {file_info['is_valid']}")
                click.echo(f"Size: {file_info['size']} bytes")
            else:
                click.echo("[ERROR] File not found")
        else:
            # Scan directory
            scan_files = detector.find_scan_files(directory)
            if scan_files:
                click.echo(f"Found {len(scan_files)} scan files:")
                for file_path, scan_type in scan_files:
                    click.echo(f"  {file_path} -> {scan_type}")
            else:
                click.echo("[INFO] No scan files found")
                
    except Exception as e:
        click.echo(f"[ERROR] Auto-detection failed: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
