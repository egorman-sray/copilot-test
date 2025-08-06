# API Key Configuration Guide

## Overview

This guide explains how to properly configure API keys for the copilot-test project.

## Setting Up Your API Key

### Method 1: Direct Configuration (Not Recommended for Production)

1. Open `test.py` in your text editor
2. Find the line: `MY_API_KEY = "blah"`
3. Replace `"blah"` with your actual API key
4. Save the file

**Warning**: Never commit real API keys to version control!

### Method 2: Environment Variables (Recommended)

1. Set an environment variable:
   ```bash
   export API_KEY="your_actual_api_key_here"
   ```

2. Modify the script to use the environment variable:
   ```python
   import os
   MY_API_KEY = os.getenv('API_KEY', 'blah')
   ```

### Method 3: Using .env Files (For Local Development)

1. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file:
   ```
   API_KEY=your_actual_api_key_here
   ```

3. Add `.env` to your `.gitignore` file

4. Load the environment variables in your script:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   MY_API_KEY = os.getenv('API_KEY', 'blah')
   ```

## Security Best Practices

- ✅ Use environment variables for sensitive data
- ✅ Add sensitive files to `.gitignore`
- ✅ Use placeholder values in committed code
- ✅ Regularly rotate API keys
- ❌ Never commit real API keys to version control
- ❌ Don't share API keys in chat or email
- ❌ Avoid hardcoding sensitive values

## Testing Your Configuration

Run the test script to verify your API key is configured:
```bash
python test.py
```

The script will show a warning if using the placeholder value, or confirm successful configuration if a real key is detected.