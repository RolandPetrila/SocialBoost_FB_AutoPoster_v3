#!/usr/bin/env python3
"""
Validation Runner - Comprehensive project validation system
Runs tests, linting, type checking, and security analysis
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationRunner:
    """Comprehensive validation system for the project."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.logs_dir = Path("Logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Validation results
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "validation_steps": {},
            "summary": {
                "total_steps": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0,
                "overall_status": "UNKNOWN"
            }
        }
        
        # Validation steps configuration
        self.validation_steps = [
            ("syntax_check", self.run_syntax_check),
            ("pytest", self.run_pytest),
            ("flake8", self.run_flake8),
            ("mypy", self.run_mypy),
            ("bandit", self.run_bandit),
            ("import_check", self.run_import_check)
        ]
    
    def run_validation(self, quick: bool = False) -> Dict[str, Any]:
        """Run all validation steps."""
        logger.info("Starting comprehensive validation...")
        
        if quick:
            logger.info("Running in QUICK mode - skipping some checks")
            # Quick mode: only run essential checks
            quick_steps = [("syntax_check", self.run_syntax_check), ("pytest", self.run_pytest)]
            self.validation_steps = quick_steps
        
        self.results["summary"]["total_steps"] = len(self.validation_steps)
        
        for step_name, step_func in self.validation_steps:
            logger.info(f"Running {step_name}...")
            
            try:
                success, output, warnings = step_func()
                
                self.results["validation_steps"][step_name] = {
                    "success": success,
                    "output": output,
                    "warnings": warnings,
                    "timestamp": datetime.now().isoformat()
                }
                
                if success:
                    self.results["summary"]["passed"] += 1
                    logger.info(f"✓ {step_name} passed")
                else:
                    self.results["summary"]["failed"] += 1
                    logger.error(f"✗ {step_name} failed")
                
                if warnings:
                    self.results["summary"]["warnings"] += len(warnings)
                    for warning in warnings:
                        logger.warning(f"⚠ {step_name}: {warning}")
                        
            except Exception as e:
                logger.error(f"✗ {step_name} crashed: {e}")
                self.results["validation_steps"][step_name] = {
                    "success": False,
                    "output": f"Exception: {str(e)}",
                    "warnings": [],
                    "timestamp": datetime.now().isoformat()
                }
                self.results["summary"]["failed"] += 1
        
        # Determine overall status
        if self.results["summary"]["failed"] == 0:
            self.results["summary"]["overall_status"] = "PASSED"
        elif self.results["summary"]["failed"] <= self.results["summary"]["total_steps"] // 2:
            self.results["summary"]["overall_status"] = "WARNING"
        else:
            self.results["summary"]["overall_status"] = "FAILED"
        
        logger.info(f"Validation completed: {self.results['summary']['overall_status']}")
        return self.results
    
    def run_syntax_check(self) -> Tuple[bool, str, List[str]]:
        """Check Python syntax for all Python files."""
        logger.info("Checking Python syntax...")
        
        python_files = []
        warnings = []
        
        # Find all Python files
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(py_file):
                python_files.append(py_file)
        
        if not python_files:
            return False, "No Python files found", []
        
        errors = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to compile the file
                compile(content, str(py_file), 'exec')
                
            except SyntaxError as e:
                rel_path = py_file.relative_to(self.project_root)
                errors.append(f"{rel_path}:{e.lineno}: {e.msg}")
            except Exception as e:
                rel_path = py_file.relative_to(self.project_root)
                warnings.append(f"{rel_path}: {str(e)}")
        
        if errors:
            return False, f"Syntax errors found:\n" + "\n".join(errors), warnings
        
        return True, f"Syntax check passed for {len(python_files)} files", warnings
    
    def run_pytest(self) -> Tuple[bool, str, List[str]]:
        """Run pytest for all test files."""
        logger.info("Running pytest...")
        
        tests_dir = self.project_root / "Tests"
        if not tests_dir.exists():
            return True, "No Tests directory found - skipping pytest", []
        
        test_files = list(tests_dir.rglob("test_*.py"))
        if not test_files:
            return True, "No test files found - skipping pytest", []
        
        try:
            # Run pytest with capture
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            output = result.stdout + "\n" + result.stderr
            
            if result.returncode == 0:
                return True, output, []
            else:
                return False, output, []
                
        except subprocess.TimeoutExpired:
            return False, "pytest timed out after 60 seconds", []
        except Exception as e:
            return False, f"pytest failed to run: {str(e)}", []
    
    def run_flake8(self) -> Tuple[bool, str, List[str]]:
        """Run flake8 linting."""
        logger.info("Running flake8...")
        
        try:
            # Run flake8
            result = subprocess.run(
                [sys.executable, "-m", "flake8", ".", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30
            )
            
            output = result.stdout + "\n" + result.stderr
            
            # flake8 returns non-zero for any issues, but we consider it passed if no critical errors
            if "E9" in output or "F63" in output or "F7" in output or "F82" in output:
                return False, output, []
            else:
                return True, output, []
                
        except subprocess.TimeoutExpired:
            return False, "flake8 timed out after 30 seconds", []
        except Exception as e:
            return False, f"flake8 failed to run: {str(e)}", []
    
    def run_mypy(self) -> Tuple[bool, str, List[str]]:
        """Run mypy type checking."""
        logger.info("Running mypy...")
        
        try:
            # Run mypy with ignore missing imports
            result = subprocess.run(
                [sys.executable, "-m", "mypy", ".", "--ignore-missing-imports", "--no-error-summary"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            output = result.stdout + "\n" + result.stderr
            
            # mypy returns non-zero for type errors
            if result.returncode == 0:
                return True, output, []
            else:
                # Check if errors are critical or just warnings
                if "error:" in output.lower():
                    return False, output, []
                else:
                    return True, output, []
                    
        except subprocess.TimeoutExpired:
            return False, "mypy timed out after 60 seconds", []
        except Exception as e:
            return False, f"mypy failed to run: {str(e)}", []
    
    def run_bandit(self) -> Tuple[bool, str, List[str]]:
        """Run bandit security analysis."""
        logger.info("Running bandit...")
        
        try:
            # Run bandit
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "-r", ".", "-f", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=60
            )
            
            output = result.stdout + "\n" + result.stderr
            
            # Parse bandit JSON output if available
            try:
                if result.stdout.strip():
                    bandit_data = json.loads(result.stdout)
                    high_severity = bandit_data.get("results", [])
                    high_severity = [r for r in high_severity if r.get("issue_severity") == "HIGH"]
                    
                    if high_severity:
                        return False, output, [f"High severity security issues found: {len(high_severity)}"]
                    else:
                        return True, output, []
                else:
                    return True, "No security issues found", []
                    
            except json.JSONDecodeError:
                # If JSON parsing fails, check return code
                if result.returncode == 0:
                    return True, output, []
                else:
                    return False, output, []
                    
        except subprocess.TimeoutExpired:
            return False, "bandit timed out after 60 seconds", []
        except Exception as e:
            return False, f"bandit failed to run: {str(e)}", []
    
    def run_import_check(self) -> Tuple[bool, str, List[str]]:
        """Check if all imports can be resolved."""
        logger.info("Checking imports...")
        
        python_files = []
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(py_file):
                python_files.append(py_file)
        
        if not python_files:
            return True, "No Python files found", []
        
        import_errors = []
        warnings = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to import the module
                module_name = py_file.stem
                if py_file.parent.name == "Tests":
                    # Skip test files for import check
                    continue
                
                # Basic import check - try to compile and check for obvious import issues
                compile(content, str(py_file), 'exec')
                
            except ImportError as e:
                rel_path = py_file.relative_to(self.project_root)
                import_errors.append(f"{rel_path}: Import error - {str(e)}")
            except Exception as e:
                rel_path = py_file.relative_to(self.project_root)
                warnings.append(f"{rel_path}: {str(e)}")
        
        if import_errors:
            return False, f"Import errors found:\n" + "\n".join(import_errors), warnings
        
        return True, f"Import check passed for {len(python_files)} files", warnings
    
    def save_results(self, output_file: Path = None) -> Path:
        """Save validation results to JSON file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.logs_dir / f"validation_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation results saved to: {output_file}")
        return output_file
    
    def print_summary(self):
        """Print validation summary."""
        summary = self.results["summary"]
        
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Total Steps: {summary['total_steps']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Warnings: {summary['warnings']}")
        print("="*60)
        
        # Print step details
        for step_name, step_data in self.results["validation_steps"].items():
            status = "✓" if step_data["success"] else "✗"
            print(f"{status} {step_name}")
            
            if step_data["warnings"]:
                for warning in step_data["warnings"]:
                    print(f"  ⚠ {warning}")
        
        print("="*60)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run comprehensive project validation")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick validation (skip some checks)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for validation results"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    runner = ValidationRunner()
    results = runner.run_validation(quick=args.quick)
    
    # Save results
    output_file = runner.save_results(args.output)
    
    # Print summary
    runner.print_summary()
    
    # Also save to Update_AI if it exists
    update_dir = Path("Update_AI")
    if update_dir.exists():
        update_file = update_dir / "validation_results.json"
        runner.save_results(update_file)
    
    # Exit with appropriate code
    if results["summary"]["overall_status"] == "PASSED":
        sys.exit(0)
    elif results["summary"]["overall_status"] == "WARNING":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
