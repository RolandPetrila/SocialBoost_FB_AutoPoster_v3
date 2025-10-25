#!/usr/bin/env python3
"""
Context Validator - Validates project context and consistency
Ensures all components are properly configured and integrated
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Collection
import ast
import re

class ContextValidator:
    """Validates project context and configuration."""
    
    def __init__(self, root_path: Optional[Path] = None):
        self.root_path = root_path or Path.cwd()
        self.validation_results: Dict[str, Any] = {
            "timestamp": "",
            "passed": [],
            "failed": [],
            "warnings": [],
            "summary": {}
        }
        
        # Critical files that must exist
        self.critical_files = [
            "orchestrator.py",
            "PROJECT_CONTEXT.json",
            "requirements.txt",
            ".gitignore"
        ]
        
        # Critical directories
        self.critical_dirs = [
            "Automatizare_Completa",
            "Scripts",
            "Config",
            "Logs",
            "Tests",
            "Prompts"
        ]
    
    def validate_all(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validation checks."""
        from datetime import datetime
        self.validation_results["timestamp"] = datetime.now().isoformat()
        
        print("Running context validation...")
        
        # Run validation checks
        checks = [
            ("Structure", self.validate_structure),
            ("Critical Files", self.validate_critical_files),
            ("Python Syntax", self.validate_python_syntax),
            ("Dependencies", self.validate_dependencies),
            ("Configuration", self.validate_configuration),
            ("Git Setup", self.validate_git),
            ("Documentation", self.validate_documentation),
            ("Context Files", self.validate_context_files)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"  Checking {check_name}...", end=" ")
            try:
                passed, message = check_func()
                
                if passed:
                    self.validation_results["passed"].append({
                        "check": check_name,
                        "message": message
                    })
                    print("✓")
                else:
                    self.validation_results["failed"].append({
                        "check": check_name,
                        "message": message
                    })
                    all_passed = False
                    print("✗")
                    
            except Exception as e:
                self.validation_results["failed"].append({
                    "check": check_name,
                    "message": f"Exception: {str(e)}"
                })
                all_passed = False
                print("✗ (Exception)")
        
        # Generate summary
        self.validation_results["summary"] = {
            "total_checks": len(checks),
            "passed": len(self.validation_results["passed"]),
            "failed": len(self.validation_results["failed"]),
            "warnings": len(self.validation_results["warnings"]),
            "status": "PASSED" if all_passed else "FAILED"
        }
        
        return all_passed, self.validation_results
    
    def validate_structure(self) -> Tuple[bool, str]:
        """Validate project directory structure."""
        missing_dirs = []
        
        for dir_name in self.critical_dirs:
            dir_path = self.root_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            return False, f"Missing directories: {', '.join(missing_dirs)}"
        
        return True, "All critical directories present"
    
    def validate_critical_files(self) -> Tuple[bool, str]:
        """Validate critical files exist."""
        missing_files = []
        
        for file_name in self.critical_files:
            file_path = self.root_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        
        return True, "All critical files present"
    
    def validate_python_syntax(self) -> Tuple[bool, str]:
        """Validate Python file syntax."""
        errors = []
        files_checked = 0
        
        # Check all Python files in key directories
        for dir_name in ["Scripts", "Automatizare_Completa", "Tests", "GUI"]:
            dir_path = self.root_path / dir_name
            if not dir_path.exists():
                continue
            
            for py_file in dir_path.rglob("*.py"):
                files_checked += 1
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse the file
                    ast.parse(content)
                    
                except SyntaxError as e:
                    rel_path = py_file.relative_to(self.root_path)
                    errors.append(f"{rel_path}: {e.msg} (line {e.lineno})")
                except Exception as e:
                    rel_path = py_file.relative_to(self.root_path)
                    errors.append(f"{rel_path}: {str(e)}")
        
        # Also check root Python files
        for py_file in self.root_path.glob("*.py"):
            files_checked += 1
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"{py_file.name}: {e.msg} (line {e.lineno})")
            except Exception as e:
                errors.append(f"{py_file.name}: {str(e)}")
        
        if errors:
            return False, f"Syntax errors in {len(errors)} file(s): {'; '.join(errors[:3])}"
        
        return True, f"All {files_checked} Python files have valid syntax"
    
    def validate_dependencies(self) -> Tuple[bool, str]:
        """Validate dependencies configuration."""
        req_file = self.root_path / "requirements.txt"
        
        if not req_file.exists():
            return False, "requirements.txt not found"
        
        with open(req_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Check for essential dependencies
        essential = ["python-dotenv", "requests"]
        found = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                for dep in essential:
                    if dep in line.lower():
                        found.append(dep)
        
        missing = set(essential) - set(found)
        if missing:
            self.validation_results["warnings"].append({
                "check": "Dependencies",
                "message": f"Essential dependencies might be missing: {', '.join(missing)}"
            })
        
        dep_count = len([l for l in lines if l.strip() and not l.startswith('#')])
        return True, f"Found {dep_count} dependencies in requirements.txt"
    
    def validate_configuration(self) -> Tuple[bool, str]:
        """Validate configuration files."""
        issues = []
        
        # Check .env.example
        env_example = self.root_path / ".env.example"
        if not env_example.exists():
            issues.append(".env.example not found")
        else:
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required keys
            required_keys = [
                "FACEBOOK_APP_ID",
                "FACEBOOK_PAGE_TOKEN",
                "OPENAI_API_KEY"
            ]
            
            for key in required_keys:
                if key not in content:
                    self.validation_results["warnings"].append({
                        "check": "Configuration",
                        "message": f"Key '{key}' not found in .env.example"
                    })
        
        # Check PROJECT_CONTEXT.json
        context_file = self.root_path / "PROJECT_CONTEXT.json"
        if context_file.exists():
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                
                # Validate required fields
                required_fields = ["project_name", "root_path", "python_version"]
                for field in required_fields:
                    if field not in context:
                        issues.append(f"PROJECT_CONTEXT.json missing field: {field}")
                        
            except json.JSONDecodeError as e:
                issues.append(f"PROJECT_CONTEXT.json is invalid JSON: {e}")
        
        if issues:
            return False, f"Configuration issues: {'; '.join(issues)}"
        
        return True, "Configuration files valid"
    
    def validate_git(self) -> Tuple[bool, str]:
        """Validate Git setup."""
        git_dir = self.root_path / ".git"
        
        if not git_dir.exists():
            return False, "Git not initialized"
        
        # Check for .gitignore
        gitignore = self.root_path / ".gitignore"
        if not gitignore.exists():
            self.validation_results["warnings"].append({
                "check": "Git",
                "message": ".gitignore file missing"
            })
        else:
            with open(gitignore, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for critical entries
            critical_entries = [".env", "__pycache__", "*.log"]
            for entry in critical_entries:
                if entry not in content:
                    self.validation_results["warnings"].append({
                        "check": "Git",
                        "message": f"'{entry}' not in .gitignore"
                    })
        
        return True, "Git initialized"
    
    def validate_documentation(self) -> Tuple[bool, str]:
        """Validate documentation files."""
        doc_files = ["README.md", "PROJECT_DNA.md", "PROJECT_TODO.md"]
        missing = []
        
        for doc_file in doc_files:
            if not (self.root_path / doc_file).exists():
                missing.append(doc_file)
        
        if missing:
            self.validation_results["warnings"].append({
                "check": "Documentation",
                "message": f"Missing docs: {', '.join(missing)}"
            })
        
        # Check CHANGELOG.md
        changelog = self.root_path / "Docs" / "CHANGELOG.md"
        if not changelog.exists():
            self.validation_results["warnings"].append({
                "check": "Documentation",
                "message": "Docs/CHANGELOG.md not found"
            })
        
        return True, f"Documentation files checked ({len(doc_files) - len(missing)}/{len(doc_files)} present)"
    
    def validate_context_files(self) -> Tuple[bool, str]:
        """Validate context management files."""
        issues = []
        
        # Check context builder
        context_builder = self.root_path / "Scripts" / "context_builder.py"
        if not context_builder.exists():
            issues.append("Scripts/context_builder.py not found")
        
        # Check prompt generator
        prompt_generator = self.root_path / "Scripts" / "prompt_generator.py"
        if not prompt_generator.exists():
            issues.append("Scripts/prompt_generator.py not found")
        
        # Check templates directory
        templates_dir = self.root_path / "Prompts" / "Templates"
        if not templates_dir.exists():
            issues.append("Prompts/Templates directory not found")
        else:
            # Check for at least one template
            templates = list(templates_dir.glob("*.md"))
            if not templates:
                self.validation_results["warnings"].append({
                    "check": "Context Files",
                    "message": "No templates found in Prompts/Templates"
                })
        
        if issues:
            return False, f"Context system issues: {'; '.join(issues)}"
        
        return True, "Context management system present"
    
    def export_report(self, output_path: Optional[Path] = None) -> Path:
        """Export validation report."""
        if not output_path:
            output_path = Path("validation_report.md")
        
        lines = []
        lines.append("# Context Validation Report")
        lines.append(f"\nGenerated: {self.validation_results['timestamp']}\n")
        
        # Summary
        summary = self.validation_results["summary"]
        lines.append("## Summary")
        lines.append(f"- **Status**: {summary['status']}")
        lines.append(f"- **Total Checks**: {summary['total_checks']}")
        lines.append(f"- **Passed**: {summary['passed']}")
        lines.append(f"- **Failed**: {summary['failed']}")
        lines.append(f"- **Warnings**: {summary['warnings']}")
        lines.append("")
        
        # Passed checks
        if self.validation_results["passed"]:
            lines.append("## Passed Checks ✓")
            for check in self.validation_results["passed"]:
                lines.append(f"- **{check['check']}**: {check['message']}")
            lines.append("")
        
        # Failed checks
        if self.validation_results["failed"]:
            lines.append("## Failed Checks ✗")
            for check in self.validation_results["failed"]:
                lines.append(f"- **{check['check']}**: {check['message']}")
            lines.append("")
        
        # Warnings
        if self.validation_results["warnings"]:
            lines.append("## Warnings ⚠")
            for warning in self.validation_results["warnings"]:
                lines.append(f"- **{warning['check']}**: {warning['message']}")
            lines.append("")
        
        # Recommendations
        lines.append("## Recommendations")
        if self.validation_results["failed"]:
            lines.append("1. Fix all failed checks before proceeding")
            lines.append("2. Run validation again after fixes")
        if self.validation_results["warnings"]:
            lines.append("3. Review and address warnings")
        if summary["status"] == "PASSED":
            lines.append("✅ All critical checks passed. System is ready.")
        lines.append("")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        # Also save to Update_AI if it exists
        update_dir = Path("Update_AI")
        if update_dir.exists():
            update_path = update_dir / "VALIDATION_REPORT.md"
            with open(update_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        
        return output_path

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate project context and configuration")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for validation report"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output"
    )
    
    args = parser.parse_args()
    
    validator = ContextValidator()
    passed, results = validator.validate_all()
    
    if not args.quiet:
        print("\n" + "="*50)
        print(f"Validation {'PASSED' if passed else 'FAILED'}")
        print("="*50)
        
        if results["failed"]:
            print("\nFailed Checks:")
            for check in results["failed"]:
                print(f"  ✗ {check['check']}: {check['message']}")
        
        if results["warnings"]:
            print("\nWarnings:")
            for warning in results["warnings"]:
                print(f"  ⚠ {warning['check']}: {warning['message']}")
    
    # Export report
    if args.json:
        output_path = args.output or Path("validation_report.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nJSON report saved to: {output_path}")
    else:
        output_path = validator.export_report(args.output)
        print(f"\nValidation report saved to: {output_path}")
    
    # Exit with appropriate code
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
