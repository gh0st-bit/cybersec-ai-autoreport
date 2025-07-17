"""
Custom Tools Integration Module - Enhanced Edition

This module provides functionality for integrating custom security tools
into the CyberSec-AI AutoReport system with advanced error handling,
tool validation, and smart installation guidance.

Key Features:
- Tool registration and management with availability checking
- Command execution with enhanced error handling and timeouts
- Auto-detection and registration of system tools
- Smart installation guidance for missing tools
- Output parsing and AI analysis with mock fallbacks
- JSON-based tool registry with metadata

Usage:
    from tools import register_tool, execute_tool, list_tools, get_tool_status
    
    # Register a new tool
    register_tool("nmap", "nmap -sV {input} -oX {output}", "Nmap version scan")
    
    # Execute a tool (with automatic fallback handling)
    output_file, stdout = execute_tool("nmap", "target.txt", "scan.xml")
    
    # List all registered tools with availability status
    tools = list_tools()
    
    # Get detailed tool status
    status = get_tool_status()

Enhanced Features:
- Automatic tool availability checking
- Smart error handling for missing tools
- Installation guidance for missing dependencies
- Timeout protection for long-running tools
- Comprehensive logging and debugging
- Mock data generation for unavailable tools
"""

try:
    from .runner_enhanced import register_tool, execute_tool, list_tools, get_tool_status
    ENHANCED_RUNNER = True
except ImportError:
    # Fallback to basic runner if enhanced version not available
    from .runner import register_tool, execute_tool, list_tools
    ENHANCED_RUNNER = False
    
    def get_tool_status():
        """Fallback tool status function"""
        tools = list_tools()
        return {
            'total_tools': len(tools),
            'available_tools': len(tools),
            'missing_tools': [],
            'tools': tools
        }

from .parser import parse_output

# Export all functions
__all__ = ['register_tool', 'execute_tool', 'list_tools', 'parse_output', 'get_tool_status']
__version__ = '1.1.0'
__author__ = 'CyberSec-AI AutoReport Team'
__enhanced__ = ENHANCED_RUNNER
