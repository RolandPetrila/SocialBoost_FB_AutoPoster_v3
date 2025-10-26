#!/usr/bin/env python3
"""
Scheduler Module - Automated task scheduling system
Reads jobs from Config/schedule.json and runs Python scripts at specified intervals
"""

import os
import sys
import json
import time
import schedule
import subprocess
import logging
import datetime
import io
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force UTF-8 encoding for stdout/stderr to prevent UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')  # type: ignore[union-attr]
    except Exception:
        # Fallback for environments where reconfigure might fail
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Setup logging with UTF-8 encoding
PROJECT_ROOT = Path(__file__).parent.parent
log_file = PROJECT_ROOT / "Logs" / "scheduler.log"

# Ensure Logs directory exists
log_file.parent.mkdir(parents=True, exist_ok=True)

# Configure logger with explicit UTF-8 encoding
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File Handler with UTF-8 encoding
file_handler = logging.FileHandler(log_file, encoding='utf-8', errors='replace')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Console Handler with UTF-8 support
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

class TaskScheduler:
    """Automated task scheduling system."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.config_dir = self.project_root / "Config"
        self.schedule_file = self.config_dir / "schedule.json"
        self.automatizare_dir = self.project_root / "Automatizare_Completa"
        
        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.automatizare_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Scheduler initialized. Project root: {self.project_root}")
        logger.info(f"Schedule file: {self.schedule_file}")
    
    def load_schedule(self) -> Dict[str, Any]:
        """Load schedule configuration from JSON file."""
        try:
            if not self.schedule_file.exists():
                logger.info("Schedule file not found, creating default template")
                default_schedule = {
                    "jobs": [
                        {
                            "type": "daily",
                            "time": "09:00",
                            "task": "auto_post.py",
                            "enabled": True,
                            "last_run": None,
                            "description": "Daily Facebook post"
                        },
                        {
                            "type": "interval",
                            "every_minutes": 180,
                            "task": "auto_generate.py",
                            "enabled": False,
                            "last_run": None,
                            "description": "Generate content every 3 hours"
                        },
                        {
                            "type": "once",
                            "run_at_datetime": "2025-10-26T12:00:00",
                            "task": "backup_manager.py",
                            "enabled": True,
                            "executed": False,
                            "description": "One-time backup"
                        }
                    ]
                }
                self.save_schedule(default_schedule)
                return default_schedule
            
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data.get('jobs', []))} jobs from schedule")
                return data
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schedule file: {e}")
            return {"jobs": []}
        except Exception as e:
            logger.error(f"Error loading schedule: {e}")
            return {"jobs": []}
    
    def save_schedule(self, data: Dict[str, Any]) -> None:
        """Save schedule configuration to JSON file."""
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info("Schedule saved successfully")
        except Exception as e:
            logger.error(f"Error saving schedule: {e}")
    
    def run_task(self, job: Dict[str, Any]) -> None:
        """Run a scheduled task."""
        try:
            task_name = job.get('task', '')
            description = job.get('description', 'No description')
            
            logger.info(f"Running task: {task_name} - {description}")
            
            # Construct script path
            script_path = self.automatizare_dir / task_name
            
            # Check if script exists
            if not script_path.exists():
                logger.error(f"Script not found: {script_path}")
                return
            
            # Build command with arguments
            cmd = [sys.executable, str(script_path)]
            
            # Add default arguments for specific tasks
            if task_name == "backup_manager.py":
                cmd.append("create")  # Add 'create' action for backup_manager
            
            # Run the script
            logger.info(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300,  # 5 minute timeout
                encoding='utf-8',
                errors='replace'
            )
            
            # Log results
            if result.returncode == 0:
                logger.info(f"SUCCESS - Task {task_name} completed successfully")
                if result.stdout:
                    logger.info(f"Output: {result.stdout[:200]}...")
            else:
                logger.error(f"FAIL - Task {task_name} failed with return code {result.returncode}")
                if result.stderr:
                    logger.error(f"Error: {result.stderr[:200]}...")
            
            # Update job status
            job['last_run'] = datetime.datetime.now().isoformat()
            
            # Mark one-time jobs as executed
            if job.get('type') == 'once':
                job['executed'] = True
                logger.info(f"One-time job {task_name} marked as executed")
                
        except subprocess.TimeoutExpired:
            logger.error(f"Task {task_name} timed out after 5 minutes")
        except Exception as e:
            logger.error(f"Error running task {task_name}: {e}")
    
    def setup_schedules(self, jobs: List[Dict[str, Any]]) -> None:
        """Setup scheduled jobs."""
        logger.info("Setting up scheduled jobs...")
        
        for job in jobs:
            if not job.get('enabled', False):
                logger.info(f"Skipping disabled job: {job.get('task', 'unknown')}")
                continue
            
            job_type = job.get('type', '')
            task_name = job.get('task', '')
            
            if job_type == 'daily':
                time_str = job.get('time', '09:00')
                schedule.every().day.at(time_str).do(self.run_task, job=job)
                logger.info(f"Scheduled daily job: {task_name} at {time_str}")
                
            elif job_type == 'weekly':
                day = job.get('day', 'monday')
                time_str = job.get('time', '09:00')
                getattr(schedule.every(), day.lower()).at(time_str).do(self.run_task, job=job)
                logger.info(f"Scheduled weekly job: {task_name} on {day} at {time_str}")
                
            elif job_type == 'interval':
                minutes = job.get('every_minutes', 60)
                schedule.every(minutes).minutes.do(self.run_task, job=job)
                logger.info(f"Scheduled interval job: {task_name} every {minutes} minutes")
                
            elif job_type == 'once':
                run_time_str = job.get('run_at_datetime', '')
                if run_time_str and not job.get('executed', False):
                    try:
                        run_time = datetime.datetime.fromisoformat(run_time_str)
                        now = datetime.datetime.now()
                        
                        if run_time <= now:
                            logger.info(f"Running one-time job immediately: {task_name}")
                            self.run_task(job)
                        else:
                            logger.info(f"One-time job {task_name} scheduled for {run_time_str}")
                            # Schedule for the specific time
                            schedule.every().day.at(run_time.strftime('%H:%M')).do(self.run_task, job=job)
                    except ValueError as e:
                        logger.error(f"Invalid datetime format for one-time job {task_name}: {e}")
                else:
                    logger.info(f"Skipping executed one-time job: {task_name}")
            else:
                logger.warning(f"Unknown job type: {job_type} for task {task_name}")
    
    def run_scheduler(self) -> None:
        """Run the scheduler main loop."""
        logger.info("Starting scheduler...")
        
        # Load schedule
        schedule_data = self.load_schedule()
        jobs = schedule_data.get('jobs', [])
        
        if not jobs:
            logger.warning("No jobs found in schedule")
            return
        
        # Setup schedules
        self.setup_schedules(jobs)
        
        # Save updated schedule
        self.save_schedule(schedule_data)
        
        logger.info("Scheduler is running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        finally:
            logger.info("Scheduler shutdown complete")

def main():
    """Main entry point for the scheduler."""
    try:
        scheduler = TaskScheduler()
        scheduler.run_scheduler()
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
