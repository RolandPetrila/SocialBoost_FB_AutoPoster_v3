# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Phase 4 Step 1] - 2025-10-25

### Added
- **Assets Tab Implementation**: Full functionality for managing media assets
  - **File Listing**: Treeview widget listing images and videos from `Assets/Images` and `Assets/Videos`
  - **Image Preview**: Thumbnail preview for selected images using Pillow
  - **Multi-Selection**: Extended selection mode for selecting multiple files
  - **Refresh Functionality**: Button to reload assets from folders
  - **Save Selection**: Button to save selected files to `selected_assets.json`
  - **JSON Storage**: Structured storage of selected assets (images and videos separated)
- **Enhanced GUI Tests**: Added 2 new tests for assets functionality
  - `test_load_assets_populates_list` - Verifies treeview population
  - `test_save_selected_assets_writes_json` - Verifies JSON structure
- **Asset Management**: Complete workflow for selecting and saving media files
  - Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, WebP)
  - Support for multiple video formats (MP4, MOV, AVI, MKV, WebM)
  - Automatic absolute path storage for selected assets
  - Success confirmation dialog with file counts
- **Image Preview System**: Integrated Pillow for image display
  - Thumbnail generation maintaining aspect ratio (max 300x300)
  - Error handling for corrupted or unsupported images
  - Preview area shows placeholder text when no image selected
  - Automatic scaling with high-quality resampling (LANCZOS)

### Technical Details
- **GUI Components**:
  - Treeview widget with column headers (File Name, Type)
  - Scrollable list with vertical and horizontal scrollbars
  - Split-panel layout (file list on left, preview on right)
  - Button controls for refresh and save operations
- **File Operations**:
  - Recursive scanning of `Assets/Images` and `Assets/Videos` folders
  - Path resolution using `pathlib.Path` for cross-platform compatibility
  - Absolute path storage for reliable file access
  - JSON file format with UTF-8 encoding for international characters
- **Image Processing**:
  - Pillow integration for image loading and manipulation
  - Thumbnail generation with aspect ratio preservation
  - ImageTk conversion for Tkinter display
  - Error handling for file read failures
- **Data Structure**:
  - JSON format: `{"images": [...], "videos": [...]}`
  - Absolute paths stored for all selected files
  - Separate arrays for images and videos
  - Pretty-printed JSON with 2-space indentation

### Testing
- **68/68 tests passing** (added 2 new GUI tests)
- **GUI file passes MyPy validation** - No type errors in main_gui.py
- Integration testing verified for asset loading and saving
- Error handling validated for missing files and corrupted images

### Files Modified
- `GUI/main_gui.py` - Added complete Assets tab implementation
- `Tests/test_gui.py` - Added 2 new tests for assets functionality
- `selected_assets.json` - Created for storing selected assets

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

## [Phase 3 Step 7] - 2025-10-25

### Added
- **Basic GUI Structure**: Implemented Tkinter-based GUI application
  - `GUI/main_gui.py` - Complete GUI application with 5 tabs
  - **Control/Status Tab**: Quick action buttons and status display
  - **Programare Tab**: Scheduling interface (placeholder for future implementation)
  - **Assets Tab**: Asset management interface (placeholder for future implementation)
  - **Generare Text Tab**: AI content generation interface with prompt input and result display
  - **Logs Tab**: System logs display with real-time updates
- **GUI-Backend Integration**: Connected GUI buttons to backend scripts via subprocess
  - **Generate Text Button**: Calls `auto_generate.py --prompt` with user input
  - **Post Text Button**: Calls `auto_post.py --message` with test message
  - Thread-safe execution to prevent GUI freezing
  - Real-time status updates and error handling
- **Command Line Arguments**: Enhanced backend scripts for GUI integration
  - `auto_post.py` now accepts `--message` argument for direct posting
  - `auto_generate.py` now accepts `--prompt` argument for direct text generation
  - Maintains backward compatibility with existing test functionality
- **GUI Testing**: Added minimal GUI tests in `Tests/test_gui.py`
  - File existence and syntax validation
  - Method presence verification
  - Command line argument validation
  - Integration testing for GUI-backend communication

### Technical Details
- **GUI Framework**: Tkinter with ttk (themed widgets) for modern appearance
- **Threading**: Background execution of subprocess calls to maintain GUI responsiveness
- **Queue System**: Thread-safe communication between background threads and GUI
- **Error Handling**: Comprehensive error display with user-friendly messages
- **Status Updates**: Real-time status indicators and progress feedback
- **Logging Integration**: GUI displays system logs in dedicated tab

### Dependencies
- Added `Pillow>=10.0.0` to requirements.txt for GUI image support
- Enhanced subprocess integration with proper error handling
- Thread-safe queue implementation for GUI updates

### Testing
- **5/5 GUI tests passing** - Basic functionality validation
- **66/66 total tests passing** - All existing functionality maintained
- **MyPy validation**: All GUI and modified backend files pass type checking
- **Integration testing**: GUI-backend communication verified

## [Phase 3 Step 6] - 2025-10-25

### Fixed
- **MyPy Type Errors**: Resolved remaining type checking errors in helper scripts
  - Fixed `Scripts/context_builder.py` type annotations
  - Added proper `Optional[Path]` type for `root_path` parameter
  - Added explicit type annotations for `Dict[str, Any]` structures
  - Resolved `Collection[str]` attribute access errors

### Added
- **Retry Logic Implementation**: Added robust retry mechanisms for API calls
  - **Facebook API Retry**: Implemented retry logic in `Automatizare_Completa/auto_post.py`
    - 3 retry attempts with exponential backoff (2^attempt seconds)
    - Handles retryable HTTP status codes: 429, 500, 502, 503, 504
    - Handles network errors: `ConnectionError`, `Timeout`, `RequestException`
    - Comprehensive logging for retry attempts and failures
  - **OpenAI API Retry**: Implemented retry logic in `Automatizare_Completa/auto_generate.py`
    - 3 retry attempts with exponential backoff (2^attempt seconds)
    - Handles OpenAI-specific errors: `RateLimitError`, `APIConnectionError`, `APITimeoutError`
    - Handles generic exceptions for additional resilience
    - Maintains existing fallback text system after all retries fail
- **Enhanced Unit Tests**: Added comprehensive retry testing
  - **Facebook Retry Tests**: 3 new tests in `Tests/test_auto_post.py`
    - `test_post_text_retry_success` - API fails once then succeeds
    - `test_post_text_retry_max_attempts` - API fails all 3 times
    - `test_post_text_connection_error_retry` - Connection error retry
  - **OpenAI Retry Tests**: 3 new tests in `Tests/test_auto_generate.py`
    - `test_generate_post_text_retry_success` - API fails once then succeeds
    - `test_generate_post_text_retry_max_attempts` - API fails all 3 times
    - `test_generate_caption_retry_success` - Caption generation retry
  - All retry tests verify correct call counts and sleep durations

### Technical Details
- **Retry Strategy**:
  - Maximum 3 attempts for all API calls
  - Exponential backoff: 1s, 2s, 4s delays
  - Specific error handling for different failure types
  - Graceful degradation to fallback systems
- **Error Handling**:
  - Distinguishes between retryable and non-retryable errors
  - Comprehensive logging for debugging and monitoring
  - Maintains existing error response formats
- **Testing Coverage**:
  - All retry scenarios covered with unit tests
  - Mock verification for API call counts and sleep calls
  - Integration with existing test framework

## [Phase 3 Step 5] - 2025-10-25

### Added
- **OpenAI Content Generation**: Implemented comprehensive AI-powered content generation system
  - `Automatizare_Completa/auto_generate.py` - Complete OpenAI integration
  - Support for text generation using GPT models (default: gpt-4o-mini)
  - Support for image caption generation using Vision API
  - Automatic fallback text generation when API calls fail
  - Comprehensive error handling for all OpenAI API scenarios
  - Environment-based configuration with OPENAI_API_KEY and OPENAI_MODEL
- **Enhanced Testing**: Added 15 new unit tests for content generation functionality
  - `test_initialization_success/from_env/missing_key` - Initialization testing
  - `test_generate_post_text_success/api_error/rate_limit_error` - Text generation testing
  - `test_generate_caption_for_image_success/file_not_found/unsupported_format/api_error` - Image caption testing
  - `test_check_api_status_success/failure` - API status verification
  - `test_get_fallback_text` - Fallback text generation
  - `test_generate_post_text_custom_parameters` - Custom parameter testing
  - `test_generate_caption_different_image_types` - Multiple image format support
- **Fallback System**: Intelligent fallback text generation
  - Context-aware fallback messages for different error types
  - Timestamp-based hashtags for uniqueness
  - Emoji-enhanced messages for engagement
  - Support for 7 different error scenarios

### Technical Details
- **OpenAI Integration**:
  - Uses OpenAI Python SDK v1.0+ with proper error handling
  - Supports both text and vision models
  - Automatic model selection (gpt-4o-mini default, configurable via OPENAI_MODEL)
  - Base64 image encoding for vision API calls
  - Proper data URL construction for image uploads
- **Content Generation Features**:
  - Text generation with customizable max_tokens (default: 500)
  - Image caption generation with context prompts
  - Temperature control (0.7) for balanced creativity
  - System prompts optimized for social media content
  - Support for multiple image formats (JPG, PNG, GIF, BMP, WebP)
- **Error Handling**:
  - Graceful handling of API errors, rate limits, and timeouts
  - Automatic fallback to pre-generated content
  - Comprehensive logging for debugging
  - Validation of image files before processing
- **Configuration Management**:
  - Environment variable support for API keys
  - Configurable model selection
  - Automatic directory creation for assets
  - Placeholder image generation for testing

### Testing
- **55/55 tests passing** (40 existing + 15 new OpenAI tests)
- **5/6 validation checks passing** (MyPy has minor issues in other files but functional)
- All OpenAI scenarios covered with comprehensive mocking
- Complete error handling testing
- Fallback text generation validation
- Image processing workflow testing

### Dependencies
- Added `openai>=1.0.0` to requirements.txt
- Enhanced error handling with proper exception types
- Base64 encoding for image processing
- Comprehensive logging integration
