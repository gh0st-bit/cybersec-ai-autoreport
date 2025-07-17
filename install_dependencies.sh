#!/bin/bash

# System Dependencies Installer for CyberSec-AI AutoReport
# Installs required system libraries for PDF generation

echo "════════════════════════════════════════════════════════════════"
echo "  CyberSec-AI AutoReport - System Dependencies Installer"
echo "════════════════════════════════════════════════════════════════"
echo

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        echo "[INFO] Detected Debian/Ubuntu system"
        echo "[INFO] Installing WeasyPrint system dependencies..."
        
        sudo apt-get update
        sudo apt-get install -y \
            python3-dev \
            python3-pip \
            python3-cffi \
            python3-brotli \
            libpango-1.0-0 \
            libharfbuzz0b \
            libpangoft2-1.0-0 \
            libfontconfig1 \
            libcairo2-dev \
            libpango1.0-dev \
            libgdk-pixbuf2.0-dev \
            libffi-dev \
            shared-mime-info \
            libxml2-dev \
            libxslt1-dev \
            libjpeg-dev \
            libopenjp2-7-dev \
            libtiff-dev
            
        echo "[INFO] Installing wkhtmltopdf..."
        sudo apt-get install -y wkhtmltopdf
        
        echo "[INFO] Installing Chrome/Chromium for headless PDF generation..."
        sudo apt-get install -y chromium-browser
        
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        echo "[INFO] Detected CentOS/RHEL system"
        echo "[INFO] Installing WeasyPrint system dependencies..."
        
        sudo yum install -y \
            python3-devel \
            python3-pip \
            cairo-devel \
            pango-devel \
            gdk-pixbuf2-devel \
            libffi-devel \
            libxml2-devel \
            libxslt-devel \
            libjpeg-devel \
            openjpeg2-devel \
            libtiff-devel
            
        echo "[INFO] Installing wkhtmltopdf..."
        sudo yum install -y wkhtmltopdf
        
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        echo "[INFO] Detected Arch Linux system"
        echo "[INFO] Installing WeasyPrint system dependencies..."
        
        sudo pacman -S --noconfirm \
            python \
            python-pip \
            cairo \
            pango \
            gdk-pixbuf2 \
            libffi \
            libxml2 \
            libxslt \
            libjpeg-turbo \
            openjpeg2 \
            libtiff
            
        echo "[INFO] Installing wkhtmltopdf..."
        sudo pacman -S --noconfirm wkhtmltopdf
        
    else
        echo "[WARNING] Unknown Linux distribution. Please install manually:"
        echo "  - cairo development libraries"
        echo "  - pango development libraries"
        echo "  - gdk-pixbuf development libraries"
        echo "  - libffi development libraries"
        echo "  - wkhtmltopdf"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "[INFO] Detected macOS system"
    
    if command -v brew &> /dev/null; then
        echo "[INFO] Installing WeasyPrint system dependencies via Homebrew..."
        
        brew install \
            python3 \
            cairo \
            pango \
            gdk-pixbuf \
            libffi \
            libxml2 \
            libxslt \
            jpeg \
            openjpeg \
            libtiff
            
        echo "[INFO] Installing wkhtmltopdf..."
        brew install wkhtmltopdf
        
        echo "[INFO] Installing Chrome..."
        brew install --cask google-chrome
        
    else
        echo "[ERROR] Homebrew not found. Please install Homebrew first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
else
    echo "[ERROR] Unsupported operating system: $OSTYPE"
    echo "Please refer to WeasyPrint documentation for manual installation:"
    echo "https://weasyprint.readthedocs.io/en/stable/install.html"
    exit 1
fi

echo
echo "[INFO] Testing PDF export capabilities..."

# Test WeasyPrint
echo "[TEST] Testing WeasyPrint..."
python3 -c "
try:
    from weasyprint import HTML
    print('[OK] WeasyPrint is working')
except ImportError as e:
    print('[ERROR] WeasyPrint import failed:', e)
except Exception as e:
    print('[ERROR] WeasyPrint test failed:', e)
"

# Test wkhtmltopdf
echo "[TEST] Testing wkhtmltopdf..."
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf --version | head -1
    echo "[OK] wkhtmltopdf is working"
else
    echo "[ERROR] wkhtmltopdf not found"
fi

# Test Chrome headless
echo "[TEST] Testing Chrome headless..."
if command -v google-chrome &> /dev/null; then
    google-chrome --version
    echo "[OK] Chrome is available"
elif command -v chromium-browser &> /dev/null; then
    chromium-browser --version
    echo "[OK] Chromium is available"
else
    echo "[WARNING] Chrome/Chromium not found"
fi

echo
echo "════════════════════════════════════════════════════════════════"
echo "  Installation Complete!"
echo "════════════════════════════════════════════════════════════════"
echo
echo "Next steps:"
echo "1. Test PDF generation: python3 -c 'from exporters.pdf_exporter import test_pdf_export; test_pdf_export()'"
echo "2. Run the tool: ./interactive.py"
echo
echo "If you encounter issues:"
echo "- Check the error messages for specific missing dependencies"
echo "- Visit: https://weasyprint.readthedocs.io/en/stable/install.html"
echo "- Report issues at: https://github.com/gh0st-bit/cybersec-ai-autoreport/issues"
