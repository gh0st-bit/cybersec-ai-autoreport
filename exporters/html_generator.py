"""
HTML Report Generator
Converts findings to HTML reports using Jinja2 templates
"""

import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from ai.summarizer import generate_executive_summary
from ai.severity_classifier import sort_by_severity

def export(findings, output_path=None, template_name="default.html.j2"):
    """
    Export findings to HTML report
    
    Args:
        findings (list): List of findings to include in report
        output_path (str): Output file path (optional)
        template_name (str): Template file name to use
        
    Returns:
        str: Path to generated HTML file
    """
    try:
        # Ensure reports directory exists
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(reports_dir, f"cybersec_report_{timestamp}.html")
        
        # Load template
        template_path = Path(__file__).parent.parent / "templates"
        env = Environment(loader=FileSystemLoader(str(template_path)))
        
        try:
            template = env.get_template(template_name)
        except:
            # Fallback to inline template if file not found
            template = Template(get_default_template())
        
        # Sort findings by severity
        sorted_findings = sort_by_severity(findings)
        
        # Generate statistics
        stats = generate_statistics(sorted_findings)
        
        # Generate executive summary
        exec_summary = generate_executive_summary(sorted_findings)
        
        # Render template
        html_content = template.render(
            report_title="Cybersecurity Assessment Report",
            company_name="Security Assessment",
            generated_date=datetime.now().strftime("%B %d, %Y"),
            generated_time=datetime.now().strftime("%H:%M:%S"),
            findings=sorted_findings,
            statistics=stats,
            executive_summary=exec_summary,
            total_findings=len(sorted_findings)
        )
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] HTML report generated: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"[ERROR] Failed to generate HTML report: {str(e)}")
        raise

def generate_statistics(findings):
    """Generate statistics from findings"""
    stats = {
        'total': len(findings),
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
        'categories': {},
        'sources': {}
    }
    
    for finding in findings:
        # Count by severity
        severity = finding.get('severity', 'Medium').lower()
        if severity == 'critical':
            stats['critical'] += 1
        elif severity == 'high':
            stats['high'] += 1
        elif severity == 'medium':
            stats['medium'] += 1
        elif severity == 'low':
            stats['low'] += 1
        
        # Count by category
        category = finding.get('category', 'other')
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        # Count by source
        source = finding.get('source', 'unknown')
        stats['sources'][source] = stats['sources'].get(source, 0) + 1
    
    return stats

def get_severity_color(severity):
    """Get CSS color class for severity"""
    colors = {
        'Critical': 'danger',
        'High': 'warning', 
        'Medium': 'info',
        'Low': 'success'
    }
    return colors.get(severity, 'secondary')

def get_default_template():
    """Default HTML template if external template file is not available"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header .meta {
            color: #6c757d;
            font-size: 14px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            border-left: 4px solid #007bff;
        }
        .stat-card.critical { border-left-color: #dc3545; }
        .stat-card.high { border-left-color: #fd7e14; }
        .stat-card.medium { border-left-color: #ffc107; }
        .stat-card.low { border-left-color: #28a745; }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #6c757d;
            font-size: 14px;
            text-transform: uppercase;
        }
        .executive-summary {
            background: #e3f2fd;
            padding: 25px;
            border-radius: 6px;
            margin-bottom: 40px;
            border-left: 4px solid #2196f3;
        }
        .executive-summary h2 {
            color: #1976d2;
            margin-top: 0;
        }
        .findings {
            margin-top: 30px;
        }
        .finding {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .finding-header {
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .finding-title {
            font-weight: 600;
            color: #2c3e50;
            margin: 0;
        }
        .severity {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .severity.critical {
            background: #fee;
            color: #dc3545;
        }
        .severity.high {
            background: #fff3cd;
            color: #fd7e14;
        }
        .severity.medium {
            background: #cff4fc;
            color: #0dcaf0;
        }
        .severity.low {
            background: #d1edff;
            color: #0d6efd;
        }
        .finding-content {
            padding: 20px;
        }
        .finding-section {
            margin-bottom: 15px;
        }
        .finding-section h4 {
            margin: 0 0 8px 0;
            color: #495057;
            font-size: 14px;
            text-transform: uppercase;
            font-weight: 600;
        }
        .finding-section p {
            margin: 0;
            color: #6c757d;
        }
        .remediation {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 3px solid #28a745;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ report_title }}</h1>
            <div class="meta">
                Generated on {{ generated_date }} at {{ generated_time }}<br>
                Total Findings: {{ total_findings }}
            </div>
        </div>

        <div class="stats">
            <div class="stat-card critical">
                <div class="stat-number">{{ statistics.critical }}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card high">
                <div class="stat-number">{{ statistics.high }}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card medium">
                <div class="stat-number">{{ statistics.medium }}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card low">
                <div class="stat-number">{{ statistics.low }}</div>
                <div class="stat-label">Low</div>
            </div>
        </div>

        <div class="executive-summary">
            <h2>[SUMMARY] Executive Summary</h2>
            <p>{{ executive_summary }}</p>
        </div>

        <div class="findings">
            <h2>[FINDINGS] Detailed Findings</h2>
            {% for finding in findings %}
            <div class="finding">
                <div class="finding-header">
                    <h3 class="finding-title">{{ finding.title }}</h3>
                    <span class="severity {{ finding.severity|lower }}">{{ finding.severity }}</span>
                </div>
                <div class="finding-content">
                    <div class="finding-section">
                        <h4>Description</h4>
                        <p>{{ finding.description }}</p>
                    </div>
                    
                    {% if finding.impact %}
                    <div class="finding-section">
                        <h4>Impact</h4>
                        <p>{{ finding.impact }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.host or finding.url %}
                    <div class="finding-section">
                        <h4>Target</h4>
                        <p>{{ finding.host or finding.url }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.evidence %}
                    <div class="finding-section">
                        <h4>Evidence</h4>
                        <p>{{ finding.evidence }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.ai_summary %}
                    <div class="finding-section">
                        <h4>AI Analysis</h4>
                        <p>{{ finding.ai_summary }}</p>
                    </div>
                    {% endif %}
                    
                    {% if finding.remediation %}
                    <div class="finding-section">
                        <h4>Remediation</h4>
                        <div class="remediation">
                            <p style="white-space: pre-line;">{{ finding.remediation }}</p>
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="footer">
            Generated by CyberSec-AI AutoReport v1.0.0
        </div>
    </div>
</body>
</html>"""
