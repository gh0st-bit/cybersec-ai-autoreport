"""
AI Severity Classifier
Classifies vulnerability severity using AI analysis
"""

from ai.prompt_templates import severity_prompt
from ai.openai_client import ai_client

def classify(vuln):
    """
    Classify vulnerability severity using AI
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Severity level (Critical, High, Medium, Low)
    """
    try:
        # If severity already exists and seems reasonable, use AI to validate/refine it
        existing_severity = vuln.get('severity', '').lower()
        
        prompt = severity_prompt(vuln)
        ai_severity = ai_client.chat_completion(prompt)
        
        # Clean up AI response
        ai_severity = ai_severity.strip().replace(':', '').replace('.', '')
        
        # Validate AI response
        valid_severities = ['Critical', 'High', 'Medium', 'Low']
        for severity in valid_severities:
            if severity.lower() in ai_severity.lower():
                return severity
        
        # Fallback to rule-based classification
        return classify_by_rules(vuln)
    
    except Exception as e:
        # Fallback to rule-based classification
        return classify_by_rules(vuln)

def classify_by_rules(vuln):
    """
    Fallback rule-based severity classification
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Severity level (Critical, High, Medium, Low)
    """
    title = vuln.get('title', '').lower()
    description = vuln.get('description', '').lower()
    category = vuln.get('category', '').lower()
    existing_severity = vuln.get('severity', '').lower()
    
    # If existing severity is valid, use it
    if existing_severity in ['critical', 'high', 'medium', 'low']:
        return existing_severity.capitalize()
    
    # Critical severity indicators
    critical_indicators = [
        'sql injection', 'sqli', 'remote code execution', 'rce',
        'command injection', 'path traversal', 'directory traversal',
        'file upload', 'arbitrary file', 'authentication bypass',
        'privilege escalation', 'buffer overflow'
    ]
    
    # High severity indicators
    high_indicators = [
        'cross-site scripting', 'xss', 'csrf', 'cross-site request forgery',
        'session fixation', 'insecure direct object', 'security misconfiguration',
        'sensitive data exposure', 'xml external entity', 'xxe',
        'broken access control', 'injection'
    ]
    
    # Medium severity indicators
    medium_indicators = [
        'information disclosure', 'information leakage', 'directory listing',
        'version disclosure', 'banner grabbing', 'weak encryption',
        'insecure transmission', 'missing security headers',
        'clickjacking', 'open redirect'
    ]
    
    # Low severity indicators
    low_indicators = [
        'information', 'disclosure', 'fingerprinting', 'enumeration',
        'default', 'test page', 'debug', 'comment', 'metadata'
    ]
    
    combined_text = f"{title} {description}"
    
    # Check for critical indicators
    if any(indicator in combined_text for indicator in critical_indicators):
        return 'Critical'
    
    # Check for high indicators
    if any(indicator in combined_text for indicator in high_indicators):
        return 'High'
    
    # Check for medium indicators
    if any(indicator in combined_text for indicator in medium_indicators):
        return 'Medium'
    
    # Check for low indicators
    if any(indicator in combined_text for indicator in low_indicators):
        return 'Low'
    
    # Check by category
    if 'web_vulnerability' in category:
        return 'High'
    elif 'network_vulnerability' in category:
        return 'Medium'
    elif 'information_disclosure' in category:
        return 'Low'
    elif 'ssl_vulnerability' in category:
        return 'Medium'
    
    # Default to Medium if uncertain
    return 'Medium'

def get_severity_score(severity):
    """
    Convert severity to numeric score for sorting
    
    Args:
        severity (str): Severity level
        
    Returns:
        int: Numeric score (higher = more severe)
    """
    severity_scores = {
        'Critical': 4,
        'High': 3,
        'Medium': 2,
        'Low': 1,
        'Unknown': 0
    }
    
    return severity_scores.get(severity, 0)

def sort_by_severity(findings_list):
    """
    Sort findings by severity (Critical first, Low last)
    
    Args:
        findings_list (list): List of findings
        
    Returns:
        list: Sorted findings list
    """
    return sorted(
        findings_list,
        key=lambda x: get_severity_score(x.get('severity', 'Medium')),
        reverse=True
    )
