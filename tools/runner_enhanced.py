#!/usr/bin/env python3
"""
Enhanced Tool Runner with improved error handling and validation
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ToolRunner:
    def __init__(self):
        self.registry_file = Path(__file__).parent / 'registry.json'
        self.tools = self._load_registry()
        self._validate_system_tools()
    
    def _load_registry(self):
        """Load tool registry from JSON file"""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
            return {}
    
    def _save_registry(self):
        """Save tool registry to JSON file"""
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self.tools, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
    
    def _validate_system_tools(self):
        """Validate that system tools are available"""
        system_tools = {
            'nmap': 'Network discovery and security auditing',
            'nuclei': 'Fast vulnerability scanner based on simple YAML templates',
            'nikto': 'Web server scanner',
            'gobuster': 'Directory/file brute-forcer',
            'sqlmap': 'SQL injection testing tool'
        }
        
        # Check which tools are available
        available_tools = {}
        for tool_name, description in system_tools.items():
            if shutil.which(tool_name):
                available_tools[tool_name] = {
                    'description': description,
                    'available': True,
                    'path': shutil.which(tool_name)
                }
            else:
                available_tools[tool_name] = {
                    'description': description,
                    'available': False,
                    'path': None
                }
        
        # Auto-register available tools
        self._auto_register_tools(available_tools)
        
        return available_tools
    
    def _auto_register_tools(self, available_tools):
        """Auto-register available system tools"""
        tool_configs = {
            'nmap': {
                'command': 'nmap -sV -sC {input} -oX {output}',
                'input_type': 'target',
                'output_type': 'xml'
            },
            'nuclei': {
                'command': 'nuclei -u {input} -o {output} -json',
                'input_type': 'target',
                'output_type': 'json'
            },
            'nikto': {
                'command': 'nikto -h {input} -o {output}',
                'input_type': 'target',
                'output_type': 'text'
            },
            'gobuster': {
                'command': 'gobuster dir -u {input} -w /usr/share/wordlists/dirb/common.txt -o {output}',
                'input_type': 'target',
                'output_type': 'text'
            },
            'sqlmap': {
                'command': 'sqlmap -u {input} --batch --output-dir={output}',
                'input_type': 'target',
                'output_type': 'directory'
            }
        }
        
        for tool_name, tool_info in available_tools.items():
            if tool_info['available'] and tool_name in tool_configs:
                config = tool_configs[tool_name]
                self.register_tool(
                    tool_name, 
                    config['command'], 
                    tool_info['description'],
                    config['input_type'],
                    config['output_type']
                )
    
    def register_tool(self, name, command, description, input_type='file', output_type='file'):
        """Register a new tool"""
        self.tools[name] = {
            'command': command,
            'description': description,
            'input_type': input_type,
            'output_type': output_type,
            'registered_at': datetime.now().isoformat()
        }
        self._save_registry()
    
    def execute_tool(self, tool_name, input_value, output_path=None):
        """Execute a registered tool with enhanced error handling"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered")
        
        tool_config = self.tools[tool_name]
        
        # Check if tool is available on system
        tool_binary = tool_name
        if not shutil.which(tool_binary):
            # Try common alternatives
            alternatives = {
                'nuclei': ['nuclei', '/usr/bin/nuclei', '/opt/nuclei/nuclei'],
                'nmap': ['nmap', '/usr/bin/nmap'],
                'nikto': ['nikto', '/usr/bin/nikto']
            }
            
            found = False
            if tool_name in alternatives:
                for alt in alternatives[tool_name]:
                    if shutil.which(alt):
                        tool_binary = alt
                        found = True
                        break
            
            if not found:
                return self._handle_missing_tool(tool_name, input_value, output_path)
        
        # Generate output path if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{tool_name}_{timestamp}.txt"
        
        # Prepare command
        command = tool_config['command'].format(input=input_value, output=output_path)
        
        # Replace tool name with full path if needed
        if tool_binary != tool_name:
            command = command.replace(tool_name, tool_binary, 1)
        
        logger.info(f"Executing: {command}")
        
        try:
            # Execute command
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Handle different return codes
            if result.returncode == 0:
                logger.info(f"Tool executed successfully. Output: {output_path}")
                return str(output_path), result.stdout
            elif result.returncode == 127:
                return self._handle_missing_tool(tool_name, input_value, output_path)
            else:
                return self._handle_tool_error(tool_name, result, output_path)
                
        except subprocess.TimeoutExpired:
            logger.error(f"Tool '{tool_name}' timed out after 5 minutes")
            return self._create_error_output(tool_name, "Tool execution timed out", output_path)
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return self._create_error_output(tool_name, str(e), output_path)
    
    def _handle_missing_tool(self, tool_name, input_value, output_path):
        """Handle missing tool by creating mock output and installation guide"""
        logger.warning(f"Tool '{tool_name}' not found on system")
        
        # Create installation guide
        install_guides = {
            'nuclei': "sudo apt-get install nuclei -y || go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest",
            'nmap': "sudo apt-get install nmap -y",
            'nikto': "sudo apt-get install nikto -y",
            'gobuster': "sudo apt-get install gobuster -y",
            'sqlmap': "sudo apt-get install sqlmap -y"
        }
        
        install_cmd = install_guides.get(tool_name, f"# Install {tool_name} manually")
        
        # Create error output with installation instructions
        error_output = f"""
TOOL NOT FOUND: {tool_name}
=========================

The tool '{tool_name}' is not installed on your system.

Installation Instructions:
{install_cmd}

Alternative Installation Methods:
1. Using package manager: sudo apt-get install {tool_name}
2. Using snap: sudo snap install {tool_name}
3. Manual installation: Check tool's official documentation

Target: {input_value}
Timestamp: {datetime.now().isoformat()}
"""
        
        # Save error output
        error_path = str(output_path).replace('.txt', '_missing.txt')
        with open(error_path, 'w') as f:
            f.write(error_output)
        
        return error_path, error_output
    
    def _handle_tool_error(self, tool_name, result, output_path):
        """Handle tool execution errors"""
        logger.warning(f"Tool '{tool_name}' completed with warnings. Return code: {result.returncode}")
        
        # Create error output
        error_output = f"""
TOOL ERROR: {tool_name}
===================

Return Code: {result.returncode}
STDOUT: {result.stdout}
STDERR: {result.stderr}

Timestamp: {datetime.now().isoformat()}
"""
        
        # Save error output
        error_path = str(output_path).replace('.txt', '_errors.txt')
        with open(error_path, 'w') as f:
            f.write(error_output)
        
        return error_path, error_output
    
    def _create_error_output(self, tool_name, error_message, output_path):
        """Create standardized error output"""
        error_output = f"""
EXECUTION ERROR: {tool_name}
============================

Error: {error_message}
Timestamp: {datetime.now().isoformat()}
"""
        
        error_path = str(output_path).replace('.txt', '_error.txt')
        with open(error_path, 'w') as f:
            f.write(error_output)
        
        return error_path, error_output
    
    def list_tools(self):
        """List all registered tools with availability status"""
        result = {}
        for name, config in self.tools.items():
            is_available = shutil.which(name) is not None
            result[name] = {
                **config,
                'available': is_available,
                'path': shutil.which(name) if is_available else None
            }
        return result
    
    def get_tool_status(self):
        """Get detailed status of all tools"""
        status = {
            'total_tools': len(self.tools),
            'available_tools': 0,
            'missing_tools': [],
            'tools': {}
        }
        
        for name, config in self.tools.items():
            is_available = shutil.which(name) is not None
            tool_path = shutil.which(name) if is_available else None
            
            if is_available:
                status['available_tools'] += 1
            else:
                status['missing_tools'].append(name)
            
            status['tools'][name] = {
                'description': config['description'],
                'available': is_available,
                'path': tool_path,
                'command': config['command']
            }
        
        return status

# Global instance
_runner = ToolRunner()

# Export functions
def register_tool(name, command, description, input_type='file', output_type='file'):
    """Register a new tool"""
    return _runner.register_tool(name, command, description, input_type, output_type)

def execute_tool(name, input_value, output_path=None):
    """Execute a registered tool"""
    return _runner.execute_tool(name, input_value, output_path)

def list_tools():
    """List all registered tools"""
    return _runner.list_tools()

def get_tool_status():
    """Get detailed status of all tools"""
    return _runner.get_tool_status()

if __name__ == "__main__":
    # Test the tool runner
    status = get_tool_status()
    print("Tool Status:")
    print(f"Total tools: {status['total_tools']}")
    print(f"Available tools: {status['available_tools']}")
    print(f"Missing tools: {', '.join(status['missing_tools'])}")
    
    for name, info in status['tools'].items():
        status_icon = "✅" if info['available'] else "❌"
        print(f"{status_icon} {name}: {info['description']}")
