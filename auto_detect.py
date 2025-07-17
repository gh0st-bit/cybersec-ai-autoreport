#!/usr/bin/env python3
"""
Auto-Detection System for CyberSec-AI AutoReport
Automatically detects scan types and handles file processing
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import mimetypes

class ScanAutoDetector:
    """Automatically detect scan types and process files"""
    
    def __init__(self):
        self.supported_types = {
            'nmap': {
                'extensions': ['.xml'],
                'signatures': ['nmaprun', 'nmap', 'scaninfo'],
                'description': 'Nmap XML scan results'
            },
            'nuclei': {
                'extensions': ['.json'],
                'signatures': ['template_id', 'template_name', 'nuclei'],
                'description': 'Nuclei JSON scan results'
            },
            'burp': {
                'extensions': ['.json', '.xml'],
                'signatures': ['burp', 'issue_name', 'confidence', 'severity'],
                'description': 'Burp Suite scan results'
            }
        }
        
    def detect_scan_type(self, file_path):
        """
        Detect scan type based on file content and extension
        
        Args:
            file_path (str): Path to the scan file
            
        Returns:
            str: Detected scan type or None
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
            
        # Check file extension first
        extension = file_path.suffix.lower()
        
        # Try to read and analyze file content
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for signatures in content
            content_lower = content.lower()
            
            for scan_type, info in self.supported_types.items():
                # Check if extension matches
                if extension in info['extensions']:
                    # Check for signatures
                    for signature in info['signatures']:
                        if signature in content_lower:
                            return scan_type
                            
        except Exception as e:
            print(f"[WARNING] Could not read file content: {e}")
            
        # Fallback to extension-based detection
        for scan_type, info in self.supported_types.items():
            if extension in info['extensions']:
                return scan_type
                
        return None
        
    def find_scan_files(self, directory='.', recursive=True):
        """
        Find potential scan files in directory
        
        Args:
            directory (str): Directory to search
            recursive (bool): Search recursively
            
        Returns:
            list: List of tuples (file_path, detected_type)
        """
        directory = Path(directory)
        scan_files = []
        
        # Extensions to look for
        extensions = []
        for info in self.supported_types.values():
            extensions.extend(info['extensions'])
            
        # Search for files
        if recursive:
            for ext in extensions:
                for file_path in directory.rglob(f'*{ext}'):
                    if file_path.is_file():
                        detected_type = self.detect_scan_type(file_path)
                        if detected_type:
                            scan_files.append((str(file_path), detected_type))
        else:
            for ext in extensions:
                for file_path in directory.glob(f'*{ext}'):
                    if file_path.is_file():
                        detected_type = self.detect_scan_type(file_path)
                        if detected_type:
                            scan_files.append((str(file_path), detected_type))
                            
        return scan_files
        
    def validate_scan_file(self, file_path, scan_type):
        """
        Validate if scan file is properly formatted
        
        Args:
            file_path (str): Path to scan file
            scan_type (str): Expected scan type
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if scan_type == 'nmap':
                # Try to parse as XML
                ET.parse(file_path)
                return True
            elif scan_type in ['nuclei', 'burp']:
                # Try to parse as JSON
                with open(file_path, 'r') as f:
                    json.load(f)
                return True
        except Exception as e:
            print(f"[WARNING] File validation failed: {e}")
            return False
            
        return False
        
    def get_file_info(self, file_path):
        """
        Get comprehensive information about a scan file
        
        Args:
            file_path (str): Path to scan file
            
        Returns:
            dict: File information
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
            
        info = {
            'path': str(file_path),
            'name': file_path.name,
            'size': file_path.stat().st_size,
            'modified': file_path.stat().st_mtime,
            'extension': file_path.suffix.lower(),
            'detected_type': self.detect_scan_type(file_path),
            'mime_type': mimetypes.guess_type(str(file_path))[0],
            'is_valid': False
        }
        
        # Validate file if type detected
        if info['detected_type']:
            info['is_valid'] = self.validate_scan_file(file_path, info['detected_type'])
            
        return info

class AutoProcessor:
    """Automatically process scan files and generate reports"""
    
    def __init__(self):
        self.detector = ScanAutoDetector()
        
    def process_directory(self, directory='.', output_format='html'):
        """
        Process all scan files in a directory
        
        Args:
            directory (str): Directory to process
            output_format (str): Output format (html/pdf)
            
        Returns:
            list: List of generated reports
        """
        scan_files = self.detector.find_scan_files(directory)
        
        if not scan_files:
            print("[INFO] No scan files found")
            return []
            
        print(f"[INFO] Found {len(scan_files)} scan files")
        
        reports = []
        for file_path, scan_type in scan_files:
            print(f"[INFO] Processing {file_path} as {scan_type}")
            
            # Generate report
            report_path = self.generate_report(file_path, scan_type, output_format)
            if report_path:
                reports.append(report_path)
                
        return reports
        
    def generate_report(self, file_path, scan_type, output_format='html'):
        """
        Generate report from scan file
        
        Args:
            file_path (str): Path to scan file
            scan_type (str): Type of scan
            output_format (str): Output format
            
        Returns:
            str: Path to generated report or None
        """
        import subprocess
        import sys
        
        try:
            # Run main.py full-report
            cmd = [
                sys.executable, 'main.py', 'full-report',
                '--input', file_path,
                '--type', scan_type,
                '--format', output_format
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract report path from output
                output_lines = result.stdout.split('\n')
                for line in output_lines:
                    if 'report completed:' in line or 'report generated:' in line:
                        report_path = line.split(':')[-1].strip()
                        return report_path
                        
            else:
                print(f"[ERROR] Report generation failed: {result.stderr}")
                
        except Exception as e:
            print(f"[ERROR] Failed to generate report: {e}")
            
        return None
        
    def batch_process(self, file_list, output_format='html'):
        """
        Process multiple files in batch
        
        Args:
            file_list (list): List of file paths
            output_format (str): Output format
            
        Returns:
            list: List of generated reports
        """
        reports = []
        
        for file_path in file_list:
            detected_type = self.detector.detect_scan_type(file_path)
            
            if detected_type:
                print(f"[INFO] Processing {file_path} as {detected_type}")
                report_path = self.generate_report(file_path, detected_type, output_format)
                if report_path:
                    reports.append(report_path)
            else:
                print(f"[WARNING] Could not detect type for {file_path}")
                
        return reports

def main():
    """CLI interface for auto-detection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-detect and process scan files')
    parser.add_argument('--directory', '-d', default='.', help='Directory to search')
    parser.add_argument('--file', '-f', help='Single file to process')
    parser.add_argument('--format', '-fmt', default='html', choices=['html', 'pdf'], 
                       help='Output format')
    parser.add_argument('--detect-only', action='store_true', 
                       help='Only detect files, do not process')
    
    args = parser.parse_args()
    
    detector = ScanAutoDetector()
    processor = AutoProcessor()
    
    if args.file:
        # Process single file
        file_info = detector.get_file_info(args.file)
        if file_info:
            print(f"File: {file_info['name']}")
            print(f"Type: {file_info['detected_type']}")
            print(f"Valid: {file_info['is_valid']}")
            
            if not args.detect_only and file_info['detected_type']:
                report = processor.generate_report(args.file, file_info['detected_type'], args.format)
                if report:
                    print(f"Report generated: {report}")
    else:
        # Process directory
        scan_files = detector.find_scan_files(args.directory)
        
        if scan_files:
            print(f"Found {len(scan_files)} scan files:")
            for file_path, scan_type in scan_files:
                print(f"  {file_path} -> {scan_type}")
                
            if not args.detect_only:
                reports = processor.process_directory(args.directory, args.format)
                print(f"\nGenerated {len(reports)} reports:")
                for report in reports:
                    print(f"  {report}")
        else:
            print("No scan files found")

if __name__ == "__main__":
    main()
