#!/usr/bin/env python3
"""
Fix Unicode encoding issues by replacing emoji with text
"""

import os
import re
from pathlib import Path

# Mapping of emojis to text
EMOJI_MAP = {
    '[SHIELD]': '[SHIELD]',
    '[OK]': '[OK]',
    '[ERROR]': '[ERROR]',
    '[WARNING]': '[WARNING]',
    '[AI]': '[AI]',
    '[FILE]': '[FILE]',
    '[LAUNCH]': '[LAUNCH]',
    '[TOOL]': '[TOOL]',
    '[EXEC]': '[EXEC]',
    '[SUCCESS]': '[SUCCESS]',
    '[STATS]': '[STATS]',
    '[FILES]': '[FILES]',
    '[SUMMARY]': '[SUMMARY]',
    '[FINDINGS]': '[FINDINGS]'
}

def fix_unicode_in_file(file_path):
    """Fix Unicode characters in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace emojis
        for emoji, replacement in EMOJI_MAP.items():
            content = content.replace(emoji, replacement)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all Python files in the project"""
    project_root = Path(__file__).parent
    python_files = list(project_root.rglob("*.py"))
    
    fixed_count = 0
    for py_file in python_files:
        if fix_unicode_in_file(py_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()
