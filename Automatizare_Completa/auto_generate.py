#!/usr/bin/env python3
"""
AI Content Generation Module
Handles automated content generation using OpenAI API
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secrets from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """Handles AI-powered content generation."""
    
    def __init__(self):
        """Initialize Content Generator."""
        self.api_key = OPENAI_API_KEY
        
        # Validate API key
        if not self.api_key:
            logger.error("Missing OpenAI API key in environment variables!")
            raise ValueError("OpenAI API key not configured")
        
        # Check if key looks valid (basic check)
        if not self.api_key.startswith("sk-"):
            logger.warning("OpenAI API key format might be invalid")
        
        logger.info("Content Generator initialized")
        logger.info(f"API Key loaded: {'Yes' if self.api_key else 'No'}")
    
    def generate_post_text(self, prompt: str, max_length: int = 500) -> str:
        """Generate post text based on prompt."""
        # TODO: Implement OpenAI API call
        logger.info(f"Generating text for prompt: {prompt[:50]}...")
        return f"[Generated content for: {prompt[:30]}...]"
    
    def generate_caption_for_image(self, image_path: Path, context: str = "") -> str:
        """Generate caption for an image using Vision API."""
        # TODO: Implement OpenAI Vision API call
        logger.info(f"Generating caption for image: {image_path}")
        return f"[Generated caption for {image_path.name}]"
    
    def improve_text(self, original_text: str) -> str:
        """Improve and optimize existing text."""
        # TODO: Implement text improvement logic
        logger.info("Improving text content...")
        return f"[Improved: {original_text[:30]}...]"
    
    def generate_hashtags(self, content: str, count: int = 5) -> List[str]:
        """Generate relevant hashtags for content."""
        # TODO: Implement hashtag generation
        logger.info(f"Generating {count} hashtags...")
        return ["#SocialBoost", "#FacebookMarketing", "#AI", "#Automation", "#Content"]
    
    def generate_variations(self, base_content: str, count: int = 3) -> List[str]:
        """Generate multiple variations of content."""
        # TODO: Implement content variation generation
        logger.info(f"Generating {count} content variations...")
        variations = []
        for i in range(count):
            variations.append(f"[Variation {i+1}: {base_content[:20]}...]")
        return variations
    
    def check_api_status(self) -> bool:
        """Check if OpenAI API is accessible."""
        # TODO: Implement API status check
        logger.info("Checking OpenAI API status...")
        return bool(self.api_key)

class PromptTemplates:
    """Predefined prompt templates for content generation."""
    
    FACEBOOK_POST = """Create an engaging Facebook post about {topic}.
    Make it friendly, conversational, and include a call-to-action.
    Maximum length: {max_length} characters."""
    
    PRODUCT_PROMOTION = """Write a promotional Facebook post for {product}.
    Highlight key benefits: {benefits}.
    Include emotional appeal and urgency.
    End with a clear call-to-action."""
    
    STORY_POST = """Tell a brief, engaging story about {topic}.
    Make it relatable and emotional.
    Connect it to {brand_message}."""
    
    QUESTION_POST = """Create an engaging question post about {topic}.
    Encourage audience interaction and comments.
    Make it thought-provoking but easy to answer."""

def main():
    """Main function for testing."""
    print("="*60)
    print("AI Content Generation Module")
    print("="*60)
    
    # Check environment variables
    print(f"OpenAI Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}")
    
    if OPENAI_API_KEY:
        # Mask the API key for display
        masked_key = OPENAI_API_KEY[:7] + "..." + OPENAI_API_KEY[-4:] if len(OPENAI_API_KEY) > 11 else "***"
        print(f"API Key format: {masked_key}")
        
        try:
            generator = ContentGenerator()
            print("\n✓ Content Generator initialized successfully")
            
            # Test API status
            if generator.check_api_status():
                print("✓ API key is present")
            else:
                print("✗ API status check failed")
            
            # Test generation (mock)
            print("\nTesting content generation (mock):")
            test_content = generator.generate_post_text("Test prompt")
            print(f"Generated: {test_content}")
            
            # Test hashtag generation
            hashtags = generator.generate_hashtags("Sample content")
            print(f"Hashtags: {', '.join(hashtags)}")
            
        except Exception as e:
            print(f"\n✗ Initialization failed: {e}")
    else:
        print("\n✗ OpenAI API key not found")
        print("Please ensure OPENAI_API_KEY is set in .env file")
    
    print("\nAvailable Templates:")
    print("- FACEBOOK_POST")
    print("- PRODUCT_PROMOTION")
    print("- STORY_POST")
    print("- QUESTION_POST")

if __name__ == "__main__":
    main()
