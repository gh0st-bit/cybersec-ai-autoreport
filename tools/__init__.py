"""
Custom Tools Integration Module

This module provides functionality for integrating custom security tools
into the CyberSec-AI AutoReport system.

Key Features:
- Tool registration and management
- Command execution with error handling
- Output parsing and AI analysis
- JSON-based tool registry

Usage:
    from tools import register_tool, execute_tool, list_tools
    
    # Register a new tool
    register_tool("nmap", "nmap -sV {input} -oX {output}", "Nmap version scan")
    
    # Execute a tool
    output_file, stdout = execute_tool("nmap", "target.txt", "scan.xml")
    
    # List all registered tools
    tools = list_tools()
"""

from .runner import register_tool, execute_tool, list_tools
from .parser import parse_output

__all__ = ['register_tool', 'execute_tool', 'list_tools', 'parse_output']
__version__ = '1.0.0'
__author__ = 'CyberSec-AI AutoReport Team'
