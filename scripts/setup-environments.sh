#!/bin/bash
# Master setup script for both Python and Node.js environments

set -e

echo "🚀 LeetCode Practice Repository - Environment Setup"
echo "=================================================="

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Make scripts executable
chmod +x scripts/*.sh

# Setup Python environment
echo ""
echo "🐍 PYTHON ENVIRONMENT SETUP"
echo "----------------------------"
./scripts/setup-python-env.sh

# Setup Node.js environment
echo ""
echo "📦 NODE.JS ENVIRONMENT SETUP" 
echo "-----------------------------"
./scripts/setup-node-env.sh

# Create environment file if it doesn't exist
echo ""
echo "⚙️  CONFIGURATION SETUP"
echo "-----------------------"

if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

# Claude Model Configuration  
CLAUDE_MODEL=anthropic/claude-3.5-sonnet

# General Settings
DEBUG=false
LOG_LEVEL=INFO

# Progress Tracking
PROGRESS_FILE=progress/stats.json
EOF
    echo "✅ .env file created"
    echo "⚠️  Please add your OpenRouter API key to the .env file"
else
    echo "✅ .env file already exists"
fi

# Create activation script
echo ""
echo "🔧 Creating activation script..."
cat > activate-env.sh << 'EOF'
#!/bin/bash
# Activate both Python and Node.js environments

echo "🔄 Activating development environment..."

# Activate Python virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Python virtual environment activated"
else
    echo "⚠️  Python virtual environment not found. Run ./scripts/setup-python-env.sh first"
fi

# Use Node.js version from .nvmrc
if [ -f "$HOME/.nvm/nvm.sh" ] && [ -f ".nvmrc" ]; then
    source "$HOME/.nvm/nvm.sh"
    nvm use
    echo "✅ Node.js environment activated"
else
    echo "⚠️  nvm or .nvmrc not found. Node.js environment may not be set correctly"
fi

echo "🎉 Development environment ready!"
echo "💡 Python: $(python --version 2>/dev/null || echo 'Not available')"
echo "💡 Node.js: $(node --version 2>/dev/null || echo 'Not available')"
EOF

chmod +x activate-env.sh

echo "✅ Environment setup complete!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Add your OpenRouter API key to .env file"
echo "2. Activate environments: source ./activate-env.sh"
echo "3. Test installation: python leetcode.py demo"
echo ""
echo "🔧 ENVIRONMENT COMMANDS:"
echo "• Activate environments: source ./activate-env.sh"
echo "• Python only: source .venv/bin/activate"
echo "• Node.js only: nvm use"
echo "• Deactivate Python: deactivate"