#!/usr/bin/env python3
"""
LeetCode Helper - Main CLI entry point
Provides quick access to all LeetCode practice tools.
"""

import sys
import subprocess
from pathlib import Path
import click


@click.group()
def cli():
    """🎯 LeetCode Practice Helper - Your AI-powered coding practice companion"""
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
    """➕ Add a new problem"""
    cmd = [
        sys.executable, 'tools/problem_manager.py', 'add',
        '--title', title,
        '--difficulty', difficulty,
        '--topics', topics
    ]
    
    if description:
        cmd.extend(['--description', description])
    if url:
        cmd.extend(['--url', url])
    
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'typescript']),
              help='Programming language')
@click.option('--approach', '-a', default='optimal',
              type=click.Choice(['brute-force', 'optimal', 'multiple']),
              help='Solution approach')
def solve(problem_id: str, language: str, approach: str):
    """🤖 Get AI solution for a problem"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'solve',
        '--problem', problem_id,
        '--language', language,
        '--approach', approach
    ]
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--level', '-l', default='subtle',
              type=click.Choice(['subtle', 'medium', 'strong']),
              help='Hint level')
def hint(problem_id: str, level: str):
    """💡 Get a progressive hint"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'hint',
        '--problem', problem_id,
        '--level', level
    ]
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'typescript']),
              help='Programming language')
def review(problem_id: str, language: str):
    """🔍 Get AI feedback on your solution"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'review',
        '--problem', problem_id,
        '--language', language
    ]
    subprocess.run(cmd)


@cli.command()
@click.argument('topic')
@click.option('--context', '-c', help='Additional context')
def explain(topic: str, context: str):
    """📚 Explain a concept or algorithm"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'explain',
        '--topic', topic
    ]
    if context:
        cmd.extend(['--context', context])
    subprocess.run(cmd)


@cli.command()
@click.option('--difficulty', '-d', default='medium',
              type=click.Choice(['easy', 'medium', 'hard']),
              help='Problem difficulty level')
@click.option('--topics', '-t', help='Comma-separated list of topics to focus on')
@click.option('--similar-to', '-s', help='Generate problem similar to this existing problem')
@click.option('--style', default='leetcode', help='Problem style')
def generate(difficulty: str, topics: str, similar_to: str, style: str):
    """🤖 Generate a new practice problem using Claude AI"""
    cmd = [
        sys.executable, 'tools/problem_manager.py', 'generate',
        '--difficulty', difficulty
    ]
    
    if topics:
        cmd.extend(['--topics', topics])
    if similar_to:
        cmd.extend(['--similar-to', similar_to])
    if style != 'leetcode':
        cmd.extend(['--style', style])
    
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'typescript']),
              help='Programming language')
@click.option('--error', '-e', help='Error message you\'re getting')
def debug(problem_id: str, language: str, error: str):
    """🐛 Get help debugging your solution"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'debug',
        '--problem', problem_id,
        '--language', language
    ]
    if error:
        cmd.extend(['--error', error])
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--approach', '-a', default='high-level',
              type=click.Choice(['high-level', 'detailed', 'implementation']),
              help='Level of pseudocode detail')
def pseudocode(problem_id: str, approach: str):
    """📝 Get pseudocode for the approach"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'pseudocode',
        '--problem', problem_id,
        '--approach', approach
    ]
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--test-case', '-t', help='Specific test case to analyze')
def walkthrough(problem_id: str, test_case: str):
    """🚶 Walk through a test case step by step"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'walkthrough',
        '--problem', problem_id
    ]
    if test_case:
        cmd.extend(['--test-case', test_case])
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--what-tried', '-w', help='What approaches you\'ve already tried')
def stuck(problem_id: str, what_tried: str):
    """🆘 Get help when completely stuck"""
    cmd = [
        sys.executable, 'tools/claude_helper.py', 'stuck',
        '--problem', problem_id
    ]
    if what_tried:
        cmd.extend(['--what-tried', what_tried])
    subprocess.run(cmd)


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l', default='both',
              type=click.Choice(['python', 'typescript', 'both']),
              help='Language to test')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def test(problem_id: str, language: str, verbose: bool):
    """🧪 Run tests for a problem"""
    cmd = [
        sys.executable, 'tools/test_runner.py', 'run',
        problem_id,
        '--language', language
    ]
    if verbose:
        cmd.append('--verbose')
    subprocess.run(cmd)


@cli.command()
@click.option('--difficulty', '-d', help='Filter by difficulty')
@click.option('--topic', '-t', help='Filter by topic')
@click.option('--solved/--unsolved', default=None, help='Filter by solved status')
def list_problems(difficulty: str, topic: str, solved: bool):
    """📋 List problems"""
    cmd = [sys.executable, 'tools/problem_manager.py', 'list']
    
    if difficulty:
        cmd.extend(['--difficulty', difficulty])
    if topic:
        cmd.extend(['--topic', topic])
    if solved is not None:
        cmd.append('--solved' if solved else '--unsolved')
    
    subprocess.run(cmd)


@cli.command()
def stats():
    """📊 Show progress statistics"""
    subprocess.run([sys.executable, 'tools/problem_manager.py', 'stats'])


@cli.command()
@click.argument('problem_id')
def show(problem_id: str):
    """👁️ Show detailed problem information"""
    subprocess.run([sys.executable, 'tools/problem_manager.py', 'show', problem_id])


@cli.command()
def setup():
    """⚙️ Run initial setup"""
    subprocess.run([sys.executable, 'setup.py'])


@cli.command()
def demo():
    """🎬 Run a quick demo"""
    click.echo("🎬 LeetCode Practice Demo")
    click.echo("="*50)
    
    click.echo("\n1. 📊 Your current progress:")
    subprocess.run([sys.executable, 'tools/problem_manager.py', 'stats'])
    
    click.echo("\n2. 📋 Available problems:")
    subprocess.run([sys.executable, 'tools/problem_manager.py', 'list'])
    
    click.echo("\n3. 🧪 Testing the example 'Two Sum' problem:")
    subprocess.run([sys.executable, 'tools/test_runner.py', 'run', 'two-sum', '--language', 'python'])
    
    click.echo("\n✨ Try these commands:")
    click.echo("  python leetcode.py hint two-sum --level subtle")
    click.echo("  python leetcode.py solve two-sum --language python")
    click.echo("  python leetcode.py explain --topic 'hash tables'")


if __name__ == '__main__':
    cli()