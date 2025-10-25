#!/usr/bin/env python3
"""
Unit tests for Health Check Module
Tests the HealthCheck class functionality with mocking.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import pathlib
import json
import tempfile
import shutil
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from Automatizare_Completa.health_check import HealthCheck


class TestHealthCheck(unittest.TestCase):
    """Test cases for HealthCheck class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = pathlib.Path(self.temp_dir)
        self.health_check = HealthCheck(self.project_root)
        
        # Create some test files
        (self.project_root / "PROJECT_CONTEXT.json").write_text('{"project_name": "Test Project"}')
        (self.project_root / "requirements.txt").write_text('requests==2.32.3\nopenai>=1.0.0')
        (self.project_root / "Automatizare_Completa").mkdir()
        (self.project_root / "GUI").mkdir()
        (self.project_root / "Tests").mkdir()
        (self.project_root / "Config").mkdir()
        (self.project_root / "Logs").mkdir()
        (self.project_root / "Assets").mkdir()
        (self.project_root / "Assets" / "Images").mkdir()
        (self.project_root / "Assets" / "Videos").mkdir()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_init_default_project_root(self):
        """Test HealthCheck initialization with default project root."""
        health_check = HealthCheck()
        self.assertIsInstance(health_check.project_root, pathlib.Path)
        self.assertTrue(health_check.project_root.exists())
    
    def test_init_custom_project_root(self):
        """Test HealthCheck initialization with custom project root."""
        health_check = HealthCheck(self.project_root)
        self.assertEqual(health_check.project_root, self.project_root)
    
    @patch('sys.version_info')
    def test_check_python_version_pass(self, mock_version_info):
        """Test Python version check with compatible version."""
        mock_version_info.major = 3
        mock_version_info.minor = 9
        mock_version_info.micro = 0
        
        result = self.health_check.check_python_version()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(result['details']['major'], 3)
        self.assertEqual(result['details']['minor'], 9)
        self.assertIn('Python 3.9.0 is compatible', result['message'])
    
    @patch('sys.version_info')
    def test_check_python_version_fail(self, mock_version_info):
        """Test Python version check with incompatible version."""
        mock_version_info.major = 3
        mock_version_info.minor = 7
        mock_version_info.micro = 0
        
        result = self.health_check.check_python_version()
        
        self.assertEqual(result['status'], 'Fail')
        self.assertEqual(result['score'], 0.0)
        self.assertIn('Python 3.7.0 is too old', result['message'])
    
    @patch('subprocess.run')
    def test_check_git_repository_pass(self, mock_run):
        """Test Git repository check with valid repository."""
        # Mock git status command
        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = ""
        
        # Mock git branch command
        mock_branch = Mock()
        mock_branch.returncode = 0
        mock_branch.stdout = "master"
        
        # Mock git log command
        mock_log = Mock()
        mock_log.returncode = 0
        mock_log.stdout = "abc123 Test commit"
        
        mock_run.side_effect = [mock_status, mock_branch, mock_log]
        
        # Create .git directory
        (self.project_root / ".git").mkdir()
        
        result = self.health_check.check_git_repository()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertTrue(result['details']['is_git_repo'])
        self.assertEqual(result['details']['current_branch'], 'master')
        self.assertEqual(result['details']['last_commit'], 'abc123 Test commit')
    
    def test_check_git_repository_no_git(self):
        """Test Git repository check without .git directory."""
        result = self.health_check.check_git_repository()
        
        self.assertEqual(result['status'], 'Fail')
        self.assertEqual(result['score'], 0.0)
        self.assertIn('Not a Git repository', result['message'])
    
    def test_check_required_files_pass(self):
        """Test required files check with all files present."""
        # Create required files
        (self.project_root / "orchestrator.py").write_text("# Test")
        (self.project_root / "backup_manager.py").write_text("# Test")
        (self.project_root / "restore_manager.py").write_text("# Test")
        
        result = self.health_check.check_required_files()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(len(result['details']['missing_files']), 0)
        self.assertEqual(len(result['details']['missing_dirs']), 0)
    
    def test_check_required_files_partial(self):
        """Test required files check with some files missing."""
        result = self.health_check.check_required_files()
        
        self.assertEqual(result['status'], 'Warning')
        self.assertGreater(result['score'], 0.5)
        self.assertGreater(len(result['details']['missing_files']), 0)
    
    @patch('builtins.__import__')
    def test_check_dependencies_pass(self, mock_import):
        """Test dependencies check with all packages available."""
        mock_import.return_value = Mock()
        
        result = self.health_check.check_dependencies()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(len(result['details']['missing_packages']), 0)
    
    @patch('builtins.__import__')
    def test_check_dependencies_fail(self, mock_import):
        """Test dependencies check with missing packages."""
        mock_import.side_effect = ImportError("No module named 'requests'")
        
        result = self.health_check.check_dependencies()
        
        self.assertEqual(result['status'], 'Fail')
        self.assertEqual(result['score'], 0.0)
        self.assertGreater(len(result['details']['missing_packages']), 0)
    
    @patch('subprocess.run')
    def test_check_github_connectivity_pass(self, mock_run):
        """Test GitHub connectivity check with working connection."""
        # Mock git remote command
        mock_remote = Mock()
        mock_remote.returncode = 0
        mock_remote.stdout = "origin  https://github.com/user/repo.git (fetch)\norigin  https://github.com/user/repo.git (push)"
        
        # Mock git fetch command
        mock_fetch = Mock()
        mock_fetch.returncode = 0
        
        mock_run.side_effect = [mock_remote, mock_fetch]
        
        result = self.health_check.check_github_connectivity()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertTrue(result['details']['has_github_remote'])
    
    @patch('subprocess.run')
    def test_check_github_connectivity_no_remote(self, mock_run):
        """Test GitHub connectivity check with no GitHub remote."""
        mock_remote = Mock()
        mock_remote.returncode = 0
        mock_remote.stdout = "origin  https://gitlab.com/user/repo.git (fetch)"
        
        mock_run.return_value = mock_remote
        
        result = self.health_check.check_github_connectivity()
        
        self.assertEqual(result['status'], 'Warning')
        self.assertEqual(result['score'], 0.3)
        self.assertFalse(result['details']['has_github_remote'])
    
    @patch('shutil.disk_usage')
    def test_check_disk_space_pass(self, mock_disk_usage):
        """Test disk space check with sufficient space."""
        # Mock disk usage: 100GB total, 30GB free (30% free)
        mock_disk_usage.return_value = Mock(
            total=100 * 1024**3,  # 100GB
            free=30 * 1024**3,    # 30GB
            used=70 * 1024**3     # 70GB
        )
        
        result = self.health_check.check_disk_space()
        
        self.assertEqual(result['status'], 'Pass')
        self.assertEqual(result['score'], 1.0)
        self.assertEqual(result['details']['free_percentage'], 30.0)
        self.assertIn('Disk space healthy', result['message'])
    
    @patch('shutil.disk_usage')
    def test_check_disk_space_warning(self, mock_disk_usage):
        """Test disk space check with low space."""
        # Mock disk usage: 100GB total, 5GB free (5% free)
        mock_disk_usage.return_value = Mock(
            total=100 * 1024**3,  # 100GB
            free=5 * 1024**3,     # 5GB
            used=95 * 1024**3     # 95GB
        )
        
        result = self.health_check.check_disk_space()
        
        self.assertEqual(result['status'], 'Fail')
        self.assertEqual(result['score'], 0.0)
        self.assertEqual(result['details']['free_percentage'], 5.0)
        self.assertIn('Disk space critical', result['message'])
    
    def test_calculate_overall_health_healthy(self):
        """Test overall health calculation with healthy results."""
        # Mock results with high scores
        self.health_check.results = {
            'Python Version': {'score': 1.0, 'status': 'Pass'},
            'Git Repository': {'score': 1.0, 'status': 'Pass'},
            'Required Files': {'score': 1.0, 'status': 'Pass'},
            'Dependencies': {'score': 1.0, 'status': 'Pass'},
            'GitHub Connectivity': {'score': 1.0, 'status': 'Pass'},
            'Disk Space': {'score': 1.0, 'status': 'Pass'}
        }
        
        health_status, health_score = self.health_check.calculate_overall_health()
        
        self.assertEqual(health_status, 'Healthy')
        self.assertEqual(health_score, 1.0)
    
    def test_calculate_overall_health_degraded(self):
        """Test overall health calculation with degraded results."""
        # Mock results with mixed scores
        self.health_check.results = {
            'Python Version': {'score': 1.0, 'status': 'Pass'},
            'Git Repository': {'score': 0.8, 'status': 'Warning'},
            'Required Files': {'score': 0.7, 'status': 'Warning'},
            'Dependencies': {'score': 1.0, 'status': 'Pass'},
            'GitHub Connectivity': {'score': 0.5, 'status': 'Warning'},
            'Disk Space': {'score': 1.0, 'status': 'Pass'}
        }
        
        health_status, health_score = self.health_check.calculate_overall_health()
        
        self.assertEqual(health_status, 'Degraded')
        self.assertGreater(health_score, 0.7)
        self.assertLess(health_score, 0.9)
    
    def test_calculate_overall_health_critical(self):
        """Test overall health calculation with critical results."""
        # Mock results with low scores
        self.health_check.results = {
            'Python Version': {'score': 0.0, 'status': 'Fail'},
            'Git Repository': {'score': 0.0, 'status': 'Fail'},
            'Required Files': {'score': 0.3, 'status': 'Fail'},
            'Dependencies': {'score': 0.0, 'status': 'Fail'},
            'GitHub Connectivity': {'score': 0.0, 'status': 'Fail'},
            'Disk Space': {'score': 0.0, 'status': 'Fail'}
        }
        
        health_status, health_score = self.health_check.calculate_overall_health()
        
        self.assertEqual(health_status, 'Critical')
        self.assertLess(health_score, 0.5)
    
    def test_save_report(self):
        """Test saving health check report."""
        # Set up mock results
        self.health_check.results = {
            'Python Version': {'score': 1.0, 'status': 'Pass', 'message': 'OK'}
        }
        self.health_check.overall_health = 'Healthy'
        self.health_check.health_score = 1.0
        
        # Save report
        report_path = self.health_check.save_report()
        
        # Verify file was created
        self.assertTrue(report_path.exists())
        
        # Verify content
        with open(report_path, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        self.assertEqual(report_data['overall_health'], 'Healthy')
        self.assertEqual(report_data['health_score'], 1.0)
        self.assertIn('timestamp', report_data)
        self.assertIn('checks', report_data)
        self.assertIn('summary', report_data)
    
    @patch('builtins.print')
    def test_print_summary(self, mock_print):
        """Test printing health check summary."""
        # Set up mock results
        self.health_check.results = {
            'Python Version': {'score': 1.0, 'status': 'Pass', 'message': 'OK'},
            'Git Repository': {'score': 0.8, 'status': 'Warning', 'message': 'Warning'}
        }
        self.health_check.overall_health = 'Degraded'
        self.health_check.health_score = 0.9
        
        # Print summary
        self.health_check.print_summary()
        
        # Verify print was called
        self.assertTrue(mock_print.called)
        
        # Check that summary contains expected information
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        summary_text = '\n'.join(print_calls)
        
        self.assertIn('SOCIALBOOST HEALTH CHECK SUMMARY', summary_text)
        self.assertIn('Overall Health: Degraded', summary_text)
        self.assertIn('Health Score: 0.90', summary_text)
    
    @patch.object(HealthCheck, 'check_python_version')
    @patch.object(HealthCheck, 'check_git_repository')
    @patch.object(HealthCheck, 'check_required_files')
    @patch.object(HealthCheck, 'check_dependencies')
    @patch.object(HealthCheck, 'check_github_connectivity')
    @patch.object(HealthCheck, 'check_disk_space')
    @patch.object(HealthCheck, 'save_report')
    @patch.object(HealthCheck, 'print_summary')
    def test_run_all_checks(self, mock_print, mock_save, mock_disk, mock_github, 
                           mock_deps, mock_files, mock_git, mock_python):
        """Test running all health checks."""
        # Mock check results
        mock_python.return_value = {'check': 'Python Version', 'status': 'Pass', 'score': 1.0}
        mock_git.return_value = {'check': 'Git Repository', 'status': 'Pass', 'score': 1.0}
        mock_files.return_value = {'check': 'Required Files', 'status': 'Pass', 'score': 1.0}
        mock_deps.return_value = {'check': 'Dependencies', 'status': 'Pass', 'score': 1.0}
        mock_github.return_value = {'check': 'GitHub Connectivity', 'status': 'Pass', 'score': 1.0}
        mock_disk.return_value = {'check': 'Disk Space', 'status': 'Pass', 'score': 1.0}
        
        mock_save.return_value = pathlib.Path('/tmp/test_report.json')
        
        # Run all checks
        result = self.health_check.run_all_checks()
        
        # Verify all checks were called
        mock_python.assert_called_once()
        mock_git.assert_called_once()
        mock_files.assert_called_once()
        mock_deps.assert_called_once()
        mock_github.assert_called_once()
        mock_disk.assert_called_once()
        
        # Verify summary and report were called
        mock_print.assert_called_once()
        mock_save.assert_called_once()
        
        # Verify result structure
        self.assertIn('overall_health', result)
        self.assertIn('health_score', result)
        self.assertIn('results', result)
        self.assertIn('report_path', result)


if __name__ == '__main__':
    unittest.main()
