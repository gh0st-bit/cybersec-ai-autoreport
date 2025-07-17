"""
OpenAI Client Wrapper
Handles OpenAI API calls with error handling and fallback options
"""

import os
from pathlib import Path

# Try to import required packages
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[WARNING] OpenAI package not installed. Using mock responses.")

class AIClient:
    """AI client that handles OpenAI API calls with fallbacks"""
    
    def __init__(self):
        self.client = None
        self.api_key = None
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.5
        self.max_tokens = 1500
        
        # Load configuration
        self.load_config()
        
        # Initialize OpenAI client if available and configured
        if OPENAI_AVAILABLE and self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("[OK] OpenAI client initialized successfully")
            except Exception as e:
                print(f"[ERROR] Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            if not OPENAI_AVAILABLE:
                print("[WARNING] OpenAI package not installed. Using mock responses.")
            else:
                print("[WARNING] OpenAI API key not configured. Using mock responses.")
    
    def load_config(self):
        """Load configuration from settings.yaml"""
        try:
            if not YAML_AVAILABLE:
                print("[WARNING] PyYAML not available, using environment variables")
                self.api_key = os.getenv('OPENAI_API_KEY')
                return
                
            config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                openai_config = config.get('openai', {})
                self.api_key = openai_config.get('api_key', os.getenv('OPENAI_API_KEY'))
                self.model = openai_config.get('model', 'gpt-3.5-turbo')
                self.temperature = openai_config.get('temperature', 0.5)
                self.max_tokens = openai_config.get('max_tokens', 1500)
                
                # Debug: Print loaded config (without exposing full API key)
                if self.api_key:
                    key_preview = self.api_key[:10] + "..." if len(self.api_key) > 10 else "short_key"
                    print(f"[DEBUG] Loaded API key: {key_preview}")
                    print(f"[DEBUG] Using model: {self.model}")
                else:
                    print("[DEBUG] No API key found in config")
            else:
                print(f"[WARNING] Config file not found at {config_path}")
                
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")
            # Try environment variable as fallback
            self.api_key = os.getenv('OPENAI_API_KEY')
    
    def reload_config(self):
        """Reload configuration (useful after config changes)"""
        self.load_config()
        if OPENAI_AVAILABLE and self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("[OK] OpenAI client reloaded successfully")
                return True
            except Exception as e:
                print(f"[ERROR] Failed to reload OpenAI client: {e}")
                self.client = None
                return False
        return False
    
    def chat_completion(self, prompt, temperature=None, max_tokens=None):
        """
        Get chat completion from OpenAI or return mock response
        
        Args:
            prompt (str): The prompt to send to the AI
            temperature (float): Override default temperature
            max_tokens (int): Override default max tokens
            
        Returns:
            str: AI response or mock response
        """
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a cybersecurity expert providing professional analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature or self.temperature,
                    max_tokens=max_tokens or self.max_tokens
                )
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                print(f"[WARNING] OpenAI API call failed: {e}")
                return self.get_mock_response(prompt)
        else:
            return self.get_mock_response(prompt)
    
    def get_mock_response(self, prompt):
        """Generate mock response based on prompt type"""
        prompt_lower = prompt.lower()
        
        # Severity classification
        if "severity" in prompt_lower and any(sev in prompt_lower for sev in ["critical", "high", "medium", "low"]):
            if "sql injection" in prompt_lower or "xss" in prompt_lower:
                return "High"
            elif "information disclosure" in prompt_lower or "version" in prompt_lower:
                return "Low"
            else:
                return "Medium"
        
        # Executive summary
        elif "executive summary" in prompt_lower:
            if "ssh" in prompt_lower:
                return "The system has SSH (remote access) enabled which could be exploited by attackers if not properly secured. This creates a potential entry point for unauthorized access to the server. Recommend implementing key-based authentication and restricting access to trusted IP addresses."
            elif "xss" in prompt_lower:
                return "A cross-site scripting vulnerability allows attackers to execute malicious code in user browsers, potentially stealing user credentials or session information. This poses a significant risk to user data security and application integrity. Immediate remediation through input validation is recommended."
            else:
                return "Security assessment has identified vulnerabilities that require attention. These findings represent potential risks to system security and data protection. Recommend prioritizing remediation efforts based on severity levels and business impact."
        
        # Remediation
        elif "remediation" in prompt_lower:
            if "ssh" in prompt_lower:
                return """1. Immediate actions:
   - Change default SSH port from 22 to a non-standard port
   - Disable root login via SSH
   - Implement fail2ban for brute force protection

2. Long-term solutions:
   - Configure key-based authentication and disable password authentication
   - Restrict SSH access to specific IP addresses using firewall rules
   - Implement multi-factor authentication where possible

3. Monitoring:
   - Monitor SSH login attempts and failed authentications
   - Set up alerts for suspicious login patterns
   - Regular review of SSH access logs

4. Prevention:
   - Regular security updates and patches
   - Strong password policies if password auth is required
   - Network segmentation to limit SSH access scope"""
            
            elif "xss" in prompt_lower:
                return """1. Immediate actions:
   - Implement input validation on all user inputs
   - Apply output encoding when displaying user data
   - Use Content Security Policy (CSP) headers

2. Long-term solutions:
   - Implement proper input sanitization framework
   - Use parameterized queries and prepared statements
   - Regular security code reviews and testing

3. Monitoring:
   - Implement web application firewall (WAF)
   - Monitor for XSS attack patterns in logs
   - Regular vulnerability scanning

4. Prevention:
   - Security awareness training for developers
   - Secure coding standards and practices
   - Automated security testing in CI/CD pipeline"""
            
            else:
                return """1. Immediate actions:
   - Assess the scope and impact of the vulnerability
   - Implement temporary mitigations if possible
   - Monitor for signs of exploitation

2. Long-term solutions:
   - Apply security patches and updates
   - Implement proper security controls
   - Review and update security configurations

3. Monitoring:
   - Set up monitoring for related security events
   - Implement detection mechanisms
   - Regular security assessments

4. Prevention:
   - Establish regular security update procedures
   - Implement security best practices
   - Conduct regular security training"""
        
        # Risk assessment
        elif "risk assessment" in prompt_lower:
            return """Likelihood of exploitation: Medium
Business impact if exploited: High
Overall risk level: High

Key risk factors:
- Vulnerability is remotely exploitable
- Affects system availability and data confidentiality
- Could lead to unauthorized access or data breach
- May have compliance implications"""
        
        # Technical analysis
        elif "technical analysis" in prompt_lower:
            return """Technical analysis reveals a security vulnerability that requires immediate attention. The issue stems from insufficient security controls in the current configuration. Attack vectors include remote exploitation through network services. Affected components include the primary service interface and underlying system resources. Root cause analysis indicates inadequate input validation and security hardening. Technical remediation should focus on implementing proper security controls, updating configurations, and applying security patches."""
        
        # Default response
        else:
            return "Security analysis indicates this finding requires attention. The vulnerability presents potential risks that should be addressed according to organizational security policies and best practices. Recommend following standard security remediation procedures."

# Global AI client instance
ai_client = AIClient()
