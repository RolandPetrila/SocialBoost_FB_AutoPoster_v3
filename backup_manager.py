#!/usr/bin/env python3
"""
Backup Manager - Automated backup system for SocialBoost project
Creates timestamped backups with compression and rotation
"""

import os
import sys
import json
import shutil
import zipfile
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupManager:
    """Manages project backups with compression and rotation."""
    
    def __init__(self, backup_dir: str = "Backups", max_backups: int = 10):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.max_backups = max_backups
        self.project_root = Path.cwd()
        self.context_file = Path("PROJECT_CONTEXT.json")
        
        # Directories and files to exclude from backup
        self.exclude_patterns = [
            "__pycache__",
            "*.pyc",
            ".git",
            ".venv",
            "venv",
            "env",
            ".env",  # Exclude sensitive data
            "Backups",  # Don't backup backups
            "Logs",  # Optional: exclude logs
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            "*.log",
            ".DS_Store",
            "Thumbs.db"
        ]
        
    def should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from backup."""
        path_str = str(path)
        
        for pattern in self.exclude_patterns:
            if pattern.startswith("*."):
                # File extension pattern
                if path.suffix == pattern[1:]:
                    return True
            elif pattern in path_str:
                return True
        
        return False
    
    def get_backup_manifest(self) -> Dict[str, Any]:
        """Generate backup manifest with metadata."""
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "project_name": "SocialBoost_FB_AutoPoster_v3",
            "backup_type": "full",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "excluded_patterns": self.exclude_patterns,
            "total_files": 0,
            "total_size_bytes": 0
        }
        
        # Load project context if available
        if self.context_file.exists():
            with open(self.context_file, 'r', encoding='utf-8') as f:
                context = json.load(f)
                manifest["project_context"] = context
        
        return manifest
    
    def create_backup(self, description: str = "") -> Path:
        """Create a new backup with optional description."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        if description:
            # Sanitize description for filename
            safe_desc = "".join(c if c.isalnum() or c in "-_" else "_" for c in description)
            backup_name = f"backup_{timestamp}_{safe_desc}"
        
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        logger.info(f"Creating backup: {backup_path}")
        
        manifest = self.get_backup_manifest()
        manifest["description"] = description
        
        file_count = 0
        total_size = 0
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add manifest
            manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
            zipf.writestr("BACKUP_MANIFEST.json", manifest_json)
            
            # Walk through project directory
            for root, dirs, files in os.walk(self.project_root):
                root_path = Path(root)
                
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d)]
                
                for file in files:
                    file_path = root_path / file
                    
                    # Skip excluded files
                    if self.should_exclude(file_path):
                        continue
                    
                    # Skip the backup directory itself
                    if self.backup_dir in file_path.parents:
                        continue
                    
                    # Get relative path for archive
                    rel_path = file_path.relative_to(self.project_root)
                    
                    try:
                        zipf.write(file_path, rel_path)
                        file_count += 1
                        total_size += file_path.stat().st_size
                        
                    except Exception as e:
                        logger.warning(f"Failed to backup {file_path}: {e}")
        
        # Update manifest with final stats
        manifest["total_files"] = file_count
        manifest["total_size_bytes"] = total_size
        
        # Save backup info
        backup_info = {
            "path": str(backup_path),
            "timestamp": timestamp,
            "description": description,
            "manifest": manifest
        }
        
        info_file = self.backup_dir / f"{backup_name}.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Backup completed: {file_count} files, {total_size / 1024 / 1024:.2f} MB")
        
        # Rotate old backups
        self.rotate_backups()
        
        return backup_path
    
    def rotate_backups(self):
        """Remove old backups if exceeding max_backups limit."""
        # Get all backup files
        backup_files = list(self.backup_dir.glob("backup_*.zip"))
        backup_files.sort(key=lambda x: x.stat().st_mtime)
        
        if len(backup_files) > self.max_backups:
            # Remove oldest backups
            to_remove = backup_files[:len(backup_files) - self.max_backups]
            
            for backup_file in to_remove:
                logger.info(f"Removing old backup: {backup_file}")
                
                # Remove zip file
                backup_file.unlink()
                
                # Remove associated json info file
                json_file = backup_file.with_suffix('.json')
                if json_file.exists():
                    json_file.unlink()
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups with their metadata."""
        backups = []
        
        for info_file in self.backup_dir.glob("backup_*.json"):
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    backup_info = json.load(f)
                    
                    # Check if zip file exists
                    zip_path = Path(backup_info["path"])
                    if zip_path.exists():
                        backup_info["size_mb"] = zip_path.stat().st_size / 1024 / 1024
                        backups.append(backup_info)
                        
            except Exception as e:
                logger.warning(f"Failed to read backup info {info_file}: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return backups
    
    def verify_backup(self, backup_path: Path) -> bool:
        """Verify backup integrity."""
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Test archive integrity
                result = zipf.testzip()
                
                if result is not None:
                    logger.error(f"Corrupted file in backup: {result}")
                    return False
                
                # Check for manifest
                if "BACKUP_MANIFEST.json" not in zipf.namelist():
                    logger.error("Backup manifest not found")
                    return False
                
                logger.info(f"Backup verified successfully: {backup_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to verify backup: {e}")
            return False

def main():
    """Main entry point for backup manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Backup Manager for SocialBoost")
    parser.add_argument(
        "action",
        choices=["create", "list", "verify", "rotate"],
        help="Action to perform"
    )
    parser.add_argument(
        "--description",
        help="Description for the backup (for create action)"
    )
    parser.add_argument(
        "--path",
        help="Path to backup file (for verify action)"
    )
    parser.add_argument(
        "--max-backups",
        type=int,
        default=10,
        help="Maximum number of backups to keep"
    )
    
    args = parser.parse_args()
    
    manager = BackupManager(max_backups=args.max_backups)
    
    if args.action == "create":
        backup_path = manager.create_backup(args.description or "")
        print(f"Backup created: {backup_path}")
        
    elif args.action == "list":
        backups = manager.list_backups()
        
        if not backups:
            print("No backups found")
        else:
            print(f"Found {len(backups)} backup(s):\n")
            for backup in backups:
                print(f"- {backup['timestamp']}")
                print(f"  Description: {backup.get('description', 'N/A')}")
                print(f"  Size: {backup.get('size_mb', 0):.2f} MB")
                print(f"  Files: {backup['manifest'].get('total_files', 0)}")
                print()
    
    elif args.action == "verify":
        if not args.path:
            print("Error: --path required for verify action")
            sys.exit(1)
        
        if manager.verify_backup(Path(args.path)):
            print("Backup is valid")
        else:
            print("Backup verification failed")
            sys.exit(1)
    
    elif args.action == "rotate":
        manager.rotate_backups()
        print("Backup rotation completed")

if __name__ == "__main__":
    main()
