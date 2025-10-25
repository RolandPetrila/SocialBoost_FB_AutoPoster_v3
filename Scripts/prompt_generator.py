#!/usr/bin/env python3
"""
Prompt Generator - Creates structured prompts for AI assistants
Combines templates with current context to generate task-specific prompts
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import re

class PromptGenerator:
    """Generates structured prompts for AI assistants."""
    
    def __init__(self, templates_dir: Path = None):
        self.templates_dir = templates_dir or Path("Prompts/Templates")
        self.prompts_dir = Path("Prompts/Generated")
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        
        self.context_file = Path("Prompts/CURRENT_CONTEXT.md")
        self.project_context_file = Path("PROJECT_CONTEXT.json")
        
        # Available templates
        self.templates = {
            "implementation": "implementation_template.md",
            "debug": "debug_template.md",
            "validation": "validation_template.md",
            "refactor": "refactor_template.md",
            "setup": "setup_template.md"
        }
    
    def load_template(self, template_name: str) -> str:
        """Load a template file."""
        template_file = self.templates_dir / self.templates.get(template_name, template_name)
        
        if not template_file.exists():
            # Return a basic template if file doesn't exist
            return self.get_default_template(template_name)
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_default_template(self, template_type: str) -> str:
        """Get default template based on type."""
        templates = {
            "implementation": """# Implementation Task

## Objective
{task_description}

## Context
{context}

## Requirements
{requirements}

## Implementation Guidelines
1. Follow existing code patterns and conventions
2. Add comprehensive error handling
3. Include logging for debugging
4. Write unit tests for new functionality
5. Update documentation as needed

## Files to Modify
{files_to_modify}

## Validation Steps
1. Run tests: `python Tests/validation_runner.py`
2. Check logs for errors
3. Verify functionality works as expected

## Success Criteria
{success_criteria}

## Additional Notes
{additional_notes}
""",
            "debug": """# Debug Task

## Issue Description
{issue_description}

## Error Details
{error_details}

## Context
{context}

## Reproduction Steps
{reproduction_steps}

## Investigation Areas
{investigation_areas}

## Debug Guidelines
1. Check logs in Logs/ directory
2. Add debug logging if needed
3. Use breakpoints or print statements
4. Test edge cases
5. Verify fix doesn't break other features

## Files to Check
{files_to_check}

## Resolution Criteria
{resolution_criteria}
""",
            "validation": """# Validation Task

## Validation Scope
{validation_scope}

## Context
{context}

## Tests to Run
{tests_to_run}

## Validation Checklist
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] No linting errors (flake8)
- [ ] No type errors (mypy)
- [ ] No security issues (bandit)
- [ ] Documentation is up to date
- [ ] CHANGELOG.md updated
- [ ] No regression in existing features

## Expected Results
{expected_results}

## Report Format
{report_format}
""",
            "refactor": """# Refactoring Task

## Refactoring Goal
{refactoring_goal}

## Context
{context}

## Current Implementation Issues
{current_issues}

## Proposed Changes
{proposed_changes}

## Refactoring Guidelines
1. Maintain backward compatibility
2. Improve code readability
3. Reduce complexity
4. Follow DRY principle
5. Add/update tests
6. Update documentation

## Files to Refactor
{files_to_refactor}

## Testing Strategy
{testing_strategy}

## Success Metrics
{success_metrics}
""",
            "setup": """# Setup Task

## Setup Objective
{setup_objective}

## Environment Requirements
{environment_requirements}

## Installation Steps
{installation_steps}

## Configuration
{configuration}

## Verification Steps
{verification_steps}

## Troubleshooting
{troubleshooting}

## Success Criteria
{success_criteria}
"""
        }
        
        return templates.get(template_type, templates["implementation"])
    
    def load_current_context(self) -> str:
        """Load current project context."""
        if self.context_file.exists():
            with open(self.context_file, 'r', encoding='utf-8') as f:
                return f.read()
        return "No current context available. Run `python Scripts/context_builder.py` first."
    
    def load_project_info(self) -> Dict[str, Any]:
        """Load project information."""
        if self.project_context_file.exists():
            with open(self.project_context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_prompt(
        self,
        template_name: str,
        task_description: str,
        variables: Dict[str, str] = None,
        include_context: bool = True
    ) -> str:
        """Generate a prompt from template and variables."""
        
        # Load template
        template = self.load_template(template_name)
        
        # Prepare variables
        prompt_vars = {
            "task_description": task_description,
            "timestamp": datetime.now().isoformat(),
            "project_name": "SocialBoost_FB_AutoPoster_v3"
        }
        
        # Add project info
        project_info = self.load_project_info()
        if project_info:
            prompt_vars["project_root"] = project_info.get("root_path", "")
            prompt_vars["current_stage"] = project_info.get("current_stage", "")
            prompt_vars["python_version"] = project_info.get("python_version", "")
        
        # Add context if requested
        if include_context:
            prompt_vars["context"] = self.load_current_context()
        
        # Add custom variables
        if variables:
            prompt_vars.update(variables)
        
        # Fill in template
        prompt = template
        for key, value in prompt_vars.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        # Handle any remaining placeholders with empty string
        prompt = re.sub(r'\{[^}]+\}', '', prompt)
        
        return prompt
    
    def save_prompt(self, prompt: str, filename: str = None) -> Path:
        """Save generated prompt to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prompt_{timestamp}.md"
        
        output_path = self.prompts_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        # Also save to Update_AI if it exists
        update_dir = Path("Update_AI")
        if update_dir.exists():
            update_path = update_dir / f"LATEST_PROMPT_{filename}"
            with open(update_path, 'w', encoding='utf-8') as f:
                f.write(prompt)
        
        return output_path
    
    def generate_implementation_prompt(
        self,
        task: str,
        files: List[str] = None,
        requirements: List[str] = None
    ) -> str:
        """Generate implementation-specific prompt."""
        
        variables = {
            "requirements": "\n".join(f"- {req}" for req in (requirements or [])),
            "files_to_modify": "\n".join(f"- {file}" for file in (files or [])),
            "success_criteria": f"- {task} is fully implemented\n- All tests pass\n- No errors in logs",
            "additional_notes": "Remember to follow the project conventions and update tests."
        }
        
        return self.generate_prompt("implementation", task, variables)
    
    def generate_debug_prompt(
        self,
        issue: str,
        error_details: str = "",
        files: List[str] = None
    ) -> str:
        """Generate debug-specific prompt."""
        
        variables = {
            "issue_description": issue,
            "error_details": error_details or "No specific error details provided",
            "reproduction_steps": "1. Run the affected component\n2. Observe the error",
            "investigation_areas": "- Check recent changes\n- Review error logs\n- Test edge cases",
            "files_to_check": "\n".join(f"- {file}" for file in (files or [])),
            "resolution_criteria": "- Error is fixed\n- No regression\n- Tests pass"
        }
        
        return self.generate_prompt("debug", issue, variables)
    
    def generate_validation_prompt(
        self,
        scope: str = "full",
        tests: List[str] = None
    ) -> str:
        """Generate validation-specific prompt."""
        
        variables = {
            "validation_scope": scope,
            "tests_to_run": "\n".join(f"- {test}" for test in (tests or ["All tests"])),
            "expected_results": "All tests should pass without errors",
            "report_format": "Markdown report with test results and recommendations"
        }
        
        return self.generate_prompt("validation", f"Validate {scope} system", variables)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate prompts for AI assistants")
    parser.add_argument(
        "--template",
        choices=["implementation", "debug", "validation", "refactor", "setup"],
        default="implementation",
        help="Template type to use"
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Task description"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Files to modify/check"
    )
    parser.add_argument(
        "--requirements",
        nargs="+",
        help="Requirements for the task"
    )
    parser.add_argument(
        "--no-context",
        action="store_true",
        help="Don't include current context"
    )
    parser.add_argument(
        "--output",
        help="Output filename"
    )
    parser.add_argument(
        "--variables",
        type=json.loads,
        help="Additional variables as JSON"
    )
    
    args = parser.parse_args()
    
    generator = PromptGenerator()
    
    # Prepare variables
    variables = args.variables or {}
    
    # Generate appropriate prompt based on template
    if args.template == "implementation":
        prompt = generator.generate_implementation_prompt(
            args.task,
            args.files,
            args.requirements
        )
    elif args.template == "debug":
        error_details = variables.pop("error_details", "")
        prompt = generator.generate_debug_prompt(
            args.task,
            error_details,
            args.files
        )
    elif args.template == "validation":
        scope = variables.pop("scope", "full")
        prompt = generator.generate_validation_prompt(scope, args.requirements)
    else:
        # Generic prompt generation
        if args.files:
            variables["files"] = "\n".join(f"- {f}" for f in args.files)
        if args.requirements:
            variables["requirements"] = "\n".join(f"- {r}" for r in args.requirements)
        
        prompt = generator.generate_prompt(
            args.template,
            args.task,
            variables,
            not args.no_context
        )
    
    # Save prompt
    output_path = generator.save_prompt(prompt, args.output)
    
    print(f"Prompt generated and saved to: {output_path}")
    
    # Also print prompt to console for easy copying
    print("\n" + "="*50)
    print("GENERATED PROMPT:")
    print("="*50)
    print(prompt)

if __name__ == "__main__":
    main()
