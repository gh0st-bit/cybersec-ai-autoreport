#!/usr/bin/env python3
"""
Enhanced AI Module with better error handling and reduced warning spam
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIManager:
    def __init__(self):
        self.openai_available = False
        self.api_key = None
        self.model = "gpt-3.5-turbo"
        self.client = None
        self.warnings_shown = set()  # Track shown warnings to avoid spam
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client with better error handling"""
        try:
            # Try to import OpenAI
            import openai
            self.openai_available = True
            
            # Load API key from various sources
            self.api_key = self._load_api_key()
            
            if self.api_key and self.api_key != "your_openai_api_key_here":
                self.client = openai.OpenAI(api_key=self.api_key)
                self._show_warning("openai_configured", "[OK] OpenAI API key configured")
            else:
                self._show_warning("openai_no_key", "[WARNING] OpenAI API key not configured - using mock responses")
                
        except ImportError:
            self._show_warning("openai_not_installed", "[WARNING] OpenAI package not installed. Using mock responses.")
            self.openai_available = False
        except Exception as e:
            self._show_warning("openai_error", f"[WARNING] OpenAI initialization failed: {e}")
            self.openai_available = False
    
    def _show_warning(self, warning_id, message):
        """Show warning only once per session"""
        if warning_id not in self.warnings_shown:
            print(message)
            self.warnings_shown.add(warning_id)
    
    def _load_api_key(self):
        """Load API key from multiple sources"""
        # 1. Environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key
        
        # 2. Config file
        config_files = [
            Path('config.json'),
            Path('config/settings.yaml'),
            Path('.env')
        ]
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    if config_file.suffix == '.json':
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                            if 'openai' in config and 'api_key' in config['openai']:
                                return config['openai']['api_key']
                    elif config_file.suffix == '.yaml':
                        try:
                            import yaml
                            with open(config_file, 'r') as f:
                                config = yaml.safe_load(f)
                                if 'openai' in config and 'api_key' in config['openai']:
                                    return config['openai']['api_key']
                        except ImportError:
                            pass
                    elif config_file.name == '.env':
                        with open(config_file, 'r') as f:
                            for line in f:
                                if line.strip().startswith('OPENAI_API_KEY='):
                                    return line.strip().split('=', 1)[1].strip('"\'')
                except Exception:
                    continue
        
        return None
    
    def _generate_mock_response(self, prompt_type, finding=None):
        """Generate intelligent mock responses based on context"""
        mock_responses = {
            'summary': {
                'network': "Network scan reveals open ports and services. Port 80 (HTTP) is accessible and may require security hardening. Consider implementing proper firewall rules and service configuration.",
                'web': "Web application scan detected potential security issues. Common vulnerabilities include missing security headers, outdated software versions, and configuration weaknesses. Implement security best practices.",
                'vulnerability': "Vulnerability assessment identified security concerns that require attention. Prioritize patching known vulnerabilities and implementing security controls according to organizational policies.",
                'default': "Security analysis indicates this finding requires attention. The identified issue presents potential risks that should be addressed according to organizational security policies and best practices."
            },
            'severity': {
                'high_risk': "High",
                'medium_risk': "Medium", 
                'low_risk': "Low",
                'info': "Info",
                'default': "Medium"
            },
            'remediation': {
                'network': "1. Configure firewall rules to restrict unnecessary port access\n2. Implement proper service hardening\n3. Enable logging and monitoring\n4. Regular security assessments",
                'web': "1. Update web server and applications to latest versions\n2. Configure security headers (HSTS, CSP, X-Frame-Options)\n3. Implement input validation and sanitization\n4. Enable HTTPS with proper SSL/TLS configuration",
                'vulnerability': "1. Apply security patches and updates\n2. Implement compensating controls if patching is not immediately possible\n3. Monitor for signs of exploitation\n4. Review and update security policies",
                'default': "1. Assess the security impact of this finding\n2. Implement appropriate security controls\n3. Monitor for suspicious activity\n4. Follow organizational security procedures"
            }
        }
        
        if finding:
            # Determine context based on finding content
            finding_str = str(finding).lower()
            if any(keyword in finding_str for keyword in ['port', 'nmap', 'tcp', 'udp', 'service']):
                context = 'network'
            elif any(keyword in finding_str for keyword in ['http', 'web', 'ssl', 'certificate', 'wordpress']):
                context = 'web'
            elif any(keyword in finding_str for keyword in ['vulnerability', 'cve', 'exploit']):
                context = 'vulnerability'
            else:
                context = 'default'
            
            return mock_responses[prompt_type].get(context, mock_responses[prompt_type]['default'])
        
        return mock_responses[prompt_type]['default']
    
    def generate_summary(self, finding):
        """Generate AI summary with fallback to mock"""
        if self.client and self.api_key:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert. Provide concise, actionable summaries of security findings."},
                        {"role": "user", "content": f"Summarize this security finding: {finding}"}
                    ],
                    max_tokens=150,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.debug(f"OpenAI API call failed: {e}")
        
        return self._generate_mock_response('summary', finding)
    
    def classify_severity(self, finding):
        """Classify severity with fallback to mock"""
        if self.client and self.api_key:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert. Classify security findings as Critical, High, Medium, Low, or Info."},
                        {"role": "user", "content": f"Classify the severity of this finding: {finding}"}
                    ],
                    max_tokens=10,
                    temperature=0.1
                )
                severity = response.choices[0].message.content.strip()
                # Ensure valid severity
                valid_severities = ['Critical', 'High', 'Medium', 'Low', 'Info']
                if severity in valid_severities:
                    return severity
            except Exception as e:
                logger.debug(f"OpenAI API call failed: {e}")
        
        # Mock severity based on keywords
        finding_str = str(finding).lower()
        if any(keyword in finding_str for keyword in ['critical', 'exploit', 'rce', 'sql injection']):
            return 'High'
        elif any(keyword in finding_str for keyword in ['vulnerability', 'cve', 'misconfiguration']):
            return 'Medium'
        elif any(keyword in finding_str for keyword in ['info', 'version', 'banner']):
            return 'Info'
        else:
            return 'Medium'
    
    def generate_remediation(self, finding):
        """Generate remediation suggestions with fallback to mock"""
        if self.client and self.api_key:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert. Provide specific, actionable remediation steps for security findings."},
                        {"role": "user", "content": f"Provide remediation steps for this finding: {finding}"}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.debug(f"OpenAI API call failed: {e}")
        
        return self._generate_mock_response('remediation', finding)
    
    def parse_tool_output(self, output_content):
        """Parse tool output with AI analysis"""
        if not output_content:
            return "No output to analyze"
        
        # Check if it's an error output
        if "TOOL NOT FOUND" in output_content or "TOOL ERROR" in output_content:
            return "Tool execution failed. Check error details above."
        
        if self.client and self.api_key:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert. Analyze tool output and provide insights."},
                        {"role": "user", "content": f"Analyze this security tool output: {output_content[:1000]}..."}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.debug(f"OpenAI API call failed: {e}")
        
        return "Security analysis indicates this finding requires attention. The vulnerability presents potential risks that should be addressed according to organizational security policies and best practices. Recommend following standard security remediation procedures."
    
    def get_status(self):
        """Get AI system status"""
        return {
            'openai_available': self.openai_available,
            'api_key_configured': bool(self.api_key and self.api_key != "your_openai_api_key_here"),
            'model': self.model,
            'warnings_shown': list(self.warnings_shown)
        }

# Global instance
_ai_manager = AIManager()

# Export functions
def generate_summary(finding):
    """Generate AI summary for a finding"""
    return _ai_manager.generate_summary(finding)

def classify_severity(finding):
    """Classify severity of a finding"""
    return _ai_manager.classify_severity(finding)

def generate_remediation(finding):
    """Generate remediation suggestions"""
    return _ai_manager.generate_remediation(finding)

def parse_tool_output(output_content):
    """Parse and analyze tool output"""
    return _ai_manager.parse_tool_output(output_content)

def get_ai_status():
    """Get AI system status"""
    return _ai_manager.get_status()

if __name__ == "__main__":
    # Test the AI manager
    status = get_ai_status()
    print("AI System Status:")
    print(f"OpenAI Available: {status['openai_available']}")
    print(f"API Key Configured: {status['api_key_configured']}")
    print(f"Model: {status['model']}")
    
    # Test functions
    test_finding = "Open Port: 80/tcp (http)"
    print(f"\nTest Finding: {test_finding}")
    print(f"Summary: {generate_summary(test_finding)}")
    print(f"Severity: {classify_severity(test_finding)}")
    print(f"Remediation: {generate_remediation(test_finding)}")
