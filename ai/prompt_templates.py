"""
AI Prompt Templates for Security Analysis
Structured prompts for different AI enhancement tasks
"""

def summary_prompt(vuln):
    """Generate prompt for executive summary"""
    return f"""You are a cybersecurity analyst writing for business executives. 

Create a clear, non-technical summary of this security finding:

Title: {vuln.get('title', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Impact: {vuln.get('impact', 'Impact unknown')}
Evidence: {vuln.get('evidence', 'No evidence provided')}

Write a 2-3 sentence executive summary that explains:
1. What the issue is in simple terms
2. Why it matters to the business
3. The potential business impact

Executive Summary:"""

def severity_prompt(vuln):
    """Generate prompt for severity classification"""
    return f"""You are a cybersecurity expert using CVSS and industry standards.

Analyze this vulnerability and assign a severity rating:

Title: {vuln.get('title', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Impact: {vuln.get('impact', 'Impact unknown')}
Host/Target: {vuln.get('host', vuln.get('url', 'Unknown target'))}
Current Severity: {vuln.get('severity', 'Not assigned')}

Based on CVSS criteria, assign ONE of these severity levels:
- Critical: Immediate threat, can cause severe damage
- High: Significant risk, should be addressed urgently  
- Medium: Moderate risk, should be addressed in reasonable timeframe
- Low: Minor risk, can be addressed during routine maintenance

Consider:
- Exploitability (how easy to exploit)
- Impact scope (data, systems, operations)
- Attack complexity and requirements
- Business context

Severity:"""

def remediation_prompt(vuln):
    """Generate prompt for remediation suggestions"""
    return f"""You are a cybersecurity expert providing remediation guidance.

Provide specific, actionable remediation steps for this vulnerability:

Title: {vuln.get('title', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Technology: {vuln.get('tech_stack', 'Unknown technology')}
Host/Target: {vuln.get('host', vuln.get('url', 'Unknown target'))}
Category: {vuln.get('category', 'General')}

Provide remediation steps that include:
1. Immediate actions (quick fixes)
2. Long-term solutions (proper fixes)
3. Detection/monitoring recommendations
4. Prevention measures

Make recommendations specific to the technology stack when possible.

Remediation Steps:"""

def risk_assessment_prompt(vuln):
    """Generate prompt for risk assessment"""
    return f"""You are a risk analyst evaluating cybersecurity threats.

Assess the business risk of this security finding:

Title: {vuln.get('title', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Severity: {vuln.get('severity', 'Unknown')}
Technology: {vuln.get('tech_stack', 'Unknown')}
Evidence: {vuln.get('evidence', 'No evidence')}

Evaluate:
1. Likelihood of exploitation (High/Medium/Low)
2. Business impact if exploited (High/Medium/Low)
3. Overall risk level (Critical/High/Medium/Low)
4. Key risk factors

Risk Assessment:"""

def executive_summary_prompt(findings_list):
    """Generate prompt for overall executive summary"""
    findings_summary = "\n".join([
        f"- {finding.get('title', 'Unknown')}: {finding.get('severity', 'Unknown')} severity"
        for finding in findings_list[:10]  # Limit to top 10 findings
    ])
    
    total_findings = len(findings_list)
    severity_counts = {}
    for finding in findings_list:
        severity = finding.get('severity', 'Unknown')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    return f"""You are a CISO writing an executive summary for senior leadership.

Based on this cybersecurity assessment with {total_findings} total findings:

Severity Breakdown:
{chr(10).join([f"- {sev}: {count} findings" for sev, count in severity_counts.items()])}

Key Findings:
{findings_summary}

Write a comprehensive executive summary (3-4 paragraphs) that covers:
1. Overall security posture assessment
2. Key risks and their business impact
3. Priority recommendations for leadership
4. Suggested next steps and timeline

Focus on business impact, not technical details. Use language appropriate for C-level executives.

Executive Summary:"""

def technical_details_prompt(vuln):
    """Generate prompt for technical analysis"""
    return f"""You are a senior security engineer providing technical analysis.

Provide detailed technical analysis of this vulnerability:

Title: {vuln.get('title', 'Unknown')}
Description: {vuln.get('description', 'No description')}
Evidence: {vuln.get('evidence', 'No evidence')}
Technology: {vuln.get('tech_stack', 'Unknown')}
Source Tool: {vuln.get('source', 'Unknown')}

Provide technical analysis including:
1. Attack vectors and exploitation methods
2. Technical impact and affected components
3. Root cause analysis
4. Technical remediation details
5. Validation/testing recommendations

Technical Analysis:"""
