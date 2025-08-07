#!/usr/bin/env python3
"""
Claude Helper - AI-powered assistance for LeetCode problems
Uses OpenRouter API to access Claude for solutions, hints, and code review.
"""

import os
import json
import requests
import click
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

@dataclass
class ProblemContext:
    """Context about a LeetCode problem"""
    title: str
    difficulty: str
    description: str
    examples: List[Dict]
    constraints: List[str]
    topics: List[str]
    

class ClaudeHelper:
    """Helper class for interacting with Claude via OpenRouter"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        self.model = os.getenv('CLAUDE_MODEL', 'anthropic/claude-3.5-sonnet')
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
    
    def _make_request(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Make a request to the OpenRouter API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/your-repo',  # Optional
            'X-Title': 'LeetCode Practice Helper'  # Optional
        }
        
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': 2000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            click.echo(f"❌ API request failed: {e}", err=True)
            return ""
        except (KeyError, IndexError) as e:
            click.echo(f"❌ Unexpected API response format: {e}", err=True)
            return ""
    
    def get_solution(self, problem: ProblemContext, language: str = "python", 
                    approach: str = "optimal") -> str:
        """Get a complete solution for a problem"""
        
        prompt = f'''
Please provide a {approach} solution for this LeetCode problem in {language}:

**Problem:** {problem.title}
**Difficulty:** {problem.difficulty}
**Topics:** {", ".join(problem.topics)}

**Description:**
{problem.description}

**Examples:**
{self._format_examples(problem.examples)}

**Constraints:**
{self._format_constraints(problem.constraints)}

Please provide:
1. A complete, working solution
2. Time and space complexity analysis
3. Step-by-step explanation of the approach
4. Any alternative approaches worth considering

Format the code with proper comments and follow best practices for {language}.
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def get_hint(self, problem: ProblemContext, hint_level: str = "subtle") -> str:
        """Get a progressive hint for a problem"""
        
        hint_prompts = {
            "subtle": "Give me a very subtle hint that points me in the right direction without giving away the solution.",
            "medium": "Give me a more concrete hint about the approach or data structure I should consider.",
            "strong": "Give me a detailed hint that explains the approach but still leaves the implementation to me."
        }
        
        prompt = f'''
I'm working on this LeetCode problem and need a {hint_level} hint:

**Problem:** {problem.title}
**Difficulty:** {problem.difficulty}
**Description:** {problem.description}

{hint_prompts.get(hint_level, hint_prompts["subtle"])}

Please don't give me the complete solution - I want to figure it out myself!
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.5)
    
    def review_solution(self, problem: ProblemContext, solution_code: str, 
                       language: str = "python") -> str:
        """Get feedback on an existing solution"""
        
        prompt = f'''
Please review my solution for this LeetCode problem:

**Problem:** {problem.title}
**Difficulty:** {problem.difficulty}

**My Solution ({language}):**
```{language}
{solution_code}
```

Please provide:
1. Correctness analysis
2. Time and space complexity analysis
3. Code quality feedback
4. Suggestions for optimization
5. Alternative approaches if applicable
6. Any edge cases I might have missed

Be constructive and educational in your feedback.
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def explain_concept(self, topic: str, context: str = "") -> str:
        """Explain a concept or algorithm"""
        
        prompt = f'''
Please explain the concept/algorithm: {topic}

{f"Context: {context}" if context else ""}

Please provide:
1. Clear explanation of the concept
2. When and why to use it
3. Time/space complexity characteristics
4. Simple example or visualization
5. Common variations or related concepts
6. LeetCode problems where this concept is useful

Keep it educational and easy to understand.
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def debug_solution(self, problem: ProblemContext, solution_code: str, 
                      language: str = "python", error_msg: str = "") -> str:
        """Help debug a solution that isn't working"""
        
        prompt = f'''
I'm having trouble with my solution for this problem. Can you help me debug it?

**Problem:** {problem.title}
**Difficulty:** {problem.difficulty}
**Description:** {problem.description}

**My Code ({language}):**
```{language}
{solution_code}
```

{f"**Error I'm getting:** {error_msg}" if error_msg else ""}

Please help me:
1. Identify what might be wrong with my approach
2. Spot any bugs in the implementation
3. Suggest specific fixes
4. Explain why the issue occurs
5. If the logic is fundamentally wrong, guide me toward the right approach

Be encouraging and educational - help me learn from this debugging process!
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def get_pseudocode(self, problem: ProblemContext, detail_level: str = "high-level") -> str:
        """Generate pseudocode for the problem approach"""
        
        level_prompts = {
            "high-level": "Provide high-level pseudocode that outlines the main approach and key steps.",
            "detailed": "Provide detailed pseudocode with more specific steps and logic.",
            "implementation": "Provide implementation-ready pseudocode that's almost like real code."
        }
        
        prompt = f'''
I understand the problem but need help with the approach. Can you provide {detail_level} pseudocode?

**Problem:** {problem.title}
**Description:** {problem.description}

**Examples:**
{self._format_examples(problem.examples)}

{level_prompts.get(detail_level, level_prompts["high-level"])}

Don't give me the full implementation - I want to code it myself. Just help me structure the approach!
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def walkthrough_test_case(self, problem: ProblemContext, test_case: str = "") -> str:
        """Walk through a test case step by step"""
        
        if test_case:
            prompt = f'''
Can you walk me through this specific test case step by step?

**Problem:** {problem.title}
**Description:** {problem.description}

**Test case to analyze:** {test_case}

Please trace through:
1. What the input represents
2. Step-by-step execution of the optimal algorithm
3. How we arrive at the expected output
4. Any edge cases or special considerations in this example

Help me understand the logic flow!
'''
        else:
            prompt = f'''
Can you walk me through one of the examples step by step?

**Problem:** {problem.title}
**Description:** {problem.description}

**Examples:**
{self._format_examples(problem.examples)}

Pick one example and trace through:
1. What the input represents
2. Step-by-step execution of the optimal algorithm  
3. How we arrive at the expected output
4. Key insights that help solve this type of problem

Help me understand the logic flow!
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def get_stuck_help(self, problem: ProblemContext, what_tried: str = "") -> str:
        """Get help when completely stuck on a problem"""
        
        prompt = f'''
I'm completely stuck on this problem and need help getting unstuck.

**Problem:** {problem.title}
**Difficulty:** {problem.difficulty}
**Topics:** {", ".join(problem.topics)}
**Description:** {problem.description}

{f"**What I've tried so far:** {what_tried}" if what_tried else ""}

I'm not looking for the complete solution, but I need help:
1. Understanding what approach to take
2. Recognizing the key insight or pattern
3. Breaking down the problem into manageable parts
4. Getting started with the right direction

Please guide me step by step to help me think through this problem!
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages)
    
    def generate_problem(self, difficulty: str = "medium", topics: List[str] = None, 
                        style: str = "leetcode", similar_to: str = "") -> Dict[str, Any]:
        """Generate a new practice problem using Claude"""
        
        topics_str = ", ".join(topics) if topics else "algorithms and data structures"
        
        if similar_to:
            prompt = f'''
Create a new {difficulty} difficulty coding problem similar in style and concept to "{similar_to}" but with a different scenario.

The problem should focus on: {topics_str}

Please return a valid JSON object with this exact structure:
{{
  "title": "Problem Title",
  "difficulty": "{difficulty}",
  "topics": ["topic1", "topic2"],
  "description": "Clear problem description with context and requirements",
  "examples": [
    {{
      "input": "Example input format",
      "output": "Expected output",
      "explanation": "Why this is the correct output"
    }}
  ],
  "constraints": [
    "List of constraints and limits",
    "Input/output ranges",
    "Special conditions"
  ],
  "hints": [
    "Subtle hint pointing toward the solution approach",
    "More specific hint about data structures or algorithms",
    "Implementation hint if needed"
  ],
  "followUp": [
    "Extension questions or optimizations"
  ],
  "testCases": [
    {{
      "input": "Test case input in proper format",
      "expectedOutput": "Expected result",
      "description": "What this test case covers"
    }}
  ]
}}

Requirements:
- Make it interesting and practical
- Include 2-3 clear examples with explanations
- Add 3-5 test cases covering edge cases
- Provide meaningful constraints
- Include progressive hints
- Ensure the problem is solvable and well-defined
- Focus on {topics_str} concepts

Return ONLY the JSON object, no additional text.
'''
        else:
            prompt = f'''
Create a new {difficulty} difficulty coding problem for practice.

Topics to focus on: {topics_str}
Style: {style} (e.g., leetcode, competitive programming)

Please return a valid JSON object with this exact structure:
{{
  "title": "Problem Title",
  "difficulty": "{difficulty}",
  "topics": ["topic1", "topic2"],
  "description": "Clear problem description with context and requirements",
  "examples": [
    {{
      "input": "Example input format",
      "output": "Expected output",
      "explanation": "Why this is the correct output"
    }}
  ],
  "constraints": [
    "List of constraints and limits",
    "Input/output ranges",
    "Special conditions"
  ],
  "hints": [
    "Subtle hint pointing toward the solution approach",
    "More specific hint about data structures or algorithms",
    "Implementation hint if needed"
  ],
  "followUp": [
    "Extension questions or optimizations"
  ],
  "testCases": [
    {{
      "input": "Test case input in proper format",
      "expectedOutput": "Expected result",
      "description": "What this test case covers"
    }}
  ]
}}

Requirements:
- Create an original, interesting problem
- Include 2-3 clear examples with explanations  
- Add 3-5 comprehensive test cases including edge cases
- Provide meaningful constraints
- Include progressive hints (subtle to more concrete)
- Ensure the problem tests {topics_str} concepts effectively
- Make it challenging but fair for {difficulty} level

Return ONLY the JSON object, no additional text.
'''
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._make_request(messages, temperature=0.8)
            
            # Try to parse the JSON response
            import json
            problem_data = json.loads(response.strip())
            
            # Validate required fields
            required_fields = ['title', 'difficulty', 'topics', 'description']
            for field in required_fields:
                if field not in problem_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set defaults for optional fields
            problem_data.setdefault('examples', [])
            problem_data.setdefault('constraints', [])
            problem_data.setdefault('hints', [])
            problem_data.setdefault('followUp', [])
            problem_data.setdefault('testCases', [])
            
            return problem_data
            
        except json.JSONDecodeError as e:
            click.echo(f"❌ Failed to parse Claude's response as JSON: {e}", err=True)
            click.echo(f"Raw response: {response[:200]}...", err=True)
            return {}
        except Exception as e:
            click.echo(f"❌ Error generating problem: {e}", err=True)
            return {}
    
    def _format_examples(self, examples: List[Dict]) -> str:
        """Format examples for the prompt"""
        formatted = []
        for i, example in enumerate(examples, 1):
            formatted.append(f"Example {i}:")
            formatted.append(f"Input: {example.get('input', '')}")
            formatted.append(f"Output: {example.get('output', '')}")
            if example.get('explanation'):
                formatted.append(f"Explanation: {example['explanation']}")
            formatted.append("")
        return "\n".join(formatted)
    
    def _format_constraints(self, constraints: List[str]) -> str:
        """Format constraints for the prompt"""
        return "\n".join(f"• {constraint}" for constraint in constraints)


def load_problem(problem_id: str) -> Optional[ProblemContext]:
    """Load problem data from JSON file"""
    problem_file = None
    
    # Search in all difficulty directories
    for difficulty in ['easy', 'medium', 'hard']:
        potential_file = Path(f"problems/{difficulty}/{problem_id}.json")
        if potential_file.exists():
            problem_file = potential_file
            break
    
    if not problem_file:
        click.echo(f"❌ Problem '{problem_id}' not found", err=True)
        return None
    
    try:
        with open(problem_file, 'r') as f:
            data = json.load(f)
        
        return ProblemContext(
            title=data['title'],
            difficulty=data['difficulty'],
            description=data['description'],
            examples=data.get('examples', []),
            constraints=data.get('constraints', []),
            topics=data.get('topics', [])
        )
    except (json.JSONDecodeError, KeyError) as e:
        click.echo(f"❌ Error loading problem file: {e}", err=True)
        return None


@click.group()
def cli():
    """Claude Helper - AI assistance for LeetCode practice"""
    pass


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--language', '-l', default='python', 
              type=click.Choice(['python', 'typescript']), 
              help='Programming language')
@click.option('--approach', '-a', default='optimal',
              type=click.Choice(['brute-force', 'optimal', 'multiple']),
              help='Solution approach')
def solve(problem: str, language: str, approach: str):
    """Get a complete solution for a problem"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    click.echo(f"🤖 Getting {approach} {language} solution for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    solution = helper.get_solution(problem_context, language, approach)
    
    if solution:
        click.echo("\n" + "="*60)
        click.echo("🎯 SOLUTION")
        click.echo("="*60)
        click.echo(solution)
        
        # Optionally save to file
        if click.confirm("\n💾 Save solution to file?"):
            save_solution(problem, language, solution)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--level', '-l', default='subtle',
              type=click.Choice(['subtle', 'medium', 'strong']),
              help='Hint level')
def hint(problem: str, level: str):
    """Get a progressive hint for a problem"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    click.echo(f"💡 Getting {level} hint for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    hint_text = helper.get_hint(problem_context, level)
    
    if hint_text:
        click.echo("\n" + "="*60)
        click.echo("💡 HINT")
        click.echo("="*60)
        click.echo(hint_text)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'typescript']),
              help='Programming language')
@click.option('--file', '-f', help='Solution file to review (optional)')
def review(problem: str, language: str, file: Optional[str]):
    """Review your solution and get feedback"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    # Load solution code
    if file:
        solution_file = Path(file)
    else:
        # Try to find the solution file automatically
        extension = 'py' if language == 'python' else 'ts'
        solution_file = Path(f"solutions/{language}/{problem}.{extension}")
    
    if not solution_file.exists():
        click.echo(f"❌ Solution file not found: {solution_file}", err=True)
        return
    
    try:
        with open(solution_file, 'r') as f:
            solution_code = f.read()
    except Exception as e:
        click.echo(f"❌ Error reading solution file: {e}", err=True)
        return
    
    click.echo(f"🔍 Reviewing your {language} solution for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    review_text = helper.review_solution(problem_context, solution_code, language)
    
    if review_text:
        click.echo("\n" + "="*60)
        click.echo("🔍 SOLUTION REVIEW")
        click.echo("="*60)
        click.echo(review_text)


@cli.command()
@click.option('--topic', '-t', required=True, help='Topic or concept to explain')
@click.option('--context', '-c', help='Additional context')
def explain(topic: str, context: Optional[str]):
    """Explain a concept or algorithm"""
    
    click.echo(f"📚 Explaining: {topic}")
    
    helper = ClaudeHelper()
    explanation = helper.explain_concept(topic, context or "")
    
    if explanation:
        click.echo("\n" + "="*60)
        click.echo("📚 EXPLANATION")
        click.echo("="*60)
        click.echo(explanation)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'typescript']),
              help='Programming language')
@click.option('--error', '-e', help='Error message you\'re getting')
def debug(problem: str, language: str, error: Optional[str]):
    """🐛 Get help debugging your solution"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    # Load solution code
    extension = 'py' if language == 'python' else 'ts'
    solution_file = Path(f"solutions/{language}/{problem}.{extension}")
    
    if not solution_file.exists():
        click.echo(f"❌ Solution file not found: {solution_file}", err=True)
        click.echo("💡 Write some code first, then use this command for debugging help!", err=True)
        return
    
    try:
        with open(solution_file, 'r') as f:
            solution_code = f.read()
    except Exception as e:
        click.echo(f"❌ Error reading solution file: {e}", err=True)
        return
    
    click.echo(f"🐛 Debugging your {language} solution for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    debug_help = helper.debug_solution(problem_context, solution_code, language, error or "")
    
    if debug_help:
        click.echo("\n" + "="*60)
        click.echo("🐛 DEBUG HELP")
        click.echo("="*60)
        click.echo(debug_help)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--approach', '-a', default='high-level',
              type=click.Choice(['high-level', 'detailed', 'implementation']),
              help='Level of pseudocode detail')
def pseudocode(problem: str, approach: str):
    """📝 Get pseudocode for the approach"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    click.echo(f"📝 Generating {approach} pseudocode for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    pseudo = helper.get_pseudocode(problem_context, approach)
    
    if pseudo:
        click.echo("\n" + "="*60)
        click.echo("📝 PSEUDOCODE")
        click.echo("="*60)
        click.echo(pseudo)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--test-case', '-t', help='Specific test case to analyze')
def walkthrough(problem: str, test_case: Optional[str]):
    """🚶 Walk through a test case step by step"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    click.echo(f"🚶 Walking through test case for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    walkthrough_text = helper.walkthrough_test_case(problem_context, test_case or "")
    
    if walkthrough_text:
        click.echo("\n" + "="*60)
        click.echo("🚶 TEST CASE WALKTHROUGH")
        click.echo("="*60)
        click.echo(walkthrough_text)


@cli.command()
@click.option('--problem', '-p', required=True, help='Problem ID')
@click.option('--what-tried', '-w', help='What approaches you\'ve already tried')
def stuck(problem: str, what_tried: Optional[str]):
    """🆘 Get help when completely stuck"""
    
    problem_context = load_problem(problem)
    if not problem_context:
        return
    
    click.echo(f"🆘 Getting unstuck help for '{problem_context.title}'...")
    
    helper = ClaudeHelper()
    stuck_help = helper.get_stuck_help(problem_context, what_tried or "")
    
    if stuck_help:
        click.echo("\n" + "="*60)
        click.echo("🆘 GETTING UNSTUCK")
        click.echo("="*60)
        click.echo(stuck_help)


@cli.command()
@click.option('--difficulty', '-d', default='medium',
              type=click.Choice(['easy', 'medium', 'hard']),
              help='Problem difficulty level')
@click.option('--topics', '-t', help='Comma-separated list of topics to focus on')
@click.option('--similar-to', '-s', help='Generate problem similar to this existing problem')
@click.option('--style', default='leetcode', help='Problem style (leetcode, competitive, etc.)')
@click.option('--save/--no-save', default=True, help='Save the generated problem to repository')
def generate(difficulty: str, topics: Optional[str], similar_to: Optional[str], 
            style: str, save: bool):
    """Generate a new practice problem using Claude"""
    
    topic_list = [topic.strip() for topic in topics.split(',')] if topics else None
    
    click.echo(f"🤖 Generating {difficulty} problem...")
    if topic_list:
        click.echo(f"   Topics: {', '.join(topic_list)}")
    if similar_to:
        click.echo(f"   Similar to: {similar_to}")
    
    helper = ClaudeHelper()
    problem_data = helper.generate_problem(
        difficulty=difficulty,
        topics=topic_list,
        style=style,
        similar_to=similar_to or ""
    )
    
    if not problem_data:
        click.echo("❌ Failed to generate problem", err=True)
        return
    
    # Display the generated problem
    click.echo("\n" + "="*60)
    click.echo("🎯 GENERATED PROBLEM")
    click.echo("="*60)
    click.echo(f"Title: {problem_data['title']}")
    click.echo(f"Difficulty: {problem_data['difficulty'].title()}")
    click.echo(f"Topics: {', '.join(problem_data['topics'])}")
    click.echo(f"\nDescription:\n{problem_data['description']}")
    
    if problem_data.get('examples'):
        click.echo("\nExamples:")
        for i, example in enumerate(problem_data['examples'], 1):
            click.echo(f"  Example {i}:")
            click.echo(f"    Input: {example.get('input', '')}")
            click.echo(f"    Output: {example.get('output', '')}")
            if example.get('explanation'):
                click.echo(f"    Explanation: {example['explanation']}")
    
    if save:
        if click.confirm("\n💾 Save this problem to your repository?"):
            save_generated_problem(problem_data)
        else:
            click.echo("Problem not saved. You can copy the details above if needed.")


def save_generated_problem(problem_data: Dict[str, Any]):
    """Save a generated problem using the ProblemManager"""
    try:
        # Import ProblemManager here to avoid circular imports
        from tools.problem_manager import ProblemManager
        
        manager = ProblemManager()
        
        # Use ProblemManager's add_problem method but with full data
        problem_id = manager._generate_id(problem_data['title'])
        difficulty = problem_data['difficulty'].lower()
        
        # Create the complete problem structure
        complete_problem = {
            "id": problem_id,
            "title": problem_data['title'],
            "difficulty": difficulty,
            "topics": problem_data.get('topics', []),
            "description": problem_data.get('description', ''),
            "examples": problem_data.get('examples', []),
            "constraints": problem_data.get('constraints', []),
            "hints": problem_data.get('hints', []),
            "follow_up": problem_data.get('followUp', []),
            "test_cases": problem_data.get('testCases', []),
            "metadata": {
                "companies": [],
                "frequency": "",
                "acceptance_rate": "",
                "leetcode_url": "",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "generated_by": "claude"
            }
        }
        
        # Save the problem file
        problem_file = manager.problems_dir / difficulty / f"{problem_id}.json"
        problem_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(problem_file, 'w') as f:
            json.dump(complete_problem, f, indent=2)
        
        # Create solution templates using a simple object with the required attributes
        class TempProblem:
            def __init__(self, data):
                self.title = data['title']
                self.difficulty = data['difficulty']
                self.topics = data['topics']
                self.description = data['description']
        
        temp_problem = TempProblem(complete_problem)
        manager._create_solution_templates(problem_id, temp_problem)
        
        click.echo(f"✅ Problem '{problem_data['title']}' saved successfully!")
        click.echo(f"   ID: {problem_id}")
        click.echo(f"   File: {problem_file}")
        
        return problem_id
        
    except Exception as e:
        click.echo(f"❌ Error saving generated problem: {e}", err=True)
        return None


def save_solution(problem_id: str, language: str, solution: str):
    """Save a solution to the appropriate file"""
    extension = 'py' if language == 'python' else 'ts'
    solution_dir = Path(f"solutions/{language}")
    solution_dir.mkdir(parents=True, exist_ok=True)
    
    solution_file = solution_dir / f"{problem_id}.{extension}"
    
    try:
        with open(solution_file, 'w') as f:
            f.write(solution)
        click.echo(f"✅ Solution saved to: {solution_file}")
    except Exception as e:
        click.echo(f"❌ Error saving solution: {e}", err=True)


if __name__ == '__main__':
    cli()