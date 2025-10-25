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
        logger.info(f"Posting image: {image_path} with message: {message[:50]}...")
        
        # Validate input
        if not message or not message.strip():
            logger.error("Empty message provided")
            return {"status": "failed", "error": "Message cannot be empty"}
        
        # Validate image file
        if not image_path.exists() or not image_path.is_file():
            logger.error(f"Image file not found or invalid: {image_path}")
            return {"status": "failed", "error": "Image file not found or invalid"}
        
        # Check file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        if image_path.suffix.lower() not in valid_extensions:
            logger.error(f"Unsupported image format: {image_path.suffix}")
            return {"status": "failed", "error": f"Unsupported image format: {image_path.suffix}"}
        
        # Construct Graph API URL for photos
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/photos"
        
        # Prepare payload (data, not params for file upload)
        payload = {
            'message': message,
            'access_token': self.page_token
        }
        
        try:
            logger.info(f"Making API call to: {url}")
            logger.debug(f"Image path: {image_path}, message length: {len(message)}")
            
            # Open image file and make the API call
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                
                # Make the API call with longer timeout for file upload
                response = requests.post(url, data=payload, files=files, timeout=120)
            
            logger.info(f"API response status: {response.status_code}")
            
            if response.status_code == 200:
                # Success
                response_data = response.json()
                post_id = response_data.get('id') or response_data.get('post_id')
                
                logger.info(f"✓ Image post successful! Post ID: {post_id}")
                return {
                    "status": "success",
                    "post_id": post_id,
                    "message": "Image post created successfully",
                    "image_path": str(image_path)
                }
            else:
                # Error
                error_text = response.text
                logger.error(f"✗ Image post failed with status {response.status_code}: {error_text}")
                
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', error_text)
                except json.JSONDecodeError:
                    error_message = error_text
                
                return {
                    "status": "failed",
                    "error": error_message,
                    "status_code": response.status_code,
                    "image_path": str(image_path)
                }
                
        except requests.exceptions.Timeout:
            logger.error("✗ Request timed out after 120 seconds")
            return {
                "status": "failed",
                "error": "Request timed out (image upload)",
                "image_path": str(image_path)
            }
        except requests.exceptions.ConnectionError:
            logger.error("✗ Connection error occurred")
            return {
                "status": "failed",
                "error": "Connection error",
                "image_path": str(image_path)
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Request exception: {str(e)}")
            return {
                "status": "failed",
                "error": f"Request error: {str(e)}",
                "image_path": str(image_path)
            }
        except FileNotFoundError:
            logger.error(f"✗ Image file not found: {image_path}")
            return {
                "status": "failed",
                "error": "Image file not found",
                "image_path": str(image_path)
            }
        except Exception as e:
            logger.error(f"✗ Unexpected error: {str(e)}")
            return {
                "status": "failed",
                "error": f"Unexpected error: {str(e)}",
                "image_path": str(image_path)
            }
    
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
                
                # Test post_image functionality
                print("\n" + "="*60)
                print("Testing post_image functionality...")
                
                # Check for test image
                test_image_path = Path("Assets/Images/test_image.png")
                if not test_image_path.exists():
                    # Create a placeholder image for testing
                    test_image_path.parent.mkdir(parents=True, exist_ok=True)
                    print(f"Creating placeholder image at: {test_image_path}")
                    
                    # Create a simple 1x1 pixel PNG
                    import struct
                    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
                    
                    with open(test_image_path, 'wb') as f:
                        f.write(png_data)
                
                if test_image_path.exists():
                    image_message = f"Test image post from SocialBoost v3 at {timestamp}"
                    print(f"Test image: {test_image_path}")
                    print(f"Image message: {image_message}")
                    print("Making image API call...")
                    
                    image_result = poster.post_image(image_message, test_image_path)
                    
                    print(f"\nImage Result: {image_result}")
                    
                    if image_result["status"] == "success":
                        print(f"✓ Image post successful! Post ID: {image_result.get('post_id')}")
                    else:
                        print(f"✗ Image post failed: {image_result.get('error')}")
                else:
                    print("✗ Could not create test image")
                    
            else:
                print("✗ Token validation failed")
                
        except Exception as e:
            print(f"\n✗ Initialization failed: {e}")
    else:
        print("\n✗ Missing required environment variables")
        print("Please ensure .env file is properly configured")

if __name__ == "__main__":
    main()
