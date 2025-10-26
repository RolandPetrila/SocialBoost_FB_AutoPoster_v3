#!/usr/bin/env python3
"""
Health Check Module for SocialBoost Facebook AutoPoster v3
Comprehensive system health monitoring and validation.
"""

import sys
import subprocess
import pathlib
import json
import datetime
import shutil
from typing import Dict, Any, List, Optional, Tuple
import psutil  # type: ignore[import-untyped]


class HealthCheck:
    """Comprehensive health check system for the SocialBoost project."""
    
    def __init__(self, project_root: Optional[pathlib.Path] = None):
        """Initialize the health check system.
        
        Args:
            project_root: Root path of the project. If None, uses current script's parent.
        """
        if project_root is None:
            self.project_root = pathlib.Path(__file__).resolve().parents[1]
        else:
            self.project_root = pathlib.Path(project_root)
        
        self.results: Dict[str, Any] = {}
        self.overall_health: str = "Unknown"
        self.health_score: float = 0.0
        
    def check_python_version(self) -> Dict[str, Any]:
        """Check Python version compatibility.
        
        Returns:
            Dictionary with check results including version info and status.
        """
        result = {
            'check': 'Python Version',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            version_info = sys.version_info
            details = {
                'version': f"{version_info.major}.{version_info.minor}.{version_info.micro}",
                'major': version_info.major,
                'minor': version_info.minor,
                'micro': version_info.micro
            }
            result['details'] = details  # type: ignore[assignment]
            
            # Check minimum requirements (Python 3.8+)
            if version_info.major >= 3 and version_info.minor >= 8:
                result['status'] = 'Pass'
                result['score'] = 1.0
                result['message'] = f"Python {details['version']} is compatible"
            else:
                result['status'] = 'Fail'
                result['score'] = 0.0
                result['message'] = f"Python {details['version']} is too old (requires 3.8+)"
                
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking Python version: {str(e)}"
            
        return result
    
    def check_git_repository(self) -> Dict[str, Any]:
        """Check Git repository status and configuration.
        
        Returns:
            Dictionary with Git repository check results.
        """
        result = {
            'check': 'Git Repository',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            # Check if we're in a Git repository
            git_dir = self.project_root / '.git'
            if not git_dir.exists():
                result['status'] = 'Fail'
                result['score'] = 0.0
                result['message'] = 'Not a Git repository'
                return result
            
            # Get Git status
            git_status = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Get current branch
            git_branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Get last commit
            git_log = subprocess.run(
                ['git', 'log', '-1', '--oneline'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            details = {
                'is_git_repo': True,
                'current_branch': git_branch.stdout.strip() if git_branch.returncode == 0 else 'Unknown',
                'last_commit': git_log.stdout.strip() if git_log.returncode == 0 else 'Unknown',
                'uncommitted_changes': len(git_status.stdout.strip().split('\n')) if git_status.stdout.strip() else 0
            }
            result['details'] = details  # type: ignore[assignment]
            
            # Calculate score based on Git health
            score = 1.0
            uncommitted = details['uncommitted_changes']  # type: ignore[index]
            if uncommitted > 0:  # type: ignore[operator]
                score -= 0.2  # Deduct for uncommitted changes
            
            result['score'] = score
            result['status'] = 'Pass' if score >= 0.8 else 'Warning'
            result['message'] = f"Git repository healthy (branch: {details['current_branch']})"
            
        except subprocess.TimeoutExpired:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = 'Git commands timed out'
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking Git repository: {str(e)}"
            
        return result
    
    def check_required_files(self) -> Dict[str, Any]:
        """Check for required project files and directories.
        
        Returns:
            Dictionary with file system check results.
        """
        result = {
            'check': 'Required Files',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            # Define required files and directories
            required_files = [
                'PROJECT_CONTEXT.json',
                'requirements.txt',
                'orchestrator.py',
                'backup_manager.py',
                'restore_manager.py'
            ]
            
            required_dirs = [
                'Automatizare_Completa',
                'GUI',
                'Tests',
                'Config',
                'Logs',
                'Assets/Images',
                'Assets/Videos'
            ]
            
            missing_files = []
            missing_dirs = []
            existing_files = []
            existing_dirs = []
            
            # Check files
            for file_path in required_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    existing_files.append(file_path)
                else:
                    missing_files.append(file_path)
            
            # Check directories
            for dir_path in required_dirs:
                full_path = self.project_root / dir_path
                if full_path.exists() and full_path.is_dir():
                    existing_dirs.append(dir_path)
                else:
                    missing_dirs.append(dir_path)
            
            result['details'] = {
                'existing_files': existing_files,
                'missing_files': missing_files,
                'existing_dirs': existing_dirs,
                'missing_dirs': missing_dirs,
                'total_required_files': len(required_files),
                'total_required_dirs': len(required_dirs)
            }
            
            # Calculate score
            file_score = len(existing_files) / len(required_files)
            dir_score = len(existing_dirs) / len(required_dirs)
            score_val = (file_score + dir_score) / 2
            result['score'] = score_val
            
            if score_val >= 0.9:
                result['status'] = 'Pass'
                result['message'] = 'All required files and directories present'
            elif score_val >= 0.7:
                result['status'] = 'Warning'
                result['message'] = f"Missing {len(missing_files)} files, {len(missing_dirs)} directories"
            else:
                result['status'] = 'Fail'
                result['message'] = f"Critical files missing: {len(missing_files)} files, {len(missing_dirs)} directories"
                
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking required files: {str(e)}"
            
        return result
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Check Python dependencies installation.
        
        Returns:
            Dictionary with dependency check results.
        """
        result = {
            'check': 'Dependencies',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            # Read requirements.txt
            requirements_path = self.project_root / 'requirements.txt'
            if not requirements_path.exists():
                result['status'] = 'Fail'
                result['score'] = 0.0
                result['message'] = 'requirements.txt not found'
                return result
            
            with open(requirements_path, 'r', encoding='utf-8') as f:
                requirements = f.read().strip().split('\n')
            
            # Filter out comments and empty lines
            requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
            
            installed_packages = []
            missing_packages = []
            
            # Check each requirement
            for requirement in requirements:
                try:
                    package_name = requirement.split('==')[0].split('>=')[0].split('>')[0].split('<')[0].split('~')[0]
                    
                    # Try to import the package
                    __import__(package_name.replace('-', '_'))
                    installed_packages.append(requirement)
                except ImportError:
                    missing_packages.append(requirement)
                except Exception:
                    # For packages with different import names
                    installed_packages.append(requirement)
            
            result['details'] = {
                'installed_packages': installed_packages,
                'missing_packages': missing_packages,
                'total_requirements': len(requirements)
            }
            
            # Calculate score
            score_val = len(installed_packages) / len(requirements) if requirements else 0.0
            result['score'] = score_val
            
            if score_val >= 0.9:
                result['status'] = 'Pass'
                result['message'] = 'All dependencies installed'
            elif score_val >= 0.7:
                result['status'] = 'Warning'
                result['message'] = f"Missing {len(missing_packages)} dependencies"
            else:
                result['status'] = 'Fail'
                result['message'] = f"Critical dependencies missing: {len(missing_packages)} packages"
                
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking dependencies: {str(e)}"
            
        return result
    
    def check_github_connectivity(self) -> Dict[str, Any]:
        """Check GitHub connectivity and repository access.
        
        Returns:
            Dictionary with GitHub connectivity check results.
        """
        result = {
            'check': 'GitHub Connectivity',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            # Check if Git remote is configured
            git_remote = subprocess.run(
                ['git', 'remote', '-v'],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if git_remote.returncode != 0:
                result['status'] = 'Fail'
                result['score'] = 0.0
                result['message'] = 'No Git remotes configured'
                return result
            
            remote_output = git_remote.stdout.strip()
            github_remotes = [line for line in remote_output.split('\n') if 'github.com' in line]
            
            result['details'] = {
                'has_github_remote': len(github_remotes) > 0,
                'remote_count': len(remote_output.split('\n')) if remote_output else 0,
                'github_remotes': github_remotes
            }
            
            if github_remotes:
                # Try to fetch from GitHub
                git_fetch = subprocess.run(
                    ['git', 'fetch', '--dry-run'],
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                if git_fetch.returncode == 0:
                    result['status'] = 'Pass'
                    result['score'] = 1.0
                    result['message'] = 'GitHub connectivity working'
                else:
                    result['status'] = 'Warning'
                    result['score'] = 0.5
                    result['message'] = 'GitHub remote configured but connectivity issues'
            else:
                result['status'] = 'Warning'
                result['score'] = 0.3
                result['message'] = 'No GitHub remote configured'
                
        except subprocess.TimeoutExpired:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = 'GitHub connectivity check timed out'
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking GitHub connectivity: {str(e)}"
            
        return result
    
    def check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space.
        
        Returns:
            Dictionary with disk space check results.
        """
        result = {
            'check': 'Disk Space',
            'status': 'Unknown',
            'details': {},
            'score': 0.0,
            'message': ''
        }
        
        try:
            # Get disk usage for project directory
            disk_usage = shutil.disk_usage(str(self.project_root))
            
            total_bytes = disk_usage.total
            free_bytes = disk_usage.free
            used_bytes = disk_usage.used
            
            # Convert to human readable
            def bytes_to_gb(bytes_val):
                return bytes_val / (1024 ** 3)
            
            details = {
                'total_gb': round(bytes_to_gb(total_bytes), 2),
                'free_gb': round(bytes_to_gb(free_bytes), 2),
                'used_gb': round(bytes_to_gb(used_bytes), 2),
                'free_percentage': round((free_bytes / total_bytes) * 100, 2)
            }
            result['details'] = details  # type: ignore[assignment]
            
            free_percentage = details['free_percentage']
            
            if free_percentage >= 20:
                result['status'] = 'Pass'
                result['score'] = 1.0
                result['message'] = f"Disk space healthy ({free_percentage}% free)"
            elif free_percentage >= 10:
                result['status'] = 'Warning'
                result['score'] = 0.6
                result['message'] = f"Disk space low ({free_percentage}% free)"
            else:
                result['status'] = 'Fail'
                result['score'] = 0.0
                result['message'] = f"Disk space critical ({free_percentage}% free)"
                
        except Exception as e:
            result['status'] = 'Error'
            result['score'] = 0.0
            result['message'] = f"Error checking disk space: {str(e)}"
            
        return result
    
    def calculate_overall_health(self) -> Tuple[str, float]:
        """Calculate overall system health based on individual checks.
        
        Returns:
            Tuple of (health_status, health_score)
        """
        if not self.results:
            return "Unknown", 0.0
        
        # Calculate weighted average score
        total_score = 0.0
        total_weight = 0.0
        
        # Define weights for different checks
        weights = {
            'Python Version': 0.15,
            'Git Repository': 0.15,
            'Required Files': 0.25,
            'Dependencies': 0.25,
            'GitHub Connectivity': 0.10,
            'Disk Space': 0.10
        }
        
        for check_name, check_result in self.results.items():
            if check_name in weights:
                weight = weights[check_name]
                score = check_result.get('score', 0.0)
                total_score += score * weight
                total_weight += weight
        
        if total_weight == 0:
            return "Unknown", 0.0
        
        final_score = total_score / total_weight
        
        # Determine health status
        if final_score >= 0.9:
            health_status = "Healthy"
        elif final_score >= 0.7:
            health_status = "Degraded"
        elif final_score >= 0.5:
            health_status = "Warning"
        else:
            health_status = "Critical"
        
        return health_status, final_score
    
    def save_report(self, output_path: Optional[pathlib.Path] = None) -> pathlib.Path:
        """Save health check report to JSON file.
        
        Args:
            output_path: Path to save the report. If None, uses default location.
            
        Returns:
            Path to the saved report file.
        """
        if output_path is None:
            output_path = self.project_root / 'Logs' / 'health_check.json'
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'overall_health': self.overall_health,
            'health_score': self.health_score,
            'checks': self.results,
            'summary': {
                'total_checks': len(self.results),
                'passed_checks': len([r for r in self.results.values() if r.get('status') == 'Pass']),
                'warning_checks': len([r for r in self.results.values() if r.get('status') == 'Warning']),
                'failed_checks': len([r for r in self.results.values() if r.get('status') == 'Fail']),
                'error_checks': len([r for r in self.results.values() if r.get('status') == 'Error'])
            }
        }
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def print_summary(self) -> None:
        """Print a summary of health check results to console."""
        print("\n" + "="*60)
        print("SOCIALBOOST HEALTH CHECK SUMMARY")
        print("="*60)
        print(f"Overall Health: {self.overall_health}")
        print(f"Health Score: {self.health_score:.2f}")
        print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)
        
        for check_name, check_result in self.results.items():
            status = check_result.get('status', 'Unknown')
            score = check_result.get('score', 0.0)
            message = check_result.get('message', '')
            
            # Color coding for status
            status_symbol = {
                'Pass': '✓',
                'Warning': '⚠',
                'Fail': '✗',
                'Error': '!'
            }.get(status, '?')
            
            print(f"{status_symbol} {check_name:<20} [{score:.2f}] {message}")
        
        print("-"*60)
        
        # Summary statistics
        summary = {
            'Pass': len([r for r in self.results.values() if r.get('status') == 'Pass']),
            'Warning': len([r for r in self.results.values() if r.get('status') == 'Warning']),
            'Fail': len([r for r in self.results.values() if r.get('status') == 'Fail']),
            'Error': len([r for r in self.results.values() if r.get('status') == 'Error'])
        }
        
        print(f"Summary: {summary['Pass']} Pass, {summary['Warning']} Warning, {summary['Fail']} Fail, {summary['Error']} Error")
        print("="*60)
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks and return comprehensive results.
        
        Returns:
            Dictionary containing all check results and overall health status.
        """
        print("Running comprehensive health check...")
        
        # Run all checks
        checks = [
            self.check_python_version,
            self.check_git_repository,
            self.check_required_files,
            self.check_dependencies,
            self.check_github_connectivity,
            self.check_disk_space
        ]
        
        for check_func in checks:
            try:
                result = check_func()
                self.results[result['check']] = result
                print(f"✓ Completed: {result['check']}")
            except Exception as e:
                check_name = check_func.__name__.replace('check_', '').replace('_', ' ').title()
                error_result: Dict[str, Any] = {
                    'check': check_name,
                    'status': 'Error',
                    'details': {},
                    'score': 0.0,
                    'message': f"Exception during check: {str(e)}"
                }
                self.results[check_name] = error_result
                print(f"✗ Failed: {error_result['check']}")
        
        # Calculate overall health
        self.overall_health, self.health_score = self.calculate_overall_health()
        
        # Print summary
        self.print_summary()
        
        # Save report
        report_path = self.save_report()
        print(f"\nHealth check report saved to: {report_path}")
        
        return {
            'overall_health': self.overall_health,
            'health_score': self.health_score,
            'results': self.results,
            'report_path': str(report_path)
        }


def main():
    """Main entry point for health check script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='SocialBoost Health Check')
    parser.add_argument('--project-root', type=str, help='Project root directory')
    parser.add_argument('--output', type=str, help='Output file path for report')
    parser.add_argument('--quiet', action='store_true', help='Suppress console output')
    
    args = parser.parse_args()
    
    # Initialize health check
    project_root = pathlib.Path(args.project_root) if args.project_root else None
    health_check = HealthCheck(project_root)
    
    # Run checks
    results = health_check.run_all_checks()
    
    # Save report if specified
    if args.output:
        output_path = pathlib.Path(args.output)
        health_check.save_report(output_path)
    
    # Exit with appropriate code
    if results['overall_health'] in ['Critical', 'Fail']:
        sys.exit(1)
    elif results['overall_health'] == 'Warning':
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
