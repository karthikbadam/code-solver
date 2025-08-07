#!/usr/bin/env python3
"""
Test Runner - Run tests for LeetCode solutions
Supports both Python and TypeScript/React solutions with automatic test discovery.
"""

import os
import json
import subprocess
import sys
import click
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import importlib.util
import tempfile

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))


class TestResult:
    """Represents the result of running tests"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = 0
        self.total = 0
        self.details = []
        self.execution_time = 0.0
    
    def add_result(self, name: str, status: str, message: str = "", time: float = 0.0):
        """Add a test result"""
        self.details.append({
            'name': name,
            'status': status,
            'message': message,
            'time': time
        })
        
        if status == 'passed':
            self.passed += 1
        elif status == 'failed':
            self.failed += 1
        elif status == 'error':
            self.errors += 1
        
        self.total += 1
    
    @property
    def success_rate(self) -> float:
        return (self.passed / self.total * 100) if self.total > 0 else 0.0


class TestRunner:
    """Runs tests for LeetCode solutions"""
    
    def __init__(self):
        self.solutions_dir = Path("solutions")
        self.problems_dir = Path("problems")
    
    def run_python_tests(self, problem_id: str) -> TestResult:
        """Run Python tests for a specific problem"""
        
        solution_file = self.solutions_dir / "python" / f"{problem_id}.py"
        
        if not solution_file.exists():
            result = TestResult()
            result.add_result(problem_id, 'error', f"Solution file not found: {solution_file}")
            return result
        
        # Try to run pytest first
        try:
            cmd = [sys.executable, "-m", "pytest", str(solution_file), "-v", "--tb=short"]
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            result = self._parse_pytest_output(process.stdout, process.stderr, process.returncode)
            
        except subprocess.TimeoutExpired:
            result = TestResult()
            result.add_result(problem_id, 'error', "Test execution timed out")
            
        except Exception as e:
            # Fallback: try to run the file directly
            result = self._run_python_file_directly(solution_file)
        
        return result
    
    def run_typescript_tests(self, problem_id: str) -> TestResult:
        """Run TypeScript tests for a specific problem"""
        
        solution_file = self.solutions_dir / "react-ts" / f"{problem_id}.ts"
        
        if not solution_file.exists():
            result = TestResult()
            result.add_result(problem_id, 'error', f"Solution file not found: {solution_file}")
            return result
        
        try:
            # Try to run with jest/node
            if self._has_jest():
                result = self._run_jest_tests(solution_file)
            else:
                result = self._run_typescript_file_directly(solution_file)
                
        except Exception as e:
            result = TestResult()
            result.add_result(problem_id, 'error', f"Test execution failed: {str(e)}")
        
        return result
    
    def run_all_tests(self, language: Optional[str] = None) -> Dict[str, TestResult]:
        """Run tests for all solutions"""
        
        results = {}
        
        languages = [language] if language else ['python', 'typescript']
        
        for lang in languages:
            if lang == 'python':
                solution_dir = self.solutions_dir / "python"
                if solution_dir.exists():
                    for solution_file in solution_dir.glob("*.py"):
                        problem_id = solution_file.stem
                        results[f"{problem_id} (Python)"] = self.run_python_tests(problem_id)
            
            elif lang in ['typescript', 'react-ts']:
                solution_dir = self.solutions_dir / "react-ts"
                if solution_dir.exists():
                    for solution_file in solution_dir.glob("*.ts"):
                        problem_id = solution_file.stem
                        results[f"{problem_id} (TypeScript)"] = self.run_typescript_tests(problem_id)
        
        return results
    
    def validate_solution(self, problem_id: str, language: str) -> Tuple[bool, List[str]]:
        """Validate that a solution is properly implemented"""
        
        issues = []
        
        if language == 'python':
            solution_file = self.solutions_dir / "python" / f"{problem_id}.py"
        else:
            solution_file = self.solutions_dir / "react-ts" / f"{problem_id}.ts"
        
        if not solution_file.exists():
            return False, [f"Solution file does not exist: {solution_file}"]
        
        try:
            with open(solution_file, 'r') as f:
                content = f.read()
            
            # Check for template placeholders
            placeholders = ['{problem_title}', '{difficulty}', '{topics}', 'TODO:', 'pass', 'null']
            for placeholder in placeholders:
                if placeholder in content:
                    issues.append(f"Template placeholder found: {placeholder}")
            
            # Check for basic implementation
            if language == 'python':
                if 'def solve(' not in content and 'def ' not in content:
                    issues.append("No solution method found")
            else:
                if 'solve(' not in content:
                    issues.append("No solve method found")
            
            # Check for test cases
            if language == 'python':
                if 'def test_' not in content and 'class Test' not in content:
                    issues.append("No test cases found")
            else:
                if 'testCases' not in content:
                    issues.append("No test cases found")
        
        except Exception as e:
            issues.append(f"Error reading solution file: {str(e)}")
        
        return len(issues) == 0, issues
    
    def _parse_pytest_output(self, stdout: str, stderr: str, returncode: int) -> TestResult:
        """Parse pytest output to extract test results"""
        
        result = TestResult()
        
        lines = stdout.split('\n') + stderr.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for test results
            if '::' in line and ('PASSED' in line or 'FAILED' in line or 'ERROR' in line):
                parts = line.split()
                test_name = parts[0] if parts else "unknown"
                
                if 'PASSED' in line:
                    result.add_result(test_name, 'passed')
                elif 'FAILED' in line:
                    result.add_result(test_name, 'failed', line)
                elif 'ERROR' in line:
                    result.add_result(test_name, 'error', line)
        
        # If no specific tests found, add general result
        if result.total == 0:
            if returncode == 0:
                result.add_result("pytest", 'passed', "All tests passed")
            else:
                result.add_result("pytest", 'failed', stderr or stdout)
        
        return result
    
    def _run_python_file_directly(self, solution_file: Path) -> TestResult:
        """Run a Python file directly and capture results"""
        
        result = TestResult()
        
        try:
            # Try to import and run the module
            spec = importlib.util.spec_from_file_location("solution", solution_file)
            module = importlib.util.module_from_spec(spec)
            
            # Capture stdout
            import io
            import contextlib
            
            stdout_capture = io.StringIO()
            
            with contextlib.redirect_stdout(stdout_capture):
                spec.loader.exec_module(module)
            
            output = stdout_capture.getvalue()
            result.add_result(solution_file.stem, 'passed', f"Executed successfully: {output}")
            
        except Exception as e:
            result.add_result(solution_file.stem, 'error', str(e))
        
        return result
    
    def _run_typescript_file_directly(self, solution_file: Path) -> TestResult:
        """Run a TypeScript file directly using ts-node"""
        
        result = TestResult()
        
        try:
            # Check if ts-node is available
            subprocess.run(['npx', 'ts-node', '--version'], 
                         capture_output=True, check=True, timeout=5)
            
            # Run the TypeScript file
            cmd = ['npx', 'ts-node', str(solution_file)]
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if process.returncode == 0:
                result.add_result(solution_file.stem, 'passed', process.stdout)
            else:
                result.add_result(solution_file.stem, 'failed', process.stderr)
                
        except subprocess.CalledProcessError:
            result.add_result(solution_file.stem, 'error', "ts-node not available")
        except subprocess.TimeoutExpired:
            result.add_result(solution_file.stem, 'error', "Execution timed out")
        except Exception as e:
            result.add_result(solution_file.stem, 'error', str(e))
        
        return result
    
    def _run_jest_tests(self, solution_file: Path) -> TestResult:
        """Run tests using Jest"""
        
        result = TestResult()
        
        try:
            cmd = ['npx', 'jest', str(solution_file), '--verbose']
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse Jest output (simplified)
            if process.returncode == 0:
                result.add_result(solution_file.stem, 'passed', "Jest tests passed")
            else:
                result.add_result(solution_file.stem, 'failed', process.stderr)
                
        except Exception as e:
            result.add_result(solution_file.stem, 'error', str(e))
        
        return result
    
    def _has_jest(self) -> bool:
        """Check if Jest is available"""
        try:
            subprocess.run(['npx', 'jest', '--version'], 
                         capture_output=True, check=True, timeout=5)
            return True
        except:
            return False


@click.group()
def cli():
    """Test Runner - Run tests for LeetCode solutions"""
    pass


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l', 
              type=click.Choice(['python', 'typescript', 'both']),
              default='both',
              help='Language to test')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def run(problem_id: str, language: str, verbose: bool):
    """Run tests for a specific problem"""
    
    runner = TestRunner()
    
    if language in ['python', 'both']:
        click.echo(f"🐍 Running Python tests for '{problem_id}'...")
        result = runner.run_python_tests(problem_id)
        _display_result(f"{problem_id} (Python)", result, verbose)
    
    if language in ['typescript', 'both']:
        click.echo(f"📘 Running TypeScript tests for '{problem_id}'...")
        result = runner.run_typescript_tests(problem_id)
        _display_result(f"{problem_id} (TypeScript)", result, verbose)


@cli.command()
@click.option('--language', '-l',
              type=click.Choice(['python', 'typescript', 'both']),
              default='both',
              help='Language to test')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def all(language: str, verbose: bool):
    """Run tests for all solutions"""
    
    runner = TestRunner()
    
    click.echo(f"🧪 Running all tests...")
    
    lang_param = None if language == 'both' else language
    results = runner.run_all_tests(lang_param)
    
    if not results:
        click.echo("No solution files found.")
        return
    
    # Display summary
    total_passed = sum(r.passed for r in results.values())
    total_failed = sum(r.failed for r in results.values())
    total_errors = sum(r.errors for r in results.values())
    total_tests = sum(r.total for r in results.values())
    
    click.echo("\n" + "="*60)
    click.echo("📊 TEST SUMMARY")
    click.echo("="*60)
    
    for name, result in results.items():
        status_icon = "✅" if result.failed == 0 and result.errors == 0 else "❌"
        click.echo(f"{status_icon} {name}: {result.passed}/{result.total} passed")
        
        if verbose and result.details:
            for detail in result.details:
                status_icon = {"passed": "✅", "failed": "❌", "error": "💥"}[detail['status']]
                click.echo(f"   {status_icon} {detail['name']}")
                if detail['message'] and detail['status'] != 'passed':
                    click.echo(f"      {detail['message']}")
    
    click.echo(f"\nOverall: {total_passed}/{total_tests} tests passed")
    if total_failed > 0:
        click.echo(f"Failed: {total_failed}")
    if total_errors > 0:
        click.echo(f"Errors: {total_errors}")


@cli.command()
@click.argument('problem_id')
@click.option('--language', '-l',
              type=click.Choice(['python', 'typescript']),
              default='python',
              help='Language to validate')
def validate(problem_id: str, language: str):
    """Validate that a solution is properly implemented"""
    
    runner = TestRunner()
    
    click.echo(f"🔍 Validating {language} solution for '{problem_id}'...")
    
    is_valid, issues = runner.validate_solution(problem_id, language)
    
    if is_valid:
        click.echo("✅ Solution is valid!")
    else:
        click.echo("❌ Solution has issues:")
        for issue in issues:
            click.echo(f"   • {issue}")


def _display_result(name: str, result: TestResult, verbose: bool = False):
    """Display test result in a formatted way"""
    
    if result.total == 0:
        click.echo(f"❓ {name}: No tests found")
        return
    
    if result.failed == 0 and result.errors == 0:
        click.echo(f"✅ {name}: All {result.passed} tests passed ({result.success_rate:.1f}%)")
    else:
        click.echo(f"❌ {name}: {result.passed}/{result.total} tests passed ({result.success_rate:.1f}%)")
        if result.failed > 0:
            click.echo(f"   Failed: {result.failed}")
        if result.errors > 0:
            click.echo(f"   Errors: {result.errors}")
    
    if verbose and result.details:
        for detail in result.details:
            status_icon = {"passed": "✅", "failed": "❌", "error": "💥"}[detail['status']]
            click.echo(f"   {status_icon} {detail['name']}")
            if detail['message'] and detail['status'] != 'passed':
                click.echo(f"      {detail['message']}")


if __name__ == '__main__':
    cli()