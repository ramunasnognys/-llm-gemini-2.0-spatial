# Gemini 2.0 Spatial Understanding Demo

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Demonstration application leveraging Google's Gemini 2.0 API for advanced spatial reasoning tasks.

## 📺 Demo Video
<a href="https://youtu.be/gIKV66HZMBU">
<img src="https://i.imgur.com/LUlTcdk.png" width="800" alt="Spatial Understanding Demo">
</a>

## ✨ Key Features
- 3D spatial relationship analysis
- Geometric reasoning with complex shapes
- Multi-modal input processing (text + spatial data)
- Batch processing capabilities
- Integration with Gemini 2.0 API
- Configurable error handling and retry mechanisms

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Cloud account with enabled Gemini API
- Valid API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation
```bash
# Create virtual environment and install dependencies
make setup

# For development tools (optional)
pip install -r requirements/requirements-dev.txt
```

## ⚙️ Configuration
Set required environment variables:
```bash
export GOOGLE_API_KEY="your-api-key-here"
export SPATIAL_DEBUG_MODE="false"  # Enable verbose output with "true"
```

## 🧠 Usage Examples

### Basic Execution
```bash
make run
```

### File Analysis
```bash
python app.py --input samples/3d_shape.json --output results.csv
```

### Batch Processing
```bash
python app.py --batch-input input_directory/ --batch-output output_directory/
```

## 🏗 Project Structure
```
.
├── app.py              # Main application logic
├── Makefile            # Build automation configuration
├── requirements/       # Dependency management
│   ├── requirements-dev.txt
│   └── requirements.txt
└── README.md           # Project documentation
```

## 🔧 Development

### Code Quality
```bash
make check  # Run linters and static analysis
make fix    # Apply automatic formatting
```

### Documentation
```bash
make help   # Show available commands
```

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push branch (`git push origin feature/your-feature`)
5. Open Pull Request

## 📄 License
MIT License - see [LICENSE](LICENSE) for details
