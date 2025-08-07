# Setup Guide

## Prerequisites

### Required Software
- **Python 3.8+**: Download from [python.org](https://python.org)
- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org)
- **Git**: For version control

### Recommended Tools
- **uv**: Fast Python package installer ([astral.sh/uv](https://astral.sh/uv))
- **nvm**: Node Version Manager ([nvm.sh](https://nvm.sh))

### API Access
- **OpenRouter Account**: Sign up at [openrouter.ai](https://openrouter.ai)
- **API Key**: Get your API key from the OpenRouter dashboard

## Installation Options

### Option 1: Quick Setup (Recommended)

```bash
# Run the automated setup
python setup.py
```

### Option 2: Virtual Environment Setup (Advanced)

```bash
# Setup both Python and Node.js virtual environments
./scripts/setup-environments.sh

# Or setup individually:
./scripts/setup-python-env.sh   # Python with uv
./scripts/setup-node-env.sh     # Node.js with nvm
```

### Option 3: Manual Setup

```bash
# Install Python dependencies (with pip)
pip install -r requirements.txt

# Or with uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .

# Install Node.js dependencies
npm install

# Make CLI tools executable (Unix/Mac)
chmod +x tools/*.py scripts/*.sh
```

## Environment Management

### Python Virtual Environment (uv)

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .
uv pip install -e ".[dev,test]"

# Deactivate
deactivate
```

### Node.js Version Management (nvm)

```bash
# Install Node.js version from .nvmrc
nvm install

# Use Node.js version
nvm use

# List installed versions
nvm list
```

### Combined Environment Activation

```bash
# Activate both environments at once
source ./activate-env.sh
```

### 2. Environment Variables

Create a `.env` file in the project root:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

# Claude Model Configuration  
CLAUDE_MODEL=anthropic/claude-3.5-sonnet

# General Settings
DEBUG=false
LOG_LEVEL=INFO

# Progress Tracking
PROGRESS_FILE=progress/stats.json
```

### 3. Verify Installation

```bash
# Test Python setup
python tools/problem_manager.py --help

# Test Claude integration (requires API key)
python tools/claude_helper.py explain --topic "hash tables"

# Test TypeScript setup
npx tsc --version
```

## Quick Start

### Add Your First Problem

```bash
python tools/problem_manager.py add \
  --title "Valid Parentheses" \
  --difficulty easy \
  --topics "string,stack" \
  --description "Determine if input string has valid parentheses"
```

### Get AI Help

```bash
# Get a solution
python tools/claude_helper.py solve --problem two-sum --language python

# Get progressive hints
python tools/claude_helper.py hint --problem two-sum --level subtle

# Review your solution
python tools/claude_helper.py review --problem two-sum --language python
```

### Run Tests

```bash
# Test specific problem
python tools/test_runner.py run two-sum --language python

# Test all solutions
python tools/test_runner.py all
```

### Track Progress

```bash
# View statistics
python tools/problem_manager.py stats

# List problems
python tools/problem_manager.py list --difficulty easy
```

## Common Issues

### API Key Not Working
- Verify your OpenRouter API key is correct
- Check that you have sufficient credits
- Ensure the `.env` file is in the project root

### TypeScript Errors
- Run `npm install` to ensure all dependencies are installed
- Check that TypeScript is properly configured with `npx tsc --version`

### Import Errors
- Ensure you're running commands from the project root
- Check that Python can find the modules with `python -c "import sys; print(sys.path)"`

### Permission Errors (Unix/Mac)
```bash
chmod +x tools/*.py
```

## Advanced Configuration

### Custom Model Selection
You can use different Claude models by updating the `.env` file:
```env
CLAUDE_MODEL=anthropic/claude-3.5-sonnet  # Latest and most capable
CLAUDE_MODEL=anthropic/claude-3-haiku     # Faster and cheaper
```

### IDE Integration
For VS Code users, install these recommended extensions:
- Python extension
- TypeScript extension
- LeetCode extension (optional)

## Troubleshooting

If you encounter issues:

1. **Check Prerequisites**: Ensure all required software is installed
2. **Verify Environment**: Check that `.env` file exists and has correct values
3. **Test Components**: Use individual commands to isolate issues
4. **Check Logs**: Look for error messages in command output
5. **Update Dependencies**: Run `pip install -r requirements.txt` and `npm install`

For additional help, check the main README.md or create an issue in the repository.