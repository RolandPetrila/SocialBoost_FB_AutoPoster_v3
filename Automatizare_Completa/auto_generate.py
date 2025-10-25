#!/usr/bin/env python3
"""
Content Generation Module - OpenAI Integration
Handles automated content generation using OpenAI API for text and vision
"""

import os
import sys
import base64
import logging
import openai
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """OpenAI-powered content generation system."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the content generator with OpenAI API key."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file.")
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            logger.info(f"ContentGenerator initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def generate_post_text(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate social media post text using OpenAI."""
        logger.info(f"Generating post text for prompt: {prompt[:50]}...")
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a social media content creator. Generate engaging, authentic posts for Facebook. Keep posts conversational, engaging, and appropriate for a general audience. Include relevant hashtags when appropriate."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            logger.info(f"Making OpenAI API call with model: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            generated_text = response.choices[0].message.content
            logger.info(f"✓ Generated text successfully ({len(generated_text)} characters)")
            
            return generated_text
            
        except openai.APIError as e:
            logger.error(f"✗ OpenAI API error: {e}")
            return self._get_fallback_text("API error occurred")
        except openai.RateLimitError as e:
            logger.error(f"✗ OpenAI rate limit error: {e}")
            return self._get_fallback_text("Rate limit exceeded")
        except TimeoutError as e:
            logger.error(f"✗ OpenAI timeout error: {e}")
            return self._get_fallback_text("Request timed out")
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            return self._get_fallback_text("Generation failed")
    
    def generate_caption_for_image(self, image_path: Path, context_prompt: str = "") -> str:
        """Generate caption for an image using OpenAI Vision."""
        logger.info(f"Generating caption for image: {image_path}")
        
        # Validate image file
        if not image_path.exists() or not image_path.is_file():
            logger.error(f"Image file not found: {image_path}")
            return self._get_fallback_text("Image file not found")
        
        # Check file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        if image_path.suffix.lower() not in valid_extensions:
            logger.error(f"Unsupported image format: {image_path.suffix}")
            return self._get_fallback_text("Unsupported image format")
        
        try:
            # Read and encode image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Determine image type
            image_type = "jpeg"
            if image_path.suffix.lower() in ['.png']:
                image_type = "png"
            elif image_path.suffix.lower() in ['.gif']:
                image_type = "gif"
            elif image_path.suffix.lower() in ['.webp']:
                image_type = "webp"
            
            # Construct data URL
            data_url = f"data:image/{image_type};base64,{base64_image}"
            
            # Build messages for Vision API
            messages = [
                {
                    "role": "system",
                    "content": "You are a social media content creator. Analyze the provided image and generate an engaging caption for Facebook. Make it conversational, relevant to the image content, and include appropriate hashtags. Keep it under 200 characters."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Generate a Facebook caption for this image.{' ' + context_prompt if context_prompt else ''}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ]
            
            logger.info(f"Making OpenAI Vision API call with model: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            generated_caption = response.choices[0].message.content
            logger.info(f"✓ Generated caption successfully ({len(generated_caption)} characters)")
            
            return generated_caption
            
        except openai.APIError as e:
            logger.error(f"✗ OpenAI API error: {e}")
            return self._get_fallback_text("API error occurred")
        except openai.RateLimitError as e:
            logger.error(f"✗ OpenAI rate limit error: {e}")
            return self._get_fallback_text("Rate limit exceeded")
        except TimeoutError as e:
            logger.error(f"✗ OpenAI timeout error: {e}")
            return self._get_fallback_text("Request timed out")
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            return self._get_fallback_text("Caption generation failed")
    
    def check_api_status(self) -> bool:
        """Check if OpenAI API is accessible."""
        try:
            logger.info("Checking OpenAI API status...")
            models = self.client.models.list(limit=1)
            logger.info("✓ OpenAI API is accessible")
            return True
        except Exception as e:
            logger.error(f"✗ OpenAI API check failed: {e}")
            return False
    
    def _get_fallback_text(self, error_type: str) -> str:
        """Generate fallback text when API calls fail."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        fallback_texts = {
            "API error occurred": f"🌟 Exciting content coming soon! Stay tuned for more updates. #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Rate limit exceeded": f"⏰ Taking a quick break! More amazing content will be shared soon. #SocialBoost #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Request timed out": f"🚀 Great things take time! Stay connected for upcoming posts. #Patience #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Generation failed": f"✨ Something wonderful is brewing! Check back soon for fresh content. #ComingSoon #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Image file not found": f"📸 Capturing the perfect moment! New visual content coming soon. #VisualStory #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Unsupported image format": f"🎨 Creating beautiful visuals! Stay tuned for amazing image content. #VisualContent #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}",
            "Caption generation failed": f"📝 Crafting the perfect words! Caption coming soon. #ContentCreation #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}"
        }
        
        return fallback_texts.get(error_type, f"🌟 Amazing content coming soon! Stay tuned! #{timestamp.replace('-', '').replace(' ', '').replace(':', '')}")

def main():
    """Main entry point for content generation testing."""
    try:
        print("="*60)
        print("OpenAI Content Generation Test")
        print("="*60)
        
        # Initialize generator
        generator = ContentGenerator()
        
        # Check API status
        print("\n1. Checking OpenAI API status...")
        if generator.check_api_status():
            print("✓ OpenAI API is accessible")
        else:
            print("✗ OpenAI API check failed")
            return
        
        # Test text generation
        print("\n2. Testing text generation...")
        text_prompt = "Create a motivational post about productivity and time management for entrepreneurs"
        print(f"Prompt: {text_prompt}")
        print("Generating text...")
        
        generated_text = generator.generate_post_text(text_prompt)
        print(f"\nGenerated Text ({len(generated_text)} characters):")
        print("-" * 40)
        print(generated_text)
        print("-" * 40)
        
        # Test image caption generation
        print("\n3. Testing image caption generation...")
        
        # Check for test image
        test_image_path = Path("Assets/Images/test_image.png")
        if not test_image_path.exists():
            # Create a placeholder image for testing
            test_image_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Creating placeholder image at: {test_image_path}")
            
            # Create a simple PNG placeholder (1x1 pixel)
            png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
            
            with open(test_image_path, 'wb') as f:
                f.write(png_data)
        
        if test_image_path.exists():
            context_prompt = "This is a motivational image about success"
            print(f"Image: {test_image_path}")
            print(f"Context: {context_prompt}")
            print("Generating caption...")
            
            generated_caption = generator.generate_caption_for_image(test_image_path, context_prompt)
            print(f"\nGenerated Caption ({len(generated_caption)} characters):")
            print("-" * 40)
            print(generated_caption)
            print("-" * 40)
        else:
            print("✗ Could not create test image")
        
        print("\n" + "="*60)
        print("Content generation test completed!")
        print("="*60)
        
    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("Please set OPENAI_API_KEY in your .env file")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == "__main__":
    main()