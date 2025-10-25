# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure setup
- Core scripts implementation (orchestrator, backup_manager, restore_manager)
- Context management system
- Prompt templates
- Git repository initialization
- **Facebook text posting functionality** - Basic text posting to Facebook page via Graph API
- **Comprehensive validation system** - Tests, linting, type checking, and security analysis
- **Unit tests for auto_post module** - Complete test coverage with mocking
- **Facebook image posting functionality** - Image upload with text to Facebook page via Graph API
- **Enhanced image posting tests** - 7 new unit tests covering all image posting scenarios
- **Validation system improvements** - Fixed mypy integration and result saving

## [Phase 3 Step 4] - 2025-10-25

### Fixed
- **MyPy Type Errors**: Resolved all MyPy errors in `Tests/validation_runner.py`
  - Fixed `Collection[str]` indexing issues by adding proper type annotations
  - Changed `Collection[str]` to `List[Tuple[str, Callable[[], Tuple[bool, str, List[str]]]]]`
  - Fixed `Optional[Path]` parameter defaults for `project_root` and `output_file`
  - Added proper type annotations for `self.results` and `self.validation_steps`
  - MyPy now passes without errors for validation_runner.py

### Added
- **Task Scheduler System**: Implemented comprehensive scheduling functionality
  - `Automatizare_Completa/scheduler.py` - Complete scheduler implementation
  - Support for multiple job types: `daily`, `weekly`, `interval`, `once`
  - JSON-based configuration system with `Config/schedule.json`
  - Automatic script execution with subprocess management
  - Comprehensive logging to `Logs/scheduler.log`
  - Job status tracking with `last_run` timestamps
  - One-time job execution tracking with `executed` flag
- **Schedule Configuration**: Created `Config/schedule.json` template
  - Daily posts at 09:00
  - Interval-based content generation (every 3 hours)
  - One-time backup jobs with specific datetime
  - Weekly Monday posts at 10:00
  - Job enable/disable functionality
- **Enhanced Testing**: Added 16 new unit tests for scheduler functionality
  - `test_load_schedule_file_not_found` - Template creation testing
  - `test_load_schedule_valid_json` - JSON loading validation
  - `test_load_schedule_invalid_json` - Error handling for malformed JSON
  - `test_save_schedule` - Schedule persistence testing
  - `test_run_task_calls_subprocess` - Subprocess execution verification
  - `test_run_task_script_not_found` - Missing script handling
  - `test_run_task_success/failure/timeout` - Execution result handling
  - `test_setup_schedules_*` - All job type scheduling tests
  - `test_setup_schedules_disabled_job` - Disabled job filtering
  - `test_setup_schedules_executed_once_job` - One-time job execution logic

### Technical Details
- **Scheduler Architecture**:
  - Uses `schedule==1.2.1` library for cron-like functionality
  - Subprocess execution with 5-minute timeout per task
  - Automatic directory creation for Config and Logs
  - JSON configuration with validation and error handling
  - Real-time job status updates and persistence
- **Job Types Supported**:
  - `daily`: Run at specific time every day
  - `weekly`: Run on specific day and time each week
  - `interval`: Run every N minutes
  - `once`: Run once at specific datetime
- **Error Handling**:
  - Script existence validation before execution
  - Timeout handling for long-running tasks
  - JSON parsing error recovery
  - Subprocess execution error logging
- **Logging System**:
  - Dual output: file (`Logs/scheduler.log`) and console
  - Detailed execution logs with timestamps
  - Success/failure status reporting
  - Error message capture and logging

### Testing
- **40/40 tests passing** (24 existing + 16 new scheduler tests)
- **4/6 validation checks passing** (MyPy has minor issues in other files but validation_runner.py is clean)
- All scheduler scenarios covered with comprehensive mocking
- Complete subprocess execution testing
- JSON configuration handling validation

### Dependencies
- Added `schedule==1.2.1` to requirements.txt
- Enhanced type annotations with `Optional`, `Callable`, `List`, `Tuple`
