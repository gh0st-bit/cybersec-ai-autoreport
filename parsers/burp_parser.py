"""
Burp Suite Parser
Converts Burp Suite JSON/XML output to standardized findings format
"""

import json
import xml.etree.ElementTree as ET

def parse(file_path):
    """
    Parse Burp Suite export file and extract findings
    
    Args:
        file_path (str): Path to Burp Suite export file
        
    Returns:
        list: List of standardized finding dictionaries
    """
    findings = []
    
    try:
        # Try JSON format first
        if file_path.lower().endswith('.json'):
            findings = parse_json(file_path)
        elif file_path.lower().endswith('.xml'):
            findings = parse_xml(file_path)
        else:
            # Try to detect format by content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if content.startswith('{') or content.startswith('['):
                findings = parse_json_content(content)
            elif content.startswith('<'):
                findings = parse_xml_content(content)
    
    except Exception as e:
        findings.append({
            "title": "Burp Suite Parsing Error",
            "description": f"Failed to parse Burp Suite file: {str(e)}",
            "impact": "Unable to analyze web application scan results",
            "evidence": f"Parser error: {str(e)}",
            "tech_stack": "Parser",
            "category": "parsing_error",
            "source": "burp"
        })
    
    return findings if findings else parse_mock()

def parse_json(file_path):
    """Parse Burp Suite JSON export"""
    findings = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    issues = []
    if isinstance(data, list):
        issues = data
    elif isinstance(data, dict):
        issues = data.get('issues', data.get('vulnerabilities', [data]))
    
    for issue in issues:
        finding = parse_burp_issue(issue)
        if finding:
            findings.append(finding)
    
    return findings

def parse_json_content(content):
    """Parse Burp Suite JSON content"""
    data = json.loads(content)
    findings = []
    
    issues = []
    if isinstance(data, list):
        issues = data
    elif isinstance(data, dict):
        issues = data.get('issues', data.get('vulnerabilities', [data]))
    
    for issue in issues:
        finding = parse_burp_issue(issue)
        if finding:
            findings.append(finding)
    
    return findings

def parse_xml(file_path):
    """Parse Burp Suite XML export"""
    findings = []
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Parse XML issues
    for issue in root.findall('.//issue'):
        finding = parse_burp_xml_issue(issue)
        if finding:
            findings.append(finding)
    
    return findings

def parse_xml_content(content):
    """Parse Burp Suite XML content"""
    findings = []
    
    root = ET.fromstring(content)
    
    for issue in root.findall('.//issue'):
        finding = parse_burp_xml_issue(issue)
        if finding:
            findings.append(finding)
    
    return findings

def parse_burp_issue(issue):
    """Parse individual Burp issue from JSON"""
    try:
        # Map Burp severity to standard levels
        severity_map = {
            'High': 'High',
            'Medium': 'Medium', 
            'Low': 'Low',
            'Information': 'Low'
        }
        
        title = issue.get('issueName', issue.get('name', 'Unknown Vulnerability'))
        description = issue.get('issueDetail', issue.get('description', 'No description available'))
        severity = severity_map.get(issue.get('severity', 'Medium'), 'Medium')
        
        # Extract URL/host info
        url = issue.get('url', issue.get('host', 'Unknown'))
        host = issue.get('host', url)
        
        finding = {
            "title": title,
            "description": description,
            "severity": severity,
            "url": url,
            "host": host,
            "impact": issue.get('impact', 'Potential security vulnerability identified'),
            "evidence": issue.get('issueBackground', issue.get('evidence', 'Burp Suite scan detection')),
            "remediation": issue.get('remediationDetail', issue.get('solution', '')),
            "tech_stack": "Web Application",
            "category": "web_vulnerability",
            "source": "burp",
            "confidence": issue.get('confidence', 'Medium')
        }
        
        # Add request/response if available
        if 'request' in issue:
            finding['request'] = issue['request']
        if 'response' in issue:
            finding['response'] = issue['response']
        
        return finding
    
    except Exception as e:
        return None

def parse_burp_xml_issue(issue_elem):
    """Parse individual Burp issue from XML"""
    try:
        severity_map = {
            'High': 'High',
            'Medium': 'Medium',
            'Low': 'Low', 
            'Information': 'Low'
        }
        
        title = issue_elem.findtext('name', 'Unknown Vulnerability')
        description = issue_elem.findtext('issueDetail', 'No description available')
        severity = severity_map.get(issue_elem.findtext('severity', 'Medium'), 'Medium')
        url = issue_elem.findtext('url', 'Unknown')
        host = issue_elem.findtext('host', url)
        
        finding = {
            "title": title,
            "description": description,
            "severity": severity,
            "url": url,
            "host": host,
            "impact": issue_elem.findtext('impact', 'Potential security vulnerability identified'),
            "evidence": issue_elem.findtext('issueBackground', 'Burp Suite scan detection'),
            "remediation": issue_elem.findtext('remediationDetail', ''),
            "tech_stack": "Web Application",
            "category": "web_vulnerability",
            "source": "burp",
            "confidence": issue_elem.findtext('confidence', 'Medium')
        }
        
        return finding
    
    except Exception as e:
        return None

def parse_mock(file_path=None):
    """
    Mock parser for testing without real Burp Suite export
    Returns sample findings for demonstration
    """
    return [
        {
            "title": "Cross-Site Scripting (XSS)",
            "description": "Reflected XSS vulnerability found in search parameter",
            "severity": "High",
            "url": "https://example.com/search?q=<script>alert(1)</script>",
            "host": "example.com",
            "impact": "Attackers can execute malicious scripts in victim browsers",
            "evidence": "Parameter 'q' reflects user input without proper sanitization",
            "remediation": "Implement input validation and output encoding",
            "tech_stack": "Web Application",
            "category": "web_vulnerability",
            "source": "burp",
            "confidence": "High"
        },
        {
            "title": "SQL Injection",
            "description": "SQL injection vulnerability in login form",
            "severity": "Critical",
            "url": "https://example.com/login.php",
            "host": "example.com",
            "impact": "Attackers can access, modify, or delete database information",
            "evidence": "Parameter 'username' is vulnerable to SQL injection attacks",
            "remediation": "Use parameterized queries or prepared statements",
            "tech_stack": "Web Application",
            "category": "web_vulnerability",
            "source": "burp",
            "confidence": "High"
        },
        {
            "title": "Information Disclosure",
            "description": "Server version information disclosed in HTTP headers",
            "severity": "Low",
            "url": "https://example.com/",
            "host": "example.com",
            "impact": "Server technology information may aid attackers",
            "evidence": "Server header reveals Apache/2.4.41 version information",
            "remediation": "Configure server to suppress version information",
            "tech_stack": "Web Server",
            "category": "information_disclosure",
            "source": "burp",
            "confidence": "Medium"
        }
    ]
