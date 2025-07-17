"""
File Loading and Saving Utilities
Handles JSON data persistence for the reporting tool
"""

import json
import os
from pathlib import Path
from datetime import datetime

def save_json(data, file_path, pretty=True):
    """
    Save data to JSON file with proper formatting
    
    Args:
        data: Data to save (dict, list, etc.)
        file_path (str): Path to save the JSON file
        pretty (bool): Whether to format JSON with indentation
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        print(f"[OK] Data saved to {file_path}")
    
    except Exception as e:
        print(f"[ERROR] Failed to save JSON to {file_path}: {str(e)}")
        raise

def load_json(file_path):
    """
    Load data from JSON file
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        Data loaded from JSON file
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[OK] Data loaded from {file_path}")
        return data
    
    except Exception as e:
        print(f"[ERROR] Failed to load JSON from {file_path}: {str(e)}")
        raise

def save_findings_with_metadata(findings, output_dir="outputs"):
    """
    Save findings with timestamp and metadata
    
    Args:
        findings (list): List of findings to save
        output_dir (str): Directory to save findings
        
    Returns:
        str: Path to saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"findings_{timestamp}.json"
    file_path = os.path.join(output_dir, filename)
    
    # Add metadata
    data = {
        "timestamp": datetime.now().isoformat(),
        "total_findings": len(findings),
        "findings": findings,
        "metadata": {
            "tool": "CyberSec-AI AutoReport",
            "version": "1.0.0",
            "generated_by": "cybersec_ai_autoreport"
        }
    }
    
    save_json(data, file_path)
    return file_path

def load_findings_from_metadata(file_path):
    """
    Load findings from file with metadata
    
    Args:
        file_path (str): Path to findings file
        
    Returns:
        tuple: (findings_list, metadata_dict)
    """
    data = load_json(file_path)
    
    # Handle both old format (direct list) and new format (with metadata)
    if isinstance(data, list):
        return data, {}
    elif isinstance(data, dict):
        findings = data.get('findings', [])
        metadata = data.get('metadata', {})
        return findings, metadata
    else:
        raise ValueError("Invalid findings file format")

def ensure_directory(dir_path):
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        dir_path (str): Directory path to ensure
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        print(f"[ERROR] Failed to create directory {dir_path}: {str(e)}")
        raise

def get_timestamp_filename(prefix="report", extension="json"):
    """
    Generate timestamped filename
    
    Args:
        prefix (str): Filename prefix
        extension (str): File extension (without dot)
        
    Returns:
        str: Timestamped filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def file_exists(file_path):
    """
    Check if file exists
    
    Args:
        file_path (str): Path to check
        
    Returns:
        bool: True if file exists
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)

def get_file_size(file_path):
    """
    Get file size in bytes
    
    Args:
        file_path (str): Path to file
        
    Returns:
        int: File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0

def backup_file(file_path, backup_dir="backups"):
    """
    Create backup of existing file
    
    Args:
        file_path (str): Path to file to backup
        backup_dir (str): Directory to store backup
        
    Returns:
        str: Path to backup file
    """
    if not file_exists(file_path):
        return None
    
    ensure_directory(backup_dir)
    
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{name}_backup_{timestamp}{ext}"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        print(f"[OK] Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"[ERROR] Failed to create backup: {str(e)}")
        return None

def clean_old_files(directory, max_age_days=30, pattern="*.json"):
    """
    Clean old files from directory
    
    Args:
        directory (str): Directory to clean
        max_age_days (int): Maximum age in days
        pattern (str): File pattern to match
        
    Returns:
        int: Number of files deleted
    """
    try:
        import glob
        from datetime import timedelta
        
        if not os.path.exists(directory):
            return 0
        
        cutoff_time = datetime.now() - timedelta(days=max_age_days)
        files_pattern = os.path.join(directory, pattern)
        files_deleted = 0
        
        for file_path in glob.glob(files_pattern):
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_time:
                    os.remove(file_path)
                    files_deleted += 1
                    print(f"🗑️ Deleted old file: {file_path}")
            except Exception as e:
                print(f"[WARNING] Failed to delete {file_path}: {str(e)}")
        
        return files_deleted
    
    except Exception as e:
        print(f"[ERROR] Failed to clean directory {directory}: {str(e)}")
        return 0
