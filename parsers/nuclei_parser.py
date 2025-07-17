"""
Nuclei Scanner Parser
Converts Nuclei JSON output to standardized findings format
"""

import json

def parse(file_path):
    """
    Parse Nuclei JSON output file and extract findings
    
    Args:
        file_path (str): Path to Nuclei JSON output file
        
    Returns:
        list: List of standardized finding dictionaries
    """
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Nuclei outputs one JSON object per line
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    finding = parse_nuclei_finding(data)
                    if finding:
                        findings.append(finding)
                except json.JSONDecodeError:
                    continue
    
    except Exception as e:
        findings.append({
            "title": "Nuclei Parsing Error",
            "description": f"Failed to parse Nuclei output file: {str(e)}",
            "impact": "Unable to analyze vulnerability scan results",
            "evidence": f"Parser error: {str(e)}",
            "tech_stack": "Parser",
            "category": "parsing_error",
            "source": "nuclei"
        })
    
    return findings if findings else parse_mock()

def parse_nuclei_finding(data):
    """Parse individual Nuclei finding"""
    try:
        # Map Nuclei severity levels
        severity_map = {
            'critical': 'Critical',
            'high': 'High',
            'medium': 'Medium',
            'low': 'Low',
            'info': 'Low',
            'unknown': 'Medium'
        }
        
        template_info = data.get('info', {})
        template_id = data.get('template-id', 'unknown')
        template_name = template_info.get('name', template_id)
        description = template_info.get('description', 'No description available')
        severity = severity_map.get(template_info.get('severity', 'medium').lower(), 'Medium')
        
        # Extract target information
        host = data.get('host', data.get('target', 'Unknown'))
        matched_at = data.get('matched-at', host)
        
        # Extract matcher information
        matcher_name = data.get('matcher-name', '')
        extracted_results = data.get('extracted-results', [])
        
        # Build evidence
        evidence_parts = [f"Nuclei template '{template_id}' matched"]
        if matcher_name:
            evidence_parts.append(f"Matcher: {matcher_name}")
        if extracted_results:
            evidence_parts.append(f"Extracted: {', '.join(extracted_results[:3])}")
        
        evidence = '. '.join(evidence_parts)
        
        # Determine impact based on template info
        impact = template_info.get('impact', f"Vulnerability detected by {template_name}")
        
        # Extract tags for categorization
        tags = template_info.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        category = "vulnerability_scan"
        tech_stack = "Web Application"
        
        # Categorize based on tags
        if any(tag in ['network', 'tcp', 'udp'] for tag in tags):
            tech_stack = "Network Service"
            category = "network_vulnerability"
        elif any(tag in ['cms', 'wordpress', 'joomla', 'drupal'] for tag in tags):
            tech_stack = "CMS"
        elif any(tag in ['ssl', 'tls', 'certificate'] for tag in tags):
            tech_stack = "SSL/TLS"
            category = "ssl_vulnerability"
        
        finding = {
            "title": template_name,
            "description": description,
            "severity": severity,
            "host": host,
            "matched_at": matched_at,
            "template_id": template_id,
            "impact": impact,
            "evidence": evidence,
            "tech_stack": tech_stack,
            "category": category,
            "source": "nuclei",
            "tags": tags
        }
        
        # Add matcher and extraction info if available
        if matcher_name:
            finding["matcher"] = matcher_name
        if extracted_results:
            finding["extracted"] = extracted_results
        
        # Add reference URLs if available
        references = template_info.get('reference', [])
        if references:
            finding["references"] = references
        
        # Add classification info
        classification = template_info.get('classification', {})
        if classification:
            finding["classification"] = classification
            
            # Map CVE info
            cve_id = classification.get('cve-id')
            if cve_id:
                finding["cve"] = cve_id
            
            # Map CWE info  
            cwe_id = classification.get('cwe-id')
            if cwe_id:
                finding["cwe"] = cwe_id
        
        return finding
    
    except Exception as e:
        return None

def parse_mock(file_path=None):
    """
    Mock parser for testing without real Nuclei output
    Returns sample findings for demonstration
    """
    return [
        {
            "title": "Apache HTTP Server Test Page",
            "description": "Apache HTTP Server default test page detected",
            "severity": "Low",
            "host": "https://example.com",
            "matched_at": "https://example.com/",
            "template_id": "apache-detect",
            "impact": "Default Apache test page may reveal server information",
            "evidence": "Nuclei template 'apache-detect' matched. Matcher: word",
            "tech_stack": "Web Server",
            "category": "information_disclosure",
            "source": "nuclei",
            "tags": ["apache", "detect", "tech"]
        },
        {
            "title": "SSL Certificate Information",
            "description": "SSL certificate information disclosure",
            "severity": "Low", 
            "host": "https://example.com:443",
            "matched_at": "https://example.com:443",
            "template_id": "ssl-cert-info",
            "impact": "SSL certificate details may provide reconnaissance information",
            "evidence": "Nuclei template 'ssl-cert-info' matched. Extracted: example.com, Organization",
            "tech_stack": "SSL/TLS",
            "category": "ssl_vulnerability",
            "source": "nuclei",
            "tags": ["ssl", "cert", "info"],
            "extracted": ["example.com", "Organization Name", "2024-12-31"]
        },
        {
            "title": "WordPress Version Detection",
            "description": "WordPress version information detected",
            "severity": "Medium",
            "host": "https://blog.example.com",
            "matched_at": "https://blog.example.com/wp-includes/",
            "template_id": "wordpress-version",
            "impact": "WordPress version disclosure may aid in targeted attacks",
            "evidence": "Nuclei template 'wordpress-version' matched. Extracted: 5.8.1",
            "tech_stack": "CMS",
            "category": "information_disclosure", 
            "source": "nuclei",
            "tags": ["wordpress", "version", "cms"],
            "extracted": ["5.8.1"]
        },
        {
            "title": "Directory Listing Enabled",
            "description": "Directory listing is enabled on the web server",
            "severity": "Medium",
            "host": "https://example.com",
            "matched_at": "https://example.com/uploads/",
            "template_id": "dir-listing",
            "impact": "Directory listing may expose sensitive files and folder structure",
            "evidence": "Nuclei template 'dir-listing' matched. Matcher: status,word",
            "tech_stack": "Web Server",
            "category": "information_disclosure",
            "source": "nuclei", 
            "tags": ["listing", "exposure", "files"]
        }
    ]
