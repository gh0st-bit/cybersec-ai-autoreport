"""
AI Remediation Generator
Generates remediation suggestions for security findings
"""

from ai.prompt_templates import remediation_prompt, technical_details_prompt
from ai.openai_client import ai_client

def suggest(vuln):
    """
    Generate AI-powered remediation suggestions for a vulnerability
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Remediation suggestions text
    """
    try:
        prompt = remediation_prompt(vuln)
        remediation = ai_client.chat_completion(prompt, max_tokens=2000)
        return remediation
    except Exception as e:
        # Fallback to rule-based remediation
        return generate_fallback_remediation(vuln)

def generate_technical_analysis(vuln):
    """
    Generate detailed technical analysis for a vulnerability
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Technical analysis text
    """
    try:
        prompt = technical_details_prompt(vuln)
        analysis = ai_client.chat_completion(prompt, max_tokens=2000)
        return analysis
    except Exception as e:
        return "Technical analysis requires further investigation by security experts."

def generate_fallback_remediation(vuln):
    """
    Generate rule-based remediation suggestions when AI is not available
    
    Args:
        vuln (dict): Vulnerability finding dictionary
        
    Returns:
        str: Remediation suggestions text
    """
    title = vuln.get('title', '').lower()
    description = vuln.get('description', '').lower()
    tech_stack = vuln.get('tech_stack', '').lower()
    category = vuln.get('category', '').lower()
    
    # SQL Injection
    if 'sql injection' in title or 'sqli' in title:
        return """1. Immediate Actions:
   - Implement parameterized queries (prepared statements)
   - Apply input validation and sanitization
   - Review and update all database queries

2. Long-term Solutions:
   - Use ORM frameworks with built-in SQL injection protection
   - Implement least privilege database access
   - Regular security code reviews

3. Monitoring:
   - Enable database query logging
   - Implement Web Application Firewall (WAF)
   - Monitor for suspicious database activities

4. Prevention:
   - Security awareness training for developers
   - Automated security testing in CI/CD pipeline
   - Regular penetration testing"""

    # Cross-Site Scripting (XSS)
    elif 'xss' in title or 'cross-site scripting' in title:
        return """1. Immediate Actions:
   - Implement output encoding for all user inputs
   - Apply input validation and sanitization
   - Use Content Security Policy (CSP) headers

2. Long-term Solutions:
   - Implement proper templating engines with auto-escaping
   - Use secure coding frameworks
   - Regular security code reviews

3. Monitoring:
   - Implement Web Application Firewall (WAF)
   - Monitor for XSS attack patterns
   - Regular vulnerability scanning

4. Prevention:
   - Security awareness training for developers
   - Automated security testing tools
   - Secure development lifecycle (SDLC)"""

    # SSH/Remote Access
    elif 'ssh' in title or 'remote' in title:
        return """1. Immediate Actions:
   - Change default SSH port (from 22 to non-standard port)
   - Disable root login via SSH
   - Implement fail2ban for brute force protection

2. Long-term Solutions:
   - Configure key-based authentication only
   - Restrict SSH access by IP address
   - Implement multi-factor authentication

3. Monitoring:
   - Monitor SSH login attempts and failures
   - Set up alerts for suspicious activities
   - Regular audit of SSH access logs

4. Prevention:
   - Regular security updates and patches
   - Network segmentation
   - VPN access for remote connections"""

    # Information Disclosure
    elif 'information disclosure' in title or 'version' in title or 'banner' in title:
        return """1. Immediate Actions:
   - Remove or obscure version information from headers
   - Configure servers to suppress detailed error messages
   - Review and remove unnecessary information exposure

2. Long-term Solutions:
   - Implement proper error handling
   - Configure security headers appropriately
   - Regular security configuration reviews

3. Monitoring:
   - Monitor for information leakage in logs
   - Regular security scanning
   - Automated configuration compliance checks

4. Prevention:
   - Security hardening guidelines
   - Regular security assessments
   - Security awareness training"""

    # Web Application vulnerabilities
    elif 'web' in tech_stack or 'application' in tech_stack:
        return """1. Immediate Actions:
   - Review and validate all user inputs
   - Implement proper authentication and authorization
   - Apply security patches and updates

2. Long-term Solutions:
   - Implement secure coding practices
   - Use security frameworks and libraries
   - Regular security code reviews

3. Monitoring:
   - Implement Web Application Firewall (WAF)
   - Regular vulnerability scanning
   - Security event monitoring

4. Prevention:
   - Security development lifecycle (SDLC)
   - Automated security testing
   - Regular penetration testing"""

    # Network vulnerabilities
    elif 'network' in tech_stack or 'network' in category:
        return """1. Immediate Actions:
   - Review and restrict network access
   - Apply security patches to network services
   - Implement proper firewall rules

2. Long-term Solutions:
   - Network segmentation and isolation
   - Implement intrusion detection systems
   - Regular network security assessments

3. Monitoring:
   - Network traffic monitoring
   - Intrusion detection and prevention
   - Regular network scanning

4. Prevention:
   - Network security policies
   - Regular security updates
   - Network access controls"""

    # SSL/TLS issues
    elif 'ssl' in title or 'tls' in title or 'certificate' in title:
        return """1. Immediate Actions:
   - Update SSL/TLS certificates if expired
   - Configure strong cipher suites
   - Disable weak protocols (SSLv2, SSLv3, TLS 1.0, TLS 1.1)

2. Long-term Solutions:
   - Implement proper certificate management
   - Use TLS 1.2 or higher with strong ciphers
   - Implement certificate pinning where appropriate

3. Monitoring:
   - Monitor certificate expiration dates
   - Regular SSL/TLS configuration testing
   - Automated certificate renewal

4. Prevention:
   - SSL/TLS configuration standards
   - Regular security assessments
   - Certificate lifecycle management"""

    # Generic remediation
    else:
        return """1. Immediate Actions:
   - Assess the scope and impact of the vulnerability
   - Apply available security patches and updates
   - Implement temporary mitigations if needed

2. Long-term Solutions:
   - Follow security best practices for the affected technology
   - Implement proper security controls and configurations
   - Regular security reviews and assessments

3. Monitoring:
   - Implement monitoring for the affected systems
   - Set up alerts for suspicious activities
   - Regular vulnerability scanning

4. Prevention:
   - Establish regular security update procedures
   - Implement security awareness training
   - Regular security assessments and testing"""
