# CyberSec-AI AutoReport

An intelligent cybersecurity reporting tool that automatically parses security scan results, enhances them with AI-powered analysis, and generates professional reports.

## Features

- **Multi-Scanner Support**: Nmap, Burp Suite, Nuclei, and custom tools
- **AI Enhancement**: OpenAI GPT integration for intelligent analysis
- **Professional Reports**: HTML and PDF generation with executive summaries  
- **Custom Tool Integration**: Extensible framework for security tools
- **CLI Interface**: Easy-to-use command-line interface
- **Modular Architecture**: Easily extensible and maintainable codebase

## Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/cybersec-ai-autoreport.git
cd cybersec-ai-autoreport
```

2. **Create virtual environment:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure OpenAI API:**
```bash
cp config/settings.yaml.template config/settings.yaml
# Edit config/settings.yaml and add your OpenAI API key
```

### Basic Usage

#### Generate a Complete Report (One Command)
```bash
python main.py full-report --input scan_results.xml --type nmap --format html
```

#### Step-by-Step Process
```bash
# 1. Parse scan file
python main.py parse --input scan.xml --type nmap --output findings.json

# 2. Enhance with AI
python main.py enhance --file findings.json --output enhanced.json

# 3. Generate report
python main.py export --file enhanced.json --format html
```

#### Custom Tools Integration
```bash
# List available tools
python main.py tools list

# Register a new tool
python main.py tools register --name mytool --command "mytool {input} -o {output}"

# Run a tool
python main.py tools run --name nmap --input targets.txt
```

## Supported Scanners

| Scanner | Format | Status |
|---------|--------|--------|
| Nmap | XML (`-oX`) | ✅ |
| Burp Suite | JSON/XML Export | ✅ |
| Nuclei | JSON (`-json`) | ✅ |
| Custom Tools | Any CLI tool | ✅ |

## Report Features

- **Executive Dashboard**: High-level statistics and severity breakdown
- **AI-Enhanced Analysis**: Intelligent summaries and risk assessments
- **Detailed Findings**: Comprehensive vulnerability descriptions
- **Remediation Guidance**: AI-generated fix recommendations
- **Professional Styling**: Client-ready HTML reports
- **Export Options**: HTML and PDF formats

## Architecture

```
cybersec_ai_autoreport/
├── main.py                 # CLI entry point
├── parsers/                # Scanner-specific parsers
│   ├── nmap_parser.py
│   ├── burp_parser.py
│   └── nuclei_parser.py
├── ai/                     # AI enhancement modules
│   ├── openai_client.py
│   ├── summarizer.py
│   ├── severity_classifier.py
│   └── remediation_generator.py
├── exporters/              # Report generation
│   ├── html_generator.py
│   └── pdf_exporter.py
├── tools/                  # Custom tool integration
│   ├── runner.py
│   └── registry.json
├── utils/                  # Shared utilities
├── config/                 # Configuration files
├── data/                   # Sample data and inputs
└── reports/                # Generated reports
```

## Configuration

The tool uses a YAML configuration file at `config/settings.yaml`:

```yaml
openai:
  api_key: "your_openai_api_key_here"
  model: "gpt-3.5-turbo"
  temperature: 0.5
  max_tokens: 1500

report:
  title: "Cybersecurity Assessment Report"
  company: "Your Company Name"
  author: "Security Team"
```

## Examples

### Example 1: Nmap Scan Report
```bash
# Run Nmap scan
nmap -sV -sC target.com -oX nmap_results.xml

# Generate AI-enhanced report
python main.py full-report --input nmap_results.xml --type nmap --format html
```

### Example 2: Nuclei Vulnerability Scan
```bash
# Run Nuclei scan
nuclei -l targets.txt -json -o nuclei_results.json

# Process with AI enhancement
python main.py full-report --input nuclei_results.json --type nuclei --format html
```

### Example 3: Custom Tool Integration
```bash
# Register a custom tool
python main.py tools register \
  --name "custom-scanner" \
  --command "custom-scanner {input} --output {output}" \
  --description "Custom vulnerability scanner"

# Use the registered tool
python main.py tools run --name custom-scanner --input targets.txt
```

## Dependencies

Core dependencies:
- `openai>=1.0.0` - AI integration
- `jinja2` - HTML templating
- `click` - CLI framework
- `xmltodict` - XML parsing
- `pyyaml` - Configuration management

Optional dependencies:
- `weasyprint` - PDF generation (requires system libraries)
- `fastapi` - Web interface (planned feature)

## Development

### Running Tests
```bash
python test_basic.py
python demo_test.py
```

### Adding New Parsers
1. Create a new parser in `parsers/`
2. Implement the `parse(input_file)` function
3. Return findings in standard format
4. Register in `main.py`

### Custom AI Prompts
Edit templates in `ai/prompt_templates.py` to customize AI behavior.

## Security Considerations

- API keys are stored in configuration files (excluded from git)
- Tool execution uses subprocess with security controls
- Input validation on all user-provided data
- Optional offline mode for sensitive environments

## Roadmap

- [ ] Web interface with FastAPI
- [ ] Additional scanner support (OpenVAS, Nessus)
- [ ] Advanced analytics and trending
- [ ] Team collaboration features
- [ ] Integration with ticketing systems
- [ ] Docker containerization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the documentation
- Review example configurations

---

**Note**: Remember to configure your OpenAI API key before using AI features. The tool gracefully falls back to mock responses when AI is unavailable.
