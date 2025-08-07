#!/usr/bin/env python3
"""
Problem Manager - CLI tool for managing LeetCode problems
Helps add new problems, track progress, and organize practice sessions.
"""

import os
import json
import click
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import shutil
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))


@dataclass
class Problem:
    """Represents a LeetCode problem"""
    id: str
    title: str
    difficulty: str
    topics: List[str]
    description: str
    examples: List[Dict[str, str]] = None
    constraints: List[str] = None
    hints: List[str] = None
    follow_up: List[str] = None
    test_cases: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []
        if self.constraints is None:
            self.constraints = []
        if self.hints is None:
            self.hints = []
        if self.follow_up is None:
            self.follow_up = []
        if self.test_cases is None:
            self.test_cases = []
        if self.metadata is None:
            self.metadata = {
                "companies": [],
                "frequency": "",
                "acceptance_rate": "",
                "leetcode_url": "",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }


class ProblemManager:
    """Manages LeetCode problems and solutions"""
    
    def __init__(self):
        self.problems_dir = Path("problems")
        self.solutions_dir = Path("solutions")
        self.templates_dir = Path("templates")
        self.progress_dir = Path("progress")
        
        # Ensure directories exist
        for directory in [self.problems_dir, self.solutions_dir, self.progress_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def add_problem(self, title: str, difficulty: str, topics: List[str], 
                   description: str = "", leetcode_url: str = "") -> Problem:
        """Add a new problem to the repository"""
        
        # Generate problem ID from title
        problem_id = self._generate_id(title)
        
        # Create problem object
        problem = Problem(
            id=problem_id,
            title=title,
            difficulty=difficulty.lower(),
            topics=topics,
            description=description
        )
        
        if leetcode_url:
            problem.metadata["leetcode_url"] = leetcode_url
        
        # Save problem file
        problem_file = self.problems_dir / difficulty.lower() / f"{problem_id}.json"
        problem_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(problem_file, 'w') as f:
            json.dump(asdict(problem), f, indent=2)
        
        # Create solution template files
        self._create_solution_templates(problem_id, problem)
        
        click.echo(f"✅ Problem '{title}' added successfully!")
        click.echo(f"   ID: {problem_id}")
        click.echo(f"   File: {problem_file}")
        
        return problem
    
    def list_problems(self, difficulty: Optional[str] = None, 
                     topic: Optional[str] = None, solved: Optional[bool] = None) -> List[Dict]:
        """List problems with optional filtering"""
        
        problems = []
        
        # Search all difficulty directories
        search_dirs = [difficulty.lower()] if difficulty else ['easy', 'medium', 'hard']
        
        for diff in search_dirs:
            diff_dir = self.problems_dir / diff
            if not diff_dir.exists():
                continue
                
            for problem_file in diff_dir.glob("*.json"):
                try:
                    with open(problem_file, 'r') as f:
                        problem_data = json.load(f)
                    
                    # Apply filters
                    if topic and topic.lower() not in [t.lower() for t in problem_data.get('topics', [])]:
                        continue
                    
                    if solved is not None:
                        is_solved = self._is_problem_solved(problem_data['id'])
                        if solved != is_solved:
                            continue
                    
                    problems.append(problem_data)
                    
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return sorted(problems, key=lambda x: (x['difficulty'], x['title']))
    
    def get_problem(self, problem_id: str) -> Optional[Dict]:
        """Get a specific problem by ID"""
        
        # Search in all difficulty directories
        for difficulty in ['easy', 'medium', 'hard']:
            problem_file = self.problems_dir / difficulty / f"{problem_id}.json"
            if problem_file.exists():
                try:
                    with open(problem_file, 'r') as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def update_problem(self, problem_id: str, **updates) -> bool:
        """Update a problem with new information"""
        
        problem_data = self.get_problem(problem_id)
        if not problem_data:
            return False
        
        # Update fields
        for key, value in updates.items():
            if key in problem_data:
                problem_data[key] = value
        
        problem_data['metadata']['updated_at'] = datetime.now().isoformat()
        
        # Save back to file
        problem_file = self.problems_dir / problem_data['difficulty'] / f"{problem_id}.json"
        with open(problem_file, 'w') as f:
            json.dump(problem_data, f, indent=2)
        
        return True
    
    def delete_problem(self, problem_id: str) -> bool:
        """Delete a problem and its solutions"""
        
        problem_data = self.get_problem(problem_id)
        if not problem_data:
            return False
        
        # Delete problem file
        problem_file = self.problems_dir / problem_data['difficulty'] / f"{problem_id}.json"
        problem_file.unlink()
        
        # Delete solution files
        for lang in ['python', 'react-ts']:
            extension = 'py' if lang == 'python' else 'ts'
            solution_file = self.solutions_dir / lang / f"{problem_id}.{extension}"
            if solution_file.exists():
                solution_file.unlink()
        
        click.echo(f"✅ Problem '{problem_id}' deleted successfully!")
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about problems and progress"""
        
        stats = {
            "total_problems": 0,
            "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
            "by_topic": {},
            "solved": {"total": 0, "easy": 0, "medium": 0, "hard": 0},
            "unsolved": {"total": 0, "easy": 0, "medium": 0, "hard": 0},
            "solve_rate": 0.0
        }
        
        all_problems = self.list_problems()
        stats["total_problems"] = len(all_problems)
        
        for problem in all_problems:
            difficulty = problem['difficulty']
            stats["by_difficulty"][difficulty] += 1
            
            # Count topics
            for topic in problem.get('topics', []):
                if topic not in stats["by_topic"]:
                    stats["by_topic"][topic] = {"total": 0, "solved": 0}
                stats["by_topic"][topic]["total"] += 1
            
            # Check if solved
            if self._is_problem_solved(problem['id']):
                stats["solved"]["total"] += 1
                stats["solved"][difficulty] += 1
                
                # Update topic solved count
                for topic in problem.get('topics', []):
                    stats["by_topic"][topic]["solved"] += 1
            else:
                stats["unsolved"]["total"] += 1
                stats["unsolved"][difficulty] += 1
        
        # Calculate solve rate
        if stats["total_problems"] > 0:
            stats["solve_rate"] = stats["solved"]["total"] / stats["total_problems"] * 100
        
        return stats
    
    def _generate_id(self, title: str) -> str:
        """Generate a URL-friendly ID from problem title"""
        import re
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        problem_id = re.sub(r'[^\w\s-]', '', title.lower())
        problem_id = re.sub(r'[-\s]+', '-', problem_id)
        problem_id = problem_id.strip('-')
        
        return problem_id
    
    def _create_solution_templates(self, problem_id: str, problem: Problem):
        """Create solution template files for a new problem"""
        
        # Template replacements
        replacements = {
            '{problem_title}': problem.title,
            '{difficulty}': problem.difficulty.title(),
            '{topics}': ', '.join(problem.topics),
            '{description}': problem.description or 'TODO: Add description',
            '{examples}': 'TODO: Add examples',
            '{constraints}': 'TODO: Add constraints'
        }
        
        # Create Python solution
        python_template = self.templates_dir / "python_solution_template.py"
        if python_template.exists():
            with open(python_template, 'r') as f:
                content = f.read()
            
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            
            python_solution = self.solutions_dir / "python" / f"{problem_id}.py"
            python_solution.parent.mkdir(parents=True, exist_ok=True)
            
            with open(python_solution, 'w') as f:
                f.write(content)
        
        # Create TypeScript solution
        ts_template = self.templates_dir / "react_ts_solution_template.ts"
        if ts_template.exists():
            with open(ts_template, 'r') as f:
                content = f.read()
            
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            
            ts_solution = self.solutions_dir / "react-ts" / f"{problem_id}.ts"
            ts_solution.parent.mkdir(parents=True, exist_ok=True)
            
            with open(ts_solution, 'w') as f:
                f.write(content)
        
        click.echo(f"   📝 Created solution templates for {problem_id}")
    
    def _is_problem_solved(self, problem_id: str) -> bool:
        """Check if a problem has been solved"""
        
        # Check for Python solution
        python_solution = self.solutions_dir / "python" / f"{problem_id}.py"
        ts_solution = self.solutions_dir / "react-ts" / f"{problem_id}.ts"
        
        # Consider solved if either solution exists and has non-template content
        for solution_file in [python_solution, ts_solution]:
            if solution_file.exists():
                try:
                    with open(solution_file, 'r') as f:
                        content = f.read()
                    
                    # Check if it's more than just the template
                    # (simple heuristic: look for actual implementation)
                    if 'pass' not in content and 'null' not in content:
                        return True
                except:
                    continue
        
        return False


@click.group()
def cli():
    """Problem Manager - Manage your LeetCode practice problems"""
    pass


@cli.command()
@click.option('--title', '-t', required=True, help='Problem title')
@click.option('--difficulty', '-d', required=True,
              type=click.Choice(['easy', 'medium', 'hard'], case_sensitive=False),
              help='Problem difficulty')
@click.option('--topics', required=True, help='Comma-separated list of topics')
@click.option('--description', help='Problem description')
@click.option('--url', help='LeetCode URL')
def add(title: str, difficulty: str, topics: str, description: str, url: str):
    """Add a new problem"""
    
    topic_list = [topic.strip() for topic in topics.split(',')]
    
    manager = ProblemManager()
    problem = manager.add_problem(
        title=title,
        difficulty=difficulty,
        topics=topic_list,
        description=description or "",
        leetcode_url=url or ""
    )


@cli.command()
@click.option('--difficulty', '-d', help='Filter by difficulty')
@click.option('--topic', '-t', help='Filter by topic')
@click.option('--solved/--unsolved', default=None, help='Filter by solved status')
@click.option('--format', '-f', default='table',
              type=click.Choice(['table', 'json']),
              help='Output format')
def list_cmd(difficulty: str, topic: str, solved: bool, format: str):
    """List problems"""
    
    manager = ProblemManager()
    problems = manager.list_problems(difficulty, topic, solved)
    
    if not problems:
        click.echo("No problems found matching the criteria.")
        return
    
    if format == 'json':
        click.echo(json.dumps(problems, indent=2))
        return
    
    # Table format
    from tabulate import tabulate
    
    table_data = []
    for problem in problems:
        solved_status = "✅" if manager._is_problem_solved(problem['id']) else "❌"
        table_data.append([
            problem['id'],
            problem['title'],
            problem['difficulty'].title(),
            ', '.join(problem.get('topics', [])),
            solved_status
        ])
    
    headers = ['ID', 'Title', 'Difficulty', 'Topics', 'Solved']
    click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))


@cli.command()
@click.argument('problem_id')
def show(problem_id: str):
    """Show detailed information about a problem"""
    
    manager = ProblemManager()
    problem = manager.get_problem(problem_id)
    
    if not problem:
        click.echo(f"❌ Problem '{problem_id}' not found", err=True)
        return
    
    click.echo(f"📋 {problem['title']}")
    click.echo("=" * 60)
    click.echo(f"ID: {problem['id']}")
    click.echo(f"Difficulty: {problem['difficulty'].title()}")
    click.echo(f"Topics: {', '.join(problem.get('topics', []))}")
    
    if problem.get('description'):
        click.echo(f"\nDescription:\n{problem['description']}")
    
    if problem.get('examples'):
        click.echo("\nExamples:")
        for i, example in enumerate(problem['examples'], 1):
            click.echo(f"  Example {i}:")
            click.echo(f"    Input: {example.get('input', '')}")
            click.echo(f"    Output: {example.get('output', '')}")
            if example.get('explanation'):
                click.echo(f"    Explanation: {example['explanation']}")
    
    if problem.get('constraints'):
        click.echo("\nConstraints:")
        for constraint in problem['constraints']:
            click.echo(f"  • {constraint}")
    
    # Show solution status
    solved = manager._is_problem_solved(problem_id)
    status = "✅ Solved" if solved else "❌ Not solved"
    click.echo(f"\nStatus: {status}")


@cli.command()
@click.argument('problem_id')
def delete(problem_id: str):
    """Delete a problem"""
    
    if not click.confirm(f"Are you sure you want to delete problem '{problem_id}'?"):
        return
    
    manager = ProblemManager()
    success = manager.delete_problem(problem_id)
    
    if not success:
        click.echo(f"❌ Problem '{problem_id}' not found", err=True)


@cli.command()
def stats():
    """Show statistics about your practice progress"""
    
    manager = ProblemManager()
    stats = manager.get_stats()
    
    click.echo("📊 PRACTICE STATISTICS")
    click.echo("=" * 60)
    
    # Overall progress
    click.echo(f"Total Problems: {stats['total_problems']}")
    click.echo(f"Solved: {stats['solved']['total']} ({stats['solve_rate']:.1f}%)")
    click.echo(f"Remaining: {stats['unsolved']['total']}")
    
    # By difficulty
    click.echo("\n📈 BY DIFFICULTY:")
    for difficulty in ['easy', 'medium', 'hard']:
        total = stats['by_difficulty'][difficulty]
        solved = stats['solved'][difficulty]
        if total > 0:
            percentage = (solved / total) * 100
            click.echo(f"  {difficulty.title()}: {solved}/{total} ({percentage:.1f}%)")
    
    # By topic (top 10)
    if stats['by_topic']:
        click.echo("\n🏷️  TOP TOPICS:")
        sorted_topics = sorted(
            stats['by_topic'].items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )[:10]
        
        for topic, data in sorted_topics:
            percentage = (data['solved'] / data['total'] * 100) if data['total'] > 0 else 0
            click.echo(f"  {topic}: {data['solved']}/{data['total']} ({percentage:.1f}%)")


@cli.command()
@click.option('--difficulty', '-d', default='medium',
              type=click.Choice(['easy', 'medium', 'hard']),
              help='Problem difficulty level')
@click.option('--topics', '-t', help='Comma-separated list of topics to focus on')
@click.option('--similar-to', '-s', help='Generate problem similar to this existing problem')
@click.option('--style', default='leetcode', help='Problem style')
def generate(difficulty: str, topics: str, similar_to: str, style: str):
    """Generate a new problem using Claude AI"""
    
    # Check if OpenRouter API key is set
    if not os.getenv('OPENROUTER_API_KEY'):
        click.echo("❌ OPENROUTER_API_KEY environment variable is required", err=True)
        click.echo("   Please set your OpenRouter API key in the .env file", err=True)
        return
    
    try:
        # Import claude_helper here to avoid import issues
        from tools.claude_helper import ClaudeHelper
        
        topic_list = [topic.strip() for topic in topics.split(',')] if topics else None
        
        click.echo(f"🤖 Generating {difficulty} problem using Claude...")
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
        
        # Save the problem
        if click.confirm("\n💾 Save this problem to your repository?"):
            # Create problem using existing ProblemManager infrastructure
            manager = ProblemManager()
            problem_id = manager._generate_id(problem_data['title'])
            
            # Save with full structure
            complete_problem = {
                "id": problem_id,
                "title": problem_data['title'],
                "difficulty": difficulty.lower(),
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
            problem_file = manager.problems_dir / difficulty.lower() / f"{problem_id}.json"
            problem_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(problem_file, 'w') as f:
                json.dump(complete_problem, f, indent=2)
            
            # Create solution templates
            problem_obj = Problem(
                id=problem_id,
                title=problem_data['title'],
                difficulty=difficulty.lower(),
                topics=problem_data.get('topics', []),
                description=problem_data.get('description', '')
            )
            manager._create_solution_templates(problem_id, problem_obj)
            
            click.echo(f"✅ Problem '{problem_data['title']}' saved successfully!")
            click.echo(f"   ID: {problem_id}")
            click.echo(f"   File: {problem_file}")
        else:
            click.echo("Problem not saved. You can copy the details above if needed.")
            
    except ImportError:
        click.echo("❌ Claude helper not available. Make sure all dependencies are installed.", err=True)
    except Exception as e:
        click.echo(f"❌ Error generating problem: {e}", err=True)


# Alias for 'list' command (since 'list' is a Python keyword)
cli.add_command(list_cmd, name='list')


if __name__ == '__main__':
    cli()