# Copilot Test Project

A simple Python project for testing and demonstrating API key configuration and GitHub Copilot integration.

## Overview

This project contains a basic Python script that demonstrates API key management and serves as a testing ground for GitHub Copilot functionality.

## Files

- `test.py` - Main Python script containing API key configuration
- `.github/copilot-instructions.md` - GitHub Copilot configuration instructions

## Setup

### Prerequisites

- Python 3.x installed on your system

### Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/egorman-sray/copilot-test.git
   cd copilot-test
   ```

2. Configure your API key:
   - Open `test.py`
   - Replace `"blah"` with your actual API key value
   - **Important**: Never commit real API keys to version control

### Security Best Practices

- Use environment variables for sensitive data:
  ```python
  import os
  MY_API_KEY = os.getenv('API_KEY', 'default_value')
  ```
- Consider using `.env` files with python-dotenv for local development
- Add sensitive files to `.gitignore`

## Usage

Run the test script:
```bash
python test.py
```

## Development

This project is designed for:
- Testing GitHub Copilot integration
- Demonstrating basic Python API key management
- Serving as a template for simple Python projects

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add appropriate documentation
5. Submit a pull request

## License

This project is for testing purposes.