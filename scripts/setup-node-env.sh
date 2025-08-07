#!/bin/bash
# Setup Node.js environment using nvm

set -e

echo "📦 Setting up Node.js environment with nvm..."

# Check if nvm is installed
if ! command -v nvm &> /dev/null; then
    # Check if nvm is available but not in PATH
    if [ -f "$HOME/.nvm/nvm.sh" ]; then
        echo "🔄 Loading nvm..."
        source "$HOME/.nvm/nvm.sh"
    else
        echo "📦 Installing nvm..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
    fi
fi

# Source nvm if it exists
if [ -f "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
fi

# Check nvm version
echo "✅ nvm version: $(nvm --version)"

# Install and use Node.js version from .nvmrc
if [ -f ".nvmrc" ]; then
    NODE_VERSION=$(cat .nvmrc)
    echo "🔄 Installing Node.js v$NODE_VERSION..."
    nvm install
    nvm use
else
    echo "⚠️  No .nvmrc file found, using default Node.js version"
fi

# Check Node.js version
echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Install global tools (optional)
echo "📦 Installing global TypeScript tools..."
npm install -g typescript ts-node

echo "✅ Node.js environment setup complete!"
echo "💡 To use this Node.js version, run: nvm use"
echo "💡 To see installed versions, run: nvm list"