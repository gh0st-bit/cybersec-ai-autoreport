"""
AI Summarizer
Generates executive summaries for security findings
"""

from ai.prompt_templates import summary_prompt
from ai.openai_client import ai_client

def generate(vuln):
    """
    Generate AI-powered executive summary for a vulnerability
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Executive summary text
    """
    try:
        prompt = summary_prompt(vuln)
        summary = ai_client.chat_completion(prompt)
        return summary
    except Exception as e:
        # Fallback to basic summary
        title = vuln.get('title', 'Security Finding')
        severity = vuln.get('severity', 'Medium')
        return f"A {severity.lower()} severity security issue was identified: {title}. This finding requires review and remediation according to security best practices."

def generate_executive_summary(findings_list):
    """
    Generate overall executive summary for all findings
    
    Args:
        findings_list (list): List of all vulnerability findings
        
    Returns:
        str: Executive summary for the entire report
    """
    try:
        from ai.prompt_templates import executive_summary_prompt
        prompt = executive_summary_prompt(findings_list)
        summary = ai_client.chat_completion(prompt, max_tokens=2000)
        return summary
    except Exception as e:
        # Fallback to basic summary
        total = len(findings_list)
        high_severity = len([f for f in findings_list if f.get('severity') in ['Critical', 'High']])
        
        return f"""Security Assessment Summary

This assessment identified {total} security findings across the tested systems and applications. Of these, {high_severity} findings are classified as high or critical severity and require immediate attention.

The findings indicate various security concerns including network service exposures, web application vulnerabilities, and configuration issues. These vulnerabilities could potentially be exploited by attackers to gain unauthorized access, compromise data integrity, or disrupt system operations.

Priority should be given to addressing the high and critical severity findings first, followed by medium and low severity items. A coordinated remediation effort involving system administrators, developers, and security teams is recommended to ensure comprehensive security improvements.

Regular security assessments and monitoring should be implemented to maintain the security posture and detect new vulnerabilities as they emerge."""
