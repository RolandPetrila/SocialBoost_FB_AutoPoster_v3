#!/usr/bin/env python3
"""
Load secrets from GitHub Codespaces environment and create .env file
This script is safe to run - it only creates .env which is in .gitignore
"""

import os
import sys
from pathlib import Path

def load_secrets():
    """Load secrets from Codespaces environment variables and create .env file."""
    
    print("🔐 Loading secrets from Codespaces environment...")
    
    # Check if running in Codespaces
    if not os.getenv('CODESPACE_NAME'):
        print("⚠️  Warning: Not running in GitHub Codespaces")
        print("   Secrets may not be available")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            sys.exit(1)
    
    # Define required secrets
    required_secrets = {
        'FACEBOOK_APP_ID': 'Facebook App ID',
        'FACEBOOK_APP_SECRET': 'Facebook App Secret',
        'FACEBOOK_PAGE_ID': 'Facebook Page ID',
        'FACEBOOK_PAGE_TOKEN': 'Facebook Page Token (long-lived)',
        'OPENAI_API_KEY': 'OpenAI API Key'
    }
    
    # Load secrets from environment
    secrets = {}
    missing_secrets = []
    
    for env_var, description in required_secrets.items():
        value = os.getenv(env_var)
        if value:
            secrets[env_var] = value
            print(f"   ✓ {env_var}: Found")
        else:
            missing_secrets.append(env_var)
            print(f"   ✗ {env_var}: Missing")
    
    # Check if any secrets are missing
    if missing_secrets:
        print(f"\n❌ Missing {len(missing_secrets)} required secret(s):")
        for secret in missing_secrets:
            print(f"   - {secret}: {required_secrets[secret]}")
        print("\n📝 To add secrets:")
        print("   1. Go to: https://github.com/RolandPetrila/SocialBoost_FB_AutoPoster_v3/settings/secrets/codespaces")
        print("   2. Click 'New repository secret'")
        print("   3. Add each missing secret")
        print("   4. Restart Codespace or rebuild container")
        sys.exit(1)
    
    # Create .env file
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'
    
    print(f"\n📝 Creating .env file at: {env_file}")
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("# === SECRETS - AUTO-GENERATED FROM CODESPACES ===\n")
            f.write(f"# Generated: {os.popen('date').read().strip()}\n")
            f.write("# DO NOT COMMIT THIS FILE\n\n")
            
            f.write("# Facebook API Credentials\n")
            f.write(f"FACEBOOK_APP_ID={{secrets['FACEBOOK_APP_ID']}}\n")
            f.write(f"FACEBOOK_APP_SECRET={{secrets['FACEBOOK_APP_SECRET']}}\n")
            f.write(f"FACEBOOK_PAGE_ID={{secrets['FACEBOOK_PAGE_ID']}}\n")
            f.write(f"FACEBOOK_PAGE_TOKEN={{secrets['FACEBOOK_PAGE_TOKEN']}}\n\n")
            
            f.write("# OpenAI API Key\n")
            f.write(f"OPENAI_API_KEY={{secrets['OPENAI_API_KEY']}}\n\n")
            
            f.write("# === CONFIGURATIONS ===\n")
            f.write("PYTHONIOENCODING=utf-8\n")
            f.write("LOG_LEVEL=INFO\n")
        
        print("✅ .env file created successfully!\n")
        
        # Verify .env is in .gitignore
        gitignore_file = project_root / '.gitignore'
        if gitignore_file.exists():
            with open(gitignore_file, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            if '.env' in gitignore_content or '*.env' in gitignore_content:
                print("✅ .env is in .gitignore - safe from commits")
            else:
                print("⚠️  Warning: .env might not be in .gitignore!")
                print("   Run: echo '.env' >> .gitignore")
        
        # Display summary
        print("\n🔍 Secrets loaded:")
        for env_var in required_secrets.keys():
            value = secrets[env_var]
            # Mask the value for security
            if len(value) > 10:
                masked = value[:4] + '*' * (len(value) - 8) + value[-4:]
            else:
                masked = '*' * len(value)
            print(f"   ✓ {env_var}: {masked}")
        
        print("\n⚠️  Remember:")
        print("   - .env file is in .gitignore and will NOT be committed")
        print("   - Never share these credentials")
        print("   - Run 'python Scripts/validate_env.py' to test credentials")
        
        return True
        
    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {env_file}")
        return False
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    """Main entry point."""
    print("="*60)
    print("GitHub Codespaces Secrets → .env File")
    print("="*60)
    print()    
    success = load_secrets()    
    if success:
        print("\n" + "="*60)
        print("✅ SUCCESS - Ready to use!")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("❌ FAILED - Check errors above")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()