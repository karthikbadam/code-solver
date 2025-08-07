# Usage Guide

## Overview

This guide covers the main workflows for practicing LeetCode problems with AI assistance.

## Core Workflows

### 1. Adding a New Problem

#### Manual Addition
```bash
python tools/problem_manager.py add \
  --title "Two Sum" \
  --difficulty easy \
  --topics "array,hash-table" \
  --description "Find two numbers that add up to target" \
  --url "https://leetcode.com/problems/two-sum/"
```

#### What This Creates
- Problem JSON file in `problems/{difficulty}/{problem-id}.json`
- Python solution template in `solutions/python/{problem-id}.py`
- TypeScript solution template in `solutions/react-ts/{problem-id}.ts`

### 2. Getting AI Assistance

#### Complete Solutions
```bash
# Get an optimal solution
python tools/claude_helper.py solve --problem two-sum --language python --approach optimal

# Get multiple approaches
python tools/claude_helper.py solve --problem two-sum --language python --approach multiple

# Get a brute force solution first
python tools/claude_helper.py solve --problem two-sum --language python --approach brute-force
```

#### Progressive Hints
```bash
# Subtle hint (just direction)
python tools/claude_helper.py hint --problem two-sum --level subtle

# Medium hint (concrete approach)
python tools/claude_helper.py hint --problem two-sum --level medium

# Strong hint (detailed approach)
python tools/claude_helper.py hint --problem two-sum --level strong
```

#### Code Review
```bash
# Review your solution
python tools/claude_helper.py review --problem two-sum --language python

# Review specific file
python tools/claude_helper.py review --problem two-sum --language python --file path/to/solution.py
```

#### Concept Learning
```bash
# Learn about algorithms/concepts
python tools/claude_helper.py explain --topic "dynamic programming"
python tools/claude_helper.py explain --topic "binary search" --context "finding insertion point"
```

### 3. Testing Solutions

#### Individual Problems
```bash
# Test Python solution
python tools/test_runner.py run two-sum --language python

# Test TypeScript solution
python tools/test_runner.py run two-sum --language typescript

# Test both languages
python tools/test_runner.py run two-sum --language both
```

#### All Solutions
```bash
# Test all Python solutions
python tools/test_runner.py all --language python

# Test all solutions with verbose output
python tools/test_runner.py all --verbose
```

#### Solution Validation
```bash
# Check if solution is properly implemented
python tools/test_runner.py validate two-sum --language python
```

### 4. Progress Tracking

#### View Statistics
```bash
# Overall progress
python tools/problem_manager.py stats

# List all problems
python tools/problem_manager.py list

# Filter by difficulty
python tools/problem_manager.py list --difficulty easy

# Filter by topic
python tools/problem_manager.py list --topic array

# Show only solved problems
python tools/problem_manager.py list --solved

# Show only unsolved problems
python tools/problem_manager.py list --unsolved
```

#### Problem Details
```bash
# View detailed problem information
python tools/problem_manager.py show two-sum
```

## Recommended Learning Workflow

### 1. Start with Understanding
```bash
# First, read the problem
python tools/problem_manager.py show {problem-id}

# If you need concept clarification
python tools/claude_helper.py explain --topic "{concept}" --context "{problem context}"
```

### 2. Try Solving Yourself
1. Open the solution file: `solutions/python/{problem-id}.py`
2. Implement your solution
3. Test it: `python tools/test_runner.py run {problem-id}`

### 3. Get Progressive Help
```bash
# If stuck, start with subtle hints
python tools/claude_helper.py hint --problem {problem-id} --level subtle

# If still stuck, get stronger hints
python tools/claude_helper.py hint --problem {problem-id} --level medium
python tools/claude_helper.py hint --problem {problem-id} --level strong
```

### 4. Review and Learn
```bash
# Get feedback on your solution
python tools/claude_helper.py review --problem {problem-id} --language python

# Compare with optimal solution
python tools/claude_helper.py solve --problem {problem-id} --language python
```

### 5. Practice Variations
```bash
# Try implementing in different language
# Edit: solutions/react-ts/{problem-id}.ts

# Test the new implementation
python tools/test_runner.py run {problem-id} --language typescript
```

## Tips for Effective Practice

### Use Progressive Difficulty
1. Start with easy problems to build confidence
2. Focus on understanding patterns before moving to harder problems
3. Revisit solved problems to reinforce learning

### Topic-Based Practice
```bash
# Focus on specific topics
python tools/problem_manager.py list --topic "dynamic-programming"
python tools/problem_manager.py list --topic "tree"
```

### Regular Review
```bash
# Check your progress weekly
python tools/problem_manager.py stats

# Review solutions you solved a while ago
python tools/claude_helper.py review --problem old-problem --language python
```

### Combine Languages
- Solve in Python first (often easier to prototype)
- Implement in TypeScript for additional practice
- Compare performance and code structure

## Advanced Features

### Batch Operations
```bash
# Add multiple problems from a list
# (Create a script that reads from a CSV/JSON file)

# Test all problems of a specific difficulty
python tools/test_runner.py all --language python | grep -E "(Easy|Medium|Hard)"
```

### Custom Workflows
Create shell aliases for common operations:
```bash
# Add to your .bashrc or .zshrc
alias lc-add="python tools/problem_manager.py add"
alias lc-solve="python tools/claude_helper.py solve"
alias lc-hint="python tools/claude_helper.py hint"
alias lc-test="python tools/test_runner.py run"
alias lc-stats="python tools/problem_manager.py stats"
```

### Integration with IDEs
- Set up VS Code tasks for common operations
- Use the integrated terminal for quick commands
- Install LeetCode extension for additional problem browsing

## Common Patterns

### When Starting a New Topic
1. Use `claude_helper.py explain` to understand the concept
2. Find 2-3 easy problems in that topic
3. Solve them with progressive hints
4. Move to medium difficulty

### When Stuck on a Problem
1. Take a break and come back fresh
2. Ask for a subtle hint first
3. Think about similar problems you've solved
4. If still stuck, get a stronger hint
5. Implement and test your solution
6. Review the optimal solution to learn

### Before Moving to Next Difficulty
1. Solve at least 10-15 problems in current difficulty
2. Achieve >80% solve rate in that difficulty
3. Be comfortable with common patterns
4. Review and understand time/space complexities