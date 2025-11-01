#!/usr/bin/env python3
"""
Validate .env configuration and test Facebook API credentials
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Dict, Any
import requests
from dotenv import load_dotenv

def check_file_exists() -> Tuple[bool, str]:
    """Check if .env file exists."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        return True, f".env file found at: {env_file}"
    else:
        return False, f".env file NOT found at: {env_file}"

def check_required_variables() -> Tuple[bool, Dict[str, bool]]:
    """Check if all required environment variables are present and not empty."""
    required_vars = [
        'FACEBOOK_APP_ID',
        'FACEBOOK_APP_SECRET',
        'FACEBOOK_PAGE_ID',
        'FACEBOOK_PAGE_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    results = {}
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        is_present = bool(value and value.strip())
        results[var] = is_present
        if not is_present:
            all_present = False
    
    return all_present, results

def test_facebook_token() -> Tuple[bool, str]:
    """Test if Facebook token is valid by making API call."""
    token = os.getenv('FACEBOOK_PAGE_TOKEN')
    
    if not token:
        return False, "Token not found in environment"
    
    try:
        # Test token with /me endpoint
        url = "https://graph.facebook.com/v18.0/me"
        params = {'access_token': token}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token_name = data.get('name', 'Unknown')
            token_id = data.get('id', 'Unknown')
            return True, f"Valid token for: {token_name} (ID: {token_id})"
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            return False, f"Invalid token: {error_msg}"
            
    except requests.exceptions.Timeout:
        return False, "Request timed out - check internet connection"
    except requests.exceptions.ConnectionError:
        return False, "Connection error - check internet connection"
    except Exception as e:
        return False, f"Error testing token: {str(e)}"

def test_page_access() -> Tuple[bool, str]:
    """Test if Page ID is accessible with the token."""
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_TOKEN')
    
    if not page_id or not token:
        return False, "Page ID or token not found"
    
    try:
        # Get page info
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {
            'fields': 'name,id,access_token',
            'access_token': token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            page_name = data.get('name', 'Unknown')
            return True, f"Page accessible: {page_name} (ID: {page_id})"
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            return False, f"Cannot access page: {error_msg}"
            
    except Exception as e:
        return False, f"Error accessing page: {str(e)}"

def test_openai_key() -> Tuple[bool, str]:
    """Test if OpenAI API key is present (not validating with actual API call)."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return False, "OpenAI API key not found"
    
    if api_key.startswith('sk-') and len(api_key) > 20:
        return True, f"OpenAI key present (starts with 'sk-', length: {len(api_key)})"
    else:
        return False, "OpenAI key format seems invalid (should start with 'sk-')"

def display_result(check_name: str, passed: bool, message: str):
    """Display validation result with colored output."""
    icon = "✅" if passed else "❌"
    status = "PASS" if passed else "FAIL"
    print(f"{icon} {check_name}: {status}")
    print(f"   {message}")

def main():
    """Main validation routine."""
    print("="*60)
    print("Environment Validation & Facebook API Test")
    print("="*60)
    print()    
    # Load .env file
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    load_dotenv(env_path)
    
    results = []
    
    # Check 1: .env file exists
    print("🔍 Check 1: .env File Existence")
    passed, message = check_file_exists()
    display_result(".env File", passed, message)
    results.append(passed)
    print()    
    if not passed:
        print("💡 Tip: Run 'python Scripts/load_secrets.py' to create .env from Codespaces secrets")
        print()        
        sys.exit(1)    
    
    # Check 2: Required variables
    print("🔍 Check 2: Required Environment Variables")
    all_present, var_results = check_required_variables()
    
    for var, is_present in var_results.items():
        icon = "✅" if is_present else "❌"
        status = "Present" if is_present else "Missing"
        
        # Mask value if present
        value = os.getenv(var)
        if is_present and value:
            if len(value) > 10:
                masked = value[:4] + '*' * (len(value) - 8) + value[-4:]
            else:
                masked = '*' * len(value)
            print(f"   {icon} {var}: {status} ({masked})")
        else:
            print(f"   {icon} {var}: {status}")
    
    results.append(all_present)
    print()    
    if not all_present:
        print("💡 Tip: Add missing variables to GitHub Codespaces secrets")
        print()    
    
    # Check 3: Facebook token validity
    print("🔍 Check 3: Facebook Token Validity")
    passed, message = test_facebook_token()
    display_result("Token Validation", passed, message)
    results.append(passed)
    print()    
    # Check 4: Page access
    print("🔍 Check 4: Facebook Page Access")
    passed, message = test_page_access()
    display_result("Page Access", passed, message)
    results.append(passed)
    print()    
    # Check 5: OpenAI key
    print("🔍 Check 5: OpenAI API Key")
    passed, message = test_openai_key()
    display_result("OpenAI Key", passed, message)
    results.append(passed)
    print()    
    # Summary
    print("="*60)
    passed_count = sum(results)
    total_count = len(results)
    
    if all(results):
        print(f"✅ ALL CHECKS PASSED ({passed_count}/{total_count})")
        print("="*60)
        print("\n🚀 Your environment is ready!")
        print("   You can now run: python Automatizare_Completa/auto_post.py")
        print()        
        sys.exit(0)
    else:
        print(f"❌ SOME CHECKS FAILED ({passed_count}/{total_count} passed)")
        print("="*60)
        print("\n🔧 Fix the issues above before proceeding")
        print()        
        sys.exit(1)

if __name__ == "__main__":
    main()