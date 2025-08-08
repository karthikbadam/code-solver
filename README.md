# Coding Practice Repository

A comprehensive practice environment for LeetCode-style problems with Python and React/TypeScript support, featuring Claude AI integration for learning assistance.

## 🚀 Features

- **Organized Problem Structure**: Problems categorized by difficulty and topic
- **Multi-Language Support**: Python and React/TypeScript solutions
- **AI-Powered Learning**: Claude integration via OpenRouter for hints and solutions
- **Testing Framework**: Automated testing for all solutions
- **Progress Tracking**: Monitor your solving progress
- **CLI Tools**: Easy commands to add problems and run solutions

## 📁 Project Structure

```
├── problems/                    # Problem definitions and test cases
│   ├── easy/
│   ├── medium/
│   └── hard/
├── solutions/                   # Your solution implementations
│   ├── python/
│   └── react-ts/
├── tools/                       # CLI tools and utilities
│   ├── claude_helper.py        # Claude AI integration
│   ├── problem_manager.py      # Problem management CLI
│   └── test_runner.py          # Testing utilities
├── templates/                   # Templates for new problems/solutions
├── docs/                       # Documentation and guides
└── progress/                   # Progress tracking files
```

## 🛠️ Setup

### Prerequisites

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Node.js 18+** - Download from [nodejs.org](https://nodejs.org)  
- **OpenRouter API key** - Get from [openrouter.ai](https://openrouter.ai)

### Recommended Tools

- **uv** - Fast Python package manager ([astral.sh/uv](https://astral.sh/uv))
- **nvm** - Node Version Manager ([nvm.sh](https://nvm.sh))

### Quick Installation

```bash
# Automated setup (recommended)
python setup.py

# Or with virtual environments (advanced)
./scripts/setup-environments.sh
```

### Manual Installation

```bash
# Python setup (choose one):
pip install -r requirements.txt           # Standard pip
# OR
uv venv && source .venv/bin/activate     # With virtual environment
uv pip install -e .

# Node.js setup:
npm install                              # Standard npm
# OR  
nvm use && npm install                   # With version management

# Configuration:
cp .env.example .env
# Add your OpenRouter API key to .env
```

### Environment Activation

```bash
# Activate both Python and Node.js environments
source ./activate-env.sh

# Or individually:
source .venv/bin/activate  # Python only
nvm use                    # Node.js only
```

## 🎯 Quick Start

### Quick Start: Interactive Learning Workflow

**1. Generate or Add a Problem**
```bash
# Generate AI-powered problems
leetcode generate --difficulty medium --topics "dynamic-programming,graphs"

# Or add existing problems
leetcode add --title "Two Sum" --difficulty easy --topics "array,hash-table"
```

**2. Use Claude as Your Coding Partner**
```bash
# When you're stuck - get progressive hints
leetcode hint two-sum --level subtle        # Gentle nudge
leetcode hint two-sum --level medium        # More concrete help  
leetcode hint two-sum --level strong        # Detailed guidance

# Need approach help - get pseudocode (not full solution!)
leetcode pseudocode two-sum --approach high-level     # Overview
leetcode pseudocode two-sum --approach detailed       # Step-by-step
leetcode pseudocode two-sum --approach implementation # Almost-code

# Understand the problem better
leetcode walkthrough two-sum                          # Trace through examples
leetcode explain "hash tables" --context "two-sum"   # Learn concepts

# When completely stuck
leetcode stuck two-sum --what-tried "brute force, sorting"
```

**3. Code Your Solution & Get Feedback**
```bash
# After writing your solution, get help
leetcode debug two-sum --language python --error "IndexError"  # Debug issues
leetcode review two-sum --language python                      # Code review
leetcode test two-sum --language python                        # Test it

# Only when you want the complete solution
leetcode solve two-sum --language python --approach optimal
```

### Running Tests
```bash
# Test Python solutions
python tools/test_runner.py python two-sum

# Test React/TS solutions
npm test two-sum
```

### Tracking Progress
```bash
python tools/problem_manager.py stats
```

## 📚 Learning Features

- **Structured Practice**: Problems organized by difficulty and topics
- **AI Assistance**: Get hints, explanations, and multiple solution approaches from Claude
- **Test-Driven Development**: Write tests first, then implement solutions
- **Progress Analytics**: Track your improvement over time
- **Multiple Languages**: Practice the same problem in different languages

## 🤖 Claude Integration

The Claude helper provides:
- **Solution Generation**: Get complete solutions with explanations
- **Hint System**: Ask for progressive hints without full spoilers
- **Code Review**: Get feedback on your existing solutions
- **Alternative Approaches**: Explore different algorithms and optimizations

## 📈 Progress Tracking

- Solved problems count by difficulty
- Topics mastery progression
- Time complexity analysis
- Solution comparison metrics

---

Happy coding! 🎉