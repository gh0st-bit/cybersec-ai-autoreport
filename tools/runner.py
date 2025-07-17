"""
Custom Tools Runner
Executes registered tools and captures output for analysis
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = "tools/registry.json"
OUTPUT_DIR = "outputs"

def load_registry():
    """Load tools registry from JSON file"""
    try:
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, 'r') as f:
                return json.load(f)
        else:
            # Create empty registry if it doesn't exist
            os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
            return {}
    except Exception as e:
        print(f"[ERROR] Failed to load registry: {str(e)}")
        return {}

def save_registry(tools):
    """Save tools registry to JSON file"""
    try:
        os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
        with open(REGISTRY_FILE, 'w') as f:
            json.dump(tools, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save registry: {str(e)}")
        raise

def register_tool(name, command, description, input_type="file", output_type="file"):
    """
    Register a new custom tool
    
    Args:
        name (str): Tool name identifier
        command (str): Command template with {input} and {output} placeholders
        description (str): Tool description
        input_type (str): Input type (file, url, etc.)
        output_type (str): Output type (file, json, xml, etc.)
    """
    tools = load_registry()
    
    tools[name] = {
        "name": name,
        "command": command,
        "description": description,
        "input_type": input_type,
        "output_type": output_type,
        "category": "custom",
        "registered_at": datetime.now().isoformat()
    }
    
    save_registry(tools)
    print(f"[TOOL] Tool '{name}' registered successfully")

def execute_tool(name, input_file=None, output_file=None, timeout=300):
    """
    Execute a registered tool
    
    Args:
        name (str): Tool name to execute
        input_file (str): Path to input file (optional)
        output_file (str): Path to output file (optional)
        timeout (int): Execution timeout in seconds
        
    Returns:
        tuple: (output_file_path, stdout_content)
    """
    tools = load_registry()
    
    if name not in tools:
        raise ValueError(f"Tool '{name}' not found in registry")
    
    tool = tools[name]
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate output filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"{name}_{timestamp}.txt")
    
    # Replace placeholders in command
    command = tool["command"]
    command = command.replace("{input}", input_file or "")
    command = command.replace("{output}", output_file)
    
    print(f"[EXEC] Executing: {command}")
    
    try:
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )
        
        # Save stdout to output file if not already saved by tool
        if result.stdout and not os.path.exists(output_file):
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
        
        # Also save stderr if there were errors
        if result.stderr:
            error_file = output_file.replace('.txt', '_errors.txt')
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(result.stderr)
        
        # Log execution details
        log_execution(name, command, output_file, result.returncode, result.stderr)
        
        if result.returncode == 0:
            print(f"[OK] Tool executed successfully. Output: {output_file}")
            return output_file, result.stdout
        else:
            print(f"[WARNING] Tool completed with warnings. Return code: {result.returncode}")
            return output_file, result.stdout
    
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Tool execution timed out after {timeout} seconds")
        return None, None
    
    except Exception as e:
        print(f"[ERROR] Tool execution failed: {str(e)}")
        return None, None

def list_tools():
    """List all registered tools"""
    return load_registry()

def remove_tool(name):
    """Remove a tool from registry"""
    tools = load_registry()
    
    if name in tools:
        del tools[name]
        save_registry(tools)
        print(f"🗑️ Tool '{name}' removed from registry")
    else:
        print(f"[WARNING] Tool '{name}' not found in registry")

def log_execution(tool_name, command, output_file, return_code, stderr):
    """Log tool execution details"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": tool_name,
        "command": command,
        "output_file": output_file,
        "return_code": return_code,
        "has_errors": bool(stderr),
        "stderr_preview": stderr[:200] if stderr else None
    }
    
    log_file = os.path.join(OUTPUT_DIR, "execution_log.json")
    
    # Load existing log
    log_entries = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                log_entries = json.load(f)
        except:
            log_entries = []
    
    # Add new entry
    log_entries.append(log_entry)
    
    # Keep only last 100 entries
    log_entries = log_entries[-100:]
    
    # Save log
    try:
        with open(log_file, 'w') as f:
            json.dump(log_entries, f, indent=2)
    except:
        pass  # Ignore logging errors

def get_execution_history(tool_name=None, limit=10):
    """Get execution history for tools"""
    log_file = os.path.join(OUTPUT_DIR, "execution_log.json")
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            log_entries = json.load(f)
        
        # Filter by tool name if specified
        if tool_name:
            log_entries = [entry for entry in log_entries if entry.get('tool_name') == tool_name]
        
        # Return most recent entries
        return log_entries[-limit:]
    
    except:
        return []

def validate_command(command):
    """
    Validate command template for security
    
    Args:
        command (str): Command template to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Basic security checks
    dangerous_patterns = [
        'rm -rf', 'del /f', 'format', 'fdisk',
        '> /dev/null', 'dd if=', 'chmod 777',
        'sudo rm', 'sudo dd', '&& rm', '; rm'
    ]
    
    command_lower = command.lower()
    
    for pattern in dangerous_patterns:
        if pattern in command_lower:
            return False, f"Potentially dangerous command pattern detected: {pattern}"
    
    # Check for required placeholders
    if "{output}" not in command:
        return False, "Command must include {output} placeholder"
    
    return True, "Command appears safe"

def test_tool(name, sample_input=None):
    """
    Test a registered tool with sample input
    
    Args:
        name (str): Tool name to test
        sample_input (str): Sample input file path
        
    Returns:
        bool: True if test successful
    """
    try:
        # Create a test input file if none provided
        if not sample_input:
            test_input = os.path.join(OUTPUT_DIR, "test_input.txt")
            with open(test_input, 'w') as f:
                f.write("test.example.com\n192.168.1.1\n")
            sample_input = test_input
        
        output_file, stdout = execute_tool(name, sample_input, timeout=60)
        
        if output_file and os.path.exists(output_file):
            print(f"[OK] Tool test successful: {name}")
            return True
        else:
            print(f"[ERROR] Tool test failed: {name}")
            return False
    
    except Exception as e:
        print(f"[ERROR] Tool test error: {str(e)}")
        return False
