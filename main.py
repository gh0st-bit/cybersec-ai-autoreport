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
from exporters import html_generator, pdf_exporter
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
              type=click.Choice(['html', 'pdf']), help='Export format')
@click.option('--output', '-o', help='Output file path')
def export(file, format, output):
    """Export report to HTML or PDF"""
    click.echo(f"[FILE] Exporting report as {format.upper()}: {file}")
    
    try:
        findings = load_json(file)
        
        # Generate HTML first
        html_path = html_generator.export(findings, output_path=output)
        
        if format == "pdf":
            pdf_path = pdf_exporter.export(html_path)
            click.echo(f"[OK] PDF report generated: {pdf_path}")
        else:
            click.echo(f"[OK] HTML report generated: {html_path}")
            
    except Exception as e:
        click.echo(f"[ERROR] Error exporting report: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', required=True, help='Path to scan file')
@click.option('--type', '-t', required=True, 
              type=click.Choice(['nmap', 'burp', 'nuclei']), 
              help='Type of scan file')
@click.option('--format', '-fmt', default='pdf', 
              type=click.Choice(['html', 'pdf']), help='Export format')
def full_report(input, type, format):
    """One-click: Parse → AI Enhance → Export"""
    click.echo("[LAUNCH] Running full report generation pipeline...")
    
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
    
    # Step 3: Export
    click.echo("Step 3/3: Generating report...")
    try:
        html_path = html_generator.export(findings)
        
        if format == "pdf":
            pdf_path = pdf_exporter.export(html_path)
            click.echo(f"[SUCCESS] Full report completed: {pdf_path}")
        else:
            click.echo(f"[SUCCESS] Full report completed: {html_path}")
            
    except Exception as e:
        click.echo(f"[ERROR] Export failed: {str(e)}", err=True)
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

if __name__ == '__main__':
    cli()
