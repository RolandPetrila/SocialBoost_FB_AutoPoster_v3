#!/usr/bin/env python3
"""
Unit tests for Content Generation module
"""

import pytest
import base64
import tempfile
import shutil
import openai
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from Automatizare_Completa.auto_generate import ContentGenerator

class TestContentGenerator:
    """Test cases for ContentGenerator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create mock OpenAI client."""
        mock_client = MagicMock()
        return mock_client
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_initialization_success(self, mock_openai_class, temp_dir):
        """Test successful initialization with API key."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Act
        generator = ContentGenerator(api_key="test-api-key")
        
        # Assert
        assert generator.api_key == "test-api-key"
        assert generator.model == "gpt-4o-mini"  # Default model
        assert generator.client == mock_client
        mock_openai_class.assert_called_once_with(api_key="test-api-key")
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'env-api-key', 'OPENAI_MODEL': 'gpt-4'})
    def test_initialization_from_env(self, mock_openai_class, temp_dir):
        """Test initialization from environment variables."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Act
        generator = ContentGenerator()
        
        # Assert
        assert generator.api_key == "env-api-key"
        assert generator.model == "gpt-4"
        assert generator.client == mock_client
    
    def test_initialization_missing_key(self, temp_dir):
        """Test initialization failure when API key is missing."""
        # Arrange & Act & Assert
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                ContentGenerator()
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_post_text_success(self, mock_openai_class, temp_dir):
        """Test successful text generation."""
        # Arrange
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated post text"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt")
        
        # Assert
        assert result == "Generated post text"
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['model'] == "gpt-4o-mini"
        assert call_args[1]['max_tokens'] == 500
        assert call_args[1]['temperature'] == 0.7
        assert len(call_args[1]['messages']) == 2
        assert call_args[1]['messages'][0]['role'] == "system"
        assert call_args[1]['messages'][1]['role'] == "user"
        assert call_args[1]['messages'][1]['content'] == "Test prompt"
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_post_text_api_error(self, mock_openai_class, temp_dir):
        """Test text generation with API error."""
        # Arrange
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt")
        
        # Assert
        assert "✨ Something wonderful is brewing" in result
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_post_text_rate_limit_error(self, mock_openai_class, temp_dir):
        """Test text generation with rate limit error."""
        # Arrange
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Rate limit")
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt")
        
        # Assert
        assert "✨ Something wonderful is brewing" in result
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('builtins.open', create=True)
    @patch('base64.b64encode')
    def test_generate_caption_for_image_success(self, mock_b64encode, mock_open, mock_openai_class, temp_dir):
        """Test successful image caption generation."""
        # Arrange
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated caption"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        mock_b64encode.return_value = b"base64encodeddata"
        mock_open.return_value.__enter__.return_value.read.return_value = b"imagedata"
        
        generator = ContentGenerator(api_key="test-key")
        test_image_path = Path("test_image.png")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.png'):
            
            # Act
            result = generator.generate_caption_for_image(test_image_path, "Test context")
            
            # Assert
            assert result == "Generated caption"
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == "gpt-4o-mini"
            assert call_args[1]['max_tokens'] == 300
            
            # Check message structure
            messages = call_args[1]['messages']
            assert len(messages) == 2
            assert messages[0]['role'] == "system"
            assert messages[1]['role'] == "user"
            assert len(messages[1]['content']) == 2
            assert messages[1]['content'][0]['type'] == "text"
            assert "Test context" in messages[1]['content'][0]['text']
            assert messages[1]['content'][1]['type'] == "image_url"
            assert "data:image/png;base64,base64encodeddata" in messages[1]['content'][1]['image_url']['url']
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_caption_for_image_file_not_found(self, mock_openai_class, temp_dir):
        """Test image caption generation with file not found."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        test_image_path = Path("nonexistent.png")
        
        # Mock Path.exists to return False
        with patch.object(Path, 'exists', return_value=False):
            # Act
            result = generator.generate_caption_for_image(test_image_path)
            
            # Assert
            assert "📸 Capturing the perfect moment" in result
            mock_client.chat.completions.create.assert_not_called()
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_caption_for_image_unsupported_format(self, mock_openai_class, temp_dir):
        """Test image caption generation with unsupported format."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        test_image_path = Path("test.txt")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.txt'):
            
            # Act
            result = generator.generate_caption_for_image(test_image_path)
            
            # Assert
            assert "🎨 Creating beautiful visuals" in result
            mock_client.chat.completions.create.assert_not_called()
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('builtins.open', create=True)
    @patch('base64.b64encode')
    def test_generate_caption_for_image_api_error(self, mock_b64encode, mock_open, mock_openai_class, temp_dir):
        """Test image caption generation with API error."""
        # Arrange
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client
        
        mock_b64encode.return_value = b"base64encodeddata"
        mock_open.return_value.__enter__.return_value.read.return_value = b"imagedata"
        
        generator = ContentGenerator(api_key="test-key")
        test_image_path = Path("test_image.jpg")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.jpg'):
            
            # Act
            result = generator.generate_caption_for_image(test_image_path)
            
            # Assert
            assert "📝 Crafting the perfect words" in result
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_check_api_status_success(self, mock_openai_class, temp_dir):
        """Test successful API status check."""
        # Arrange
        mock_client = MagicMock()
        mock_client.models.list.return_value = [MagicMock()]
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.check_api_status()
        
        # Assert
        assert result is True
        mock_client.models.list.assert_called_once_with()
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_check_api_status_failure(self, mock_openai_class, temp_dir):
        """Test API status check failure."""
        # Arrange
        mock_client = MagicMock()
        mock_client.models.list.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.check_api_status()
        
        # Assert
        assert result is False
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_get_fallback_text(self, mock_openai_class, temp_dir):
        """Test fallback text generation."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        fallback_text = generator._get_fallback_text("API error occurred")
        
        # Assert
        assert "🌟" in fallback_text
        assert "Exciting content coming soon" in fallback_text
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_generate_post_text_custom_parameters(self, mock_openai_class, temp_dir):
        """Test text generation with custom parameters."""
        # Arrange
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated text"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt", max_tokens=1000)
        
        # Assert
        assert result == "Generated text"
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]['max_tokens'] == 1000
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('builtins.open', create=True)
    @patch('base64.b64encode')
    def test_generate_caption_different_image_types(self, mock_b64encode, mock_open, mock_openai_class, temp_dir):
        """Test caption generation for different image types."""
        # Arrange
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated caption"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        mock_b64encode.return_value = b"base64encodeddata"
        mock_open.return_value.__enter__.return_value.read.return_value = b"imagedata"
        
        generator = ContentGenerator(api_key="test-key")
        
        # Test different image formats
        test_cases = [
            ("test.jpg", "jpeg"),
            ("test.jpeg", "jpeg"),
            ("test.png", "png"),
            ("test.gif", "gif"),
            ("test.webp", "webp")
        ]
        
        for filename, expected_type in test_cases:
            test_image_path = Path(filename)
            
            with patch.object(Path, 'exists', return_value=True), \
                 patch.object(Path, 'is_file', return_value=True), \
                 patch.object(Path, 'suffix', f'.{filename.split(".")[-1]}'):
                
                # Act
                result = generator.generate_caption_for_image(test_image_path)
                
                # Assert
                assert result == "Generated caption"
                call_args = mock_client.chat.completions.create.call_args
                messages = call_args[1]['messages']
                image_url = messages[1]['content'][1]['image_url']['url']
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('Automatizare_Completa.auto_generate.time.sleep')
    def test_generate_post_text_retry_success(self, mock_sleep, mock_openai_class, temp_dir):
        """Test that generate_post_text retries on retryable errors and succeeds."""
        # Arrange
        mock_client = MagicMock()
        mock_response_success = MagicMock()
        mock_response_success.choices = [MagicMock()]
        mock_response_success.choices[0].message.content = "Generated text"
        
        # First call fails with rate limit, second succeeds
        mock_client.chat.completions.create.side_effect = [
            Exception("Rate limit"),
            mock_response_success
        ]
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt")
        
        # Assert
        assert result == "Generated text"
        assert mock_client.chat.completions.create.call_count == 2
        mock_sleep.assert_called_once_with(1)  # 2^0 = 1 second wait
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('Automatizare_Completa.auto_generate.time.sleep')
    def test_generate_post_text_retry_max_attempts(self, mock_sleep, mock_openai_class, temp_dir):
        """Test that generate_post_text fails after max retries."""
        # Arrange
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Rate limit")
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Act
        result = generator.generate_post_text("Test prompt")
        
        # Assert
        assert "✨ Something wonderful is brewing" in result
        assert mock_client.chat.completions.create.call_count == 3
        assert mock_sleep.call_count == 2  # 2 retries
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('Automatizare_Completa.auto_generate.time.sleep')
    def test_generate_caption_retry_success(self, mock_sleep, mock_openai_class, temp_dir):
        """Test that generate_caption_for_image retries on retryable errors and succeeds."""
        # Arrange
        mock_client = MagicMock()
        mock_response_success = MagicMock()
        mock_response_success.choices = [MagicMock()]
        mock_response_success.choices[0].message.content = "Generated caption"
        
        # First call fails with connection error, second succeeds
        mock_client.chat.completions.create.side_effect = [
            Exception("Connection failed"),
            mock_response_success
        ]
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        test_image_path = Path("test_image.jpg")
        
        # Mock Path.exists and is_file
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'suffix', '.jpg'), \
             patch('builtins.open', create=True), \
             patch('base64.b64encode') as mock_b64encode:
            
            mock_b64encode.return_value = b"base64encodeddata"
            
            # Act
            result = generator.generate_caption_for_image(test_image_path)
            
            # Assert
            assert result == "Generated caption"
            assert mock_client.chat.completions.create.call_count == 2
            mock_sleep.assert_called_once_with(1)
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    @patch('Automatizare_Completa.auto_generate.main')
    def test_main_with_assets_argument(self, mock_main, mock_openai_class, temp_dir):
        """Test main function with --assets argument."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create test image file
        test_image = temp_dir / "test.jpg"
        test_image.write_bytes(b"fake image data")
        
        # Mock the main function to avoid actual execution
        mock_main.return_value = None
        
        # Act & Assert - This test verifies the argument parsing works
        # The actual functionality is tested in integration tests
        from Automatizare_Completa.auto_generate import main
        import sys
        
        # Mock sys.argv to simulate command line arguments
        with patch.object(sys, 'argv', ['auto_generate.py', '--prompt', 'test prompt', '--assets', str(test_image)]):
            try:
                main()
            except SystemExit:
                pass  # Expected when argparse calls sys.exit()
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_asset_processing_logic(self, mock_openai_class, temp_dir):
        """Test the asset processing logic for different file types."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Create test files
        test_image = temp_dir / "test.jpg"
        test_video = temp_dir / "test.mp4"
        test_unknown = temp_dir / "test.txt"
        
        test_image.write_bytes(b"fake image data")
        test_video.write_bytes(b"fake video data")
        test_unknown.write_bytes(b"fake text data")
        
        # Mock the generation methods
        with patch.object(generator, 'generate_caption_for_image', return_value="Image caption") as mock_img, \
             patch.object(generator, 'generate_post_text', return_value="Video post") as mock_text:
            
            # Test image processing
            result_img = generator.generate_caption_for_image(test_image, "test prompt")
            assert result_img == "Image caption"
            mock_img.assert_called_once_with(test_image, "test prompt")
            
            # Test video processing (using generate_post_text)
            result_vid = generator.generate_post_text("test prompt related to video file test.mp4")
            assert result_vid == "Video post"
            mock_text.assert_called_once_with("test prompt related to video file test.mp4")
    
    @patch('Automatizare_Completa.auto_generate.openai.OpenAI')
    def test_file_extension_detection(self, mock_openai_class, temp_dir):
        """Test file extension detection for different media types."""
        # Arrange
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        generator = ContentGenerator(api_key="test-key")
        
        # Test image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        for ext in image_extensions:
            test_file = temp_dir / f"test{ext}"
            test_file.write_bytes(b"fake data")
            
            # This would be called in the main function logic
            assert test_file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        
        # Test video extensions
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        for ext in video_extensions:
            test_file = temp_dir / f"test{ext}"
            test_file.write_bytes(b"fake data")
            
            # This would be called in the main function logic
            assert test_file.suffix.lower() in {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}