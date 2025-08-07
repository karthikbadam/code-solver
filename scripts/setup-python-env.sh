#!/bin/bash
# Setup Python environment using uv

set -e

echo "🐍 Setting up Python environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Check uv version
echo "✅ uv version: $(uv --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🏗️  Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt

# Install development dependencies
echo "📦 Installing development dependencies..."
uv pip install pytest>=7.4.0 pytest-cov>=4.1.0 black>=23.7.0 flake8>=6.0.0 mypy>=1.5.0

echo "✅ Python environment setup complete!"
echo "💡 To activate the environment, run: source .venv/bin/activate"
echo "💡 To deactivate, run: deactivate"