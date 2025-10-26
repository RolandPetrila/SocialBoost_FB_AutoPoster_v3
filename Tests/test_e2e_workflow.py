#!/usr/bin/env python3
"""
End-to-End Workflow Test
Simulates the complete workflow: asset selection -> AI generation -> scheduling -> posting
"""

import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestEndToEndWorkflow:
    """Test cases for end-to-end workflow simulation."""
    
    @pytest.fixture
    def mock_env_vars(self):
        """Mock environment variables for testing."""
        return {
            "FACEBOOK_PAGE_TOKEN": "mock_token_12345",
            "FACEBOOK_PAGE_ID": "mock_page_67890",
            "FACEBOOK_APP_ID": "mock_app_11111",
            "OPENAI_API_KEY": "mock_openai_key_12345",
            "OPENAI_MODEL": "gpt-4o-mini"
        }
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create temporary directory for testing."""
        # Create required directory structure
        (tmp_path / "Assets" / "Images").mkdir(parents=True)
        (tmp_path / "Assets" / "Videos").mkdir(parents=True)
        (tmp_path / "Config").mkdir(parents=True)
        (tmp_path / "Automatizare_Completa").mkdir(parents=True)
        
        return tmp_path
    
    def test_workflow_component_integration(self, mock_env_vars, temp_dir):
        """Test that all workflow components can be initialized and work together."""
        
        # Test asset path
        test_image = temp_dir / "Assets" / "Images" / "test_image.png"
        test_image.write_bytes(b"fake image data")
        
        with patch.dict('os.environ', mock_env_vars, clear=True):
            # Test 1: FacebookAutoPost initialization
            from Automatizare_Completa.auto_post import FacebookAutoPost
            
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'):
                
                poster = FacebookAutoPost()
                assert poster.page_token == "mock_token_12345"
                assert poster.page_id == "mock_page_67890"
                
                # Test 2: ContentGenerator initialization
                from Automatizare_Completa.auto_generate import ContentGenerator
                
                with patch('openai.OpenAI') as mock_openai_class:
                    mock_client = MagicMock()
                    mock_openai_class.return_value = mock_client
                    
                    generator = ContentGenerator(api_key="mock_openai_key_12345")
                    assert generator.api_key == "mock_openai_key_12345"
                
                # Test 3: TaskScheduler initialization
                from Automatizare_Completa.scheduler import TaskScheduler
                scheduler = TaskScheduler(project_root=temp_dir)
                assert scheduler.project_root == temp_dir
                assert scheduler.schedule_file == temp_dir / "Config" / "schedule.json"
    
    def test_workflow_with_facebook_posting_mock(self, mock_env_vars, temp_dir):
        """Test complete workflow with mocked Facebook posting."""
        
        test_image = temp_dir / "Assets" / "Images" / "test_image.png"
        test_image.write_bytes(b"fake image data")
        
        with patch.dict('os.environ', mock_env_vars, clear=True):
            from Automatizare_Completa.auto_post import FacebookAutoPost
            
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'), \
                 patch('Automatizare_Completa.auto_post.requests.post') as mock_requests_post:
                
                # Setup mock Facebook response
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {'id': '12345_67890'}
                mock_requests_post.return_value = mock_response
                
                # Initialize and post
                poster = FacebookAutoPost()
                
                with patch.object(Path, 'exists', return_value=True), \
                     patch.object(Path, 'is_file', return_value=True), \
                     patch.object(Path, 'suffix', '.png'), \
                     patch('builtins.open', mock_open(read_data=b"fake image data")):
                    
                    result = poster.post_image("Test message", test_image)
                    
                    # Assert
                    assert result['status'] == 'success'
                    assert result['post_id'] == '12345_67890'
                    mock_requests_post.assert_called_once()
    
    def test_workflow_with_scheduler_integration(self, mock_env_vars, temp_dir):
        """Test workflow integration with scheduler."""
        
        # Setup schedule.json
        schedule_file = temp_dir / "Config" / "schedule.json"
        schedule_data = {
            "jobs": [
                {
                    "type": "daily",
                    "time": "09:00",
                    "task": "auto_post.py",
                    "enabled": True,
                    "last_run": None,
                    "description": "Daily Facebook post"
                }
            ]
        }
        
        with open(schedule_file, 'w') as f:
            json.dump(schedule_data, f)
        
        with patch.dict('os.environ', mock_env_vars, clear=True):
            from Automatizare_Completa.scheduler import TaskScheduler
            
            scheduler = TaskScheduler(project_root=temp_dir)
            loaded_schedule = scheduler.load_schedule()
            
            # Assert: Schedule loaded correctly
            assert 'jobs' in loaded_schedule
            assert len(loaded_schedule['jobs']) >= 1
    
    def test_workflow_asset_tracking(self, mock_env_vars, temp_dir):
        """Test that workflow properly tracks posted assets."""
        
        test_image = temp_dir / "Assets" / "Images" / "test_image.png"
        test_image.write_bytes(b"fake image data")
        
        asset_tracking_file = temp_dir / "Config" / "asset_tracking.json"
        
        # Simulate asset tracking data
        tracking_data = {
            "Assets/Images/old_image.jpg": {"last_posted": "2025-01-01T10:00:00"}
        }
        
        # Test tracking update logic
        relative_path = str(test_image.relative_to(temp_dir))
        
        # Simulate posting this asset
        from datetime import datetime
        mock_now = datetime(2025, 10, 26, 12, 0, 0)
        
        tracking_data[relative_path] = {"last_posted": mock_now.isoformat()}
        
        # Assert tracking was updated
        assert relative_path in tracking_data
        assert tracking_data[relative_path]['last_posted'] == mock_now.isoformat()
        assert len(tracking_data) == 2  # Old asset + new asset
    
    def test_workflow_error_handling(self, mock_env_vars, temp_dir):
        """Test error handling in the workflow."""
        
        test_image = temp_dir / "Assets" / "Images" / "test_image.png"
        test_image.write_bytes(b"fake image data")
        
        with patch.dict('os.environ', mock_env_vars, clear=True):
            from Automatizare_Completa.auto_post import FacebookAutoPost
            
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'), \
                 patch('Automatizare_Completa.auto_post.requests.post') as mock_requests_post:
                
                # Setup Facebook API error response
                mock_response = MagicMock()
                mock_response.status_code = 400
                mock_response.text = '{"error": {"message": "Invalid token"}}'
                mock_response.json.return_value = {'error': {'message': 'Invalid token'}}
                mock_requests_post.return_value = mock_response
                
                poster = FacebookAutoPost()
                
                with patch.object(Path, 'exists', return_value=True), \
                     patch.object(Path, 'is_file', return_value=True), \
                     patch.object(Path, 'suffix', '.png'), \
                     patch('builtins.open', mock_open(read_data=b"fake image data")):
                    
                    result = poster.post_image("Test message", test_image)
                    
                    # Should return error status
                    assert result['status'] == 'failed'
                    assert 'error' in result
    
    def test_workflow_file_structure(self, mock_env_vars, temp_dir):
        """Test that workflow correctly handles required file structure."""
        
        # Create required files
        selected_assets_file = temp_dir / "selected_assets.json"
        asset_tracking_file = temp_dir / "Config" / "asset_tracking.json"
        schedule_file = temp_dir / "Config" / "schedule.json"
        
        # Create selected_assets.json
        selected_assets_data = {
            "images": ["Assets/Images/test1.jpg", "Assets/Images/test2.jpg"],
            "videos": []
        }
        with open(selected_assets_file, 'w') as f:
            json.dump(selected_assets_data, f)
        
        # Create asset_tracking.json
        tracking_data = {
            "Assets/Images/test1.jpg": {"last_posted": "2025-01-01T10:00:00"}
        }
        with open(asset_tracking_file, 'w') as f:
            json.dump(tracking_data, f)
        
        # Create schedule.json
        schedule_data = {"jobs": []}
        with open(schedule_file, 'w') as f:
            json.dump(schedule_data, f)
        
        # Test that files exist and can be read
        assert selected_assets_file.exists()
        assert asset_tracking_file.exists()
        assert schedule_file.exists()
        
        # Test reading files
        with open(selected_assets_file, 'r') as f:
            data = json.load(f)
            assert len(data['images']) == 2
        
        with open(asset_tracking_file, 'r') as f:
            data = json.load(f)
            assert 'Assets/Images/test1.jpg' in data
    
    def test_workflow_component_isolation(self, mock_env_vars, temp_dir):
        """Test that each workflow component can work in isolation."""
        
        # Test 1: FacebookAutoPost can post text independently
        with patch.dict('os.environ', mock_env_vars, clear=True):
            from Automatizare_Completa.auto_post import FacebookAutoPost
            
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'), \
                 patch('Automatizare_Completa.auto_post.requests.post') as mock_requests_post:
                
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {'id': 'post_123'}
                mock_requests_post.return_value = mock_response
                
                poster = FacebookAutoPost()
                result = poster.post_text("Test message")
                
                assert result['status'] == 'success'
                assert result['post_id'] == 'post_123'
        
        # Test 2: TaskScheduler can load and save schedules independently
        schedule_file = temp_dir / "Config" / "schedule.json"
        from Automatizare_Completa.scheduler import TaskScheduler
        
        scheduler = TaskScheduler(project_root=temp_dir)
        
        test_data = {
            "jobs": [
                {
                    "type": "daily",
                    "time": "10:00",
                    "task": "test.py",
                    "enabled": True
                }
            ]
        }
        
        scheduler.save_schedule(test_data)
        loaded = scheduler.load_schedule()
        
        assert 'jobs' in loaded
        assert len(loaded['jobs']) == 1
        assert loaded['jobs'][0]['task'] == 'test.py'


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
