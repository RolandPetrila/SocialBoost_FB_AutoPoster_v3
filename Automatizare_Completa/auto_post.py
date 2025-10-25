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
import time
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
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Making API call to: {url} (attempt {attempt + 1}/{max_retries})")
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
                elif response.status_code in [429, 500, 502, 503, 504]:
                    # Retryable errors
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Retryable error {response.status_code}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"✗ API call failed after {max_retries} attempts. Status: {response.status_code}")
                        return {
                            "status": "failed",
                            "error": f"API call failed after {max_retries} attempts. Status: {response.status_code}"
                        }
                else:
                    # Non-retryable errors
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
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Request timed out. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("✗ Request timed out after 30 seconds")
                    return {
                        "status": "failed",
                        "error": "Request timed out"
                    }
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Connection error. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("✗ Connection error occurred")
                    return {
                        "status": "failed",
                        "error": "Connection error"
                    }
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Request exception: {str(e)}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
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
        
        # This should never be reached, but just in case
        return {"status": "failed", "error": "Unexpected error in retry logic"}
    
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
        """Post video with text to Facebook page using resumable upload."""
        logger.info(f"Posting video: {video_path} with message: {message[:50]}...")
        
        # Validate input
        if not message or not message.strip():
            logger.error("Empty message provided")
            return {"status": "failed", "error": "Message cannot be empty"}
        
        # Validate video file
        if not video_path.exists() or not video_path.is_file():
            logger.error(f"Video file not found or invalid: {video_path}")
            return {"status": "failed", "error": "Video file not found or invalid"}
        
        # Check file extension
        valid_extensions = {'.mp4', '.mov', '.avi', '.wmv', '.mkv', '.flv', '.webm'}
        if video_path.suffix.lower() not in valid_extensions:
            logger.error(f"Unsupported video format: {video_path.suffix}")
            return {"status": "failed", "error": f"Unsupported video format: {video_path.suffix}"}
        
        # Get file size
        try:
            file_size = video_path.stat().st_size
            logger.info(f"Video file size: {file_size} bytes")
        except OSError as e:
            logger.error(f"Could not get file size: {str(e)}")
            return {"status": "failed", "error": f"Could not get file size: {str(e)}"}
        
        # Construct Graph API URL for videos
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/videos"
        
        try:
            # Stage 1: Start Upload Session
            logger.info("Starting video upload session...")
            start_params = {
                'upload_phase': 'start',
                'file_size': file_size,
                'access_token': self.page_token
            }
            
            start_response = requests.post(url, data=start_params, timeout=30)
            logger.info(f"Start upload response status: {start_response.status_code}")
            
            if start_response.status_code != 200:
                error_text = start_response.text
                logger.error(f"✗ Start upload failed with status {start_response.status_code}: {error_text}")
                try:
                    error_data = start_response.json()
                    error_message = error_data.get('error', {}).get('message', error_text)
                except json.JSONDecodeError:
                    error_message = error_text
                return {"status": "failed", "error": f"Start upload failed: {error_message}"}
            
            start_data = start_response.json()
            video_id = start_data.get('video_id')
            upload_session_id = start_data.get('upload_session_id')
            start_offset = start_data.get('start_offset', 0)
            
            logger.info(f"✓ Upload session started. Video ID: {video_id}, Session ID: {upload_session_id}")
            
            # Stage 2: Transfer File Chunks
            logger.info("Transferring video file chunks...")
            chunk_size = 4 * 1024 * 1024  # 4MB chunks
            current_offset = start_offset
            
            with open(video_path, 'rb') as video_file:
                while current_offset < file_size:
                    # Read chunk
                    chunk_data = video_file.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    logger.debug(f"Uploading chunk at offset {current_offset}, size {len(chunk_data)}")
                    
                    # Transfer chunk
                    transfer_params = {
                        'upload_phase': 'transfer',
                        'upload_session_id': upload_session_id,
                        'start_offset': current_offset,
                        'access_token': self.page_token
                    }
                    
                    files = {'video_file_chunk': chunk_data}
                    
                    transfer_response = requests.post(url, data=transfer_params, files=files, timeout=120)
                    
                    if transfer_response.status_code != 200:
                        error_text = transfer_response.text
                        logger.error(f"✗ Transfer failed at offset {current_offset}: {error_text}")
                        try:
                            error_data = transfer_response.json()
                            error_message = error_data.get('error', {}).get('message', error_text)
                        except json.JSONDecodeError:
                            error_message = error_text
                        return {"status": "failed", "error": f"Transfer failed: {error_message}"}
                    
                    transfer_data = transfer_response.json()
                    new_offset = transfer_data.get('start_offset', current_offset + len(chunk_data))
                    current_offset = new_offset
                    
                    logger.debug(f"✓ Chunk uploaded. New offset: {current_offset}")
            
            logger.info("✓ All chunks transferred successfully")
            
            # Stage 3: Finish Upload Session
            logger.info("Finishing video upload session...")
            finish_params = {
                'upload_phase': 'finish',
                'upload_session_id': upload_session_id,
                'description': message,
                'access_token': self.page_token
            }
            
            finish_response = requests.post(url, data=finish_params, timeout=30)
            logger.info(f"Finish upload response status: {finish_response.status_code}")
            
            if finish_response.status_code != 200:
                error_text = finish_response.text
                logger.error(f"✗ Finish upload failed with status {finish_response.status_code}: {error_text}")
                try:
                    error_data = finish_response.json()
                    error_message = error_data.get('error', {}).get('message', error_text)
                except json.JSONDecodeError:
                    error_message = error_text
                return {"status": "failed", "error": f"Finish upload failed: {error_message}"}
            
            finish_data = finish_response.json()
            success = finish_data.get('success', False)
            
            if not success:
                logger.error("✗ Upload finish returned success=False")
                return {"status": "failed", "error": "Upload finish failed"}
            
            logger.info(f"✓ Video upload completed successfully! Video ID: {video_id}")
            
            # Optional: Check video processing status
            logger.info("Checking video processing status...")
            max_checks = 10
            check_interval = 5  # seconds
            
            for check_num in range(max_checks):
                status_url = f"https://graph.facebook.com/v18.0/{video_id}"
                status_params = {
                    'fields': 'status',
                    'access_token': self.page_token
                }
                
                status_response = requests.get(status_url, params=status_params, timeout=30)
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    video_status = status_data.get('status', 'unknown')
                    logger.info(f"Video status check {check_num + 1}: {video_status}")
                    
                    if video_status == 'ready':
                        logger.info("✓ Video is ready for viewing")
                        break
                    elif video_status == 'failed':
                        logger.warning("⚠ Video processing failed")
                        break
                else:
                    logger.warning(f"Status check failed: {status_response.status_code}")
                
                if check_num < max_checks - 1:
                    time.sleep(check_interval)
            
            return {
                "status": "success",
                "video_id": video_id,
                "message": "Video upload initiated successfully",
                "video_path": str(video_path),
                "file_size": file_size
            }
            
        except requests.exceptions.Timeout:
            logger.error("✗ Request timed out")
            return {
                "status": "failed",
                "error": "Request timed out",
                "video_path": str(video_path)
            }
        except requests.exceptions.ConnectionError:
            logger.error("✗ Connection error occurred")
            return {
                "status": "failed",
                "error": "Connection error",
                "video_path": str(video_path)
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Request exception: {str(e)}")
            return {
                "status": "failed",
                "error": f"Request error: {str(e)}",
                "video_path": str(video_path)
            }
        except FileNotFoundError:
            logger.error(f"✗ Video file not found: {video_path}")
            return {
                "status": "failed",
                "error": "Video file not found",
                "video_path": str(video_path)
            }
        except Exception as e:
            logger.error(f"✗ Unexpected error: {str(e)}")
            return {
                "status": "failed",
                "error": f"Unexpected error: {str(e)}",
                "video_path": str(video_path)
            }
    
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
                
                # Test post_video functionality
                print("\n" + "="*60)
                print("Testing post_video functionality...")
                
                # Check for test video
                test_video_path = Path("Assets/Videos/test_video.mp4")
                if not test_video_path.exists():
                    # Create a placeholder video for testing
                    test_video_path.parent.mkdir(parents=True, exist_ok=True)
                    print(f"Creating placeholder video at: {test_video_path}")
                    
                    # Create a minimal MP4 file (just header, no actual video data)
                    mp4_header = b'\x00\x00\x00\x20ftypmp42\x00\x00\x00\x00mp41mp42isom\x00\x00\x00\x08mdat\x00\x00\x00\x00'
                    
                    with open(test_video_path, 'wb') as f:
                        f.write(mp4_header)
                
                if test_video_path.exists():
                    video_message = f"Test video post from SocialBoost v3 at {timestamp}"
                    print(f"Test video: {test_video_path}")
                    print(f"Video message: {video_message}")
                    print("Making video API call...")
                    
                    video_result = poster.post_video(video_message, test_video_path)
                    
                    print(f"\nVideo Result: {video_result}")
                    
                    if video_result["status"] == "success":
                        print(f"✓ Video post successful! Video ID: {video_result.get('video_id')}")
                    else:
                        print(f"✗ Video post failed: {video_result.get('error')}")
                else:
                    print("✗ Could not create test video")
                    
            else:
                print("✗ Token validation failed")
                
        except Exception as e:
            print(f"\n✗ Initialization failed: {e}")
    else:
        print("\n✗ Missing required environment variables")
        print("Please ensure .env file is properly configured")

if __name__ == "__main__":
    main()
