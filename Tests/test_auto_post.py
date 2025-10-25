#!/usr/bin/env python3
"""
Unit tests for Facebook Auto Post module
"""

import pytest
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from Automatizare_Completa.auto_post import FacebookAutoPost

class TestFacebookAutoPost:
    """Test cases for FacebookAutoPost class."""
    
    @pytest.fixture
    def mock_env_vars(self):
        """Mock environment variables for testing."""
        return {
            "FACEBOOK_PAGE_TOKEN": "mock_token_12345",
            "FACEBOOK_PAGE_ID": "mock_page_67890",
            "FACEBOOK_APP_ID": "mock_app_11111"
        }
    
    @pytest.fixture
    def poster(self, mock_env_vars):
        """Create FacebookAutoPost instance with mocked environment."""
        with patch.dict(os.environ, mock_env_vars, clear=True):
            # Also need to patch the module-level variables
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'):
                return FacebookAutoPost()
    
    def test_initialization_with_valid_credentials(self, mock_env_vars):
        """Test successful initialization with valid credentials."""
        with patch.dict(os.environ, mock_env_vars, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'mock_token_12345'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page_67890'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'mock_app_11111'):
                poster = FacebookAutoPost()
                
                assert poster.page_token == "mock_token_12345"
                assert poster.page_id == "mock_page_67890"
                assert poster.app_id == "mock_app_11111"
    
    def test_initialization_with_missing_credentials(self):
        """Test initialization fails with missing credentials."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', None), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', None), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', None):
                with pytest.raises(ValueError, match="Facebook credentials not properly configured"):
                    FacebookAutoPost()
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    def test_post_text_success(self, mock_post, poster):
        """Test successful text posting."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': '12345_67890'}
        mock_post.return_value = mock_response
        
        test_message = "Hello World"
        
        # Act
        result = poster.post_text(test_message)
        
        # Assert
        expected_url = "https://graph.facebook.com/v18.0/mock_page_67890/feed"
        expected_params = {'message': test_message, 'access_token': 'mock_token_12345'}
        
        mock_post.assert_called_once_with(expected_url, params=expected_params, timeout=30)
        
        assert result['status'] == 'success'
        assert result['post_id'] == '12345_67890'
        assert result['message'] == 'Post created successfully'
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    def test_post_text_api_error(self, mock_post, poster):
        """Test text posting with API error."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": {"message": "Invalid token"}}'
        mock_response.json.return_value = {'error': {'message': 'Invalid token'}}
        mock_post.return_value = mock_response
        
        test_message = "Hello World"
        
        # Act
        result = poster.post_text(test_message)
        
        # Assert
        assert result['status'] == 'failed'
        assert result['error'] == 'Invalid token'
        assert result['status_code'] == 400
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    def test_post_text_network_error(self, mock_post, poster):
        """Test text posting with network error."""
        # Arrange
        mock_post.side_effect = Exception("Network error")
        
        test_message = "Hello World"
        
        # Act
        result = poster.post_text(test_message)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Network error' in result['error']
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    def test_post_text_timeout(self, mock_post, poster):
        """Test text posting with timeout."""
        # Arrange
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Request timed out")
        
        test_message = "Hello World"
        
        # Act
        result = poster.post_text(test_message)
        
        # Assert
        assert result['status'] == 'failed'
        assert result['error'] == 'Request timed out'
    
    def test_post_text_empty_message(self, poster):
        """Test posting empty message."""
        # Act
        result = poster.post_text("")
        
        # Assert
        assert result['status'] == 'failed'
        assert result['error'] == 'Message cannot be empty'
    
    def test_post_text_whitespace_only(self, poster):
        """Test posting whitespace-only message."""
        # Act
        result = poster.post_text("   \n\t   ")
        
        # Assert
        assert result['status'] == 'failed'
        assert result['error'] == 'Message cannot be empty'
    
    def test_check_token_validity(self, poster):
        """Test token validity check."""
        # Act
        result = poster.check_token_validity()
        
        # Assert
        assert result is True
    
    def test_check_token_validity_no_token(self):
        """Test token validity check with no token."""
        with patch.dict(os.environ, {"FACEBOOK_PAGE_ID": "mock_page"}, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', None), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'mock_page'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', None):
                with pytest.raises(ValueError, match="Facebook credentials not properly configured"):
                    FacebookAutoPost()
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('builtins.open', create=True)
    def test_post_image_success(self, mock_open, mock_post, poster):
        """Test successful image posting."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': '12345_67890'}
        mock_post.return_value = mock_response
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        test_message = "Hello World"
        test_image_path = Path("test_image.png")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.png'):
            
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            expected_url = "https://graph.facebook.com/v18.0/mock_page_67890/photos"
            expected_data = {'message': test_message, 'access_token': 'mock_token_12345'}
            expected_files = {'source': mock_file}
            
            mock_post.assert_called_once_with(
                expected_url, 
                data=expected_data, 
                files=expected_files, 
                timeout=120
            )
            
            assert result['status'] == 'success'
            assert result['post_id'] == '12345_67890'
            assert result['message'] == 'Image post created successfully'
            assert result['image_path'] == str(test_image_path)
    
    def test_post_image_file_not_found(self, poster):
        """Test image posting with file not found."""
        # Arrange
        test_message = "Hello World"
        test_image_path = Path("nonexistent.png")
        
        # Mock Path.exists to return False
        with patch.object(Path, 'exists', return_value=False):
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Image file not found or invalid'
    
    def test_post_image_invalid_file(self, poster):
        """Test image posting with invalid file."""
        # Arrange
        test_message = "Hello World"
        test_image_path = Path("test.txt")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=False), \
             patch.object(Path, 'suffix', '.txt'):
            
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Image file not found or invalid'
    
    def test_post_image_unsupported_format(self, poster):
        """Test image posting with unsupported format."""
        # Arrange
        test_message = "Hello World"
        test_image_path = Path("test.xyz")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.xyz'):
            
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Unsupported image format: .xyz'
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('builtins.open', create=True)
    def test_post_image_api_error(self, mock_open, mock_post, poster):
        """Test image posting with API error."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": {"message": "Invalid image format"}}'
        mock_response.json.return_value = {'error': {'message': 'Invalid image format'}}
        mock_post.return_value = mock_response
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        test_message = "Hello World"
        test_image_path = Path("test_image.png")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.png'):
            
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Invalid image format'
            assert result['status_code'] == 400
            assert result['image_path'] == str(test_image_path)
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('builtins.open', create=True)
    def test_post_image_timeout(self, mock_open, mock_post, poster):
        """Test image posting with timeout."""
        # Arrange
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Request timed out")
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        test_message = "Hello World"
        test_image_path = Path("test_image.png")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.png'):
            
            # Act
            result = poster.post_image(test_message, test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Request timed out (image upload)'
            assert result['image_path'] == str(test_image_path)
    
    def test_post_image_empty_message(self, poster):
        """Test posting image with empty message."""
        # Arrange
        test_image_path = Path("test_image.png")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.png'):
            
            # Act
            result = poster.post_image("", test_image_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Message cannot be empty'
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('Automatizare_Completa.auto_post.requests.get')
    @patch('builtins.open', create=True)
    def test_post_video_success(self, mock_open, mock_get, mock_post, poster):
        """Test successful video posting."""
        # Arrange
        mock_file = MagicMock()
        mock_file.read.side_effect = [b'chunk1', b'chunk2', b'']  # Simulate chunks
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock start upload response
        start_response = MagicMock()
        start_response.status_code = 200
        start_response.json.return_value = {
            'video_id': '12345_67890',
            'upload_session_id': 'session_123',
            'start_offset': 0
        }
        
        # Mock transfer responses
        transfer_response = MagicMock()
        transfer_response.status_code = 200
        transfer_response.json.return_value = {'start_offset': 1024}
        
        # Mock finish response
        finish_response = MagicMock()
        finish_response.status_code = 200
        finish_response.json.return_value = {'success': True}
        
        # Mock status check response
        status_response = MagicMock()
        status_response.status_code = 200
        status_response.json.return_value = {'status': 'ready'}
        
        mock_post.side_effect = [start_response, transfer_response, transfer_response, finish_response]
        mock_get.return_value = status_response
        
        test_message = "Hello World"
        test_video_path = Path("test_video.mp4")
        
        # Mock Path.exists, is_file, suffix, and stat
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.mp4'), \
             patch.object(Path, 'stat') as mock_stat:
            
            mock_stat.return_value.st_size = 2048
            
            # Act
            result = poster.post_video(test_message, test_video_path)
            
            # Assert
            assert result['status'] == 'success'
            assert result['video_id'] == '12345_67890'
            assert result['message'] == 'Video upload initiated successfully'
            assert result['video_path'] == str(test_video_path)
            assert result['file_size'] == 2048
    
    def test_post_video_file_not_found(self, poster):
        """Test video posting with file not found."""
        # Arrange
        test_message = "Hello World"
        test_video_path = Path("nonexistent.mp4")
        
        # Mock Path.exists to return False
        with patch.object(Path, 'exists', return_value=False):
            # Act
            result = poster.post_video(test_message, test_video_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Video file not found or invalid'
    
    def test_post_video_unsupported_format(self, poster):
        """Test video posting with unsupported format."""
        # Arrange
        test_message = "Hello World"
        test_video_path = Path("test.txt")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.txt'):
            
            # Act
            result = poster.post_video(test_message, test_video_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Unsupported video format: .txt'
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('builtins.open', create=True)
    def test_post_video_api_error_start(self, mock_open, mock_post, poster):
        """Test video posting with API error at start phase."""
        # Arrange
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock start upload error response
        start_response = MagicMock()
        start_response.status_code = 400
        start_response.text = '{"error": {"message": "Invalid video format"}}'
        start_response.json.return_value = {'error': {'message': 'Invalid video format'}}
        
        mock_post.return_value = start_response
        
        test_message = "Hello World"
        test_video_path = Path("test_video.mp4")
        
        # Mock Path.exists, is_file, suffix, and stat
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.mp4'), \
             patch.object(Path, 'stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            
            # Act
            result = poster.post_video(test_message, test_video_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert 'Start upload failed' in result['error']
            assert 'Invalid video format' in result['error']
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('builtins.open', create=True)
    def test_post_video_api_error_transfer(self, mock_open, mock_post, poster):
        """Test video posting with API error at transfer phase."""
        # Arrange
        mock_file = MagicMock()
        mock_file.read.side_effect = [b'chunk1', b'']  # Simulate chunks
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock start upload success response
        start_response = MagicMock()
        start_response.status_code = 200
        start_response.json.return_value = {
            'video_id': '12345_67890',
            'upload_session_id': 'session_123',
            'start_offset': 0
        }
        
        # Mock transfer error response
        transfer_response = MagicMock()
        transfer_response.status_code = 500
        transfer_response.text = '{"error": {"message": "Transfer failed"}}'
        transfer_response.json.return_value = {'error': {'message': 'Transfer failed'}}
        
        mock_post.side_effect = [start_response, transfer_response]
        
        test_message = "Hello World"
        test_video_path = Path("test_video.mp4")
        
        # Mock Path.exists, is_file, suffix, and stat
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.mp4'), \
             patch.object(Path, 'stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            
            # Act
            result = poster.post_video(test_message, test_video_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert 'Transfer failed' in result['error']
    
    def test_post_video_empty_message(self, poster):
        """Test posting video with empty message."""
        # Arrange
        test_video_path = Path("test_video.mp4")
        
        # Mock Path.exists, is_file, suffix, and stat
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.mp4'), \
             patch.object(Path, 'stat') as mock_stat:
            
            mock_stat.return_value.st_size = 1024
            
            # Act
            result = poster.post_video("", test_video_path)
            
            # Assert
            assert result['status'] == 'failed'
            assert result['error'] == 'Message cannot be empty'

class TestFacebookAutoPostIntegration:
    """Integration tests for FacebookAutoPost."""
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    def test_full_post_workflow(self, mock_post):
        """Test complete posting workflow."""
        # Arrange
        mock_env_vars = {
            "FACEBOOK_PAGE_TOKEN": "test_token",
            "FACEBOOK_PAGE_ID": "test_page",
            "FACEBOOK_APP_ID": "test_app"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'test_post_123'}
        mock_post.return_value = mock_response
        
        with patch.dict(os.environ, mock_env_vars, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'test_token'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'test_page'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'test_app'):
                poster = FacebookAutoPost()
                
                # Act
                result = poster.post_text("Integration test message")
                
                # Assert
                assert result['status'] == 'success'
                assert result['post_id'] == 'test_post_123'
                
                # Verify API call was made correctly
                mock_post.assert_called_once()
                call_args = mock_post.call_args
                
                assert call_args[0][0] == "https://graph.facebook.com/v18.0/test_page/feed"
                assert call_args[1]['params']['message'] == "Integration test message"
                assert call_args[1]['params']['access_token'] == "test_token"
                assert call_args[1]['timeout'] == 30

    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('Automatizare_Completa.auto_post.time.sleep')
    def test_post_text_retry_success(self, mock_sleep, mock_post):
        """Test that post_text retries on retryable errors and succeeds."""
        # Arrange
        mock_env_vars = {
            "FACEBOOK_PAGE_TOKEN": "test_token",
            "FACEBOOK_PAGE_ID": "test_page",
            "FACEBOOK_APP_ID": "test_app"
        }
        
        # First call fails with retryable error, second succeeds
        mock_response_fail = MagicMock()
        mock_response_fail.status_code = 500
        
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"id": "post_123"}
        
        mock_post.side_effect = [mock_response_fail, mock_response_success]
        
        with patch.dict(os.environ, mock_env_vars, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'test_token'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'test_page'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'test_app'):
                poster = FacebookAutoPost()
                
                # Act
                result = poster.post_text("Test message")
                
                # Assert
                assert result["status"] == "success"
                assert result["post_id"] == "post_123"
                assert mock_post.call_count == 2
                mock_sleep.assert_called_once_with(1)  # 2^0 = 1 second wait
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('Automatizare_Completa.auto_post.time.sleep')
    def test_post_text_retry_max_attempts(self, mock_sleep, mock_post):
        """Test that post_text fails after max retries."""
        # Arrange
        mock_env_vars = {
            "FACEBOOK_PAGE_TOKEN": "test_token",
            "FACEBOOK_PAGE_ID": "test_page",
            "FACEBOOK_APP_ID": "test_app"
        }
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        with patch.dict(os.environ, mock_env_vars, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'test_token'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'test_page'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'test_app'):
                poster = FacebookAutoPost()
                
                # Act
                result = poster.post_text("Test message")
                
                # Assert
                assert result["status"] == "failed"
                assert "failed after 3 attempts" in result["error"]
                assert mock_post.call_count == 3
                assert mock_sleep.call_count == 2  # 2 retries
    
    @patch('Automatizare_Completa.auto_post.requests.post')
    @patch('Automatizare_Completa.auto_post.time.sleep')
    def test_post_text_connection_error_retry(self, mock_sleep, mock_post):
        """Test that post_text retries on connection errors."""
        # Arrange
        mock_env_vars = {
            "FACEBOOK_PAGE_TOKEN": "test_token",
            "FACEBOOK_PAGE_ID": "test_page",
            "FACEBOOK_APP_ID": "test_app"
        }
        
        from requests.exceptions import ConnectionError
        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {"id": "post_123"}
        
        mock_post.side_effect = [ConnectionError("Connection failed"), mock_response_success]
        
        with patch.dict(os.environ, mock_env_vars, clear=True):
            with patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_TOKEN', 'test_token'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_PAGE_ID', 'test_page'), \
                 patch('Automatizare_Completa.auto_post.FACEBOOK_APP_ID', 'test_app'):
                poster = FacebookAutoPost()
                
                # Act
                result = poster.post_text("Test message")
                
                # Assert
                assert result["status"] == "success"
                assert result["post_id"] == "post_123"
                assert mock_post.call_count == 2
                mock_sleep.assert_called_once_with(1)  # 2^0 = 1 second wait

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
