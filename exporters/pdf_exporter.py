"""
PDF Export Module
Converts HTML reports to PDF using WeasyPrint or fallback methods
"""

import os
from pathlib import Path

# Try to import WeasyPrint
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("[WARNING] WeasyPrint not available. PDF export will use alternative method.")

def export(html_file_path, output_path=None):
    """
    Export HTML report to PDF
    
    Args:
        html_file_path (str): Path to HTML file to convert
        output_path (str): Output PDF file path (optional)
        
    Returns:
        str: Path to generated PDF file
    """
    try:
        # Generate output path if not provided
        if not output_path:
            html_path = Path(html_file_path)
            output_path = str(html_path.with_suffix('.pdf'))
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if WEASYPRINT_AVAILABLE:
            return export_with_weasyprint(html_file_path, output_path)
        else:
            return export_fallback(html_file_path, output_path)
    
    except Exception as e:
        print(f"[ERROR] PDF export failed: {str(e)}")
        raise

def export_with_weasyprint(html_file_path, output_path):
    """Export PDF using WeasyPrint"""
    try:
        # Convert HTML to PDF
        HTML(filename=html_file_path).write_pdf(output_path)
        print(f"[OK] PDF report generated with WeasyPrint: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"[ERROR] WeasyPrint export failed: {str(e)}")
        # Fall back to alternative method
        return export_fallback(html_file_path, output_path)

def export_fallback(html_file_path, output_path):
    """Fallback PDF export method"""
    try:
        # Try wkhtmltopdf if available
        if check_wkhtmltopdf():
            return export_with_wkhtmltopdf(html_file_path, output_path)
        
        # If no PDF libraries available, just copy HTML with .pdf extension
        print("[WARNING] No PDF export libraries available. Creating HTML copy...")
        
        # Read HTML content
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Create a notice about PDF unavailability
        notice = """
        <div style="background: #fff3cd; border: 1px solid #ffc107; padding: 15px; margin: 20px; border-radius: 5px;">
            <strong>[WARNING] PDF Export Notice:</strong> PDF libraries are not available. 
            This file contains the report in HTML format. To convert to PDF, please:
            <ul>
                <li>Open this file in a web browser</li>
                <li>Use the browser's "Print to PDF" function</li>
                <li>Or install WeasyPrint: <code>pip install weasyprint</code></li>
            </ul>
        </div>
        """
        
        # Insert notice after body tag
        html_content = html_content.replace('<body>', f'<body>{notice}')
        
        # Save as .pdf.html file
        pdf_html_path = output_path + '.html'
        with open(pdf_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[WARNING] PDF export not available. HTML report saved as: {pdf_html_path}")
        print("💡 Tip: Install WeasyPrint for proper PDF export: pip install weasyprint")
        
        return pdf_html_path
    
    except Exception as e:
        print(f"[ERROR] Fallback PDF export failed: {str(e)}")
        # Just return the original HTML path
        return html_file_path

def check_wkhtmltopdf():
    """Check if wkhtmltopdf is available"""
    try:
        import subprocess
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def export_with_wkhtmltopdf(html_file_path, output_path):
    """Export PDF using wkhtmltopdf"""
    try:
        import subprocess
        
        # wkhtmltopdf command
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '0.75in',
            '--margin-right', '0.75in', 
            '--margin-bottom', '0.75in',
            '--margin-left', '0.75in',
            '--encoding', 'UTF-8',
            '--no-outline',
            html_file_path,
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[OK] PDF report generated with wkhtmltopdf: {output_path}")
            return output_path
        else:
            raise Exception(f"wkhtmltopdf failed: {result.stderr}")
    
    except Exception as e:
        print(f"[ERROR] wkhtmltopdf export failed: {str(e)}")
        raise

def install_weasyprint_guide():
    """Print installation guide for WeasyPrint"""
    guide = """
📖 WeasyPrint Installation Guide:

For Windows:
1. Install GTK+ for Windows: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. pip install weasyprint

For Linux (Ubuntu/Debian):
1. sudo apt-get install python3-dev python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
2. pip install weasyprint

For macOS:
1. brew install python3 cairo pango gdk-pixbuf libffi
2. pip install weasyprint

Alternative (using wkhtmltopdf):
1. Download from: https://wkhtmltopdf.org/downloads.html
2. Install and ensure it's in your PATH
"""
    print(guide)

def test_pdf_export():
    """Test PDF export functionality"""
    try:
        # Create a simple test HTML
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>PDF Export Test</title></head>
        <body>
            <h1>PDF Export Test</h1>
            <p>This is a test of the PDF export functionality.</p>
        </body>
        </html>
        """
        
        test_path = "test_export.html"
        with open(test_path, 'w') as f:
            f.write(test_html)
        
        # Try to export
        pdf_path = export(test_path, "test_export.pdf")
        
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)
        
        print(f"[OK] PDF export test successful: {pdf_path}")
        return True
    
    except Exception as e:
        print(f"[ERROR] PDF export test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Run test if executed directly
    test_pdf_export()
    install_weasyprint_guide()
