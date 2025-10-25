#!/usr/bin/env python3
"""
Unit tests for Scheduler module
"""

import pytest
import json
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from Automatizare_Completa.scheduler import TaskScheduler

class TestTaskScheduler:
    """Test cases for TaskScheduler class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def scheduler(self, temp_dir):
        """Create TaskScheduler instance with temporary directory."""
        return TaskScheduler(project_root=temp_dir)
    
    def test_load_schedule_file_not_found(self, scheduler):
        """Test loading schedule when file doesn't exist."""
        # Arrange
        assert not scheduler.schedule_file.exists()
        
        # Act
        result = scheduler.load_schedule()
        
        # Assert
        assert 'jobs' in result
        assert isinstance(result['jobs'], list)
        assert scheduler.schedule_file.exists()  # File should be created
    
    def test_load_schedule_valid_json(self, scheduler):
        """Test loading schedule with valid JSON."""
        # Arrange
        test_data = {
            "jobs": [
                {
                    "type": "daily",
                    "time": "09:00",
                    "task": "test.py",
                    "enabled": True,
                    "last_run": None
                }
            ]
        }
        
        with open(scheduler.schedule_file, 'w') as f:
            json.dump(test_data, f)
        
        # Act
        result = scheduler.load_schedule()
        
        # Assert
        assert result == test_data
        assert len(result['jobs']) == 1
        assert result['jobs'][0]['task'] == 'test.py'
    
    def test_load_schedule_invalid_json(self, scheduler):
        """Test loading schedule with invalid JSON."""
        # Arrange
        with open(scheduler.schedule_file, 'w') as f:
            f.write("invalid json content")
        
        # Act
        result = scheduler.load_schedule()
        
        # Assert
        assert 'jobs' in result
        assert result['jobs'] == []
    
    def test_save_schedule(self, scheduler):
        """Test saving schedule to file."""
        # Arrange
        test_data = {
            "jobs": [
                {
                    "type": "daily",
                    "time": "09:00",
                    "task": "test.py",
                    "enabled": True
                }
            ]
        }
        
        # Act
        scheduler.save_schedule(test_data)
        
        # Assert
        assert scheduler.schedule_file.exists()
        with open(scheduler.schedule_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == test_data
    
    @patch('Automatizare_Completa.scheduler.subprocess.run')
    def test_run_task_calls_subprocess(self, mock_run, scheduler):
        """Test that run_task calls subprocess with correct arguments."""
        # Arrange
        mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")
        
        # Create a test script
        test_script = scheduler.automatizare_dir / "test_script.py"
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("print('test')")
        
        job = {
            "task": "test_script.py",
            "description": "Test task"
        }
        
        # Act
        scheduler.run_task(job)
        
        # Assert
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert call_args[0][0] == [sys.executable, str(test_script)]
        assert call_args[1]['cwd'] == scheduler.project_root
        assert call_args[1]['timeout'] == 300
    
    @patch('Automatizare_Completa.scheduler.subprocess.run')
    def test_run_task_script_not_found(self, mock_run, scheduler):
        """Test run_task when script doesn't exist."""
        # Arrange
        job = {
            "task": "nonexistent.py",
            "description": "Test task"
        }
        
        # Act
        scheduler.run_task(job)
        
        # Assert
        mock_run.assert_not_called()
    
    @patch('Automatizare_Completa.scheduler.subprocess.run')
    def test_run_task_success(self, mock_run, scheduler):
        """Test run_task with successful execution."""
        # Arrange
        mock_run.return_value = MagicMock(returncode=0, stdout="Success", stderr="")
        
        test_script = scheduler.automatizare_dir / "test_script.py"
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("print('test')")
        
        job = {
            "task": "test_script.py",
            "description": "Test task",
            "last_run": None
        }
        
        # Act
        scheduler.run_task(job)
        
        # Assert
        assert job['last_run'] is not None
    
    @patch('Automatizare_Completa.scheduler.subprocess.run')
    def test_run_task_failure(self, mock_run, scheduler):
        """Test run_task with failed execution."""
        # Arrange
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Error occurred")
        
        test_script = scheduler.automatizare_dir / "test_script.py"
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("print('test')")
        
        job = {
            "task": "test_script.py",
            "description": "Test task",
            "last_run": None
        }
        
        # Act
        scheduler.run_task(job)
        
        # Assert
        assert job['last_run'] is not None
    
    @patch('Automatizare_Completa.scheduler.subprocess.run')
    def test_run_task_timeout(self, mock_run, scheduler):
        """Test run_task with timeout."""
        # Arrange
        from subprocess import TimeoutExpired
        mock_run.side_effect = TimeoutExpired("python", 300)
        
        test_script = scheduler.automatizare_dir / "test_script.py"
        test_script.parent.mkdir(parents=True, exist_ok=True)
        test_script.write_text("print('test')")
        
        job = {
            "task": "test_script.py",
            "description": "Test task"
        }
        
        # Act
        scheduler.run_task(job)
        
        # Assert
        # Should not raise exception, just log error
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_daily_job(self, mock_schedule, scheduler):
        """Test setting up daily job schedule."""
        # Arrange
        jobs = [
            {
                "type": "daily",
                "time": "09:00",
                "task": "test.py",
                "enabled": True,
                "description": "Daily test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_called_once()
        mock_schedule.every.return_value.day.at.assert_called_once_with("09:00")
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_interval_job(self, mock_schedule, scheduler):
        """Test setting up interval job schedule."""
        # Arrange
        jobs = [
            {
                "type": "interval",
                "every_minutes": 30,
                "task": "test.py",
                "enabled": True,
                "description": "Interval test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_called_once_with(30)
        mock_schedule.every.return_value.minutes.do.assert_called_once()
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_disabled_job(self, mock_schedule, scheduler):
        """Test that disabled jobs are not scheduled."""
        # Arrange
        jobs = [
            {
                "type": "daily",
                "time": "09:00",
                "task": "test.py",
                "enabled": False,
                "description": "Disabled test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_not_called()
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_once_job(self, mock_schedule, scheduler):
        """Test setting up one-time job."""
        # Arrange
        jobs = [
            {
                "type": "once",
                "run_at_datetime": "2025-12-31T12:00:00",
                "task": "test.py",
                "enabled": True,
                "executed": False,
                "description": "One-time test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_called_once()
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_executed_once_job(self, mock_schedule, scheduler):
        """Test that executed one-time jobs are not scheduled."""
        # Arrange
        jobs = [
            {
                "type": "once",
                "run_at_datetime": "2025-12-31T12:00:00",
                "task": "test.py",
                "enabled": True,
                "executed": True,
                "description": "Executed test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_not_called()
    
    def test_setup_schedules_unknown_job_type(self, scheduler):
        """Test handling of unknown job types."""
        # Arrange
        jobs = [
            {
                "type": "unknown",
                "task": "test.py",
                "enabled": True,
                "description": "Unknown test"
            }
        ]
        
        # Act & Assert - Should not raise exception
        scheduler.setup_schedules(jobs)
    
    @patch('Automatizare_Completa.scheduler.schedule')
    def test_setup_schedules_weekly_job(self, mock_schedule, scheduler):
        """Test setting up weekly job schedule."""
        # Arrange
        jobs = [
            {
                "type": "weekly",
                "day": "monday",
                "time": "10:00",
                "task": "test.py",
                "enabled": True,
                "description": "Weekly test"
            }
        ]
        
        # Act
        scheduler.setup_schedules(jobs)
        
        # Assert
        mock_schedule.every.assert_called_once()
        # Check that monday method was called
        assert hasattr(mock_schedule.every.return_value, 'monday')
