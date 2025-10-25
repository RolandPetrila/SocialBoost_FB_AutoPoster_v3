#!/usr/bin/env python3
"""
Unit tests for Facebook Auto Post module
"""

import pytest
import os
import json
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

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
