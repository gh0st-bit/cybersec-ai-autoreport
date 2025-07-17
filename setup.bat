@echo off
echo 🛡️ CyberSec-AI AutoReport Setup
echo ================================

echo.
echo 1. Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 2. Testing MVP functionality...
python test_mvp.py

echo.
echo 3. Setup complete! Try these commands:
echo    python main.py --help
echo    python main.py full-report --input data/sample_inputs/nmap_sample.xml --type nmap
echo    python main.py tools list

pause
