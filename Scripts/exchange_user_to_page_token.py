#!/usr/bin/env python3
"""
Facebook Token Exchange Script
Exchanges short-lived user token for long-lived page token
"""

import os
import sys
import requests
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv, set_key

# Load environment variables
load_dotenv()

# Configuration from environment
TARGET_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
APP_ID = os.getenv("FACEBOOK_APP_ID")
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

# Validate required environment variables
if not all([TARGET_PAGE_ID, APP_ID, APP_SECRET]):
    print("Error: Missing required environment variables!")
    print("Please ensure FACEBOOK_PAGE_ID, FACEBOOK_APP_ID, and FACEBOOK_APP_SECRET are set in .env")
    sys.exit(1)

def exchange_for_long_lived_user_token(short_lived_token):
    """Exchange short-lived user token for long-lived user token."""
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": short_lived_token
    }
    
    print(f"Exchanging short-lived token for long-lived user token...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Successfully obtained long-lived user token")
        print(f"  - Expires in: {data.get('expires_in', 'unknown')} seconds")
        return data["access_token"]
    else:
        print(f"✗ Failed to exchange token: {response.status_code}")
        print(f"  Error: {response.text}")
        return None

def get_page_access_token(user_token):
    """Get long-lived page access token using long-lived user token."""
    url = f"https://graph.facebook.com/v18.0/{TARGET_PAGE_ID}"
    params = {
        "fields": "access_token,name,id",
        "access_token": user_token
    }
    
    print(f"Fetching page access token for page ID: {TARGET_PAGE_ID}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Successfully obtained page access token")
        print(f"  - Page Name: {data.get('name', 'unknown')}")
        print(f"  - Page ID: {data.get('id', 'unknown')}")
        return data.get("access_token")
    else:
        print(f"✗ Failed to get page token: {response.status_code}")
        print(f"  Error: {response.text}")
        return None

def verify_token(token):
    """Verify token and get debug info."""
    url = "https://graph.facebook.com/v18.0/debug_token"
    params = {
        "input_token": token,
        "access_token": f"{APP_ID}|{APP_SECRET}"
    }
    
    print("Verifying token...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        
        # Check if token is valid
        is_valid = data.get('is_valid', False)
        
        print(f"✓ Token verified successfully")
        print(f"  - Type: {data.get('type', 'unknown')}")
        print(f"  - App ID: {data.get('app_id', 'unknown')}")
        print(f"  - Valid: {is_valid}")
        
        if data.get('expires_at'):
            expires_at = datetime.fromtimestamp(data['expires_at'])
            print(f"  - Expires at: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"  - Expires: Never (permanent token)")
        
        return is_valid
    else:
        print(f"✗ Token verification failed: {response.status_code}")
        return False

def update_env_file(token):
    """Update the .env file with new page token."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("Error: .env file not found!")
        return False
    
    try:
        # Use python-dotenv's set_key to update the value
        set_key(env_path, "FACEBOOK_PAGE_TOKEN", token)
        print(f"✓ Updated FACEBOOK_PAGE_TOKEN in .env file")
        return True
    except Exception as e:
        print(f"✗ Failed to update .env file: {e}")
        return False

def main():
    """Main execution flow."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Exchange Facebook user token for page token',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--check-only', action='store_true',
                        help='Only check if the current page token in .env is valid')
    parser.add_argument('--user-token', type=str,
                        help='User token to use (non-interactive mode)')
    
    args = parser.parse_args()
    
    # Handle --check-only mode
    if args.check_only:
        print("="*60)
        print("Facebook Token Check Mode")
        print("="*60)
        
        # Load current page token from .env
        page_token = os.getenv("FACEBOOK_PAGE_TOKEN")
        
        if not page_token or page_token.strip() == "":
            print("\n✗ No FACEBOOK_PAGE_TOKEN found in .env file")
            sys.exit(2)
        
        print(f"\nChecking token: {page_token[:20]}...{page_token[-10:]}")
        
        # Verify the token
        is_valid = verify_token(page_token)
        
        if is_valid:
            print("\n✓ Token is VALID")
            sys.exit(0)
        else:
            print("\n✗ Token is INVALID or EXPIRED")
            sys.exit(1)
    
    # Normal token exchange flow
    print("="*60)
    print("Facebook Token Exchange Script")
    print("="*60)
    
    # Get user token
    user_token = args.user_token if args.user_token else os.getenv("FACEBOOK_USER_TOKEN")
    
    if not user_token or user_token.strip() == "":
        print("\nNo user token found in .env file or command-line argument.")
        user_token = input("Please enter your short-lived user token: ").strip()
        
        if not user_token:
            print("Error: No token provided!")
            sys.exit(1)
    
    # Step 1: Exchange for long-lived user token
    long_lived_user_token = exchange_for_long_lived_user_token(user_token)
    if not long_lived_user_token:
        print("\n✗ Token exchange failed!")
        sys.exit(1)
    
    # Step 2: Get page access token
    page_token = get_page_access_token(long_lived_user_token)
    if not page_token:
        print("\n✗ Failed to get page token!")
        sys.exit(1)
    
    # Step 3: Verify the page token
    print("\n" + "="*60)
    is_valid = verify_token(page_token)
    if is_valid:
        print("\n✓ Page token is valid and ready to use!")
    else:
        print("\n⚠ Warning: Token verification failed, but token might still work")
    
    # Step 4: Update .env file
    print("\n" + "="*60)
    if update_env_file(page_token):
        print("\n✓ SUCCESS: Long-lived page token has been saved to .env file")
        print("  You can now use this token for posting to your Facebook page")
    else:
        print("\n⚠ Could not update .env file automatically")
        print(f"  Please manually update FACEBOOK_PAGE_TOKEN in .env with:")
        print(f"  {page_token[:20]}...{page_token[-10:]}")
    
    print("\n" + "="*60)
    print("Token exchange completed!")
    print("="*60)

if __name__ == "__main__":
    main()
