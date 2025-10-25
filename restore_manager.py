#!/usr/bin/env python3
"""
Restore Manager - Restore system from backups
Handles safe restoration with validation and rollback capabilities
"""

import os
import sys
import json
import shutil
import zipfile
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RestoreManager:
    """Manages restoration from backups with safety checks."""
    
    def __init__(self, backup_dir: str = "Backups"):
        self.backup_dir = Path(backup_dir)
        self.project_root = Path.cwd()
        self.temp_dir = Path("temp_restore")
        self.rollback_dir = Path("rollback_backup")
        
    def find_backup(self, identifier: str) -> Optional[Path]:
        """Find backup by timestamp or filename."""
        # Try exact filename first
        backup_path = self.backup_dir / identifier
        if backup_path.exists():
            return backup_path
        
        # Try with .zip extension
        backup_path = self.backup_dir / f"{identifier}.zip"
        if backup_path.exists():
            return backup_path
        
        # Search by timestamp pattern
        for backup_file in self.backup_dir.glob("backup_*.zip"):
            if identifier in str(backup_file):
                return backup_file
        
        return None
    
    def read_manifest(self, backup_path: Path) -> Optional[Dict[str, Any]]:
        """Read manifest from backup file."""
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                if "BACKUP_MANIFEST.json" in zipf.namelist():
                    manifest_data = zipf.read("BACKUP_MANIFEST.json")
                    return json.loads(manifest_data.decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to read manifest: {e}")
        
        return None
    
    def create_rollback_backup(self) -> bool:
        """Create a rollback backup of current state before restoration."""
        logger.info("Creating rollback backup...")
        
        # Clean up old rollback if exists
        if self.rollback_dir.exists():
            shutil.rmtree(self.rollback_dir)
        
        self.rollback_dir.mkdir(parents=True, exist_ok=True)
        
        # Define what to backup for rollback
        important_dirs = [
            "Automatizare_Completa",
            "Config",
            "GUI",
            "Scripts",
            "Tests",
            "Prompts/Templates"
        ]
        
        important_files = [
            "orchestrator.py",
            "backup_manager.py",
            "restore_manager.py",
            "PROJECT_CONTEXT.json",
            ".cursorrules",
            "requirements.txt"
        ]
        
        try:
            # Backup directories
            for dir_name in important_dirs:
                src_dir = self.project_root / dir_name
                if src_dir.exists():
                    dst_dir = self.rollback_dir / dir_name
                    dst_dir.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            
            # Backup files
            for file_name in important_files:
                src_file = self.project_root / file_name
                if src_file.exists():
                    dst_file = self.rollback_dir / file_name
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
            
            # Save rollback info
            rollback_info = {
                "timestamp": datetime.now().isoformat(),
                "reason": "pre-restore backup",
                "original_backup": ""
            }
            
            with open(self.rollback_dir / "ROLLBACK_INFO.json", 'w', encoding='utf-8') as f:
                json.dump(rollback_info, f, indent=2)
            
            logger.info("Rollback backup created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create rollback backup: {e}")
            return False
    
    def restore_from_backup(self, backup_path: Path, dry_run: bool = False) -> bool:
        """Restore project from backup file."""
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        # Read and display manifest
        manifest = self.read_manifest(backup_path)
        if not manifest:
            logger.error("Failed to read backup manifest")
            return False
        
        logger.info(f"Backup info:")
        logger.info(f"  Created: {manifest.get('timestamp', 'Unknown')}")
        logger.info(f"  Files: {manifest.get('total_files', 'Unknown')}")
        logger.info(f"  Size: {manifest.get('total_size_bytes', 0) / 1024 / 1024:.2f} MB")
        
        if dry_run:
            logger.info("DRY RUN - No changes will be made")
            return self.validate_restore(backup_path)
        
        # Create rollback backup
        if not self.create_rollback_backup():
            logger.error("Failed to create rollback backup. Aborting restore.")
            return False
        
        # Extract to temp directory first
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info("Extracting backup...")
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(self.temp_dir)
            
            # Remove BACKUP_MANIFEST.json from extracted files
            manifest_file = self.temp_dir / "BACKUP_MANIFEST.json"
            if manifest_file.exists():
                manifest_file.unlink()
            
            logger.info("Restoring files...")
            
            # Copy files from temp to project root
            for item in self.temp_dir.iterdir():
                if item.is_file():
                    # Skip .env file to preserve current secrets
                    if item.name == ".env":
                        logger.info("Skipping .env file (preserving current secrets)")
                        continue
                    
                    dst = self.project_root / item.name
                    shutil.copy2(item, dst)
                    
                elif item.is_dir():
                    dst = self.project_root / item.name
                    
                    # Remove existing directory (except special ones)
                    if dst.exists() and item.name not in ["Backups", "Logs", "Update_AI", ".git"]:
                        shutil.rmtree(dst)
                    
                    # Copy directory
                    shutil.copytree(item, dst, dirs_exist_ok=True)
            
            # Update PROJECT_CONTEXT.json with restore info
            context_file = self.project_root / "PROJECT_CONTEXT.json"
            if context_file.exists():
                with open(context_file, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                
                context["last_restore"] = datetime.now().isoformat()
                context["last_restore_from"] = str(backup_path)
                
                with open(context_file, 'w', encoding='utf-8') as f:
                    json.dump(context, f, indent=2, ensure_ascii=False)
            
            # Clean up temp directory
            shutil.rmtree(self.temp_dir)
            
            logger.info("Restore completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            
            # Attempt rollback
            if self.rollback():
                logger.info("Rollback completed")
            else:
                logger.error("Rollback failed - manual intervention may be required")
            
            return False
    
    def validate_restore(self, backup_path: Path) -> bool:
        """Validate backup file before restoration."""
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Test archive integrity
                result = zipf.testzip()
                if result is not None:
                    logger.error(f"Corrupted file in backup: {result}")
                    return False
                
                # Check for critical files
                namelist = zipf.namelist()
                critical_files = [
                    "orchestrator.py",
                    "PROJECT_CONTEXT.json"
                ]
                
                for critical_file in critical_files:
                    if critical_file not in namelist:
                        logger.warning(f"Critical file missing in backup: {critical_file}")
                
                logger.info("Backup validation passed")
                return True
                
        except Exception as e:
            logger.error(f"Backup validation failed: {e}")
            return False
    
    def rollback(self) -> bool:
        """Rollback to pre-restore state."""
        if not self.rollback_dir.exists():
            logger.error("No rollback backup found")
            return False
        
        logger.info("Rolling back to previous state...")
        
        try:
            # Copy rollback files back
            for item in self.rollback_dir.iterdir():
                if item.name == "ROLLBACK_INFO.json":
                    continue
                
                if item.is_file():
                    dst = self.project_root / item.name
                    shutil.copy2(item, dst)
                    
                elif item.is_dir():
                    dst = self.project_root / item.name
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(item, dst)
            
            # Clean up rollback directory
            shutil.rmtree(self.rollback_dir)
            
            logger.info("Rollback completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def list_available_backups(self) -> list:
        """List all available backups."""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob("backup_*.zip"), reverse=True):
            info = {
                "filename": backup_file.name,
                "path": str(backup_file),
                "size_mb": backup_file.stat().st_size / 1024 / 1024,
                "modified": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
            }
            
            # Try to read manifest
            manifest = self.read_manifest(backup_file)
            if manifest:
                info["created"] = manifest.get("timestamp", "Unknown")
                info["files"] = manifest.get("total_files", 0)
                info["description"] = manifest.get("description", "")
            
            backups.append(info)
        
        return backups

def main():
    """Main entry point for restore manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Restore Manager for SocialBoost")
    parser.add_argument(
        "action",
        choices=["restore", "list", "validate", "rollback"],
        help="Action to perform"
    )
    parser.add_argument(
        "--backup",
        help="Backup identifier (timestamp or filename)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform dry run without making changes"
    )
    
    args = parser.parse_args()
    
    manager = RestoreManager()
    
    if args.action == "list":
        backups = manager.list_available_backups()
        
        if not backups:
            print("No backups found")
        else:
            print(f"Found {len(backups)} backup(s):\n")
            for backup in backups:
                print(f"- {backup['filename']}")
                print(f"  Created: {backup.get('created', backup['modified'])}")
                print(f"  Size: {backup['size_mb']:.2f} MB")
                print(f"  Files: {backup.get('files', 'Unknown')}")
                if backup.get('description'):
                    print(f"  Description: {backup['description']}")
                print()
    
    elif args.action == "restore":
        if not args.backup:
            print("Error: --backup required for restore action")
            sys.exit(1)
        
        backup_path = manager.find_backup(args.backup)
        if not backup_path:
            print(f"Backup not found: {args.backup}")
            sys.exit(1)
        
        if args.dry_run:
            print(f"Validating backup: {backup_path}")
            if manager.validate_restore(backup_path):
                print("Validation passed - backup can be restored")
            else:
                print("Validation failed")
                sys.exit(1)
        else:
            print(f"Restoring from: {backup_path}")
            if manager.restore_from_backup(backup_path):
                print("Restore completed successfully")
            else:
                print("Restore failed")
                sys.exit(1)
    
    elif args.action == "validate":
        if not args.backup:
            print("Error: --backup required for validate action")
            sys.exit(1)
        
        backup_path = manager.find_backup(args.backup)
        if not backup_path:
            print(f"Backup not found: {args.backup}")
            sys.exit(1)
        
        if manager.validate_restore(backup_path):
            print("Backup is valid")
        else:
            print("Backup validation failed")
            sys.exit(1)
    
    elif args.action == "rollback":
        if manager.rollback():
            print("Rollback completed successfully")
        else:
            print("Rollback failed")
            sys.exit(1)

if __name__ == "__main__":
    main()
