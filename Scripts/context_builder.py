#!/usr/bin/env python3
"""
Context Builder - Generates comprehensive project context for AI assistants
Analyzes project structure, code, and documentation to create context files
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import ast
import re

class ContextBuilder:
    """Builds comprehensive context from project files."""
    
    def __init__(self, root_path: Path = None):
        self.root_path = root_path or Path.cwd()
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "project_info": {},
            "structure": {},
            "modules": {},
            "dependencies": {},
            "configuration": {},
            "documentation": {},
            "tests": {},
            "current_state": {}
        }
        
        # File patterns to analyze
        self.code_extensions = [".py", ".pyw"]
        self.doc_extensions = [".md", ".txt", ".rst"]
        self.config_extensions = [".json", ".yaml", ".yml", ".toml", ".ini", ".env.example"]
        
        # Directories to focus on
        self.important_dirs = [
            "Automatizare_Completa",
            "Scripts",
            "GUI",
            "Tests",
            "Config"
        ]
        
    def build_context(self, context_type: str = "general") -> Dict[str, Any]:
        """Build context based on type."""
        print(f"Building {context_type} context...")
        
        # Load project info
        self.load_project_info()
        
        # Analyze project structure
        self.analyze_structure()
        
        # Analyze code modules
        self.analyze_modules()
        
        # Load dependencies
        self.load_dependencies()
        
        # Load configuration
        self.load_configuration()
        
        # Analyze documentation
        self.analyze_documentation()
        
        # Analyze tests
        self.analyze_tests()
        
        # Get current state
        self.get_current_state()
        
        return self.context
    
    def load_project_info(self):
        """Load basic project information."""
        # Load from PROJECT_CONTEXT.json
        context_file = self.root_path / "PROJECT_CONTEXT.json"
        if context_file.exists():
            with open(context_file, 'r', encoding='utf-8') as f:
                self.context["project_info"] = json.load(f)
        
        # Load from PROJECT_DNA.md if exists
        dna_file = self.root_path / "PROJECT_DNA.md"
        if dna_file.exists():
            with open(dna_file, 'r', encoding='utf-8') as f:
                self.context["project_info"]["dna"] = f.read()
    
    def analyze_structure(self):
        """Analyze project directory structure."""
        structure = {}
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip hidden and cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            rel_path = Path(root).relative_to(self.root_path)
            level = str(rel_path) if str(rel_path) != '.' else 'root'
            
            structure[level] = {
                "directories": dirs,
                "files": files,
                "python_files": [f for f in files if f.endswith('.py')],
                "config_files": [f for f in files if any(f.endswith(ext) for ext in self.config_extensions)]
            }
        
        self.context["structure"] = structure
    
    def analyze_modules(self):
        """Analyze Python modules and extract metadata."""
        modules = {}
        
        for dir_name in self.important_dirs:
            dir_path = self.root_path / dir_name
            if not dir_path.exists():
                continue
            
            for py_file in dir_path.rglob("*.py"):
                rel_path = py_file.relative_to(self.root_path)
                module_info = self.analyze_python_file(py_file)
                if module_info:
                    modules[str(rel_path)] = module_info
        
        # Also analyze root Python files
        for py_file in self.root_path.glob("*.py"):
            module_info = self.analyze_python_file(py_file)
            if module_info:
                modules[py_file.name] = module_info
        
        self.context["modules"] = modules
    
    def analyze_python_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            module_info = {
                "docstring": ast.get_docstring(tree),
                "imports": [],
                "classes": [],
                "functions": [],
                "size_lines": len(content.splitlines()),
                "size_bytes": len(content.encode('utf-8'))
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_info["imports"].append(alias.name)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_info["imports"].append(node.module)
                        
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "methods": []
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info["methods"].append({
                                "name": item.name,
                                "docstring": ast.get_docstring(item)
                            })
                    
                    module_info["classes"].append(class_info)
                    
                elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                    # Top-level functions only
                    func_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node),
                        "args": [arg.arg for arg in node.args.args]
                    }
                    module_info["functions"].append(func_info)
            
            return module_info
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def load_dependencies(self):
        """Load project dependencies."""
        deps = {}
        
        # Load from requirements.txt
        req_file = self.root_path / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r', encoding='utf-8') as f:
                deps["requirements"] = [
                    line.strip() for line in f 
                    if line.strip() and not line.startswith('#')
                ]
        
        # Check for other dependency files
        for dep_file in ["Pipfile", "pyproject.toml", "setup.py"]:
            file_path = self.root_path / dep_file
            if file_path.exists():
                deps[dep_file] = f"Present (size: {file_path.stat().st_size} bytes)"
        
        self.context["dependencies"] = deps
    
    def load_configuration(self):
        """Load configuration files."""
        config = {}
        
        # Load .env.example
        env_example = self.root_path / ".env.example"
        if env_example.exists():
            with open(env_example, 'r', encoding='utf-8') as f:
                config["env_template"] = f.read()
        
        # Load other config files
        config_dir = self.root_path / "Config"
        if config_dir.exists():
            config["config_files"] = [f.name for f in config_dir.iterdir() if f.is_file()]
        
        # Load .cursorrules
        cursor_rules = self.root_path / ".cursorrules"
        if cursor_rules.exists():
            with open(cursor_rules, 'r', encoding='utf-8') as f:
                config["cursor_rules"] = f.read()
        
        self.context["configuration"] = config
    
    def analyze_documentation(self):
        """Analyze documentation files."""
        docs = {}
        
        # Analyze markdown files
        for md_file in self.root_path.rglob("*.md"):
            rel_path = md_file.relative_to(self.root_path)
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract headers
            headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
            
            docs[str(rel_path)] = {
                "size": len(content),
                "lines": len(content.splitlines()),
                "headers": headers[:10]  # First 10 headers
            }
        
        self.context["documentation"] = docs
    
    def analyze_tests(self):
        """Analyze test files."""
        tests = {}
        
        tests_dir = self.root_path / "Tests"
        if tests_dir.exists():
            test_files = list(tests_dir.rglob("test_*.py")) + list(tests_dir.rglob("*_test.py"))
            
            for test_file in test_files:
                rel_path = test_file.relative_to(self.root_path)
                module_info = self.analyze_python_file(test_file)
                
                if module_info:
                    # Count test functions
                    test_count = sum(
                        1 for func in module_info.get("functions", [])
                        if func["name"].startswith("test_")
                    )
                    
                    tests[str(rel_path)] = {
                        "test_count": test_count,
                        "functions": [f["name"] for f in module_info.get("functions", [])]
                    }
        
        self.context["tests"] = tests
    
    def get_current_state(self):
        """Get current project state."""
        state = {}
        
        # Check for TODO items
        todo_file = self.root_path / "PROJECT_TODO.md"
        if todo_file.exists():
            with open(todo_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract TODO items
                todos = re.findall(r'^\s*[-*]\s*\[[ x]\]\s+(.+)$', content, re.MULTILINE)
                state["todos"] = todos[:20]  # First 20 TODOs
        
        # Check git status
        git_dir = self.root_path / ".git"
        if git_dir.exists():
            state["git_initialized"] = True
            
            # Try to get current branch
            head_file = git_dir / "HEAD"
            if head_file.exists():
                with open(head_file, 'r') as f:
                    ref = f.read().strip()
                    if ref.startswith("ref: refs/heads/"):
                        state["git_branch"] = ref.replace("ref: refs/heads/", "")
        
        # Check for logs
        logs_dir = self.root_path / "Logs"
        if logs_dir.exists():
            log_files = list(logs_dir.rglob("*.log"))
            state["log_files_count"] = len(log_files)
            if log_files:
                # Get most recent log
                most_recent = max(log_files, key=lambda f: f.stat().st_mtime)
                state["most_recent_log"] = str(most_recent.relative_to(self.root_path))
        
        self.context["current_state"] = state
    
    def export_context(self, output_path: Path, format: str = "markdown") -> Path:
        """Export context to file."""
        if format == "markdown":
            return self.export_markdown(output_path)
        elif format == "json":
            return self.export_json(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def export_markdown(self, output_path: Path) -> Path:
        """Export context as markdown."""
        lines = []
        
        lines.append("# Project Context")
        lines.append(f"\nGenerated: {self.context['timestamp']}\n")
        
        # Project Info
        if self.context["project_info"]:
            lines.append("## Project Information\n")
            for key, value in self.context["project_info"].items():
                if key != "dna":
                    lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        # Structure Overview
        lines.append("## Project Structure\n")
        structure = self.context["structure"]
        if "root" in structure:
            root_info = structure["root"]
            lines.append(f"- **Directories**: {len(root_info['directories'])}")
            lines.append(f"- **Python Files**: {len(root_info['python_files'])}")
            lines.append(f"- **Config Files**: {len(root_info['config_files'])}")
        lines.append("")
        
        # Key Modules
        if self.context["modules"]:
            lines.append("## Key Modules\n")
            for module_path, module_info in list(self.context["modules"].items())[:10]:
                lines.append(f"### {module_path}")
                
                if module_info.get("docstring"):
                    lines.append(f"_{module_info['docstring']}_")
                
                lines.append(f"- Lines: {module_info['size_lines']}")
                
                if module_info["classes"]:
                    lines.append(f"- Classes: {', '.join(c['name'] for c in module_info['classes'])}")
                
                if module_info["functions"]:
                    lines.append(f"- Functions: {', '.join(f['name'] for f in module_info['functions'][:5])}")
                
                lines.append("")
        
        # Dependencies
        if self.context["dependencies"].get("requirements"):
            lines.append("## Dependencies\n")
            for dep in self.context["dependencies"]["requirements"][:15]:
                lines.append(f"- {dep}")
            lines.append("")
        
        # Current State
        if self.context["current_state"]:
            lines.append("## Current State\n")
            state = self.context["current_state"]
            
            if "git_branch" in state:
                lines.append(f"- Git Branch: {state['git_branch']}")
            
            if "todos" in state and state["todos"]:
                lines.append("\n### Active TODOs")
                for todo in state["todos"][:10]:
                    lines.append(f"- {todo}")
            
            lines.append("")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return output_path
    
    def export_json(self, output_path: Path) -> Path:
        """Export context as JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False, default=str)
        return output_path

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build project context for AI assistants")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Prompts/CURRENT_CONTEXT.md"),
        help="Output file path"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--type",
        choices=["general", "implementation", "debug", "refactor"],
        default="general",
        help="Context type"
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Project root path (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Build context
    builder = ContextBuilder(args.root)
    context = builder.build_context(args.type)
    
    # Export context
    output_path = builder.export_context(args.output, args.format)
    
    print(f"Context exported to: {output_path}")
    
    # Also save to Update_AI if it exists
    update_dir = Path("Update_AI")
    if update_dir.exists():
        update_path = update_dir / args.output.name
        if args.format == "markdown":
            builder.export_markdown(update_path)
        else:
            builder.export_json(update_path)
        print(f"Context also copied to: {update_path}")

if __name__ == "__main__":
    main()
