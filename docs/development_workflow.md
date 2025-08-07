# Development Workflow

This guide covers the recommended development workflow using virtual environments and modern tooling.

## 🚀 Environment Setup

### Initial Setup

```bash
# Option 1: Full automated setup
./scripts/setup-environments.sh

# Option 2: Individual setup
./scripts/setup-python-env.sh   # Python with uv
./scripts/setup-node-env.sh     # Node.js with nvm

# Option 3: Quick combined activation
source ./activate-env.sh
```

### Daily Workflow

```bash
# Start your coding session
source ./activate-env.sh

# Verify environments
python --version    # Should show Python from .venv
node --version      # Should show Node.js from .nvmrc
which python        # Should point to .venv/bin/python
```

## 🐍 Python Development

### Virtual Environment with uv

```bash
# Create virtual environment (done in setup)
uv venv

# Activate environment
source .venv/bin/activate

# Install/update dependencies
uv pip install -e .
uv pip install -e ".[dev,test]"

# Add new dependencies
uv add requests
uv add --dev pytest

# Update dependencies
uv pip install --upgrade-all

# Export requirements (for compatibility)
uv pip freeze > requirements.txt
```

### Running Python Tools

```bash
# With virtual environment activated
python leetcode.py demo
python tools/problem_manager.py stats
python tools/claude_helper.py solve two-sum

# Or directly (if environment is activated)
leetcode demo  # If installed as script
```

### Python Development Best Practices

```bash
# Code formatting
black tools/ solutions/python/

# Linting
flake8 tools/ solutions/python/

# Type checking
mypy tools/ solutions/python/

# Testing
pytest solutions/python/ -v
pytest --cov=tools tests/
```

## 📦 Node.js Development

### Version Management with nvm

```bash
# Use project Node.js version
nvm use

# Install different version
nvm install 20.0.0
nvm use 20.0.0

# Set default version
nvm alias default 18.19.0

# List installed versions
nvm list
```

### Package Management

```bash
# Install dependencies
npm install

# Add new dependency
npm install lodash
npm install --save-dev @types/lodash

# Update dependencies
npm update

# Run scripts
npm test
npm run build
npm run lint
```

### TypeScript Development

```bash
# Compile TypeScript
npx tsc

# Run TypeScript files directly
npx ts-node solutions/react-ts/two-sum.ts

# Run tests
npm test
jest solutions/react-ts/

# Linting and formatting
npm run lint
npm run format
```

## 🔄 Switching Between Projects

### Deactivating Environments

```bash
# Deactivate Python virtual environment
deactivate

# Switch to different Node.js version
nvm use system  # or nvm use <version>
```

### Environment Isolation

Each project should have its own:
- Python virtual environment (`.venv/`)
- Node.js version (`.nvmrc`)
- Dependencies (`pyproject.toml`, `package.json`)

## 🧪 Testing Workflow

### Python Testing

```bash
# Run tests for specific problem
python tools/test_runner.py run two-sum --language python

# Run all Python tests
python tools/test_runner.py all --language python

# Run with coverage
pytest --cov=tools --cov=solutions/python tests/

# Run specific test file
pytest solutions/python/two-sum.py -v
```

### TypeScript Testing

```bash
# Run TypeScript tests
python tools/test_runner.py run two-sum --language typescript

# Or directly with npm
npm test two-sum

# Run all TypeScript tests
npm test
```

### Integration Testing

```bash
# Test both languages
python tools/test_runner.py run two-sum --language both

# Validate solutions
python tools/test_runner.py validate two-sum --language python
```

## 🛠️ Development Tools

### Recommended IDE Setup

**VS Code Extensions:**
- Python extension (with virtual environment detection)
- TypeScript extension
- ESLint
- Prettier
- GitLens

**Configuration:**
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "typescript.preferences.includePackageJsonAutoImports": "on",
  "eslint.workingDirectories": ["solutions/react-ts"],
  "python.formatting.provider": "black"
}
```

### Git Integration

```bash
# Pre-commit hooks (recommended)
pip install pre-commit
pre-commit install

# Manual checks before commit
black --check .
flake8 .
mypy tools/
npm run lint
npm test
```

### Debugging

**Python:**
```bash
# Debug with pdb
python -m pdb tools/problem_manager.py add --title "Test"

# Debug tests
pytest --pdb solutions/python/two-sum.py
```

**TypeScript:**
```bash
# Debug with VS Code
# Set breakpoints and use F5 to debug

# Or with node debugger
node --inspect-brk node_modules/.bin/ts-node solutions/react-ts/two-sum.ts
```

## 📊 Performance Monitoring

### Python Performance

```bash
# Profile code execution
python -m cProfile tools/problem_manager.py stats

# Memory profiling
pip install memory-profiler
python -m memory_profiler solutions/python/two-sum.py
```

### Node.js Performance

```bash
# Node.js built-in profiler
node --prof solutions/react-ts/two-sum.ts

# Performance monitoring
npm install --save-dev clinic
npx clinic doctor -- node solutions/react-ts/two-sum.ts
```

## 🚨 Troubleshooting

### Python Issues

```bash
# Virtual environment not found
./scripts/setup-python-env.sh

# Wrong Python version
which python
source .venv/bin/activate

# Dependencies not installed
uv pip install -e .
```

### Node.js Issues

```bash
# Wrong Node.js version
nvm use
cat .nvmrc

# Dependencies not installed
npm install

# Module not found
npm ls
npm install --save missing-module
```

### Environment Conflicts

```bash
# Clean slate setup
deactivate
rm -rf .venv node_modules
./scripts/setup-environments.sh

# Check environment isolation
which python
which node
echo $PATH
```

This workflow ensures consistent, reproducible development environments across different machines and team members.