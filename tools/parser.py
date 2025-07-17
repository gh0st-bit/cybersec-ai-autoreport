"""
Custom Tool Output Parser
Uses AI to parse and extract findings from custom tool outputs
"""

from ai.prompt_templates import summary_prompt, severity_prompt
from ai.openai_client import ai_client

def parse_output(output_file_path):
    """
    Parse custom tool output using AI
    
    Args:
        output_file_path (str): Path to tool output file
        
    Returns:
        str: AI-generated summary of findings
    """
    try:
        # Read the output file
        with open(output_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Limit content size to avoid token limits
        if len(content) > 10000:
            content = content[:10000] + "\n... (truncated)"
        
        # Generate AI-powered analysis
        prompt = custom_tool_analysis_prompt(content, output_file_path)
        summary = ai_client.chat_completion(prompt, max_tokens=2000)
        
        return summary
    
    except Exception as e:
        return f"Failed to parse tool output: {str(e)}"

def extract_findings(output_file_path, tool_name=None):
    """
    Extract structured findings from custom tool output
    
    Args:
        output_file_path (str): Path to tool output file
        tool_name (str): Name of the tool that generated output
        
    Returns:
        list: List of structured findings
    """
    try:
        with open(output_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Limit content size
        if len(content) > 15000:
            content = content[:15000] + "\n... (truncated)"
        
        # Generate structured findings using AI
        prompt = findings_extraction_prompt(content, tool_name or "custom_tool")
        findings_text = ai_client.chat_completion(prompt, max_tokens=2500)
        
        # Try to parse the AI response into structured findings
        findings = parse_ai_findings_response(findings_text, output_file_path, tool_name)
        
        return findings
    
    except Exception as e:
        # Return a basic finding if parsing fails
        return [{
            "title": f"Custom Tool Output: {tool_name or 'Unknown Tool'}",
            "description": f"Custom tool execution completed. See output file for details: {output_file_path}",
            "impact": "Manual review required to determine security impact",
            "evidence": f"Tool output saved to {output_file_path}",
            "tech_stack": "Custom Tool",
            "category": "custom_tool_output",
            "source": tool_name or "custom_tool",
            "severity": "Medium"
        }]

def custom_tool_analysis_prompt(content, file_path):
    """Generate prompt for custom tool analysis"""
    return f"""You are a cybersecurity analyst reviewing output from a security tool.

Analyze the following tool output and provide a summary of any security findings:

Tool Output File: {file_path}
Content:
{content}

Please provide:
1. A brief summary of what the tool found
2. Any security issues or vulnerabilities identified
3. Notable findings that require attention
4. Overall assessment of the security posture

If no significant security issues are found, indicate that the scan completed without notable findings.

Analysis:"""

def findings_extraction_prompt(content, tool_name):
    """Generate prompt for extracting structured findings"""
    return f"""You are a cybersecurity analyst extracting findings from tool output.

Extract security findings from this {tool_name} output and format them as structured findings:

Tool Output:
{content}

For each security finding you identify, provide:
- Title: Brief descriptive title
- Severity: Critical/High/Medium/Low
- Description: What was found
- Impact: Potential security impact
- Host/Target: Affected system or URL (if identifiable)

Format each finding as:
FINDING: [Title]
SEVERITY: [Severity Level]  
DESCRIPTION: [Description]
IMPACT: [Impact]
TARGET: [Host/URL/System]
---

If no security findings are present, respond with "NO SECURITY FINDINGS IDENTIFIED"

Findings:"""

def parse_ai_findings_response(ai_response, output_file, tool_name):
    """
    Parse AI response into structured findings list
    
    Args:
        ai_response (str): AI-generated findings text
        output_file (str): Path to original output file
        tool_name (str): Name of the tool
        
    Returns:
        list: List of structured finding dictionaries
    """
    findings = []
    
    if "NO SECURITY FINDINGS IDENTIFIED" in ai_response.upper():
        # Return a basic info finding
        return [{
            "title": f"{tool_name} Scan Completed",
            "description": f"Security scan completed successfully with no significant findings identified",
            "impact": "No immediate security concerns detected",
            "evidence": f"Tool output: {output_file}",
            "tech_stack": "Security Tool",
            "category": "scan_complete",
            "source": tool_name or "custom_tool",
            "severity": "Low"
        }]
    
    # Split findings by separator
    finding_blocks = ai_response.split('---')
    
    for block in finding_blocks:
        block = block.strip()
        if not block:
            continue
        
        finding = parse_finding_block(block, output_file, tool_name)
        if finding:
            findings.append(finding)
    
    # If no findings parsed, create a generic one
    if not findings:
        findings.append({
            "title": f"Custom Tool Analysis: {tool_name}",
            "description": ai_response[:500] + "..." if len(ai_response) > 500 else ai_response,
            "impact": "Manual review required",
            "evidence": f"Tool output: {output_file}",
            "tech_stack": "Security Tool",
            "category": "custom_analysis",
            "source": tool_name or "custom_tool",
            "severity": "Medium"
        })
    
    return findings

def parse_finding_block(block, output_file, tool_name):
    """Parse individual finding block from AI response"""
    try:
        finding = {
            "title": "Unknown Finding",
            "description": "No description provided",
            "impact": "Impact unknown",
            "evidence": f"Tool output: {output_file}",
            "tech_stack": "Security Tool",
            "category": "custom_tool_finding",
            "source": tool_name or "custom_tool",
            "severity": "Medium"
        }
        
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().upper()
                value = value.strip()
                
                if key in ['FINDING', 'TITLE']:
                    finding["title"] = value
                elif key == 'SEVERITY':
                    # Validate severity
                    valid_severities = ['Critical', 'High', 'Medium', 'Low']
                    for sev in valid_severities:
                        if sev.lower() in value.lower():
                            finding["severity"] = sev
                            break
                elif key == 'DESCRIPTION':
                    finding["description"] = value
                elif key == 'IMPACT':
                    finding["impact"] = value
                elif key in ['TARGET', 'HOST', 'URL']:
                    finding["host"] = value
                    finding["target"] = value
        
        # Only return finding if it has meaningful content
        if finding["title"] != "Unknown Finding" or finding["description"] != "No description provided":
            return finding
        
        return None
    
    except Exception as e:
        return None

def analyze_output_patterns(content):
    """
    Analyze output for common security tool patterns
    
    Args:
        content (str): Tool output content
        
    Returns:
        dict: Analysis results with pattern matches
    """
    patterns = {
        'vulnerabilities': [
            'vulnerability', 'vuln', 'cve-', 'exploit', 'injection',
            'xss', 'sql injection', 'buffer overflow', 'rce'
        ],
        'network_issues': [
            'open port', 'service', 'banner', 'version', 'protocol',
            'ssl', 'tls', 'certificate', 'cipher'
        ],
        'web_issues': [
            'http', 'https', 'web', 'cookie', 'session', 'authentication',
            'authorization', 'redirect', 'cors'
        ],
        'info_disclosure': [
            'information disclosure', 'directory listing', 'backup',
            'config', 'debug', 'error', 'stacktrace'
        ]
    }
    
    content_lower = content.lower()
    matches = {}
    
    for category, keywords in patterns.items():
        matches[category] = sum(1 for keyword in keywords if keyword in content_lower)
    
    return matches

def suggest_remediation_for_tool_output(content, tool_name):
    """
    Generate remediation suggestions for custom tool findings
    
    Args:
        content (str): Tool output content
        tool_name (str): Name of the tool
        
    Returns:
        str: Remediation suggestions
    """
    try:
        prompt = f"""You are a cybersecurity expert providing remediation guidance.

Based on this {tool_name} tool output, provide specific remediation recommendations:

Tool Output:
{content[:5000]}

Provide actionable remediation steps for any security issues identified. If no specific issues are found, provide general security hardening recommendations.

Remediation Recommendations:"""

        return ai_client.chat_completion(prompt, max_tokens=1500)
    
    except Exception as e:
        return "Manual review of tool output recommended. Apply security best practices for identified issues."
