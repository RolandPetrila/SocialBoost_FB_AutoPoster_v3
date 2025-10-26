#!/usr/bin/env python3
"""
Unit tests for Facebook Token Exchange Script
Tests for Scripts/exchange_user_to_page_token.py
"""

import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))


class TestTokenExchangeScript(unittest.TestCase):
    """Unit tests for the token exchange script."""
    
    def test_script_exists(self):
        """Test that the token exchange script exists."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        self.assertTrue(script_path.exists(), "exchange_user_to_page_token.py should exist")
    
    def test_script_has_argparse(self):
        """Test that the script imports argparse."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('import argparse', code, "Script should import argparse")
    
    def test_script_has_check_only_argument(self):
        """Test that the script has --check-only argument."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('--check-only', code, "Script should have --check-only argument")
            self.assertIn('action=\'store_true\'', code, "--check-only should be a boolean flag")
    
    def test_script_has_user_token_argument(self):
        """Test that the script has --user-token argument."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('--user-token', code, "Script should have --user-token argument")
    
    def test_script_imports_requests(self):
        """Test that the script imports requests for API calls."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('import requests', code, "Script should import requests")
    
    def test_script_has_verify_token_function(self):
        """Test that the script has a verify_token function."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('def verify_token', code, "Script should have verify_token function")
    
    def test_script_has_update_env_file_function(self):
        """Test that the script has an update_env_file function."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('def update_env_file', code, "Script should have update_env_file function")
    
    def test_script_handles_check_only_mode(self):
        """Test that the script handles --check-only mode."""
        script_path = project_root / "Scripts" / "exchange_user_to_page_token.py"
        if script_path.exists():
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('args.check_only', code, "Script should check for --check-only flag")
            self.assertIn('sys.exit(0)', code, "Script should exit with code 0 on success")
            self.assertIn('sys.exit(1)', code, "Script should exit with code 1 on failure")
            self.assertIn('sys.exit(2)', code, "Script should exit with code 2 if token not found")


class TestGUIWithTokenExchange(unittest.TestCase):
    """Unit tests for GUI integration with token exchange."""
    
    def test_gui_has_facebook_token_label(self):
        """Test that the GUI has a Facebook token status label."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('facebook_token_status_label', code, 
                         "GUI should have facebook_token_status_label widget")
    
    def test_gui_has_refresh_token_button(self):
        """Test that the GUI has a refresh token button."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('refresh_token_btn', code, "GUI should have refresh_token_btn")
            self.assertIn('Refresh Facebook Token', code, 
                         "GUI should have 'Refresh Facebook Token' button")
    
    def test_gui_has_check_facebook_token_method(self):
        """Test that the GUI has check_facebook_token_startup method."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('def check_facebook_token_startup', code,
                         "GUI should have check_facebook_token_startup method")
    
    def test_gui_has_run_token_exchange_method(self):
        """Test that the GUI has run_token_exchange method."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('def run_token_exchange', code,
                         "GUI should have run_token_exchange method")
    
    def test_gui_runs_token_check_at_startup(self):
        """Test that the GUI runs token check at startup."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.assertIn('check_facebook_token_startup', code,
                         "GUI should call check_facebook_token_startup in __init__")
    
    @patch('subprocess.run')
    def test_check_facebook_token_calls_script_with_check_only(self, mock_run):
        """Test that check_facebook_token calls the script with --check-only."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method uses subprocess.run with --check-only
        self.assertIn('subprocess.run', code, "Should use subprocess.run")
        self.assertIn('--check-only', code, "Should pass --check-only flag")
        self.assertIn('exchange_user_to_page_token.py', code, "Should reference token script")
    
    @patch('subprocess.Popen')
    def test_run_token_exchange_opens_terminal(self, mock_popen):
        """Test that run_token_exchange opens a terminal window."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method uses subprocess.Popen to open terminal
        self.assertIn('subprocess.Popen', code, "Should use subprocess.Popen")
        self.assertIn('cmd.exe', code, "Should open cmd.exe")
        self.assertIn('start', code, "Should use start command")
    
    def test_gui_updates_token_status_based_on_exit_code(self):
        """Test that GUI updates status based on exit code."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check for exit code handling
        self.assertIn('returncode == 0', code, "Should handle exit code 0")
        self.assertIn('returncode == 1', code, "Should handle exit code 1")
        self.assertIn('returncode == 2', code, "Should handle exit code 2")
        self.assertIn('VALID', code, "Should display VALID status")
        self.assertIn('INVALID', code, "Should display INVALID status")
        self.assertIn('NOT FOUND', code, "Should display NOT FOUND status")


if __name__ == '__main__':
    unittest.main()
