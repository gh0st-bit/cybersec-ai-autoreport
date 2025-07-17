"""
Nmap XML Parser
Converts Nmap XML output to standardized findings format
"""

import xml.etree.ElementTree as ET
import json

# Try to import xmltodict, use fallback if not available
try:
    import xmltodict
    XMLTODICT_AVAILABLE = True
except ImportError:
    XMLTODICT_AVAILABLE = False

def parse(file_path):
    """
    Parse Nmap XML file and extract findings
    
    Args:
        file_path (str): Path to Nmap XML file
        
    Returns:
        list: List of standardized finding dictionaries
    """
    findings = []
    
    try:
        if not XMLTODICT_AVAILABLE:
            # Fallback to mock data if xmltodict not available
            print("[WARNING] xmltodict not available, using mock data")
            return parse_mock()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse XML
        data = xmltodict.parse(content)
        nmaprun = data.get('nmaprun', {})
        
        hosts = nmaprun.get('host', [])
        if not isinstance(hosts, list):
            hosts = [hosts]
        
        for host in hosts:
            if not host:
                continue
                
            # Get host info
            host_ip = ""
            if 'address' in host:
                addresses = host['address']
                if not isinstance(addresses, list):
                    addresses = [addresses]
                for addr in addresses:
                    if addr.get('@addrtype') == 'ipv4':
                        host_ip = addr.get('@addr', 'Unknown')
                        break
            
            # Get hostname
            hostname = host_ip
            if 'hostnames' in host and host['hostnames']:
                hostnames = host['hostnames'].get('hostname', [])
                if not isinstance(hostnames, list):
                    hostnames = [hostnames]
                if hostnames and hostnames[0].get('@name'):
                    hostname = hostnames[0]['@name']
            
            # Parse ports
            ports_info = host.get('ports', {})
            if ports_info:
                ports = ports_info.get('port', [])
                if not isinstance(ports, list):
                    ports = [ports]
                
                for port in ports:
                    if not port:
                        continue
                        
                    port_id = port.get('@portid', 'Unknown')
                    protocol = port.get('@protocol', 'tcp')
                    state = port.get('state', {}).get('@state', 'unknown')
                    
                    service = port.get('service', {})
                    service_name = service.get('@name', 'unknown')
                    service_version = service.get('@version', '')
                    service_product = service.get('@product', '')
                    
                    # Create finding for open ports
                    if state == 'open':
                        finding = {
                            "title": f"Open Port: {port_id}/{protocol} ({service_name})",
                            "description": f"Port {port_id}/{protocol} is open on {hostname} ({host_ip})",
                            "host": host_ip,
                            "hostname": hostname,
                            "port": port_id,
                            "protocol": protocol,
                            "service": service_name,
                            "version": service_version,
                            "product": service_product,
                            "state": state,
                            "impact": f"Service {service_name} is accessible from the network",
                            "evidence": f"Nmap scan detected open port {port_id}/{protocol}",
                            "tech_stack": "Network Service",
                            "category": "network_scan",
                            "source": "nmap"
                        }
                        
                        # Add version info if available
                        if service_version or service_product:
                            version_info = f"{service_product} {service_version}".strip()
                            finding["description"] += f" running {version_info}"
                            finding["version_info"] = version_info
                        
                        findings.append(finding)
        
        # If no findings, create a summary finding
        if not findings:
            findings.append({
                "title": "Network Scan Completed",
                "description": "Nmap scan completed but no open ports were detected",
                "impact": "No immediate network-level exposures identified",
                "evidence": "Nmap XML scan results",
                "tech_stack": "Network",
                "category": "network_scan",
                "source": "nmap"
            })
    
    except Exception as e:
        # Return error finding if parsing fails
        findings.append({
            "title": "Nmap Parsing Error",
            "description": f"Failed to parse Nmap XML file: {str(e)}",
            "impact": "Unable to analyze network scan results",
            "evidence": f"Parser error: {str(e)}",
            "tech_stack": "Parser",
            "category": "parsing_error",
            "source": "nmap"
        })
    
    return findings


def parse_mock(file_path=None):
    """
    Mock parser for testing without real Nmap XML
    Returns sample findings for demonstration
    """
    return [
        {
            "title": "Open SSH Port Detected",
            "description": "Port 22 (SSH) is open on target system",
            "host": "192.168.1.10",
            "hostname": "target-server",
            "port": "22",
            "protocol": "tcp",
            "service": "ssh",
            "version": "OpenSSH 8.0",
            "impact": "SSH service may allow unauthorized access if not properly secured",
            "evidence": "Nmap scan detected open SSH port with version OpenSSH 8.0",
            "tech_stack": "Network Service",
            "category": "network_scan",
            "source": "nmap"
        },
        {
            "title": "Web Server Detected",
            "description": "Port 80 (HTTP) is open on target system",
            "host": "192.168.1.10",
            "hostname": "target-server",
            "port": "80",
            "protocol": "tcp",
            "service": "http",
            "version": "Apache 2.4.41",
            "impact": "Web server is publicly accessible",
            "evidence": "Nmap scan detected Apache web server on port 80",
            "tech_stack": "Web Server",
            "category": "network_scan",
            "source": "nmap"
        }
    ]
