#!/usr/bin/env python3
"""
Facebook Auto Post Module
Handles automated posting to Facebook page
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secrets from environment
FACEBOOK_PAGE_TOKEN = os.getenv("FACEBOOK_PAGE_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FacebookAutoPost:
    """Handles Facebook posting operations."""
    
    def __init__(self):
        """Initialize Facebook Auto Post."""
        self.page_token = FACEBOOK_PAGE_TOKEN
        self.page_id = FACEBOOK_PAGE_ID
        self.app_id = FACEBOOK_APP_ID
        
        # Validate credentials
        if not all([self.page_token, self.page_id]):
            logger.error("Missing Facebook credentials in environment variables!")
            raise ValueError("Facebook credentials not properly configured")
        
        logger.info("Facebook Auto Post initialized")
        logger.info(f"Page ID: {self.page_id}")
    
    def post_text(self, message: str) -> Dict[str, Any]:
        """Post text message to Facebook page."""
        logger.info(f"Posting text message: {message[:50]}...")
        
        # Validate input
        if not message or not message.strip():
            logger.error("Empty message provided")
            return {"status": "failed", "error": "Message cannot be empty"}
        
        # Construct Graph API URL
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        
        # Prepare parameters
        params = {
            'message': message,
            'access_token': self.page_token
        }
        
        try:
            logger.info(f"Making API call to: {url}")
            logger.debug(f"Parameters: message length={len(message)}, token present={bool(self.page_token)}")
            
            # Make the API call
            response = requests.post(url, params=params, timeout=30)
            
            logger.info(f"API response status: {response.status_code}")
            
            if response.status_code == 200:
                # Success
                response_data = response.json()
                post_id = response_data.get('id')
                
                logger.info(f"✓ Post successful! Post ID: {post_id}")
                return {
                    "status": "success",
                    "post_id": post_id,
                    "message": "Post created successfully"
                }
            else:
                # Error
                error_text = response.text
                logger.error(f"✗ Post failed with status {response.status_code}: {error_text}")
                
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', error_text)
                except json.JSONDecodeError:
                    error_message = error_text
                
                return {
                    "status": "failed",
                    "error": error_message,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            logger.error("✗ Request timed out after 30 seconds")
            return {
                "status": "failed",
                "error": "Request timed out"
            }
        except requests.exceptions.ConnectionError:
            logger.error("✗ Connection error occurred")
            return {
                "status": "failed",
                "error": "Connection error"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Request exception: {str(e)}")
            return {
                "status": "failed",
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"✗ Unexpected error: {str(e)}")
            return {
                "status": "failed",
                "error": f"Unexpected error: {str(e)}"
            }
    
    def post_image(self, message: str, image_path: Path) -> Dict[str, Any]:
        """Post image with text to Facebook page."""
        # TODO: Implement Facebook Graph API call for image posting
        logger.info(f"Posting image: {image_path} with message: {message[:50]}...")
        return {"status": "pending", "message": "Not yet implemented"}
    
    def post_video(self, message: str, video_path: Path) -> Dict[str, Any]:
        """Post video with text to Facebook page."""
        # TODO: Implement Facebook Graph API call for video posting
        logger.info(f"Posting video: {video_path} with message: {message[:50]}...")
        return {"status": "pending", "message": "Not yet implemented"}
    
    def schedule_post(self, message: str, scheduled_time: datetime) -> Dict[str, Any]:
        """Schedule a post for future publishing."""
        # TODO: Implement scheduling logic
        logger.info(f"Scheduling post for {scheduled_time}: {message[:50]}...")
        return {"status": "pending", "message": "Not yet implemented"}
    
    def check_token_validity(self) -> bool:
        """Check if the current token is valid."""
        # TODO: Implement token validation
        logger.info("Checking token validity...")
        return bool(self.page_token)

def main():
    """Main function for testing."""
    print("="*60)
    print("Facebook Auto Post Module")
    print("="*60)
    
    # Check environment variables
    print(f"Page Token loaded: {'Yes' if FACEBOOK_PAGE_TOKEN else 'No'}")
    print(f"Page ID loaded: {'Yes' if FACEBOOK_PAGE_ID else 'No'}")
    print(f"App ID loaded: {'Yes' if FACEBOOK_APP_ID else 'No'}")
    
    if all([FACEBOOK_PAGE_TOKEN, FACEBOOK_PAGE_ID]):
        try:
            poster = FacebookAutoPost()
            print("\n✓ Facebook Auto Post initialized successfully")
            
            # Test token validity
            if poster.check_token_validity():
                print("✓ Token appears to be present")
                
                # Test post_text functionality
                print("\n" + "="*60)
                print("Testing post_text functionality...")
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                test_message = f"Test post from SocialBoost v3 via Cursor at {timestamp}"
                
                print(f"Test message: {test_message}")
                print("Making API call...")
                
                result = poster.post_text(test_message)
                
                print(f"\nResult: {result}")
                
                if result["status"] == "success":
                    print(f"✓ Post successful! Post ID: {result.get('post_id')}")
                else:
                    print(f"✗ Post failed: {result.get('error')}")
                    
            else:
                print("✗ Token validation failed")
                
        except Exception as e:
            print(f"\n✗ Initialization failed: {e}")
    else:
        print("\n✗ Missing required environment variables")
        print("Please ensure .env file is properly configured")

if __name__ == "__main__":
    main()
