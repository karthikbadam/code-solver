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