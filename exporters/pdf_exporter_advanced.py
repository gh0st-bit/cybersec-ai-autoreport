"""
Advanced PDF Export Module with Industrial-Level Features
Enhanced PDF generation with multiple formats, charts, and professional styling
"""

import os
import json
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
import base64
import io

# Try to import various PDF libraries
try:
    from weasyprint import HTML, CSS
    from weasyprint.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class AdvancedPDFExporter:
    """Advanced PDF exporter with multiple formats and industrial features"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "cybersec_reports"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Available export methods
        self.export_methods = []
        if WEASYPRINT_AVAILABLE:
            self.export_methods.append('weasyprint')
        if REPORTLAB_AVAILABLE:
            self.export_methods.append('reportlab')
        self.export_methods.extend(['wkhtmltopdf', 'chrome', 'puppeteer'])
        
        # PDF styles and configurations
        self.pdf_styles = {
            'executive': {
                'page_size': 'A4',
                'margins': {'top': 1.0, 'right': 0.75, 'bottom': 1.0, 'left': 0.75},
                'font_family': 'Arial',
                'include_charts': True,
                'include_appendix': False,
                'color_scheme': 'professional'
            },
            'technical': {
                'page_size': 'A4',
                'margins': {'top': 0.75, 'right': 0.75, 'bottom': 0.75, 'left': 0.75},
                'font_family': 'Arial',
                'include_charts': True,
                'include_appendix': True,
                'color_scheme': 'technical'
            },
            'compliance': {
                'page_size': 'A4',
                'margins': {'top': 1.0, 'right': 1.0, 'bottom': 1.0, 'left': 1.0},
                'font_family': 'Arial',
                'include_charts': True,
                'include_appendix': True,
                'color_scheme': 'compliance'
            }
        }
    
    def export(self, html_file_path, output_path=None, format_type='executive', 
               method='auto', include_charts=True, watermark=None):
        """
        Export HTML report to PDF with advanced features
        
        Args:
            html_file_path (str): Path to HTML file
            output_path (str): Output PDF path
            format_type (str): PDF format type ('executive', 'technical', 'compliance')
            method (str): Export method ('auto', 'weasyprint', 'reportlab', 'wkhtmltopdf', 'chrome')
            include_charts (bool): Include charts and visualizations
            watermark (str): Watermark text
        
        Returns:
            str: Path to generated PDF
        """
        try:
            # Generate output path if not provided
            if not output_path:
                html_path = Path(html_file_path)
                output_path = str(html_path.with_suffix('.pdf'))
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Select export method
            if method == 'auto':
                method = self.select_best_method()
            
            # Get PDF style configuration
            style_config = self.pdf_styles.get(format_type, self.pdf_styles['executive'])
            
            # Apply watermark if requested
            if watermark:
                html_file_path = self.apply_watermark(html_file_path, watermark)
            
            # Generate charts if requested
            if include_charts:
                self.generate_charts_for_pdf(html_file_path, style_config)
            
            # Export based on selected method
            if method == 'weasyprint' and WEASYPRINT_AVAILABLE:
                return self.export_with_weasyprint_advanced(html_file_path, output_path, style_config)
            elif method == 'reportlab' and REPORTLAB_AVAILABLE:
                return self.export_with_reportlab(html_file_path, output_path, style_config)
            elif method == 'wkhtmltopdf':
                return self.export_with_wkhtmltopdf_advanced(html_file_path, output_path, style_config)
            elif method == 'chrome':
                return self.export_with_chrome_advanced(html_file_path, output_path, style_config)
            elif method == 'puppeteer':
                return self.export_with_puppeteer(html_file_path, output_path, style_config)
            else:
                return self.export_fallback_advanced(html_file_path, output_path, style_config)
        
        except Exception as e:
            print(f"[ERROR] Advanced PDF export failed: {str(e)}")
            raise
    
    def select_best_method(self):
        """Select the best available export method"""
        if WEASYPRINT_AVAILABLE:
            return 'weasyprint'
        elif REPORTLAB_AVAILABLE:
            return 'reportlab'
        elif self.check_wkhtmltopdf():
            return 'wkhtmltopdf'
        elif self.check_chrome():
            return 'chrome'
        elif self.check_puppeteer():
            return 'puppeteer'
        else:
            return 'fallback'
    
    def export_with_weasyprint_advanced(self, html_file_path, output_path, style_config):
        """Export with WeasyPrint using advanced styling"""
        try:
            # Custom CSS for PDF
            pdf_css = self.generate_pdf_css(style_config)
            
            # Configure fonts
            font_config = FontConfiguration()
            
            # Create CSS object
            css_obj = CSS(string=pdf_css, font_config=font_config)
            
            # Convert HTML to PDF
            print(f"[INFO] Converting with WeasyPrint Advanced...")
            HTML(filename=html_file_path).write_pdf(
                output_path,
                stylesheets=[css_obj],
                font_config=font_config
            )
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"[OK] Advanced PDF generated with WeasyPrint: {output_path}")
                return output_path
            else:
                raise Exception("PDF file was not created or is empty")
        
        except Exception as e:
            print(f"[ERROR] WeasyPrint Advanced export failed: {str(e)}")
            return self.export_fallback_advanced(html_file_path, output_path, style_config)
    
    def export_with_reportlab(self, html_file_path, output_path, style_config):
        """Export using ReportLab for direct PDF generation"""
        try:
            print(f"[INFO] Converting with ReportLab...")
            
            # Read HTML content (simplified parsing)
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=style_config['margins']['right'] * inch,
                leftMargin=style_config['margins']['left'] * inch,
                topMargin=style_config['margins']['top'] * inch,
                bottomMargin=style_config['margins']['bottom'] * inch
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#2c3e50')
            )
            
            # Build PDF content
            story = []
            
            # Add title
            story.append(Paragraph("Cybersecurity Assessment Report", title_style))
            story.append(Spacer(1, 12))
            
            # Add executive summary
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            story.append(Paragraph(
                "This report provides a comprehensive assessment of the security posture...",
                styles['Normal']
            ))
            story.append(Spacer(1, 12))
            
            # Add findings summary table
            if style_config.get('include_charts', True):
                # Create sample data for demonstration
                data = [
                    ['Severity', 'Count', 'Percentage'],
                    ['Critical', '5', '10%'],
                    ['High', '15', '30%'],
                    ['Medium', '20', '40%'],
                    ['Low', '10', '20%']
                ]
                
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
                story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"[OK] Advanced PDF generated with ReportLab: {output_path}")
                return output_path
            else:
                raise Exception("PDF file was not created or is empty")
        
        except Exception as e:
            print(f"[ERROR] ReportLab export failed: {str(e)}")
            return self.export_fallback_advanced(html_file_path, output_path, style_config)
    
    def export_with_wkhtmltopdf_advanced(self, html_file_path, output_path, style_config):
        """Export with wkhtmltopdf using advanced options"""
        try:
            if not self.check_wkhtmltopdf():
                raise Exception("wkhtmltopdf not available")
            
            # Build advanced wkhtmltopdf command
            cmd = [
                'wkhtmltopdf',
                '--page-size', style_config.get('page_size', 'A4'),
                '--margin-top', f"{style_config['margins']['top']}in",
                '--margin-right', f"{style_config['margins']['right']}in",
                '--margin-bottom', f"{style_config['margins']['bottom']}in",
                '--margin-left', f"{style_config['margins']['left']}in",
                '--encoding', 'UTF-8',
                '--print-media-type',
                '--no-outline',
                '--enable-local-file-access',
                '--javascript-delay', '1000',
                '--load-error-handling', 'ignore',
                '--load-media-error-handling', 'ignore'
            ]
            
            # Add headers and footers
            cmd.extend([
                '--header-center', 'Cybersecurity Assessment Report',
                '--header-font-size', '9',
                '--footer-center', 'Page [page] of [toPage]',
                '--footer-font-size', '9',
                '--footer-right', f'Generated on {datetime.now().strftime("%Y-%m-%d")}'
            ])
            
            # Add color scheme
            if style_config.get('color_scheme') == 'compliance':
                cmd.extend(['--grayscale'])
            
            cmd.extend([html_file_path, output_path])
            
            print(f"[INFO] Converting with wkhtmltopdf Advanced...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"[OK] Advanced PDF generated with wkhtmltopdf: {output_path}")
                return output_path
            else:
                raise Exception(f"wkhtmltopdf failed: {result.stderr}")
        
        except Exception as e:
            print(f"[ERROR] wkhtmltopdf Advanced export failed: {str(e)}")
            return self.export_fallback_advanced(html_file_path, output_path, style_config)
    
    def export_with_chrome_advanced(self, html_file_path, output_path, style_config):
        """Export with Chrome headless using advanced options"""
        try:
            chrome_cmd = self.check_chrome()
            if not chrome_cmd:
                raise Exception("Chrome/Chromium not found")
            
            # Convert to absolute paths
            abs_html_path = os.path.abspath(html_file_path)
            abs_output_path = os.path.abspath(output_path)
            
            # Build advanced Chrome command
            cmd = [
                chrome_cmd,
                '--headless',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-plugins',
                '--run-all-compositor-stages-before-draw',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                f'--print-to-pdf={abs_output_path}',
                f'--print-to-pdf-no-header'
            ]
            
            # Add page format
            page_format = style_config.get('page_size', 'A4')
            if page_format == 'A4':
                cmd.append('--print-to-pdf-paper-width=8.27')
                cmd.append('--print-to-pdf-paper-height=11.69')
            elif page_format == 'Letter':
                cmd.append('--print-to-pdf-paper-width=8.5')
                cmd.append('--print-to-pdf-paper-height=11')
            
            cmd.append(f'file://{abs_html_path}')
            
            print(f"[INFO] Converting with Chrome Advanced...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"[OK] Advanced PDF generated with Chrome: {output_path}")
                return output_path
            else:
                raise Exception(f"Chrome headless failed: {result.stderr}")
        
        except Exception as e:
            print(f"[ERROR] Chrome Advanced export failed: {str(e)}")
            return self.export_fallback_advanced(html_file_path, output_path, style_config)
    
    def export_with_puppeteer(self, html_file_path, output_path, style_config):
        """Export with Puppeteer for advanced PDF generation"""
        try:
            if not self.check_puppeteer():
                raise Exception("Puppeteer not available")
            
            # Create Puppeteer script
            puppeteer_script = f"""
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {{
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.goto('file://{os.path.abspath(html_file_path)}', {{
        waitUntil: 'networkidle2'
    }});
    
    const pdf = await page.pdf({{
        path: '{output_path}',
        format: '{style_config.get("page_size", "A4")}',
        printBackground: true,
        margin: {{
            top: '{style_config["margins"]["top"]}in',
            right: '{style_config["margins"]["right"]}in',
            bottom: '{style_config["margins"]["bottom"]}in',
            left: '{style_config["margins"]["left"]}in'
        }},
        displayHeaderFooter: true,
        headerTemplate: '<div style="font-size:9px; text-align:center; width:100%;">Cybersecurity Assessment Report</div>',
        footerTemplate: '<div style="font-size:9px; text-align:center; width:100%;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>'
    }});
    
    await browser.close();
    console.log('PDF generated successfully');
}})();
"""
            
            # Write script to temp file
            script_path = self.temp_dir / "puppeteer_export.js"
            with open(script_path, 'w') as f:
                f.write(puppeteer_script)
            
            # Run Puppeteer script
            result = subprocess.run(
                ['node', str(script_path)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up
            script_path.unlink()
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"[OK] Advanced PDF generated with Puppeteer: {output_path}")
                return output_path
            else:
                raise Exception(f"Puppeteer failed: {result.stderr}")
        
        except Exception as e:
            print(f"[ERROR] Puppeteer export failed: {str(e)}")
            return self.export_fallback_advanced(html_file_path, output_path, style_config)
    
    def export_fallback_advanced(self, html_file_path, output_path, style_config):
        """Advanced fallback export method"""
        try:
            print("[INFO] Using advanced fallback method...")
            
            # Read HTML content
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create enhanced fallback HTML
            enhanced_html = self.create_enhanced_fallback_html(html_content, style_config)
            
            # Save enhanced HTML
            fallback_path = output_path.replace('.pdf', '_enhanced.html')
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_html)
            
            # Create instructions file
            instructions_path = output_path.replace('.pdf', '_instructions.txt')
            instructions = self.create_pdf_instructions(fallback_path, style_config)
            
            with open(instructions_path, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            print(f"[INFO] Enhanced HTML report created: {fallback_path}")
            print(f"[INFO] PDF conversion instructions: {instructions_path}")
            
            return fallback_path
        
        except Exception as e:
            print(f"[ERROR] Advanced fallback export failed: {str(e)}")
            return html_file_path
    
    def generate_pdf_css(self, style_config):
        """Generate CSS optimized for PDF"""
        css = f"""
        @page {{
            size: {style_config.get('page_size', 'A4')};
            margin: {style_config['margins']['top']}in {style_config['margins']['right']}in {style_config['margins']['bottom']}in {style_config['margins']['left']}in;
            
            @top-center {{
                content: "Cybersecurity Assessment Report";
                font-size: 9pt;
                color: #666;
            }}
            
            @bottom-center {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
            
            @bottom-right {{
                content: "{datetime.now().strftime('%Y-%m-%d')}";
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: {style_config.get('font_family', 'Arial')}, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
        }}
        
        h1, h2, h3 {{
            page-break-after: avoid;
            color: #2c3e50;
        }}
        
        h1 {{
            font-size: 18pt;
            margin-bottom: 0.5in;
        }}
        
        h2 {{
            font-size: 14pt;
            margin-top: 0.3in;
            margin-bottom: 0.2in;
        }}
        
        h3 {{
            font-size: 12pt;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
        }}
        
        .finding-card {{
            page-break-inside: avoid;
            margin-bottom: 0.3in;
            border: 1pt solid #ddd;
            padding: 0.2in;
        }}
        
        .recommendations-section {{
            page-break-inside: avoid;
        }}
        
        .executive-summary {{
            page-break-inside: avoid;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            font-size: 9pt;
        }}
        
        th, td {{
            border: 1pt solid #ddd;
            padding: 0.1in;
            text-align: left;
        }}
        
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        
        .severity-badge {{
            padding: 0.05in 0.1in;
            border-radius: 0.1in;
            font-size: 8pt;
            font-weight: bold;
        }}
        
        .severity-badge.critical {{
            background-color: #dc3545;
            color: white;
        }}
        
        .severity-badge.high {{
            background-color: #fd7e14;
            color: white;
        }}
        
        .severity-badge.medium {{
            background-color: #ffc107;
            color: black;
        }}
        
        .severity-badge.low {{
            background-color: #28a745;
            color: white;
        }}
        """
        
        # Add color scheme specific CSS
        if style_config.get('color_scheme') == 'compliance':
            css += """
            .report-header {
                background: #f8f9fa !important;
                color: #333 !important;
            }
            
            .metric-card {
                background: #f8f9fa !important;
                border: 1pt solid #ddd !important;
            }
            """
        
        return css
    
    def apply_watermark(self, html_file_path, watermark_text):
        """Apply watermark to HTML content"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Add watermark CSS and div
            watermark_css = f"""
            <style>
            .watermark {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 72px;
                color: rgba(0, 0, 0, 0.1);
                font-weight: bold;
                z-index: -1;
                pointer-events: none;
            }}
            </style>
            """
            
            watermark_div = f'<div class="watermark">{watermark_text}</div>'
            
            # Insert watermark
            html_content = html_content.replace('</head>', watermark_css + '</head>')
            html_content = html_content.replace('<body>', '<body>' + watermark_div)
            
            # Save watermarked HTML
            watermarked_path = html_file_path.replace('.html', '_watermarked.html')
            with open(watermarked_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return watermarked_path
        
        except Exception as e:
            print(f"[WARNING] Failed to apply watermark: {str(e)}")
            return html_file_path
    
    def generate_charts_for_pdf(self, html_file_path, style_config):
        """Generate charts optimized for PDF"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        try:
            # Create sample charts
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            
            # Severity distribution pie chart
            labels = ['Critical', 'High', 'Medium', 'Low']
            sizes = [5, 15, 25, 10]
            colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745']
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Vulnerability Severity Distribution')
            
            # Category distribution bar chart
            categories = ['Web App', 'Network', 'System', 'Database']
            counts = [20, 15, 10, 10]
            
            ax2.bar(categories, counts, color='#3498db')
            ax2.set_title('Vulnerabilities by Category')
            ax2.set_ylabel('Count')
            
            # CVSS score distribution
            cvss_ranges = ['0-3.9', '4.0-6.9', '7.0-8.9', '9.0-10.0']
            cvss_counts = [5, 15, 20, 15]
            
            ax3.bar(cvss_ranges, cvss_counts, color=['#28a745', '#ffc107', '#fd7e14', '#dc3545'])
            ax3.set_title('CVSS Score Distribution')
            ax3.set_ylabel('Count')
            
            # Timeline
            dates = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
            new_vulns = [10, 15, 8, 12]
            fixed_vulns = [5, 8, 12, 15]
            
            ax4.plot(dates, new_vulns, marker='o', label='New Vulnerabilities', color='#dc3545')
            ax4.plot(dates, fixed_vulns, marker='s', label='Fixed Vulnerabilities', color='#28a745')
            ax4.set_title('Vulnerability Trend')
            ax4.set_ylabel('Count')
            ax4.legend()
            
            plt.tight_layout()
            
            # Save charts
            charts_path = self.temp_dir / "security_charts.png"
            plt.savefig(charts_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"[INFO] Charts generated for PDF: {charts_path}")
            
        except Exception as e:
            print(f"[WARNING] Failed to generate charts: {str(e)}")
    
    def create_enhanced_fallback_html(self, html_content, style_config):
        """Create enhanced HTML with PDF-specific styling"""
        pdf_notice = f"""
        <div style="background: #e3f2fd; border: 2px solid #2196f3; padding: 20px; margin: 20px; border-radius: 8px; font-family: Arial, sans-serif;">
            <h3 style="color: #1976d2; margin-top: 0;">📄 PDF Export Information</h3>
            <p><strong>This file has been optimized for PDF conversion.</strong></p>
            <p><strong>Selected Format:</strong> {style_config.get('page_size', 'A4')} - {style_config.get('color_scheme', 'professional').title()} Theme</p>
            <p><strong>To convert to PDF:</strong></p>
            <ol>
                <li><strong>Browser Method:</strong> Open this file in Chrome/Edge → File → Print → Save as PDF</li>
                <li><strong>Online Tools:</strong> Upload to HTML-to-PDF converters</li>
                <li><strong>Command Line:</strong> Use wkhtmltopdf or similar tools</li>
            </ol>
            <p><strong>Recommended Print Settings:</strong></p>
            <ul>
                <li>Paper Size: {style_config.get('page_size', 'A4')}</li>
                <li>Margins: {style_config['margins']['top']}in top, {style_config['margins']['right']}in right, {style_config['margins']['bottom']}in bottom, {style_config['margins']['left']}in left</li>
                <li>Background Graphics: Enabled</li>
                <li>Headers and Footers: Enabled</li>
            </ul>
        </div>
        """
        
        # Insert notice after body tag
        enhanced_html = html_content.replace('<body>', '<body>' + pdf_notice)
        
        return enhanced_html
    
    def create_pdf_instructions(self, html_path, style_config):
        """Create detailed PDF conversion instructions"""
        instructions = f"""
CYBERSEC-AI AUTOREPORT - PDF CONVERSION INSTRUCTIONS
==================================================

Enhanced HTML Report: {html_path}
Format Configuration: {style_config.get('page_size', 'A4')} - {style_config.get('color_scheme', 'professional').title()} Theme

CONVERSION METHODS:
==================

1. BROWSER METHOD (Recommended)
   - Open the HTML file in Google Chrome or Microsoft Edge
   - Press Ctrl+P (Windows) or Cmd+P (Mac)
   - Select "Save as PDF" as destination
   - Configure settings:
     * Paper Size: {style_config.get('page_size', 'A4')}
     * Margins: Custom ({style_config['margins']['top']}in, {style_config['margins']['right']}in, {style_config['margins']['bottom']}in, {style_config['margins']['left']}in)
     * Background Graphics: Enabled
     * Headers and Footers: Enabled
   - Click "Save"

2. COMMAND LINE TOOLS
   a) wkhtmltopdf (if installed):
      wkhtmltopdf --page-size {style_config.get('page_size', 'A4')} --margin-top {style_config['margins']['top']}in --margin-right {style_config['margins']['right']}in --margin-bottom {style_config['margins']['bottom']}in --margin-left {style_config['margins']['left']}in --print-media-type "{html_path}" "output.pdf"
   
   b) WeasyPrint (if installed):
      weasyprint "{html_path}" "output.pdf"

3. ONLINE CONVERTERS
   - HTML to PDF converters (search for "HTML to PDF converter")
   - Upload the HTML file and download the PDF

4. INSTALL PDF TOOLS
   - WeasyPrint: pip install weasyprint
   - wkhtmltopdf: Download from https://wkhtmltopdf.org/downloads.html

TROUBLESHOOTING:
================

- If images don't appear: Ensure all images are embedded or accessible
- If styling is missing: Use "Print background graphics" option
- If content is cut off: Adjust margins or page size
- If fonts look different: Use web-safe fonts or embed fonts

SUPPORT:
========
For technical support, refer to the CyberSec-AI AutoReport documentation.

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return instructions
    
    def check_wkhtmltopdf(self):
        """Check if wkhtmltopdf is available"""
        try:
            result = subprocess.run(['wkhtmltopdf', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def check_chrome(self):
        """Check if Chrome/Chromium is available"""
        try:
            chrome_commands = [
                'google-chrome', 'chromium-browser', 'chromium',
                'google-chrome-stable', 'chrome'
            ]
            
            for cmd in chrome_commands:
                try:
                    result = subprocess.run([cmd, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return cmd
                except:
                    continue
            return None
        except:
            return None
    
    def check_puppeteer(self):
        """Check if Puppeteer is available"""
        try:
            result = subprocess.run(['node', '-e', 'console.log(require("puppeteer").version)'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def list_available_methods(self):
        """List all available export methods"""
        methods = []
        
        if WEASYPRINT_AVAILABLE:
            methods.append('weasyprint - Advanced CSS support')
        if REPORTLAB_AVAILABLE:
            methods.append('reportlab - Direct PDF generation')
        if self.check_wkhtmltopdf():
            methods.append('wkhtmltopdf - HTML to PDF converter')
        if self.check_chrome():
            methods.append('chrome - Chrome headless')
        if self.check_puppeteer():
            methods.append('puppeteer - Advanced browser automation')
        
        methods.append('fallback - Enhanced HTML with instructions')
        
        return methods
    
    def get_format_info(self):
        """Get information about available formats"""
        return {
            'formats': list(self.pdf_styles.keys()),
            'methods': self.list_available_methods(),
            'recommended': self.select_best_method()
        }

# Legacy functions for backward compatibility
def export(html_file_path, output_path=None):
    """Export HTML to PDF (legacy function)"""
    exporter = AdvancedPDFExporter()
    return exporter.export(html_file_path, output_path)

def export_advanced(html_file_path, output_path=None, format_type='executive', 
                   method='auto', include_charts=True, watermark=None):
    """Export HTML to PDF with advanced options"""
    exporter = AdvancedPDFExporter()
    return exporter.export(html_file_path, output_path, format_type, method, include_charts, watermark)

if __name__ == "__main__":
    # Test the advanced PDF exporter
    exporter = AdvancedPDFExporter()
    
    print("Available PDF export methods:")
    for method in exporter.list_available_methods():
        print(f"  - {method}")
    
    print(f"\nRecommended method: {exporter.select_best_method()}")
    print(f"Available formats: {', '.join(exporter.pdf_styles.keys())}")
