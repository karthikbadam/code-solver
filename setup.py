#!/usr/bin/env python3
"""
Setup script for LeetCode Practice Repository
Automates initial configuration and dependency installation.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Tuple, Dict, Any


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_step(message: str):
    """Print a setup step with styling"""
    print(f"{Colors.BLUE}{Colors.BOLD}🔧 {message}{Colors.END}")


def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def run_command(command: List[str], description: str, check: bool = True) -> Tuple[bool, str]:
    """Run a shell command and return success status and output"""
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=check,
            timeout=120
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except subprocess.TimeoutExpired:
        return False, f"Command timed out: {' '.join(command)}"
    except Exception as e:
        return False, str(e)


def check_python_version() -> bool:
    """Check if Python version is 3.8+"""
    print_step("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ✓")
    return True


def check_node_version() -> bool:
    """Check if Node.js is installed and version 16+"""
    print_step("Checking Node.js version...")
    
    success, output = run_command(['node', '--version'], "Check Node.js version", check=False)
    
    if not success:
        print_warning("Node.js not found. Please install Node.js 16+ from https://nodejs.org")
        return False
    
    try:
        version = output.strip().replace('v', '')
        major_version = int(version.split('.')[0])
        
        if major_version < 16:
            print_error(f"Node.js 16+ required, found {version}")
            return False
        
        print_success(f"Node.js {version} ✓")
        return True
        
    except (ValueError, IndexError):
        print_warning(f"Could not parse Node.js version: {output}")
        return False


def install_python_dependencies() -> bool:
    """Install Python dependencies using uv or pip"""
    print_step("Installing Python dependencies...")
    
    # Check if uv is available
    uv_available, _ = run_command(['uv', '--version'], "Check uv availability", check=False)
    
    if uv_available:
        print_step("Using uv for Python package management...")
        
        # Create virtual environment if it doesn't exist
        if not Path(".venv").exists():
            success, output = run_command(['uv', 'venv'], "Create virtual environment")
            if not success:
                print_error(f"Failed to create virtual environment: {output}")
                return False
        
        # Install dependencies with uv (from requirements.txt to avoid build issues)
        success, output = run_command(['uv', 'pip', 'install', '-r', 'requirements.txt'], "Install Python packages with uv")
        if success:
            # Install dev dependencies
            success, output = run_command(['uv', 'pip', 'install', 'pytest>=7.4.0', 'pytest-cov>=4.1.0', 'black>=23.7.0', 'flake8>=6.0.0', 'mypy>=1.5.0'], "Install dev dependencies")
        
        if success:
            print_success("Python dependencies installed with uv ✓")
            print_warning("💡 To activate: source .venv/bin/activate")
            return True
        else:
            print_error(f"Failed to install Python dependencies with uv: {output}")
            return False
    else:
        # Fallback to pip with requirements.txt
        print_step("uv not available, using pip...")
        
        if not Path("requirements.txt").exists():
            print_error("requirements.txt not found")
            return False
        
        success, output = run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                                    "Install Python packages")
        
        if success:
            print_success("Python dependencies installed with pip ✓")
            return True
        else:
            print_error(f"Failed to install Python dependencies: {output}")
            return False


def install_node_dependencies() -> bool:
    """Install Node.js dependencies with nvm support"""
    print_step("Installing Node.js dependencies...")
    
    if not Path("package.json").exists():
        print_error("package.json not found")
        return False
    
    # Check if .nvmrc exists and nvm is available
    nvmrc_exists = Path(".nvmrc").exists()
    nvm_available = Path.home().joinpath(".nvm/nvm.sh").exists()
    
    if nvmrc_exists and nvm_available:
        print_step("Using Node.js version from .nvmrc...")
        # Use bash to source nvm and install/use correct version
        bash_cmd = """
        source ~/.nvm/nvm.sh && 
        nvm install && 
        nvm use && 
        npm install
        """
        success, output = run_command(['bash', '-c', bash_cmd], "Install with nvm")
        
        if success:
            print_success("Node.js dependencies installed with nvm ✓")
            with open(".nvmrc", "r") as f:
                version = f.read().strip()
            print_warning(f"💡 To use Node.js v{version}: nvm use")
            return True
        else:
            print_warning("nvm setup failed, falling back to system Node.js...")
    
    # Fallback to regular npm install
    success, output = run_command(['npm', 'install'], "Install Node.js packages")
    
    if success:
        print_success("Node.js dependencies installed ✓")
        return True
    else:
        print_error(f"Failed to install Node.js dependencies: {output}")
        return False


def setup_environment_file() -> bool:
    """Create .env file from template"""
    print_step("Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    # Create a basic .env file
    env_content = """# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions

# Claude Model Configuration  
CLAUDE_MODEL=anthropic/claude-3.5-sonnet

# General Settings
DEBUG=false
LOG_LEVEL=INFO

# Progress Tracking
PROGRESS_FILE=progress/stats.json
"""
    
    if env_file.exists():
        print_warning(".env file already exists - skipping")
        return True
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print_success(".env file created ✓")
        print_warning("⚠️  Remember to add your OpenRouter API key to the .env file!")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False


def make_scripts_executable() -> bool:
    """Make CLI scripts executable on Unix systems"""
    if os.name == 'nt':  # Windows
        return True
    
    print_step("Making CLI scripts executable...")
    
    scripts = [
        'tools/problem_manager.py',
        'tools/claude_helper.py', 
        'tools/test_runner.py'
    ]
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            try:
                os.chmod(script_path, 0o755)
            except Exception as e:
                print_warning(f"Could not make {script} executable: {e}")
                return False
    
    print_success("CLI scripts made executable ✓")
    return True


def verify_installation() -> bool:
    """Verify that the installation works"""
    print_step("Verifying installation...")
    
    # Test Python CLI
    success, output = run_command([sys.executable, 'tools/problem_manager.py', '--help'], 
                                "Test problem manager", check=False)
    if not success:
        print_error("Problem manager CLI test failed")
        return False
    
    # Test TypeScript compilation
    success, output = run_command(['npx', 'tsc', '--noEmit'], 
                                "Test TypeScript compilation", check=False)
    if not success:
        print_warning("TypeScript compilation test failed (non-critical)")
    
    print_success("Installation verification complete ✓")
    return True


def display_next_steps():
    """Display next steps for the user"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Setup Complete!{Colors.END}\n")
    
    print(f"{Colors.BOLD}Environment Management:{Colors.END}")
    print("🐍 Python Virtual Environment:")
    if Path(".venv").exists():
        print("   ✅ Virtual environment created")
        print("   📝 Activate: source .venv/bin/activate")
        print("   📝 Deactivate: deactivate")
    else:
        print("   📝 Setup manually: ./scripts/setup-python-env.sh")
    
    print("\n📦 Node.js Version Management:")
    if Path(".nvmrc").exists():
        with open(".nvmrc", "r") as f:
            version = f.read().strip()
        print(f"   ✅ Node.js v{version} configured")
        print("   📝 Use version: nvm use")
        print("   📝 Install nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash")
    
    print(f"\n{Colors.BOLD}Quick Start:{Colors.END}")
    print("1. Activate environments: source ./activate-env.sh")
    print("2. Add your OpenRouter API key to the .env file")
    print("3. Test installation: python leetcode.py demo")
    
    print(f"\n{Colors.BOLD}Alternative Setup:{Colors.END}")
    print("🔧 For advanced setup with uv and nvm:")
    print("   ./scripts/setup-environments.sh")
    
    print(f"\n{Colors.BOLD}Basic Usage:{Colors.END}")
    print("• Add problem: python leetcode.py add --title \"Problem\" --difficulty easy --topics \"array\"")
    print("• Get solution: python leetcode.py solve two-sum --language python")
    print("• Run tests: python leetcode.py test two-sum")
    print("• View progress: python leetcode.py stats")
    
    print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
    print("📖 Setup Guide: docs/setup_guide.md")
    print("📖 Usage Guide: docs/usage_guide.md")
    print("📖 Main README: README.md")
    
    print(f"\n{Colors.BOLD}Example Problem:{Colors.END}")
    print("📝 A 'Two Sum' problem has been included as an example")
    print("   Try: python leetcode.py test two-sum")


def main():
    """Main setup function"""
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("="*60)
    print("  LeetCode Practice Repository Setup")
    print("="*60)
    print(f"{Colors.END}\n")
    
    # Track setup success
    all_success = True
    
    # Check prerequisites
    if not check_python_version():
        all_success = False
    
    node_available = check_node_version()
    if not node_available:
        print_warning("Node.js not available - TypeScript features will be limited")
    
    # Install dependencies
    if not install_python_dependencies():
        all_success = False
    
    if node_available and not install_node_dependencies():
        print_warning("Node.js dependency installation failed - TypeScript features may not work")
    
    # Setup configuration
    if not setup_environment_file():
        all_success = False
    
    if not make_scripts_executable():
        print_warning("Could not make scripts executable - you may need to use 'python script.py' instead of './script.py'")
    
    # Verify installation
    if not verify_installation():
        all_success = False
    
    # Display results
    if all_success:
        display_next_steps()
    else:
        print_error("\nSetup completed with some issues. Please check the errors above.")
        print("You may still be able to use the repository with limited functionality.")
    
    return 0 if all_success else 1


if __name__ == "__main__":
    exit(main())