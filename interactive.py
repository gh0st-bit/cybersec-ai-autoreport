#!/usr/bin/env python3
"""
Interactive CLI Mode for CyberSec-AI AutoReport
Provides a user-friendly interface for running the tool
"""

import os
import sys
import subprocess
from pathlib import Path
import click

class InteractiveCLI:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / "config" / "settings.yaml"
        
    def print_banner(self):
        """Print application banner"""
        print("=" * 60)
        print("    CyberSec-AI AutoReport - Interactive Mode")
        print("=" * 60)
        print()
        
    def check_setup(self):
        """Check if tool is properly set up"""
        if not self.config_path.exists():
            print("[ERROR] Configuration not found!")
            print("Please run: cp config/settings.yaml.template config/settings.yaml")
            return False
            
        # Check if OpenAI is configured
        try:
            with open(self.config_path, 'r') as f:
                content = f.read()
                if "your_openai_api_key_here" in content:
                    print("[WARNING] OpenAI API key not configured - using mock responses")
                else:
                    print("[OK] OpenAI API key configured")
        except Exception as e:
            print(f"[WARNING] Could not read config: {e}")
            
        return True
        
    def auto_scan_workflow(self):
        """Automated scanning workflow"""
        print("\n=== Automated Scanning Workflow ===")
        print("This will guide you through a complete security scan and report generation.")
        print()
        
        # Step 1: Choose scan type
        print("1. Choose your scanning approach:")
        print("   a) I have existing scan results")
        print("   b) I want to run a new scan")
        print("   c) I want to run multiple scans")
        
        choice = input("\nEnter your choice (a/b/c): ").lower().strip()
        
        if choice == 'a':
            self.process_existing_scan()
        elif choice == 'b':
            self.run_new_scan()
        elif choice == 'c':
            self.run_multiple_scans()
        else:
            print("Invalid choice!")
            
    def process_existing_scan(self):
        """Process existing scan results"""
        print("\n=== Process Existing Scan Results ===")
        
        # Auto-detect scan files
        scan_files = []
        for ext in ['*.xml', '*.json']:
            scan_files.extend(Path('.').glob(f'**/{ext}'))
            
        if scan_files:
            print("\nFound potential scan files:")
            for i, file in enumerate(scan_files[:10]):  # Show first 10
                print(f"  {i+1}. {file}")
            print()
            
            choice = input("Enter file number (or 'o' for other file): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(scan_files):
                scan_file = scan_files[int(choice)-1]
            else:
                scan_file = input("Enter full path to scan file: ").strip()
        else:
            scan_file = input("Enter path to scan file: ").strip()
            
        if not Path(scan_file).exists():
            print(f"[ERROR] File not found: {scan_file}")
            return
            
        # Auto-detect scan type
        scan_type = self.detect_scan_type(scan_file)
        print(f"[INFO] Detected scan type: {scan_type}")
        
        # Generate report
        self.generate_report(scan_file, scan_type)
        
    def detect_scan_type(self, file_path):
        """Auto-detect scan type based on file content"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            if 'nmaprun' in content.lower():
                return 'nmap'
            elif 'template_id' in content.lower():
                return 'nuclei'
            elif 'burp' in content.lower() or 'issue_name' in content.lower():
                return 'burp'
            else:
                # Ask user
                print("\nCould not auto-detect scan type. Please choose:")
                print("1. Nmap XML")
                print("2. Burp Suite JSON/XML")
                print("3. Nuclei JSON")
                
                choice = input("Enter choice (1-3): ").strip()
                return ['nmap', 'burp', 'nuclei'][int(choice)-1]
                
        except Exception as e:
            print(f"[ERROR] Could not read file: {e}")
            return 'nmap'  # Default
            
    def run_new_scan(self):
        """Run a new scan using built-in tools"""
        print("\n=== Run New Scan ===")
        
        # Show available tools
        result = subprocess.run([sys.executable, 'main.py', 'tools', 'list'], 
                              capture_output=True, text=True)
        print("Available tools:")
        print(result.stdout)
        
        tool_name = input("Enter tool name to use: ").strip()
        target = input("Enter target (IP, domain, or file): ").strip()
        
        # Run the tool
        print(f"\n[INFO] Running {tool_name} against {target}...")
        result = subprocess.run([sys.executable, 'main.py', 'tools', 'run', 
                               '--name', tool_name, '--input', target])
        
        if result.returncode == 0:
            print("[OK] Scan completed successfully!")
            # Find the output file and process it
            output_dir = Path('outputs')
            if output_dir.exists():
                output_files = list(output_dir.glob(f'{tool_name}_*.txt'))
                if output_files:
                    latest_file = max(output_files, key=lambda x: x.stat().st_mtime)
                    print(f"[INFO] Scan output saved to: {latest_file}")
                    
                    # Ask if user wants to generate report
                    if input("\nGenerate report from this scan? (y/n): ").lower() == 'y':
                        scan_type = 'nmap' if tool_name == 'nmap' else 'nuclei'
                        self.generate_report(str(latest_file), scan_type)
        else:
            print("[ERROR] Scan failed!")
            
    def run_multiple_scans(self):
        """Run multiple scans in sequence"""
        print("\n=== Multiple Scans Workflow ===")
        
        target = input("Enter target (IP or domain): ").strip()
        
        scans_to_run = []
        print("\nAvailable scans:")
        print("1. Nmap port scan")
        print("2. Nuclei vulnerability scan")
        print("3. Both")
        
        choice = input("Choose scans to run (1-3): ").strip()
        
        if choice in ['1', '3']:
            scans_to_run.append('nmap')
        if choice in ['2', '3']:
            scans_to_run.append('nuclei')
            
        output_files = []
        
        for scan_tool in scans_to_run:
            print(f"\n[INFO] Running {scan_tool} scan...")
            result = subprocess.run([sys.executable, 'main.py', 'tools', 'run', 
                                   '--name', scan_tool, '--input', target])
            
            if result.returncode == 0:
                # Find the output file
                output_dir = Path('outputs')
                if output_dir.exists():
                    scan_files = list(output_dir.glob(f'{scan_tool}_*.txt'))
                    if scan_files:
                        latest_file = max(scan_files, key=lambda x: x.stat().st_mtime)
                        output_files.append((str(latest_file), scan_tool))
                        print(f"[OK] {scan_tool} scan completed: {latest_file}")
                        
        # Generate combined report
        if output_files:
            print(f"\n[INFO] Generated {len(output_files)} scan result(s)")
            for file_path, scan_type in output_files:
                print(f"[INFO] Generating report for {scan_type} scan...")
                self.generate_report(file_path, scan_type)
                
    def generate_report(self, scan_file, scan_type):
        """Generate report from scan file"""
        print(f"\n[INFO] Generating report from {scan_file}...")
        
        # Choose format
        format_choice = input("Choose format (html/pdf) [html]: ").strip() or 'html'
        
        # Run report generation
        cmd = [sys.executable, 'main.py', 'full-report', 
               '--input', scan_file, '--type', scan_type, '--format', format_choice]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"[OK] Report generated successfully!")
            
            # Show reports directory
            reports_dir = Path('reports')
            if reports_dir.exists():
                report_files = list(reports_dir.glob('*.html'))
                if report_files:
                    latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
                    print(f"[INFO] Latest report: {latest_report}")
                    
                    # Ask if user wants to open report
                    if input("Open report in browser? (y/n): ").lower() == 'y':
                        self.safe_open_browser(str(latest_report))
        else:
            print("[ERROR] Report generation failed!")
            print("[TIP] Check that the scan file is valid and the scan type is correct")
            
    def quick_actions_menu(self):
        """Show quick actions menu"""
        print("\n=== Quick Actions ===")
        print("1. Process existing scan file")
        print("2. Run Nmap scan")
        print("3. Run Nuclei scan")
        print("4. List available tools")
        print("5. View recent reports")
        print("6. Configure OpenAI API key")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            self.process_existing_scan()
        elif choice == '2':
            target = input("Enter target: ").strip()
            subprocess.run([sys.executable, 'main.py', 'tools', 'run', '--name', 'nmap', '--input', target])
        elif choice == '3':
            target = input("Enter target: ").strip()
            subprocess.run([sys.executable, 'main.py', 'tools', 'run', '--name', 'nuclei', '--input', target])
        elif choice == '4':
            subprocess.run([sys.executable, 'main.py', 'tools', 'list'])
        elif choice == '5':
            self.show_recent_reports()
        elif choice == '6':
            self.configure_api_key()
        elif choice == '7':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice!")
            
    def show_recent_reports(self):
        """Show recent reports"""
        reports_dir = Path('reports')
        if reports_dir.exists():
            report_files = list(reports_dir.glob('*.html'))
            if report_files:
                print("\nRecent reports:")
                for i, report in enumerate(sorted(report_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]):
                    print(f"  {i+1}. {report.name}")
                    
                choice = input("\nEnter number to open (or press Enter): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(report_files):
                    report_file = sorted(report_files, key=lambda x: x.stat().st_mtime, reverse=True)[int(choice)-1]
                    try:
                        subprocess.run(['xdg-open', str(report_file)])
                    except:
                        print(f"Please open: {report_file}")
            else:
                print("No reports found.")
        else:
            print("No reports directory found.")
            
    def configure_api_key(self):
        """Configure OpenAI API key"""
        print("\n=== Configure OpenAI API Key ===")
        current_key = "Not configured"
        
        try:
            import yaml
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            api_key = config.get('openai', {}).get('api_key', '')
            if api_key and api_key != 'your_openai_api_key_here':
                current_key = api_key[:10] + "..." if len(api_key) > 10 else "configured"
                
        except Exception as e:
            print(f"[ERROR] Could not read config: {e}")
            
        print(f"Current status: {current_key}")
        
        if input("Update API key? (y/n): ").lower() == 'y':
            new_key = input("Enter new OpenAI API key: ").strip()
            
            if new_key:
                try:
                    import yaml
                    # Read current config
                    with open(self.config_path, 'r') as f:
                        config = yaml.safe_load(f)
                    
                    # Update API key
                    config['openai']['api_key'] = new_key
                    
                    # Write back
                    with open(self.config_path, 'w') as f:
                        yaml.safe_dump(config, f, default_flow_style=False)
                    
                    print("[OK] API key updated successfully!")
                    
                    # Test the API key
                    print("[INFO] Testing API key...")
                    try:
                        # Force reload the AI client
                        from ai.openai_client import ai_client
                        ai_client.reload_config()
                        
                        # Test with a simple query
                        response = ai_client.chat_completion("Test message", max_tokens=10)
                        if "Security analysis" in response or "vulnerability" in response.lower():
                            print("[WARNING] API key test returned mock response. Check your key.")
                        else:
                            print("[OK] API key is working!")
                            
                    except Exception as e:
                        print(f"[ERROR] API key test failed: {e}")
                        
                except Exception as e:
                    print(f"[ERROR] Failed to update API key: {e}")
            else:
                print("No key provided.")
                
    def safe_open_browser(self, file_path):
        """Safely open browser with error handling"""
        try:
            import webbrowser
            import os
            
            # Convert to absolute path
            abs_path = os.path.abspath(file_path)
            file_url = f"file://{abs_path}"
            
            print(f"[INFO] Opening: {file_url}")
            
            # Try different methods
            try:
                # Method 1: webbrowser module
                webbrowser.open(file_url)
                print("[OK] Opened in default browser")
                return True
            except Exception as e:
                print(f"[WARNING] webbrowser failed: {e}")
                
            # Method 2: xdg-open (Linux)
            try:
                subprocess.run(['xdg-open', abs_path], check=True, timeout=5)
                print("[OK] Opened with xdg-open")
                return True
            except Exception as e:
                print(f"[WARNING] xdg-open failed: {e}")
                
            # Method 3: System-specific commands
            system_commands = {
                'darwin': ['open'],  # macOS
                'win32': ['start'],  # Windows
                'linux': ['xdg-open']  # Linux
            }
            
            import platform
            system = platform.system().lower()
            
            if system in system_commands:
                try:
                    cmd = system_commands[system] + [abs_path]
                    subprocess.run(cmd, check=True, timeout=5)
                    print(f"[OK] Opened with {system_commands[system][0]}")
                    return True
                except Exception as e:
                    print(f"[WARNING] {system_commands[system][0]} failed: {e}")
                    
        except Exception as e:
            print(f"[ERROR] Browser launch failed: {e}")
            
        # Fallback: just show the path
        print(f"[INFO] Please manually open: {os.path.abspath(file_path)}")
        return False
                content = f.read()
                if "your_openai_api_key_here" not in content:
                    current_key = "Configured"
        except:
            pass
            
        print(f"Current status: {current_key}")
        
        if input("Update API key? (y/n): ").lower() == 'y':
            api_key = input("Enter new OpenAI API key: ").strip()
            if api_key:
                try:
                    with open(self.config_path, 'r') as f:
                        content = f.read()
                    
                    # Replace the API key
                    import re
                    content = re.sub(r'api_key: ".*"', f'api_key: "{api_key}"', content)
                    
                    with open(self.config_path, 'w') as f:
                        f.write(content)
                        
                    print("[OK] API key updated successfully!")
                except Exception as e:
                    print(f"[ERROR] Failed to update API key: {e}")
            else:
                print("API key not updated.")
                
    def main_menu(self):
        """Main interactive menu"""
        while True:
            self.print_banner()
            
            if not self.check_setup():
                break
                
            print("Choose your workflow:")
            print("1. Automated scanning workflow (Recommended)")
            print("2. Quick actions menu")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.auto_scan_workflow()
            elif choice == '2':
                self.quick_actions_menu()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")
                
            input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    cli = InteractiveCLI()
    cli.main_menu()

if __name__ == "__main__":
    main()
