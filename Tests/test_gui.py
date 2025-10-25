#!/usr/bin/env python3
"""
Unit tests for GUI components
Minimal tests for the SocialBoost GUI application
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))


class TestGUIIntegration(unittest.TestCase):
    """Integration tests for GUI components."""
    
    def test_gui_file_exists(self):
        """Test that the GUI main file exists."""
        gui_file = project_root / "GUI" / "main_gui.py"
        self.assertTrue(gui_file.exists(), "GUI/main_gui.py file should exist")
    
    def test_gui_file_is_executable(self):
        """Test that the GUI file can be imported."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            # Try to compile the file to check for syntax errors
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            try:
                compile(code, str(gui_file), 'exec')
            except SyntaxError as e:
                self.fail(f"GUI file has syntax errors: {e}")
    
    def test_gui_file_has_required_methods(self):
        """Test that the GUI file contains required methods."""
        gui_file = project_root / "GUI" / "main_gui.py"
        if gui_file.exists():
            with open(gui_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Check for required methods
            required_methods = ['run_post_text', 'run_generate_text', 'SocialBoostApp']
            for method in required_methods:
                self.assertIn(method, code, f"GUI file should contain {method}")
    
    def test_auto_post_has_message_argument(self):
        """Test that auto_post.py accepts --message argument."""
        auto_post_file = project_root / "Automatizare_Completa" / "auto_post.py"
        if auto_post_file.exists():
            with open(auto_post_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Check for argparse and --message
            self.assertIn('argparse', code, "auto_post.py should import argparse")
            self.assertIn('--message', code, "auto_post.py should accept --message argument")
    
    def test_auto_generate_has_prompt_argument(self):
        """Test that auto_generate.py accepts --prompt argument."""
        auto_generate_file = project_root / "Automatizare_Completa" / "auto_generate.py"
        if auto_generate_file.exists():
            with open(auto_generate_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Check for argparse and --prompt
            self.assertIn('argparse', code, "auto_generate.py should import argparse")
            self.assertIn('--prompt', code, "auto_generate.py should accept --prompt argument")


if __name__ == '__main__':
    unittest.main()
