"""
Advanced HTML Report Generator with Industrial-Level Formatting
Enhanced cybersecurity reporting with professional templates and multiple export formats
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from ai.summarizer import generate_executive_summary
from ai.severity_classifier import sort_by_severity
import uuid

class AdvancedHTMLGenerator:
    """Advanced HTML report generator with industrial-level formatting"""
    
    def __init__(self, template_dir=None):
        self.template_dir = template_dir or Path(__file__).parent.parent / "templates"
        self.template_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Register custom filters
        self.env.filters['severity_color'] = self.get_severity_color
        self.env.filters['severity_icon'] = self.get_severity_icon
        self.env.filters['format_date'] = self.format_date
        self.env.filters['cvss_score'] = self.calculate_cvss_score
        self.env.filters['truncate_smart'] = self.truncate_smart
        
    def export(self, findings, output_path=None, template_name="industrial_report.html", 
               report_config=None, charts=True, executive_dashboard=True):
        """
        Export findings to advanced HTML report
        
        Args:
            findings (list): List of findings
            output_path (str): Output file path
            template_name (str): Template to use
            report_config (dict): Report configuration
            charts (bool): Include charts and visualizations
            executive_dashboard (bool): Include executive dashboard
        
        Returns:
            str: Path to generated HTML file
        """
        try:
            # Set default configuration
            if not report_config:
                report_config = self.get_default_config()
            
            # Ensure reports directory exists
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Generate output path if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = reports_dir / f"cybersec_report_{timestamp}.html"
            
            # Process findings
            processed_findings = self.process_findings(findings)
            
            # Generate report data
            report_data = self.generate_report_data(processed_findings, report_config)
            
            # Generate charts if requested
            if charts:
                report_data['charts'] = self.generate_charts_data(processed_findings)
            
            # Create template if it doesn't exist
            template_path = self.template_dir / template_name
            if not template_path.exists():
                self.create_industrial_template(template_path)
            
            # Load and render template
            template = self.env.get_template(template_name)
            html_content = template.render(**report_data)
            
            # Write HTML file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"[OK] Industrial HTML report generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"[ERROR] Failed to generate advanced HTML report: {str(e)}")
            raise
    
    def process_findings(self, findings):
        """Process and enhance findings with additional metadata"""
        processed = []
        
        for finding in findings:
            # Create enhanced finding object
            enhanced_finding = {
                'id': str(uuid.uuid4()),
                'title': finding.get('title', 'Unknown Vulnerability'),
                'description': finding.get('description', 'No description available'),
                'severity': finding.get('severity', 'Medium'),
                'cvss_score': self.calculate_cvss_score(finding),
                'category': finding.get('category', 'Security'),
                'subcategory': finding.get('subcategory', 'General'),
                'host': finding.get('host', 'Unknown'),
                'port': finding.get('port', 'N/A'),
                'service': finding.get('service', 'Unknown'),
                'protocol': finding.get('protocol', 'Unknown'),
                'evidence': finding.get('evidence', 'No evidence provided'),
                'impact': finding.get('impact', 'Impact assessment not available'),
                'remediation': finding.get('remediation', 'No remediation available'),
                'references': finding.get('references', []),
                'tags': finding.get('tags', []),
                'ai_summary': finding.get('ai_summary', ''),
                'ai_risk_assessment': finding.get('ai_risk_assessment', ''),
                'discovery_date': finding.get('discovery_date', datetime.now().isoformat()),
                'last_seen': finding.get('last_seen', datetime.now().isoformat()),
                'source': finding.get('source', 'Unknown'),
                'confidence': finding.get('confidence', 'Medium'),
                'exploitability': finding.get('exploitability', 'Unknown'),
                'assets_affected': finding.get('assets_affected', []),
                'business_impact': finding.get('business_impact', 'Unknown'),
                'compliance_impact': finding.get('compliance_impact', []),
                'technical_details': finding.get('technical_details', {}),
                'screenshots': finding.get('screenshots', []),
                'attachments': finding.get('attachments', [])
            }
            
            processed.append(enhanced_finding)
        
        return sort_by_severity(processed)
    
    def generate_report_data(self, findings, config):
        """Generate comprehensive report data"""
        stats = self.generate_advanced_statistics(findings)
        risk_matrix = self.generate_risk_matrix(findings)
        compliance_summary = self.generate_compliance_summary(findings)
        
        return {
            'report_id': str(uuid.uuid4()),
            'report_title': config.get('title', 'Cybersecurity Assessment Report'),
            'company_name': config.get('company', 'Organization'),
            'assessment_period': config.get('assessment_period', 'Not specified'),
            'assessment_scope': config.get('scope', 'Not specified'),
            'assessment_methodology': config.get('methodology', 'Automated Security Assessment'),
            'report_version': config.get('version', '1.0'),
            'classification': config.get('classification', 'CONFIDENTIAL'),
            'generated_date': datetime.now().strftime("%B %d, %Y"),
            'generated_time': datetime.now().strftime("%H:%M:%S UTC"),
            'generated_by': config.get('generated_by', 'CyberSec-AI AutoReport'),
            'findings': findings,
            'statistics': stats,
            'risk_matrix': risk_matrix,
            'compliance_summary': compliance_summary,
            'executive_summary': generate_executive_summary(findings),
            'recommendations': self.generate_recommendations(findings),
            'next_steps': self.generate_next_steps(findings, stats),
            'total_findings': len(findings),
            'report_config': config
        }
    
    def generate_advanced_statistics(self, findings):
        """Generate comprehensive statistics"""
        stats = {
            'total': len(findings),
            'by_severity': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0},
            'by_category': {},
            'by_confidence': {},
            'by_exploitability': {},
            'by_source': {},
            'by_host': {},
            'by_service': {},
            'cvss_distribution': {'0-3': 0, '4-6': 0, '7-8': 0, '9-10': 0},
            'trend_analysis': {},
            'compliance_violations': {},
            'remediation_effort': {'quick': 0, 'medium': 0, 'complex': 0},
            'business_impact': {'high': 0, 'medium': 0, 'low': 0}
        }
        
        for finding in findings:
            # Severity distribution
            severity = finding.get('severity', 'medium').lower()
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
            
            # Category distribution
            category = finding.get('category', 'Other')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Confidence distribution
            confidence = finding.get('confidence', 'Medium')
            stats['by_confidence'][confidence] = stats['by_confidence'].get(confidence, 0) + 1
            
            # Exploitability distribution
            exploitability = finding.get('exploitability', 'Unknown')
            stats['by_exploitability'][exploitability] = stats['by_exploitability'].get(exploitability, 0) + 1
            
            # Source distribution
            source = finding.get('source', 'Unknown')
            stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
            
            # Host distribution
            host = finding.get('host', 'Unknown')
            stats['by_host'][host] = stats['by_host'].get(host, 0) + 1
            
            # Service distribution
            service = finding.get('service', 'Unknown')
            stats['by_service'][service] = stats['by_service'].get(service, 0) + 1
            
            # CVSS distribution
            cvss = finding.get('cvss_score', 0)
            if cvss <= 3:
                stats['cvss_distribution']['0-3'] += 1
            elif cvss <= 6:
                stats['cvss_distribution']['4-6'] += 1
            elif cvss <= 8:
                stats['cvss_distribution']['7-8'] += 1
            else:
                stats['cvss_distribution']['9-10'] += 1
        
        return stats
    
    def generate_risk_matrix(self, findings):
        """Generate risk matrix data"""
        matrix = {
            'high_likelihood': {'high_impact': [], 'medium_impact': [], 'low_impact': []},
            'medium_likelihood': {'high_impact': [], 'medium_impact': [], 'low_impact': []},
            'low_likelihood': {'high_impact': [], 'medium_impact': [], 'low_impact': []}
        }
        
        for finding in findings:
            exploitability = finding.get('exploitability', 'Unknown').lower()
            business_impact = finding.get('business_impact', 'Unknown').lower()
            
            likelihood = 'medium_likelihood'
            if exploitability in ['easy', 'high']:
                likelihood = 'high_likelihood'
            elif exploitability in ['difficult', 'low']:
                likelihood = 'low_likelihood'
            
            impact = 'medium_impact'
            if business_impact in ['high', 'critical']:
                impact = 'high_impact'
            elif business_impact in ['low', 'minimal']:
                impact = 'low_impact'
            
            matrix[likelihood][impact].append(finding)
        
        return matrix
    
    def generate_compliance_summary(self, findings):
        """Generate compliance framework summary"""
        frameworks = {
            'OWASP': {'total': 0, 'violations': []},
            'NIST': {'total': 0, 'violations': []},
            'PCI-DSS': {'total': 0, 'violations': []},
            'ISO-27001': {'total': 0, 'violations': []},
            'GDPR': {'total': 0, 'violations': []},
            'SOX': {'total': 0, 'violations': []},
            'HIPAA': {'total': 0, 'violations': []}
        }
        
        for finding in findings:
            compliance_impacts = finding.get('compliance_impact', [])
            for framework in compliance_impacts:
                if framework in frameworks:
                    frameworks[framework]['total'] += 1
                    frameworks[framework]['violations'].append(finding)
        
        return frameworks
    
    def generate_recommendations(self, findings):
        """Generate strategic recommendations"""
        recommendations = []
        
        # Count critical and high severity findings
        critical_count = sum(1 for f in findings if f.get('severity', '').lower() == 'critical')
        high_count = sum(1 for f in findings if f.get('severity', '').lower() == 'high')
        
        if critical_count > 0:
            recommendations.append({
                'priority': 'Immediate',
                'category': 'Critical Vulnerabilities',
                'description': f'Address {critical_count} critical vulnerabilities immediately',
                'timeline': '24-48 hours',
                'effort': 'High',
                'impact': 'High'
            })
        
        if high_count > 0:
            recommendations.append({
                'priority': 'High',
                'category': 'High-Risk Vulnerabilities',
                'description': f'Remediate {high_count} high-severity vulnerabilities',
                'timeline': '1-2 weeks',
                'effort': 'Medium',
                'impact': 'High'
            })
        
        # Add general recommendations
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Security Controls',
                'description': 'Implement comprehensive security monitoring and alerting',
                'timeline': '2-4 weeks',
                'effort': 'Medium',
                'impact': 'Medium'
            },
            {
                'priority': 'Medium',
                'category': 'Process Improvement',
                'description': 'Establish regular security assessments and vulnerability management',
                'timeline': '1-3 months',
                'effort': 'Medium',
                'impact': 'Medium'
            },
            {
                'priority': 'Low',
                'category': 'Training & Awareness',
                'description': 'Conduct security awareness training for all personnel',
                'timeline': '3-6 months',
                'effort': 'Low',
                'impact': 'Medium'
            }
        ])
        
        return recommendations
    
    def generate_next_steps(self, findings, stats):
        """Generate next steps based on findings"""
        steps = []
        
        if stats['by_severity']['critical'] > 0:
            steps.append({
                'step': 1,
                'action': 'Emergency Response',
                'description': 'Initiate incident response procedures for critical vulnerabilities',
                'owner': 'Security Team',
                'deadline': '24 hours'
            })
        
        steps.extend([
            {
                'step': len(steps) + 1,
                'action': 'Vulnerability Prioritization',
                'description': 'Prioritize vulnerabilities based on risk matrix and business impact',
                'owner': 'Security Team',
                'deadline': '48 hours'
            },
            {
                'step': len(steps) + 1,
                'action': 'Remediation Planning',
                'description': 'Create detailed remediation plans for each vulnerability',
                'owner': 'IT/Security Teams',
                'deadline': '1 week'
            },
            {
                'step': len(steps) + 1,
                'action': 'Implementation',
                'description': 'Execute remediation plans according to priority',
                'owner': 'IT Teams',
                'deadline': '4 weeks'
            },
            {
                'step': len(steps) + 1,
                'action': 'Validation',
                'description': 'Verify that vulnerabilities have been properly addressed',
                'owner': 'Security Team',
                'deadline': '6 weeks'
            }
        ])
        
        return steps
    
    def generate_charts_data(self, findings):
        """Generate data for charts and visualizations"""
        charts = {
            'severity_distribution': {
                'labels': ['Critical', 'High', 'Medium', 'Low', 'Info'],
                'data': [0, 0, 0, 0, 0],
                'colors': ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#17a2b8']
            },
            'category_distribution': {
                'labels': [],
                'data': [],
                'colors': []
            },
            'cvss_distribution': {
                'labels': ['0-3.9', '4.0-6.9', '7.0-8.9', '9.0-10.0'],
                'data': [0, 0, 0, 0],
                'colors': ['#28a745', '#ffc107', '#fd7e14', '#dc3545']
            },
            'trend_analysis': {
                'labels': [],
                'data': [],
                'colors': []
            }
        }
        
        # Process severity distribution
        for finding in findings:
            severity = finding.get('severity', 'medium').lower()
            if severity == 'critical':
                charts['severity_distribution']['data'][0] += 1
            elif severity == 'high':
                charts['severity_distribution']['data'][1] += 1
            elif severity == 'medium':
                charts['severity_distribution']['data'][2] += 1
            elif severity == 'low':
                charts['severity_distribution']['data'][3] += 1
            else:
                charts['severity_distribution']['data'][4] += 1
        
        # Process category distribution
        categories = {}
        for finding in findings:
            category = finding.get('category', 'Other')
            categories[category] = categories.get(category, 0) + 1
        
        charts['category_distribution']['labels'] = list(categories.keys())
        charts['category_distribution']['data'] = list(categories.values())
        
        # Generate colors for categories
        color_palette = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1', '#fd7e14']
        charts['category_distribution']['colors'] = [
            color_palette[i % len(color_palette)] for i in range(len(categories))
        ]
        
        # Process CVSS distribution
        for finding in findings:
            cvss = finding.get('cvss_score', 0)
            if cvss < 4:
                charts['cvss_distribution']['data'][0] += 1
            elif cvss < 7:
                charts['cvss_distribution']['data'][1] += 1
            elif cvss < 9:
                charts['cvss_distribution']['data'][2] += 1
            else:
                charts['cvss_distribution']['data'][3] += 1
        
        return charts
    
    def get_default_config(self):
        """Get default report configuration"""
        return {
            'title': 'Cybersecurity Assessment Report',
            'company': 'Organization',
            'assessment_period': 'Not specified',
            'scope': 'Automated Security Assessment',
            'methodology': 'Vulnerability Scanning and Analysis',
            'version': '1.0',
            'classification': 'CONFIDENTIAL',
            'generated_by': 'CyberSec-AI AutoReport v2.0',
            'logo_path': None,
            'theme': 'professional',
            'include_charts': True,
            'include_executive_summary': True,
            'include_recommendations': True,
            'include_appendices': True
        }
    
    def get_severity_color(self, severity):
        """Get color for severity level"""
        colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
            'info': '#17a2b8'
        }
        return colors.get(severity.lower(), '#6c757d')
    
    def get_severity_icon(self, severity):
        """Get icon for severity level"""
        icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'info': '🔵'
        }
        return icons.get(severity.lower(), '⚪')
    
    def format_date(self, date_string):
        """Format date string"""
        try:
            if isinstance(date_string, str):
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                dt = date_string
            return dt.strftime("%B %d, %Y at %H:%M UTC")
        except:
            return date_string
    
    def calculate_cvss_score(self, finding):
        """Calculate CVSS score from finding data"""
        # Simplified CVSS calculation
        severity = finding.get('severity', 'medium').lower()
        scores = {
            'critical': 9.5,
            'high': 7.5,
            'medium': 5.0,
            'low': 2.5,
            'info': 0.0
        }
        return scores.get(severity, 5.0)
    
    def truncate_smart(self, text, length=100):
        """Smart text truncation"""
        if len(text) <= length:
            return text
        
        # Find the last space before the length limit
        truncated = text[:length]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            return truncated[:last_space] + '...'
        else:
            return truncated + '...'
    
    def create_industrial_template(self, template_path):
        """Create industrial-level HTML template"""
        template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        /* Industrial Report CSS */
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --accent-color: #3498db;
            --danger-color: #e74c3c;
            --warning-color: #f39c12;
            --success-color: #27ae60;
            --info-color: #3498db;
            --light-bg: #ecf0f1;
            --dark-bg: #2c3e50;
            --text-color: #2c3e50;
            --border-color: #bdc3c7;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        /* Header Section */
        .report-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
        }
        
        .report-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }
        
        .report-header h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .report-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
            position: relative;
            z-index: 1;
        }
        
        .meta-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
        
        .meta-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .meta-value {
            font-size: 1.1em;
            font-weight: 600;
        }
        
        /* Executive Dashboard */
        .executive-dashboard {
            padding: 40px;
            background: var(--light-bg);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .metric-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-color), var(--primary-color));
        }
        
        .metric-number {
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            font-size: 1.1em;
            color: var(--text-color);
            font-weight: 500;
        }
        
        .metric-description {
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
        }
        
        /* Severity Cards */
        .severity-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .severity-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid;
        }
        
        .severity-card.critical {
            border-left-color: var(--danger-color);
            background: linear-gradient(135deg, #fff, #fee);
        }
        
        .severity-card.high {
            border-left-color: var(--warning-color);
            background: linear-gradient(135deg, #fff, #fef9e7);
        }
        
        .severity-card.medium {
            border-left-color: var(--info-color);
            background: linear-gradient(135deg, #fff, #e3f2fd);
        }
        
        .severity-card.low {
            border-left-color: var(--success-color);
            background: linear-gradient(135deg, #fff, #e8f5e8);
        }
        
        .severity-number {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .severity-label {
            font-size: 1em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Executive Summary */
        .executive-summary {
            background: white;
            margin: 40px;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid var(--accent-color);
        }
        
        .executive-summary h2 {
            color: var(--primary-color);
            margin-bottom: 25px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .executive-summary h2::before {
            content: '📊';
            font-size: 1.2em;
        }
        
        .executive-summary p {
            font-size: 1.1em;
            line-height: 1.8;
            color: #444;
        }
        
        /* Risk Matrix */
        .risk-matrix {
            margin: 40px;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .risk-matrix h2 {
            color: var(--primary-color);
            margin-bottom: 25px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .risk-matrix h2::before {
            content: '🎯';
            font-size: 1.2em;
        }
        
        .matrix-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            background: var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }
        
        .matrix-cell {
            background: white;
            padding: 20px;
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .matrix-cell.high-risk {
            background: linear-gradient(135deg, #fee, #fdd);
        }
        
        .matrix-cell.medium-risk {
            background: linear-gradient(135deg, #fef9e7, #fff3cd);
        }
        
        .matrix-cell.low-risk {
            background: linear-gradient(135deg, #e8f5e8, #d4edda);
        }
        
        .matrix-label {
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--text-color);
        }
        
        .matrix-count {
            font-size: 1.5em;
            font-weight: 700;
            color: var(--primary-color);
        }
        
        /* Findings Section */
        .findings-section {
            margin: 40px;
        }
        
        .findings-section h2 {
            color: var(--primary-color);
            margin-bottom: 30px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .findings-section h2::before {
            content: '🔍';
            font-size: 1.2em;
        }
        
        .finding-card {
            background: white;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        
        .finding-card:hover {
            transform: translateY(-2px);
        }
        
        .finding-header {
            padding: 25px;
            background: linear-gradient(135deg, var(--light-bg), #fff);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
        }
        
        .finding-title {
            font-size: 1.3em;
            font-weight: 600;
            color: var(--primary-color);
            margin: 0;
            flex: 1;
        }
        
        .finding-badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .severity-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .severity-badge.critical {
            background: var(--danger-color);
            color: white;
        }
        
        .severity-badge.high {
            background: var(--warning-color);
            color: white;
        }
        
        .severity-badge.medium {
            background: var(--info-color);
            color: white;
        }
        
        .severity-badge.low {
            background: var(--success-color);
            color: white;
        }
        
        .cvss-badge {
            background: var(--secondary-color);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .finding-content {
            padding: 30px;
        }
        
        .finding-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 25px;
        }
        
        .finding-details {
            background: var(--light-bg);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--accent-color);
        }
        
        .finding-details h4 {
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .finding-details p {
            color: #555;
            line-height: 1.6;
        }
        
        .target-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
        }
        
        .target-info strong {
            color: var(--primary-color);
        }
        
        .remediation-section {
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid var(--success-color);
            margin-top: 25px;
        }
        
        .remediation-section h4 {
            color: var(--success-color);
            margin-bottom: 15px;
            font-size: 1.2em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .remediation-section h4::before {
            content: '🔧';
        }
        
        .remediation-section p {
            white-space: pre-line;
            line-height: 1.7;
            color: #2d5016;
        }
        
        /* Recommendations Section */
        .recommendations-section {
            margin: 40px;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .recommendations-section h2 {
            color: var(--primary-color);
            margin-bottom: 30px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .recommendations-section h2::before {
            content: '💡';
            font-size: 1.2em;
        }
        
        .recommendation-item {
            background: var(--light-bg);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid var(--accent-color);
        }
        
        .recommendation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .recommendation-title {
            font-size: 1.2em;
            font-weight: 600;
            color: var(--primary-color);
        }
        
        .priority-badge {
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .priority-badge.immediate {
            background: var(--danger-color);
            color: white;
        }
        
        .priority-badge.high {
            background: var(--warning-color);
            color: white;
        }
        
        .priority-badge.medium {
            background: var(--info-color);
            color: white;
        }
        
        .priority-badge.low {
            background: var(--success-color);
            color: white;
        }
        
        .recommendation-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .meta-item {
            background: white;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
        }
        
        .meta-item strong {
            color: var(--primary-color);
        }
        
        /* Footer */
        .report-footer {
            background: var(--primary-color);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .footer-section h4 {
            margin-bottom: 15px;
            color: var(--accent-color);
        }
        
        .footer-section p {
            line-height: 1.6;
            opacity: 0.9;
        }
        
        .footer-bottom {
            border-top: 1px solid rgba(255,255,255,0.2);
            padding-top: 20px;
            opacity: 0.8;
        }
        
        /* Print Styles */
        @media print {
            body {
                background: white;
            }
            
            .container {
                box-shadow: none;
                max-width: none;
            }
            
            .finding-card {
                page-break-inside: avoid;
            }
            
            .recommendations-section {
                page-break-inside: avoid;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .finding-grid {
                grid-template-columns: 1fr;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .severity-cards {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .container {
                margin: 0;
            }
            
            .report-header,
            .executive-summary,
            .findings-section,
            .recommendations-section {
                margin: 20px;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Report Header -->
        <div class="report-header">
            <h1>{{ report_title }}</h1>
            <div class="report-meta">
                <div class="meta-item">
                    <div class="meta-label">Organization</div>
                    <div class="meta-value">{{ company_name }}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Assessment Period</div>
                    <div class="meta-value">{{ assessment_period }}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Report Generated</div>
                    <div class="meta-value">{{ generated_date }}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Classification</div>
                    <div class="meta-value">{{ classification }}</div>
                </div>
            </div>
        </div>

        <!-- Executive Dashboard -->
        <div class="executive-dashboard">
            <div class="dashboard-grid">
                <div class="metric-card">
                    <div class="metric-number">{{ total_findings }}</div>
                    <div class="metric-label">Total Findings</div>
                    <div class="metric-description">Security vulnerabilities identified</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{{ statistics.by_severity.critical + statistics.by_severity.high }}</div>
                    <div class="metric-label">Critical & High</div>
                    <div class="metric-description">Require immediate attention</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{{ statistics.by_host|length }}</div>
                    <div class="metric-label">Affected Assets</div>
                    <div class="metric-description">Systems with vulnerabilities</div>
                </div>
                <div class="metric-card">
                    <div class="metric-number">{{ recommendations|length }}</div>
                    <div class="metric-label">Recommendations</div>
                    <div class="metric-description">Strategic action items</div>
                </div>
            </div>

            <!-- Severity Distribution -->
            <div class="severity-cards">
                <div class="severity-card critical">
                    <div class="severity-number">{{ statistics.by_severity.critical }}</div>
                    <div class="severity-label">Critical</div>
                </div>
                <div class="severity-card high">
                    <div class="severity-number">{{ statistics.by_severity.high }}</div>
                    <div class="severity-label">High</div>
                </div>
                <div class="severity-card medium">
                    <div class="severity-number">{{ statistics.by_severity.medium }}</div>
                    <div class="severity-label">Medium</div>
                </div>
                <div class="severity-card low">
                    <div class="severity-number">{{ statistics.by_severity.low }}</div>
                    <div class="severity-label">Low</div>
                </div>
            </div>
        </div>

        <!-- Executive Summary -->
        <div class="executive-summary">
            <h2>Executive Summary</h2>
            <p>{{ executive_summary }}</p>
        </div>

        <!-- Risk Matrix -->
        <div class="risk-matrix">
            <h2>Risk Assessment Matrix</h2>
            <div class="matrix-grid">
                <div class="matrix-cell high-risk">
                    <div class="matrix-label">High Impact<br>High Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.high_likelihood.high_impact|length }}</div>
                </div>
                <div class="matrix-cell high-risk">
                    <div class="matrix-label">High Impact<br>Medium Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.medium_likelihood.high_impact|length }}</div>
                </div>
                <div class="matrix-cell medium-risk">
                    <div class="matrix-label">High Impact<br>Low Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.low_likelihood.high_impact|length }}</div>
                </div>
                <div class="matrix-cell high-risk">
                    <div class="matrix-label">Medium Impact<br>High Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.high_likelihood.medium_impact|length }}</div>
                </div>
                <div class="matrix-cell medium-risk">
                    <div class="matrix-label">Medium Impact<br>Medium Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.medium_likelihood.medium_impact|length }}</div>
                </div>
                <div class="matrix-cell low-risk">
                    <div class="matrix-label">Medium Impact<br>Low Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.low_likelihood.medium_impact|length }}</div>
                </div>
                <div class="matrix-cell medium-risk">
                    <div class="matrix-label">Low Impact<br>High Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.high_likelihood.low_impact|length }}</div>
                </div>
                <div class="matrix-cell low-risk">
                    <div class="matrix-label">Low Impact<br>Medium Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.medium_likelihood.low_impact|length }}</div>
                </div>
                <div class="matrix-cell low-risk">
                    <div class="matrix-label">Low Impact<br>Low Likelihood</div>
                    <div class="matrix-count">{{ risk_matrix.low_likelihood.low_impact|length }}</div>
                </div>
            </div>
        </div>

        <!-- Detailed Findings -->
        <div class="findings-section">
            <h2>Detailed Findings</h2>
            {% for finding in findings %}
            <div class="finding-card">
                <div class="finding-header">
                    <h3 class="finding-title">{{ finding.title }}</h3>
                    <div class="finding-badges">
                        <span class="severity-badge {{ finding.severity|lower }}">{{ finding.severity }}</span>
                        <span class="cvss-badge">CVSS {{ finding.cvss_score }}</span>
                    </div>
                </div>
                <div class="finding-content">
                    <div class="finding-grid">
                        <div class="finding-details">
                            <h4>📋 Description</h4>
                            <p>{{ finding.description }}</p>
                        </div>
                        <div class="finding-details">
                            <h4>💥 Impact</h4>
                            <p>{{ finding.impact }}</p>
                        </div>
                    </div>
                    
                    {% if finding.host or finding.port or finding.service %}
                    <div class="target-info">
                        <strong>Target Information:</strong>
                        {% if finding.host %}<span>Host: {{ finding.host }}</span>{% endif %}
                        {% if finding.port %}<span> | Port: {{ finding.port }}</span>{% endif %}
                        {% if finding.service %}<span> | Service: {{ finding.service }}</span>{% endif %}
                    </div>
                    {% endif %}
                    
                    {% if finding.evidence %}
                    <div class="finding-details">
                        <h4>🔍 Evidence</h4>
                        <p>{{ finding.evidence }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.ai_summary %}
                    <div class="finding-details">
                        <h4>🤖 AI Analysis</h4>
                        <p>{{ finding.ai_summary }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.remediation %}
                    <div class="remediation-section">
                        <h4>Remediation Steps</h4>
                        <p>{{ finding.remediation }}</p>
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Recommendations -->
        <div class="recommendations-section">
            <h2>Strategic Recommendations</h2>
            {% for recommendation in recommendations %}
            <div class="recommendation-item">
                <div class="recommendation-header">
                    <div class="recommendation-title">{{ recommendation.category }}</div>
                    <span class="priority-badge {{ recommendation.priority|lower }}">{{ recommendation.priority }}</span>
                </div>
                <p>{{ recommendation.description }}</p>
                <div class="recommendation-meta">
                    <div class="meta-item">
                        <strong>Timeline:</strong><br>{{ recommendation.timeline }}
                    </div>
                    <div class="meta-item">
                        <strong>Effort:</strong><br>{{ recommendation.effort }}
                    </div>
                    <div class="meta-item">
                        <strong>Impact:</strong><br>{{ recommendation.impact }}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Footer -->
        <div class="report-footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>Report Information</h4>
                    <p>Generated by {{ generated_by }}<br>
                    Version {{ report_version }}<br>
                    {{ generated_date }} at {{ generated_time }}</p>
                </div>
                <div class="footer-section">
                    <h4>Assessment Scope</h4>
                    <p>{{ assessment_scope }}<br>
                    Methodology: {{ assessment_methodology }}</p>
                </div>
                <div class="footer-section">
                    <h4>Classification</h4>
                    <p>{{ classification }}<br>
                    This report contains sensitive security information<br>
                    Distribution should be limited to authorized personnel</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {{ generated_date[:4] }} {{ company_name }} - CyberSec-AI AutoReport</p>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"[OK] Created industrial HTML template: {template_path}")

# Legacy function for backward compatibility
def export(findings, output_path=None, template_name="default.html.j2"):
    """Export findings to HTML report (legacy function)"""
    generator = AdvancedHTMLGenerator()
    return generator.export(findings, output_path, "industrial_report.html")

# Enhanced export function
def export_advanced(findings, output_path=None, config=None, template_name="industrial_report.html"):
    """Export findings to advanced HTML report"""
    generator = AdvancedHTMLGenerator()
    return generator.export(findings, output_path, template_name, config)

if __name__ == "__main__":
    # Test the advanced HTML generator
    test_findings = [
        {
            'title': 'SQL Injection Vulnerability',
            'description': 'A SQL injection vulnerability was discovered in the login form',
            'severity': 'High',
            'category': 'Web Application',
            'host': 'example.com',
            'port': '80',
            'service': 'HTTP',
            'evidence': 'Error-based SQL injection confirmed',
            'impact': 'Unauthorized database access possible',
            'remediation': 'Use parameterized queries and input validation'
        }
    ]
    
    generator = AdvancedHTMLGenerator()
    output = generator.export(test_findings, "test_industrial_report.html")
    print(f"Test report generated: {output}")
