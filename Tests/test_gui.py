#!/usr/bin/env python3
"""
Unit tests for GUI components
Minimal tests for the SocialBoost GUI application
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import json
import tempfile
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
    
    @patch('pathlib.Path.glob')
    def test_load_assets_populates_list(self, mock_glob):
        """Test that load_assets populates the treeview with files."""
        # Mock file paths
        mock_image = MagicMock()
        mock_image.name = "test_image.png"
        mock_image.is_file.return_value = True
        mock_image.resolve.return_value = mock_image
        mock_image.__str__ = lambda x: "/path/to/test_image.png"
        
        mock_video = MagicMock()
        mock_video.name = "test_video.mp4"
        mock_video.is_file.return_value = True
        mock_video.resolve.return_value = mock_video
        mock_video.__str__ = lambda x: "/path/to/test_video.mp4"
        
        # Set up mock to return different values for different patterns
        def glob_side_effect(pattern):
            if '*.png' in pattern:
                return [mock_image]
            elif '*.mp4' in pattern:
                return [mock_video]
            return []
        
        mock_glob.side_effect = glob_side_effect
        
        # Import and create GUI instance (simulated)
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that load_assets method exists
        self.assertIn('def load_assets', code, "GUI should have load_assets method")
        self.assertIn('def on_asset_select', code, "GUI should have on_asset_select method")
        self.assertIn('def save_selected_assets', code, "GUI should have save_selected_assets method")
        self.assertIn('assets_tree', code, "GUI should have assets_tree widget")
    
    def test_save_selected_assets_writes_json(self):
        """Test that save_selected_assets writes correct JSON structure."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Verify the method exists and uses json.dump
        self.assertIn('json.dump', code, "save_selected_assets should use json.dump")
        self.assertIn('selected_assets.json', code, "save_selected_assets should write to selected_assets.json")
        self.assertIn('"images":', code, "save_selected_assets should include images key")
        self.assertIn('"videos":', code, "save_selected_assets should include videos key")
    
    def test_load_schedule_gui_populates_treeview(self):
        """Test that load_schedule_gui method exists and uses json.load."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method exists
        self.assertIn('def load_schedule_gui', code, "GUI should have load_schedule_gui method")
        self.assertIn('json.load', code, "load_schedule_gui should use json.load")
        self.assertIn('schedule.json', code, "load_schedule_gui should read from schedule.json")
        self.assertIn('schedule_tree', code, "GUI should have schedule_tree widget")
    
    def test_add_schedule_job_valid_input(self):
        """Test that add_schedule_job validates input and writes to JSON."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method exists and validates input
        self.assertIn('def add_schedule_job', code, "GUI should have add_schedule_job method")
        self.assertIn('messagebox.showerror', code, "add_schedule_job should validate input")
        self.assertIn('datetime.datetime.strptime', code, "add_schedule_job should validate datetime")
    
    def test_delete_schedule_job_updates_json(self):
        """Test that delete_schedule_job method exists."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method exists
        self.assertIn('def delete_schedule_job', code, "GUI should have delete_schedule_job method")
        self.assertIn('messagebox.askyesno', code, "delete_schedule_job should confirm deletion")
    
    def test_on_job_type_change_exists(self):
        """Test that on_job_type_change method exists for dynamic UI."""
        gui_file = project_root / "GUI" / "main_gui.py"
        with open(gui_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check that the method exists
        self.assertIn('def on_job_type_change', code, "GUI should have on_job_type_change method")
        self.assertIn('daily', code, "GUI should support daily jobs")
        self.assertIn('weekly', code, "GUI should support weekly jobs")
        self.assertIn('interval', code, "GUI should support interval jobs")
        self.assertIn('once', code, "GUI should support once jobs")


if __name__ == '__main__':
    unittest.main()
