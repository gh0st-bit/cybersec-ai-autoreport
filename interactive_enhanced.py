#!/usr/bin/env python3
"""
Enhanced Interactive Mode with better error handling and user experience
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class EnhancedInteractiveCLI:
    def __init__(self):
        self.clear_screen()
        self.setup_modules()
        self.show_system_status()
    
    def clear_screen(self):
        """Clear screen based on OS"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def setup_modules(self):
        """Initialize enhanced modules"""
        try:
            # Use enhanced AI module
            from ai_enhanced import generate_summary, classify_severity, generate_remediation, get_ai_status
            self.ai_generate_summary = generate_summary
            self.ai_classify_severity = classify_severity
            self.ai_generate_remediation = generate_remediation
            self.ai_get_status = get_ai_status
            self.ai_enhanced = True
        except ImportError:
            # Fallback to basic AI
            from ai import summarizer, severity_classifier, remediation_generator
            self.ai_generate_summary = summarizer.generate
            self.ai_classify_severity = severity_classifier.classify
            self.ai_generate_remediation = remediation_generator.suggest
            self.ai_enhanced = False
        
        try:
            # Use enhanced tools
            from tools import register_tool, execute_tool, list_tools, get_tool_status
            self.register_tool = register_tool
            self.execute_tool = execute_tool
            self.list_tools = list_tools
            self.get_tool_status = get_tool_status
            self.tools_enhanced = True
        except ImportError:
            # Fallback to basic tools
            from tools import register_tool, execute_tool, list_tools
            self.register_tool = register_tool
            self.execute_tool = execute_tool
            self.list_tools = list_tools
            self.tools_enhanced = False
    
    def show_system_status(self):
        """Show system status once at startup"""
        print("=" * 60)
        print("    CyberSec-AI AutoReport - Enhanced Interactive Mode")
        print("=" * 60)
        print()
        
        # AI Status
        if self.ai_enhanced:
            try:
                ai_status = self.ai_get_status()
                if ai_status['api_key_configured']:
                    print("🤖 AI Status: OpenAI API configured")
                else:
                    print("🤖 AI Status: Using mock responses (no OpenAI API key)")
            except:
                print("🤖 AI Status: Basic mode")
        else:
            print("🤖 AI Status: Basic mode")
        
        # Tools Status
        if self.tools_enhanced:
            try:
                tool_status = self.get_tool_status()
                available = tool_status['available_tools']
                total = tool_status['total_tools']
                print(f"🔧 Tools Status: {available}/{total} tools available")
                
                if tool_status['missing_tools']:
                    print(f"   Missing: {', '.join(tool_status['missing_tools'])}")
                    print("   💡 Run './install_tools.sh' to install missing tools")
            except:
                print("🔧 Tools Status: Basic mode")
        else:
            print("🔧 Tools Status: Basic mode")
        
        print()
    
    def show_menu(self):
        """Show main menu"""
        print("Choose your workflow:")
        print("1. 🚀 Automated scanning workflow (Recommended)")
        print("2. ⚡ Quick actions menu")
        print("3. 🔧 System management")
        print("4. ❌ Exit")
        print()
    
    def get_user_input(self, prompt, valid_options=None):
        """Get user input with validation"""
        while True:
            try:
                user_input = input(prompt).strip()
                if valid_options and user_input not in valid_options:
                    print(f"❌ Invalid choice! Please choose from: {', '.join(valid_options)}")
                    continue
                return user_input
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
            except EOFError:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def scanning_workflow(self):
        """Enhanced scanning workflow"""
        print("\n=== 🚀 Automated Scanning Workflow ===")
        print("This will guide you through a complete security scan and report generation.")
        print()
        
        print("1. Choose your scanning approach:")
        print("   a) 📄 I have existing scan results")
        print("   b) 🔍 I want to run a new scan")
        print("   c) 🔄 I want to run multiple scans")
        print()
        
        choice = self.get_user_input("Enter your choice (a/b/c): ", ['a', 'b', 'c'])
        
        if choice == 'a':
            self.process_existing_scan()
        elif choice == 'b':
            self.run_single_scan()
        elif choice == 'c':
            self.run_multiple_scans()
    
    def process_existing_scan(self):
        """Process existing scan files"""
        print("\n=== 📄 Process Existing Scan ===")
        
        # Look for common scan files
        scan_files = []
        for pattern in ['*.xml', '*.json', '*.txt']:
            scan_files.extend(Path('.').glob(pattern))
        
        if scan_files:
            print("Found potential scan files:")
            for i, file in enumerate(scan_files[:10], 1):
                print(f"  {i}. {file}")
            
            if len(scan_files) > 10:
                print(f"  ... and {len(scan_files) - 10} more files")
            
            file_choice = self.get_user_input("\nEnter file number or full path: ")
            
            try:
                if file_choice.isdigit():
                    file_index = int(file_choice) - 1
                    if 0 <= file_index < len(scan_files):
                        scan_file = scan_files[file_index]
                    else:
                        print("❌ Invalid file number")
                        return
                else:
                    scan_file = Path(file_choice)
                    if not scan_file.exists():
                        print(f"❌ File not found: {scan_file}")
                        return
                
                self.generate_report_from_file(scan_file)
                
            except ValueError:
                print("❌ Invalid input")
        else:
            print("📂 No scan files found in current directory")
            file_path = self.get_user_input("Enter full path to scan file: ")
            scan_file = Path(file_path)
            if scan_file.exists():
                self.generate_report_from_file(scan_file)
            else:
                print(f"❌ File not found: {scan_file}")
    
    def run_single_scan(self):
        """Run a single scan"""
        print("\n=== 🔍 Run New Scan ===")
        
        # Show available tools
        if self.tools_enhanced:
            try:
                tool_status = self.get_tool_status()
                available_tools = [name for name, info in tool_status['tools'].items() if info['available']]
                
                if not available_tools:
                    print("❌ No tools available. Please install security tools first.")
                    print("💡 Run './install_tools.sh' to install common tools")
                    return
                
                print("Available tools:")
                for i, tool in enumerate(available_tools, 1):
                    description = tool_status['tools'][tool]['description']
                    print(f"  {i}. {tool} - {description}")
                
                tool_choice = self.get_user_input("\nEnter tool number or name: ")
                
                if tool_choice.isdigit():
                    tool_index = int(tool_choice) - 1
                    if 0 <= tool_index < len(available_tools):
                        tool_name = available_tools[tool_index]
                    else:
                        print("❌ Invalid tool number")
                        return
                else:
                    tool_name = tool_choice
                    if tool_name not in available_tools:
                        print(f"❌ Tool not available: {tool_name}")
                        return
                
                target = self.get_user_input("Enter target (IP, domain, or file): ")
                
                print(f"\n🔍 Running {tool_name} against {target}...")
                output_file, stdout = self.execute_tool(tool_name, target)
                
                if output_file:
                    print(f"✅ Scan completed: {output_file}")
                    self.generate_report_from_file(output_file)
                else:
                    print("❌ Scan failed!")
                    
            except Exception as e:
                print(f"❌ Error running scan: {e}")
        else:
            print("⚠️  Basic tools mode - limited functionality")
    
    def run_multiple_scans(self):
        """Run multiple scans"""
        print("\n=== 🔄 Multiple Scans Workflow ===")
        
        target = self.get_user_input("Enter target (IP or domain): ")
        
        if self.tools_enhanced:
            try:
                tool_status = self.get_tool_status()
                available_tools = [name for name, info in tool_status['tools'].items() if info['available']]
                
                if not available_tools:
                    print("❌ No tools available")
                    return
                
                # Show common scan combinations
                print("\nAvailable scans:")
                scan_options = []
                if 'nmap' in available_tools:
                    scan_options.append(('nmap', 'Nmap port scan'))
                if 'nuclei' in available_tools:
                    scan_options.append(('nuclei', 'Nuclei vulnerability scan'))
                if 'nikto' in available_tools:
                    scan_options.append(('nikto', 'Nikto web scanner'))
                
                for i, (tool, desc) in enumerate(scan_options, 1):
                    print(f"  {i}. {desc}")
                
                if len(scan_options) > 1:
                    print(f"  {len(scan_options) + 1}. All available scans")
                
                scan_choice = self.get_user_input(f"\nChoose scans to run (1-{len(scan_options) + 1}): ")
                
                if scan_choice.isdigit():
                    choice_num = int(scan_choice)
                    if choice_num <= len(scan_options):
                        selected_tools = [scan_options[choice_num - 1][0]]
                    elif choice_num == len(scan_options) + 1:
                        selected_tools = [tool for tool, _ in scan_options]
                    else:
                        print("❌ Invalid choice")
                        return
                else:
                    print("❌ Invalid choice")
                    return
                
                # Run selected scans
                scan_results = []
                for tool in selected_tools:
                    print(f"\n🔍 Running {tool} scan...")
                    output_file, stdout = self.execute_tool(tool, target)
                    
                    if output_file:
                        print(f"✅ {tool} scan completed: {output_file}")
                        scan_results.append(output_file)
                    else:
                        print(f"❌ {tool} scan failed!")
                
                # Generate reports for all results
                print(f"\n📊 Generated {len(scan_results)} scan result(s)")
                for result_file in scan_results:
                    print(f"\n📄 Generating report for {Path(result_file).name}...")
                    self.generate_report_from_file(result_file)
                    
            except Exception as e:
                print(f"❌ Error running multiple scans: {e}")
        else:
            print("⚠️  Basic tools mode - limited functionality")
    
    def generate_report_from_file(self, scan_file):
        """Generate report from scan file"""
        print(f"\n📄 Generating report from {scan_file}...")
        
        format_choice = self.get_user_input("Choose format (html/pdf) [html]: ")
        if not format_choice:
            format_choice = "html"
        
        try:
            from main import cli
            import subprocess
            
            # Use the main CLI to generate report
            cmd = [
                sys.executable, "main.py", "full-report",
                "--input", str(scan_file),
                "--type", "auto",
                "--format", format_choice
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Report generated successfully!")
                
                # Find the latest report
                reports_dir = Path("reports")
                if reports_dir.exists():
                    report_files = list(reports_dir.glob("*.html"))
                    if report_files:
                        latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
                        print(f"📊 Latest report: {latest_report}")
                        
                        open_browser = self.get_user_input("Open report in browser? (y/n): ")
                        if open_browser.lower() == 'y':
                            self.open_file(latest_report)
            else:
                print("❌ Report generation failed!")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                    
        except Exception as e:
            print(f"❌ Error generating report: {e}")
    
    def open_file(self, file_path):
        """Open file in default application"""
        try:
            import webbrowser
            webbrowser.open(f"file://{file_path.absolute()}")
            print(f"🌐 Opened in default browser")
        except Exception as e:
            print(f"❌ Could not open file: {e}")
    
    def quick_actions_menu(self):
        """Quick actions menu"""
        print("\n=== ⚡ Quick Actions ===")
        print("1. 📄 Process existing scan file")
        print("2. 🔍 Run Nmap scan")
        print("3. 🔎 Run Nuclei scan")
        print("4. 🔧 List available tools")
        print("5. 📊 View recent reports")
        print("6. 🔑 Configure OpenAI API key")
        print("7. 🔄 Install missing tools")
        print("8. ❌ Exit")
        print()
        
        choice = self.get_user_input("Enter your choice (1-8): ", ['1', '2', '3', '4', '5', '6', '7', '8'])
        
        if choice == '1':
            self.process_existing_scan()
        elif choice == '2':
            self.run_tool_scan('nmap')
        elif choice == '3':
            self.run_tool_scan('nuclei')
        elif choice == '4':
            self.show_tools_status()
        elif choice == '5':
            self.show_recent_reports()
        elif choice == '6':
            self.configure_openai_key()
        elif choice == '7':
            self.install_missing_tools()
        elif choice == '8':
            return False
        
        return True
    
    def run_tool_scan(self, tool_name):
        """Run a specific tool scan"""
        if self.tools_enhanced:
            try:
                tool_status = self.get_tool_status()
                if tool_name not in tool_status['tools']:
                    print(f"❌ Tool {tool_name} not registered")
                    return
                
                if not tool_status['tools'][tool_name]['available']:
                    print(f"❌ Tool {tool_name} not available on system")
                    print("💡 Run './install_tools.sh' to install missing tools")
                    return
                
                target = self.get_user_input(f"Enter target for {tool_name}: ")
                
                print(f"\n🔍 Running {tool_name} scan...")
                output_file, stdout = self.execute_tool(tool_name, target)
                
                if output_file:
                    print(f"✅ {tool_name} scan completed: {output_file}")
                    self.generate_report_from_file(output_file)
                else:
                    print(f"❌ {tool_name} scan failed!")
                    
            except Exception as e:
                print(f"❌ Error running {tool_name}: {e}")
        else:
            print("⚠️  Basic tools mode - limited functionality")
    
    def show_tools_status(self):
        """Show detailed tools status"""
        print("\n🔧 Tools Status:")
        
        if self.tools_enhanced:
            try:
                tool_status = self.get_tool_status()
                print(f"Total tools: {tool_status['total_tools']}")
                print(f"Available tools: {tool_status['available_tools']}")
                
                if tool_status['missing_tools']:
                    print(f"Missing tools: {', '.join(tool_status['missing_tools'])}")
                
                print("\nDetailed status:")
                for name, info in tool_status['tools'].items():
                    status_icon = "✅" if info['available'] else "❌"
                    print(f"  {status_icon} {name}: {info['description']}")
                    if info['available']:
                        print(f"      Path: {info['path']}")
                    print(f"      Command: {info['command']}")
                    print()
                    
            except Exception as e:
                print(f"❌ Error getting tool status: {e}")
        else:
            try:
                tools = self.list_tools()
                print("Registered tools:")
                for name, info in tools.items():
                    print(f"  • {name}: {info.get('description', 'No description')}")
                    print(f"    Command: {info.get('command', 'N/A')}")
            except Exception as e:
                print(f"❌ Error listing tools: {e}")
    
    def show_recent_reports(self):
        """Show recent reports"""
        print("\n📊 Recent reports:")
        
        reports_dir = Path("reports")
        if not reports_dir.exists():
            print("📂 No reports directory found")
            return
        
        report_files = list(reports_dir.glob("*.html"))
        if not report_files:
            print("📄 No reports found")
            return
        
        # Sort by modification time (newest first)
        report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for i, report in enumerate(report_files[:10], 1):
            mod_time = datetime.fromtimestamp(report.stat().st_mtime)
            print(f"  {i}. {report.name} ({mod_time.strftime('%Y-%m-%d %H:%M')})")
        
        if len(report_files) > 10:
            print(f"  ... and {len(report_files) - 10} more reports")
        
        choice = self.get_user_input("\nEnter number to open (or press Enter): ")
        if choice.isdigit():
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(report_files):
                self.open_file(report_files[choice_num])
    
    def configure_openai_key(self):
        """Configure OpenAI API key"""
        print("\n🔑 Configure OpenAI API key:")
        print("1. Edit config.json file")
        print("2. Set environment variable")
        print("3. View current status")
        
        choice = self.get_user_input("Enter your choice (1-3): ", ['1', '2', '3'])
        
        if choice == '1':
            config_file = Path("config.json")
            if config_file.exists():
                print(f"📝 Please edit the file: {config_file.absolute()}")
                print("Look for the 'openai' section and update the 'api_key' field")
            else:
                print("❌ config.json not found")
        elif choice == '2':
            print("💻 Set environment variable:")
            print("export OPENAI_API_KEY='your-api-key-here'")
            print("Or add it to your ~/.bashrc file")
        elif choice == '3':
            if self.ai_enhanced:
                try:
                    ai_status = self.ai_get_status()
                    print(f"OpenAI available: {ai_status['openai_available']}")
                    print(f"API key configured: {ai_status['api_key_configured']}")
                    print(f"Model: {ai_status['model']}")
                except:
                    print("❌ Could not get AI status")
            else:
                print("⚠️  Basic AI mode - limited status information")
    
    def install_missing_tools(self):
        """Install missing tools"""
        print("\n🔧 Install Missing Tools:")
        
        if Path("install_tools.sh").exists():
            print("Found install_tools.sh script")
            run_installer = self.get_user_input("Run tool installer? (y/n): ")
            if run_installer.lower() == 'y':
                os.system("chmod +x install_tools.sh && ./install_tools.sh")
        else:
            print("❌ install_tools.sh not found")
            print("💡 Common installation commands:")
            print("  Nmap: sudo apt-get install nmap")
            print("  Nuclei: go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest")
            print("  Nikto: sudo apt-get install nikto")
    
    def system_management(self):
        """System management menu"""
        print("\n=== 🔧 System Management ===")
        print("1. 🔍 Run system diagnostics")
        print("2. 🛠️  Run quick fixes")
        print("3. 📦 Install missing tools")
        print("4. 🔄 Update tool registry")
        print("5. 📊 System status")
        print("6. ❌ Back to main menu")
        
        choice = self.get_user_input("Enter your choice (1-6): ", ['1', '2', '3', '4', '5', '6'])
        
        if choice == '1':
            self.run_diagnostics()
        elif choice == '2':
            self.run_quick_fixes()
        elif choice == '3':
            self.install_missing_tools()
        elif choice == '4':
            self.update_tool_registry()
        elif choice == '5':
            self.show_system_status()
        elif choice == '6':
            return False
        
        return True
    
    def run_diagnostics(self):
        """Run system diagnostics"""
        print("\n🔍 Running system diagnostics...")
        
        if Path("diagnose.py").exists():
            os.system("python3 diagnose.py")
        else:
            print("❌ diagnose.py not found")
    
    def run_quick_fixes(self):
        """Run quick fixes"""
        print("\n🛠️  Running quick fixes...")
        
        if Path("quick_fix.py").exists():
            os.system("python3 quick_fix.py")
        else:
            print("❌ quick_fix.py not found")
    
    def update_tool_registry(self):
        """Update tool registry"""
        print("\n🔄 Updating tool registry...")
        
        if self.tools_enhanced:
            try:
                # Re-initialize to refresh tool detection
                self.setup_modules()
                tool_status = self.get_tool_status()
                print(f"✅ Registry updated. {tool_status['available_tools']} tools available")
            except Exception as e:
                print(f"❌ Error updating registry: {e}")
        else:
            print("⚠️  Basic tools mode - limited functionality")
    
    def main_menu(self):
        """Main menu loop"""
        try:
            while True:
                self.show_menu()
                choice = self.get_user_input("Enter your choice (1-4): ", ['1', '2', '3', '4'])
                
                if choice == '1':
                    self.scanning_workflow()
                elif choice == '2':
                    if not self.quick_actions_menu():
                        break
                elif choice == '3':
                    if not self.system_management():
                        continue
                elif choice == '4':
                    break
                
                input("\nPress Enter to continue...")
                self.clear_screen()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    cli = EnhancedInteractiveCLI()
    cli.main_menu()
