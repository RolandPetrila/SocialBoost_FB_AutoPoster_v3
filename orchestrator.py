#!/usr/bin/env python3
"""
Orchestrator Script - Version 3.0
Central control system for SocialBoost_FB_AutoPoster_v3
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
LOG_DIR = Path("Logs/RunAll")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"orchestrator_{timestamp}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

class Orchestrator:
    """Main orchestrator class for managing system operations."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.context_file = Path("PROJECT_CONTEXT.json")
        self.context = self.load_context()
        self.scripts_dir = Path("Scripts")
        self.automation_dir = Path("Automatizare_Completa")
        
    def load_context(self) -> Dict[str, Any]:
        """Load project context from JSON file."""
        if self.context_file.exists():
            with open(self.context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_context(self):
        """Save project context to JSON file."""
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
    
    def update_context_after_execution(self, exit_code: int, operation: str):
        """Update context after script execution."""
        self.context['last_run'] = datetime.now().isoformat()
        self.context['last_exit_code'] = exit_code
        self.context['last_operation'] = operation
        self.context['last_log_dir'] = str(LOG_DIR)
        self.save_context()
        
    def run_script(self, script_path: Path, args: List[str] = None) -> int:
        """Run a Python script with optional arguments."""
        if not script_path.exists():
            self.logger.error(f"Script not found: {script_path}")
            return 1
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        self.logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.stdout:
                self.logger.info(f"Output: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error: {result.stderr}")
            
            return result.returncode
            
        except Exception as e:
            self.logger.error(f"Failed to run script: {e}")
            return 1
    
    def health_check(self) -> bool:
        """Perform system health check."""
        self.logger.info("Performing health check...")
        
        # Check critical directories
        critical_dirs = [
            self.scripts_dir,
            self.automation_dir,
            Path("Config"),
            Path("Logs"),
            Path("Tests")
        ]
        
        for dir_path in critical_dirs:
            if not dir_path.exists():
                self.logger.error(f"Missing critical directory: {dir_path}")
                return False
        
        # Check for .env file
        if not Path(".env").exists():
            self.logger.warning(".env file not found. Using .env.example as reference.")
        
        # Check Python version
        if sys.version_info < (3, 11):
            self.logger.error(f"Python 3.11+ required. Current: {sys.version}")
            return False
        
        self.logger.info("Health check passed")
        return True
    
    def backup_project(self) -> int:
        """Create project backup."""
        self.logger.info("Creating backup...")
        backup_script = Path("backup_manager.py")
        return self.run_script(backup_script)
    
    def validate_system(self) -> int:
        """Run system validation."""
        self.logger.info("Running validation...")
        validation_script = Path("Tests/validation_runner.py")
        if validation_script.exists():
            return self.run_script(validation_script)
        else:
            self.logger.warning("Validation script not found. Skipping validation.")
            return 0
    
    def sync_github(self) -> int:
        """Sync with GitHub repository."""
        self.logger.info("Syncing with GitHub...")
        sync_script = self.scripts_dir / "sync_github.py"
        if sync_script.exists():
            return self.run_script(sync_script)
        else:
            self.logger.warning("GitHub sync script not found. Skipping sync.")
            return 0
    
    def build_context(self) -> int:
        """Build current context."""
        self.logger.info("Building context...")
        context_script = self.scripts_dir / "context_builder.py"
        if context_script.exists():
            return self.run_script(context_script, ["--output", "Prompts/CURRENT_CONTEXT.md"])
        else:
            self.logger.warning("Context builder not found. Skipping context build.")
            return 0
    
    def run_automation(self, mode: str = "full") -> int:
        """Run automation tasks."""
        self.logger.info(f"Running automation in {mode} mode...")
        
        if mode == "post":
            script = self.automation_dir / "auto_post.py"
            return self.run_script(script) if script.exists() else 1
        
        elif mode == "generate":
            script = self.automation_dir / "auto_generate.py"
            return self.run_script(script) if script.exists() else 1
        
        elif mode == "schedule":
            script = self.automation_dir / "scheduler.py"
            return self.run_script(script) if script.exists() else 1
        
        elif mode == "full":
            # Run all automation tasks
            results = []
            for task in ["generate", "post"]:
                result = self.run_automation(task)
                results.append(result)
                if result != 0:
                    self.logger.error(f"Task {task} failed")
                    return result
            return 0
        
        else:
            self.logger.error(f"Unknown automation mode: {mode}")
            return 1
    
    def execute_command(self, command: str, **kwargs) -> int:
        """Execute orchestrator command."""
        self.logger.info(f"Executing command: {command}")
        
        commands = {
            "health": self.health_check,
            "backup": self.backup_project,
            "validate": self.validate_system,
            "sync": self.sync_github,
            "context": self.build_context,
            "auto": lambda: self.run_automation(kwargs.get('mode', 'full')),
            "full": self.run_full_pipeline
        }
        
        if command in commands:
            result = commands[command]()
            exit_code = 0 if result else 1 if isinstance(result, bool) else result
            self.update_context_after_execution(exit_code, command)
            return exit_code
        else:
            self.logger.error(f"Unknown command: {command}")
            return 1
    
    def run_full_pipeline(self) -> int:
        """Run full orchestration pipeline."""
        self.logger.info("Running full pipeline...")
        
        pipeline = [
            ("health", self.health_check),
            ("backup", self.backup_project),
            ("context", self.build_context),
            ("validate", self.validate_system),
            ("automation", lambda: self.run_automation("full")),
            ("sync", self.sync_github)
        ]
        
        for step_name, step_func in pipeline:
            self.logger.info(f"Pipeline step: {step_name}")
            result = step_func()
            
            # Convert boolean to exit code
            if isinstance(result, bool):
                result = 0 if result else 1
            
            if result != 0:
                self.logger.error(f"Pipeline failed at step: {step_name}")
                return result
        
        self.logger.info("Pipeline completed successfully")
        return 0

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SocialBoost Orchestrator")
    parser.add_argument(
        "command",
        choices=["health", "backup", "validate", "sync", "context", "auto", "full"],
        help="Command to execute"
    )
    parser.add_argument(
        "--mode",
        choices=["post", "generate", "schedule", "full"],
        default="full",
        help="Automation mode (for 'auto' command)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set log level from environment or argument
    log_level = os.getenv("LOG_LEVEL", args.log_level)
    os.environ["LOG_LEVEL"] = log_level
    
    orchestrator = Orchestrator()
    exit_code = orchestrator.execute_command(args.command, mode=args.mode)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
