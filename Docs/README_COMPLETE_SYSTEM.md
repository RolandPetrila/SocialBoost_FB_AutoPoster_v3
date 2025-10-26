# SocialBoost Facebook AutoPoster v3 - User Guide

## 📋 Table of Contents

- [Introduction](#introduction)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Initial Configuration](#initial-configuration)
- [Getting Your Facebook API Credentials](#getting-your-facebook-api-credentials)
- [Getting Your OpenAI API Key](#getting-your-openai-api-key)
- [Running the Application](#running-the-application)
- [Using the GUI Interface](#using-the-gui-interface)
  - [Control/Status Tab](#controlstatus-tab)
  - [Programare (Scheduling) Tab](#programare-scheduling-tab)
  - [Assets Tab](#assets-tab)
  - [Generare Text (Text Generation) Tab](#generare-text-text-generation-tab)
  - [Logs Tab](#logs-tab)
- [Common Workflows](#common-workflows)
- [Facebook Token Management](#facebook-token-management)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## Introduction

**SocialBoost Facebook AutoPoster v3** is an automated social media management system that helps you:

- **Automatically post** content to your Facebook page
- **Generate AI-powered captions** for your media assets
- **Schedule posts** for optimal engagement times
- **Manage your media library** with intelligent asset rotation
- **Monitor system health** and track posting history

The application features a user-friendly graphical interface with comprehensive automation capabilities, making it easy to maintain an active social media presence without manual intervention.

---

## System Requirements

### Operating System
- **Windows**: Windows 10 or later
- **macOS**: macOS 10.15 (Catalina) or later
- **Linux**: Ubuntu 20.04+ or compatible distributions

### Software Requirements
- **Python**: Version 3.11 or higher (3.13.7 tested)
- **Git**: For version control (optional but recommended)
- **pip**: Python package manager (included with Python 3.11+)

### Hardware Requirements
- **RAM**: Minimum 4GB, 8GB recommended
- **Disk Space**: Minimum 500MB free space
- **Internet**: Required for API calls (Facebook Graph API, OpenAI API)

### Account Requirements
- **Facebook Developer Account**: Required for API access
- **Facebook Page**: The page you want to post to
- **OpenAI Account**: Required for AI-powered content generation

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository (GitHub URL placeholder - replace with actual URL when available)
git clone <repository-url>
cd SocialBoost_FB_AutoPoster_v3
```

### Step 2: Create Virtual Environment

Create an isolated Python environment to prevent dependency conflicts:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

When the virtual environment is activated, you'll see `(venv)` at the beginning of your command prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install all dependencies including:
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests for API calls
- `openai` - OpenAI API integration
- `schedule` - Task scheduling
- `Pillow` - Image processing
- `psutil` - System monitoring
- And development tools (pytest, flake8, mypy, bandit)

### Step 4: Verify Installation

Run a quick test to verify everything is installed correctly:

```bash
python Tests/validation_runner.py --quick
```

This will run a quick validation check. All 6 checks should pass.

---

## Initial Configuration

### Creating the .env File

The application requires environment variables for API credentials. Create a `.env` file in the project root directory.

**Windows:**
```bash
# In project root directory
notepad .env
```

**macOS/Linux:**
```bash
nano .env
```

### Required Environment Variables

Add the following variables to your `.env` file:

```env
# Facebook API Configuration
FACEBOOK_PAGE_ID=your_page_id_here
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_PAGE_TOKEN=your_page_token_here

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# System Configuration
PYTHONIOENCODING=utf-8
LOG_LEVEL=INFO
```

**Important**: 
- Do NOT share your `.env` file with anyone
- Do NOT commit your `.env` file to Git (it's already in `.gitignore`)
- Keep your API keys secure

---

## Getting Your Facebook API Credentials

### Step 1: Create a Facebook Developer Account

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click "Get Started" or "My Apps"
3. Click "Create App"
4. Select "Business" as the app type
5. Enter app name and contact email
6. Complete the setup process

### Step 2: Get App ID and App Secret

1. In your app dashboard, go to **Settings > Basic**
2. Copy the **App ID**
3. Copy the **App Secret** (click "Show" to reveal it)
4. Add these to your `.env` file as `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET`

### Step 3: Add Facebook Login Product

1. In the app dashboard, click **"Add Product"**
2. Find **"Facebook Login"** and click **"Set Up"**
3. Under **"Settings"**, add your redirect URI: `https://localhost/`
4. Click **"Save Changes"**

### Step 4: Get Page ID

1. Go to your Facebook page
2. Click **"About"**
3. Scroll down to find **"Page ID"**
4. Copy this ID to your `.env` file as `FACEBOOK_PAGE_ID`

### Step 5: Get Short-Lived User Token

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from the dropdown
3. Click **"Generate Access Token"**
4. Select these permissions:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `pages_read_user_content`
5. Copy the generated token (this is a short-lived token, valid for ~1 hour)

### Step 6: Exchange for Long-Lived Page Token

After obtaining the short-lived user token and configuring your `.env` file with `FACEBOOK_PAGE_ID`, `FACEBOOK_APP_ID`, and `FACEBOOK_APP_SECRET`, run the token exchange script:

**Windows:**
```bash
python Scripts\exchange_user_to_page_token.py
```

**macOS/Linux:**
```bash
python Scripts/exchange_user_to_page_token.py
```

You'll be prompted to enter your short-lived user token. The script will:
1. Exchange it for a long-lived user token
2. Get a page access token
3. Verify the token is valid
4. Save it to your `.env` file as `FACEBOOK_PAGE_TOKEN`

The script provides clear instructions and confirms when the process completes successfully.

**Alternative: Non-Interactive Mode**

If you already have a user token, you can provide it directly:

```bash
python Scripts/exchange_user_to_page_token.py --user-token YOUR_SHORT_LIVED_TOKEN
```

---

## Getting Your OpenAI API Key

### Step 1: Create an OpenAI Account

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Click **"Sign Up"** and create an account
3. Complete the verification process

### Step 2: Get API Key

1. Go to [API Keys page](https://platform.openai.com/api-keys)
2. Click **"Create new secret key"**
3. Give it a name (e.g., "SocialBoost")
4. Copy the key immediately (you won't be able to see it again)
5. Add it to your `.env` file as `OPENAI_API_KEY`

### Step 3: Add Payment Method

1. Go to [Billing Settings](https://platform.openai.com/account/billing)
2. Click **"Add payment method"**
3. Add your payment details
4. Note: OpenAI charges per API call. Check current pricing at [OpenAI Pricing](https://openai.com/pricing)

### Model Selection

The application uses `gpt-4o-mini` by default (configured as `OPENAI_MODEL` in `.env`). You can change this to:

- `gpt-4o-mini` - Fast and economical (recommended)
- `gpt-4o` - More capable but more expensive
- `gpt-4-turbo` - Most capable but expensive

---

## Running the Application

### Starting the GUI

**Windows:**
```bash
python GUI\main_gui.py
```

**macOS/Linux:**
```bash
python GUI/main_gui.py
```

The GUI window will open with 5 tabs:
1. **Control/Status** - System monitoring and control
2. **Programare** - Schedule management
3. **Assets** - Media asset management
4. **Generare Text** - AI content generation
5. **Logs** - System logs

### Starting the Scheduler (Background Automation)

The scheduler can be started in two ways:

**Option 1: From GUI**
1. Open the GUI
2. Go to **Control/Status** tab
3. Click **"Start Scheduler"** in the Scheduler Control panel

**Option 2: Command Line**
```bash
python Automatizare_Completa/scheduler.py
```

The scheduler runs in the background and executes scheduled jobs from `Config/schedule.json`. To stop it, use **"Stop Scheduler"** in the GUI or press `Ctrl+C` in the terminal.

---

## Using the GUI Interface

### Control/Status Tab

The **Control/Status** tab provides system monitoring and quick actions.

#### Project Information Panel

Displays real-time project status:
- **Project Name**: "SocialBoost_FB_AutoPoster_v3"
- **Current Stage**: Current development phase
- **Last Commit**: Latest Git commit hash
- **Last Run**: Timestamp of last execution

#### Health Status

Displays system health information:
- **Status**: Healthy / Degraded / Warning / Critical
- **Score**: Numerical health score (0.00 to 1.00)

The system runs 6 health checks:
1. Python version compatibility
2. Git repository status
3. Required files exist
4. Dependencies installed
5. GitHub connectivity
6. Available disk space

#### Facebook Token Status

Shows the validity status of your Facebook page token:
- **VALID ✅** (green) - Token is valid and ready to use
- **INVALID/EXPIRED ❌** (red) - Token needs refreshing
- **NOT FOUND** (orange) - Token not configured

The status is automatically checked at startup. Use **"Refresh Facebook Token"** to update it.

#### Quick Actions

**Run Health Check**: Executes all 6 health checks and displays results.

**Create Backup**: Creates a complete backup of:
- Configuration files
- Asset tracking data
- Schedule data
- Selected assets

Backups are saved to the `Backups/` directory with timestamp.

**Start Scheduler**: Starts the automated task scheduler in the background.

**Stop Scheduler**: Stops the scheduler (only enabled when scheduler is running).

#### Test Actions

**Postează Text Test**: Posts a test message to your Facebook page.

**Generează Text Test**: Generates a test AI message.

#### Recent Logs

Displays the last 20 lines from `Logs/system.log` for quick reference.

### Programare (Scheduling) Tab

The **Programare** tab allows you to manage scheduled automated tasks.

#### Viewing Scheduled Jobs

The left panel displays all scheduled jobs in a table:

| Column | Description |
|--------|-------------|
| **#** | Job number |
| **Tip** | Job type (daily, weekly, interval, once) |
| **Ora/Interval** | Time or interval specification |
| **Task** | Script to execute |
| **Activat** | Enabled status (Da/Nu) |
| **Ultima Rulare** | Last execution timestamp |

#### Adding a New Job

1. Select job type from the dropdown:
   - **Daily**: Runs every day at a specific time
   - **Weekly**: Runs on a specific day of the week
   - **Interval**: Runs every N minutes
   - **Once**: Runs once at a specific date/time

2. Fill in the required fields based on job type:

   **Daily Job:**
   - **Ora (HH:MM)**: Time in 24-hour format (e.g., 09:00, 14:30)

   **Weekly Job:**
   - **Ziua**: Day of the week (Monday, Tuesday, etc.)
   - **Ora (HH:MM)**: Time in 24-hour format

   **Interval Job:**
   - **Interval (minute)**: Number of minutes between runs

   **Once Job:**
   - **Data și Ora (YYYY-MM-DD HH:MM)**: Specific date and time

3. Enter **Task**: The Python script filename (e.g., `auto_post.py`, `auto_generate.py`)

4. Check **Activat** if you want the job enabled immediately

5. Click **"Add Job"**

#### Deleting a Job

1. Select a job from the list
2. Click **"Delete Selected"**
3. Confirm deletion in the dialog

#### Refreshing the List

Click **"Refresh List"** to reload jobs from `Config/schedule.json`.

#### Example Schedules

**Daily Morning Post:**
```
Tip: daily
Ora: 09:00
Task: auto_post.py
Activat: Yes
```

**Weekly Monday Post:**
```
Tip: weekly
Ziua: monday
Ora: 10:00
Task: auto_post.py
Activat: Yes
```

**Content Generation Every 3 Hours:**
```
Tip: interval
Interval: 180
Task: auto_generate.py
Activat: Yes
```

### Assets Tab

The **Assets** tab manages your media library (images and videos).

#### Viewing Available Assets

The left panel lists all media files from:
- `Assets/Images/` - Image files (PNG, JPG, JPEG, GIF, BMP, WebP)
- `Assets/Videos/` - Video files (MP4, MOV, AVI, MKV, WebM)

Each file shows:
- **Nume Fișier**: File name
- **Tip**: File type (Imagine / Video)

#### Image Preview

When you select a single image, a preview thumbnail appears in the right panel. The preview:
- Maintains aspect ratio
- Scales to fit (max 300x300 pixels)
- Shows errors for corrupted images

**Note**: Video previews are not supported. You'll see "Preview disponibil doar pentru imagini" when selecting videos.

#### Selecting Assets

1. **Single Selection**: Click a file to select it and see the preview
2. **Multi-Selection**: 
   - **Windows/Linux**: Hold `Ctrl` and click multiple files
   - **macOS**: Hold `Command` and click multiple files
   - Select multiple files by dragging

3. **Saving Selection**:
   - Click **"Save Selection"**
   - Assets are saved to `selected_assets.json` in the project root
   - A confirmation dialog shows the count of images and videos saved

4. **Posting Selected Assets**:
   - Click **"Post Selected Assets"**
   - Confirm the posting in the dialog
   - Assets will be posted to Facebook with AI-generated captions

#### Refreshing the List

Click **"Refresh List"** to reload assets from the folders. Use this after:
- Adding new files to `Assets/Images/` or `Assets/Videos/`
- Deleting files from the folders
- When files don't appear in the list

#### Asset Selection Workflow

1. Add your media files to `Assets/Images/` or `Assets/Videos/` folders
2. Open the **Assets** tab
3. Click **"Refresh List"** to see your files
4. Select the files you want to post (use Ctrl/Cmd for multiple)
5. Click **"Save Selection"** to save your selection
6. (Optional) Go to **Generare Text** tab to generate captions
7. Click **"Post Selected Assets"** to post with AI-generated captions

### Generare Text (Text Generation) Tab

The **Generare Text** tab uses OpenAI to generate AI-powered content for your selected assets.

#### Entering a Prompt

The prompt tells the AI what kind of content to generate:

**Examples:**
- "Generează un post Facebook despre importanța tehnologiei în viața de zi cu zi"
- "Creează o descriere captivantă pentru această imagine"
- "Generează un mesaj de plată pentru acest videoclip"

#### Asset Information

Below the prompt input, you'll see:
- Number of images selected for caption generation
- Number of videos selected for post text generation

This helps you understand what will be generated before clicking the button.

#### Generating Content

1. Enter your prompt in the text area
2. Review the asset information (X images, Y videos)
3. Click **"Generează Text"**

The system will:
- Process each selected asset individually
- Generate appropriate content based on file type:
  - **Images**: Detailed captions using OpenAI Vision API
  - **Videos**: Post text based on file name and context
- Display the results in the output area
- Save generated content for later use

#### Viewing Results

Generated content appears in the **"Rezultat Generare"** area below the input. The output shows:
- Generated text for each asset
- Success/failure status
- Any errors encountered

#### Workflow with Assets

**Complete Workflow:**
1. Go to **Assets** tab
2. Select images/videos you want to post
3. Click **"Save Selection"**
4. Go to **Generare Text** tab
5. Enter your prompt (or leave default)
6. Click **"Generează Text"**
7. Review the generated content
8. Go back to **Assets** tab
9. Click **"Post Selected Assets"** to post with AI-generated content

**Note**: The system automatically uses the most recent generated content when posting.

### Logs Tab

The **Logs** tab provides access to system logs for monitoring and debugging.

#### Viewing Logs

The log viewer displays content from `Logs/system.log`:
- **Auto-refresh**: Logs update automatically every 5 seconds
- **Manual Refresh**: Click **"Refresh Logs"** for immediate update
- **Large Files**: If the log file is very large (1000+ lines), only the last 1000 lines are shown

#### Log Content

Logs include:
- Application startup and shutdown
- API call details (Facebook, OpenAI)
- Success/failure messages
- Error messages and stack traces
- Scheduled job executions
- GUI actions and user interactions

#### Using Logs for Troubleshooting

**Common Log Patterns:**

**Successful Post:**
```
2025-10-26 10:30:15 - auto_post - INFO - Posting text message...
2025-10-26 10:30:16 - auto_post - INFO - ✓ Post successful! Post ID: page_id_post_id
```

**API Error:**
```
2025-10-26 10:30:15 - auto_post - ERROR - API response status: 401
2025-10-26 10:30:15 - auto_post - ERROR - Invalid token
```

**Network Error:**
```
2025-10-26 10:30:15 - auto_post - ERROR - Connection error: Connection refused
```

Check the **Logs** tab regularly to monitor system health and identify issues.

---

## Common Workflows

### Workflow 1: Immediate Post with AI-Generated Caption

**Goal**: Post a single image or video immediately with AI-generated caption.

**Steps**:
1. Add your media file to `Assets/Images/` or `Assets/Videos/`
2. Open GUI: `python GUI/main_gui.py`
3. Go to **Assets** tab
4. Click **"Refresh List"**
5. Select your image/video
6. Click **"Save Selection"**
7. Go to **Generare Text** tab
8. Enter a prompt (e.g., "Generează un post despre...")
9. Click **"Generează Text"**
10. Wait for generation to complete
11. Go back to **Assets** tab
12. Click **"Post Selected Assets"**
13. Confirm posting in the dialog

**Time**: 2-3 minutes

### Workflow 2: Schedule Daily Posts with Auto-Rotation

**Goal**: Schedule daily automated posts that rotate through your media library.

**Steps**:
1. Add multiple media files to `Assets/Images/` and/or `Assets/Videos/`
2. Open GUI
3. Go to **Programare** tab
4. Add a daily job:
   - Tip: `daily`
   - Ora: `09:00` (or your preferred time)
   - Task: `auto_post.py`
   - Activat: Yes
   - Click **"Add Job"**
5. Go to **Control/Status** tab
6. Click **"Start Scheduler"**
7. The system will automatically:
   - Select unposted assets first
   - Rotate to oldest posted assets when all are posted
   - Generate AI captions for each post
   - Post to Facebook at scheduled time

**Advanced**: You can add multiple jobs for different times:
- 09:00 - Morning post
- 14:00 - Afternoon post
- 18:00 - Evening post

### Workflow 3: Batch Generation and Manual Posting

**Goal**: Generate captions for multiple assets, then post them manually later.

**Steps**:
1. Add multiple assets to folders
2. Open GUI
3. Go to **Assets** tab, select multiple files
4. Click **"Save Selection"**
5. Go to **Generare Text** tab
6. Enter a batch prompt (e.g., "Generează post-uri despre...")
7. Click **"Generează Text"**
8. Review all generated content in output area
9. Later, go to **Assets** tab and click **"Post Selected Assets"**

This workflow separates generation from posting, giving you control over timing.

---

## Facebook Token Management

### Understanding Tokens

The application uses Facebook Page Access Tokens for posting:

1. **Short-Lived User Token** (1 hour validity)
   - Obtained from Graph API Explorer
   - Used to exchange for long-lived token

2. **Long-Lived User Token** (60 days validity)
   - Exchanged from short-lived token
   - Can be extended

3. **Long-Lived Page Token** (60 days validity, can be indefinite)
   - Obtained from long-lived user token
   - Used for posting to Facebook page
   - Stored in `.env` as `FACEBOOK_PAGE_TOKEN`

### Checking Token Status

**From GUI:**
1. Open GUI
2. Go to **Control/Status** tab
3. Check **"Facebook Token Status"** panel:
   - **VALID ✅** - Token is working
   - **INVALID/EXPIRED ❌** - Need to refresh
   - **NOT FOUND** - Need to configure

**From Command Line:**
```bash
python Scripts/exchange_user_to_page_token.py --check-only
```

Exit codes:
- `0` - Token is valid
- `1` - Token is invalid/expired
- `2` - Token not found

### Refreshing Your Token

**From GUI (Recommended):**
1. Go to **Control/Status** tab
2. Click **"Refresh Facebook Token"**
3. A new terminal window opens
4. Follow the instructions:
   - If you have a user token, paste it when prompted
   - If not, obtain one from [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
5. Token is automatically saved to `.env`

**From Command Line:**
```bash
# Interactive mode
python Scripts/exchange_user_to_page_token.py

# Non-interactive mode (if you have user token)
python Scripts/exchange_user_to_page_token.py --user-token YOUR_USER_TOKEN
```

### Token Expiration

Page tokens should last 60 days, but may expire earlier if:
- The user password is changed
- The user revokes permissions
- Facebook security policies require refresh

**Best Practice**: Check token status weekly using the GUI or `--check-only` command.

### Token Security

**Important**: 
- Never share your `FACEBOOK_PAGE_TOKEN`
- Never commit it to version control (it's in `.gitignore`)
- Keep your `.env` file secure
- Don't post your token online or in support forums

---

## Troubleshooting

### Problem: GUI Won't Start

**Symptoms**: 
- Error message when running `python GUI/main_gui.py`
- Window doesn't open

**Solutions**:
1. **Check Python version**: Run `python --version` (should be 3.11+)
2. **Check virtual environment**: Make sure it's activated (`venv` in prompt)
3. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
4. **Check logs**: Look in `Logs/system.log` for error messages

**Error: "Module not found"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Facebook Posting Fails

**Symptoms**:
- Post fails with "Invalid token" or "Permission denied"
- Token status shows INVALID

**Solutions**:
1. **Refresh token**: Use **"Refresh Facebook Token"** button in GUI
2. **Check permissions**: Verify these permissions in Graph API Explorer:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
3. **Verify page ID**: Check `FACEBOOK_PAGE_ID` in `.env` matches your page
4. **Check token manually**: Run `python Scripts/exchange_user_to_page_token.py --check-only`

**Error: "OAuthException"**
- Solution: Token expired. Run token refresh script.

### Problem: OpenAI Generation Fails

**Symptoms**:
- Error message when generating text
- "API key not found" or "Rate limit exceeded"

**Solutions**:
1. **Check API key**: Verify `OPENAI_API_KEY` in `.env` is correct
2. **Check billing**: Ensure your OpenAI account has active payment method
3. **Check quota**: Verify you haven't exceeded your OpenAI quota
4. **Verify network**: Check internet connection
5. **Wait and retry**: If rate-limited, wait a few minutes and try again

**Error: "Rate limit exceeded"**
- Solution: This is normal with free tier. Wait 1-2 minutes between requests.

### Problem: Scheduler Not Running Jobs

**Symptoms**:
- Scheduler is running but jobs don't execute
- Jobs are enabled but never run

**Solutions**:
1. **Check job configuration**: Verify jobs in `Config/schedule.json` are correct
2. **Check "enabled" field**: Ensure `"enabled": true` in job configuration
3. **Check time format**: Verify time is in correct format (HH:MM for daily/weekly)
4. **Verify task file exists**: Task file (e.g., `auto_post.py`) must exist in `Automatizare_Completa/`
5. **Check logs**: Look in `Logs/scheduler.log` for error messages

**Error: "Task file not found"**
```bash
# Solution: Ensure task file exists
ls Automatizare_Completa/auto_post.py  # Should exist
```

### Problem: Assets Not Showing

**Symptoms**:
- Files in folders but not appearing in GUI
- "Refresh List" doesn't update

**Solutions**:
1. **Check file locations**: Files must be in `Assets/Images/` or `Assets/Videos/`
2. **Check file extensions**: Supported formats:
   - Images: PNG, JPG, JPEG, GIF, BMP, WebP
   - Videos: MP4, MOV, AVI, MKV, WebM
3. **Refresh manually**: Click **"Refresh List"** button
4. **Check file permissions**: Ensure files are readable (not locked)
5. **Verify file names**: Avoid special characters in file names

**Error: "No files found"**
```bash
# Solution: Check file structure
Assets/
  Images/
    file1.jpg  # Files should be here
  Videos/
    file1.mp4
```

### Problem: Encoding Errors

**Symptoms**:
- Error messages about encoding (UTF-8)
- Special characters not displaying correctly

**Solutions**:
1. **Check `.env`**: Ensure `PYTHONIOENCODING=utf-8` is set
2. **Reinstall**: Run `pip install --upgrade pip` and reinstall packages
3. **Check file content**: Ensure asset names don't have problematic characters

### Problem: GUI is Slow or Freezing

**Symptoms**:
- GUI becomes unresponsive
- Buttons don't respond
- Window freezes

**Solutions**:
1. **Close other applications**: Free up system resources
2. **Check disk space**: Ensure enough disk space (500MB+)
3. **Restart GUI**: Close and reopen the application
4. **Check logs**: Look for errors in `Logs/system.log`
5. **Update dependencies**: Run `pip install --upgrade -r requirements.txt`

### Getting More Help

**Check Logs**:
- Main logs: `Logs/system.log`
- Scheduler logs: `Logs/scheduler.log`
- Health check: `Logs/health_check.json`

**Run Health Check**:
- From GUI: Go to **Control/Status** tab, click **"Run Health Check"**
- From command line: `python Automatizare_Completa/health_check.py`

**Validation**:
- Run: `python Tests/validation_runner.py`
- Check all 6 validation checks pass

---

## FAQ

### Can I post to multiple Facebook pages?

**Currently**: No, the application supports posting to one Facebook page at a time. You can create separate installations with different `.env` files for multiple pages.

**Future**: Multi-page support may be added in future versions.

### How do I add new assets?

Simply copy your image/video files to:
- `Assets/Images/` for images (PNG, JPG, JPEG, GIF, BMP, WebP)
- `Assets/Videos/` for videos (MP4, MOV, AVI, MKV, WebM)

Then click **"Refresh List"** in the Assets tab.

### How much does OpenAI API cost?

Check current pricing at [OpenAI Pricing](https://openai.com/pricing). With the default `gpt-4o-mini` model, costs are typically very low (under $0.01 per post).

### Can I use my own captions instead of AI-generated ones?

**Currently**: AI generation is integrated. Manual captions would require editing the generated content before posting.

**Workaround**: You can generate captions, copy them to a text editor, modify them, then manually post via Facebook's interface.

### How often can I post?

**Facebook Limits**: 
- Standard pages: Up to 25 posts per 24 hours
- Verified pages: Higher limits apply

**Best Practice**: Don't exceed 3-5 posts per day to avoid appearing spammy.

### What if my token expires while the scheduler is running?

The scheduler will fail jobs with token errors. Logs will show the error. To fix:
1. Stop the scheduler from GUI
2. Click **"Refresh Facebook Token"** in Control/Status tab
3. Restart scheduler

### Can I schedule posts with different prompts for different assets?

**Currently**: No. The scheduling system uses the default asset rotation. For custom prompts per asset, generate them manually in the GUI first.

**Workaround**: Generate different content for different asset selections, then manually post them.

### How do I backup my configuration?

**Automatic**: Click **"Create Backup"** in the Control/Status tab. Backups are saved to `Backups/` with timestamps.

**Manual**: Copy these files:
- `.env` (keep secure!)
- `Config/schedule.json`
- `Config/asset_tracking.json`
- `selected_assets.json`

### Can I run the scheduler on a server?

**Yes!** The scheduler runs independently and can run on any computer or server that:
- Has Python 3.11+ installed
- Has your `.env` file configured
- Can access the internet (for API calls)
- Can access `Assets/` folders

### How do I stop all automated posting?

**Option 1**: Stop the scheduler
- From GUI: **Control/Status** tab → **"Stop Scheduler"**
- From command line: Press `Ctrl+C` in the terminal

**Option 2**: Disable all jobs
- Edit `Config/schedule.json`
- Set `"enabled": false` for all jobs
- The scheduler will not execute disabled jobs

### Do I need to keep the GUI open for the scheduler to work?

**No!** The scheduler runs independently as a background process. You can close the GUI and the scheduler will continue running. Just remember to stop it before shutting down your computer.

---

## Support and Updates

### Checking Version

Run the health check to see your current system status:
```bash
python Automatizare_Completa/health_check.py
```

### Getting Updates

When updates are available:
1. Pull latest changes: `git pull`
2. Reinstall dependencies: `pip install -r requirements.txt --upgrade`
3. Restart the application

### Reporting Issues

When reporting issues, please include:
1. Python version: `python --version`
2. Operating system and version
3. Error messages from `Logs/system.log`
4. Steps to reproduce the issue
5. Health check results

---

## Appendix: File Structure

```
SocialBoost_FB_AutoPoster_v3/
├── Assets/                    # Your media files
│   ├── Images/               # Image files (PNG, JPG, etc.)
│   └── Videos/               # Video files (MP4, etc.)
├── Automatizare_Completa/    # Automation scripts
│   ├── auto_post.py          # Facebook posting
│   ├── auto_generate.py     # AI content generation
│   ├── scheduler.py          # Task scheduler
│   └── health_check.py       # System health monitoring
├── Config/                    # Configuration files
│   ├── schedule.json         # Scheduled jobs
│   └── asset_tracking.json   # Asset posting history
├── Docs/                     # Documentation
│   ├── README_COMPLETE_SYSTEM.md  # This file
│   └── CHANGELOG.md          # Version history
├── GUI/                      # GUI application
│   └── main_gui.py           # Main GUI window
├── Logs/                     # System logs
│   ├── system.log           # Main application logs
│   ├── scheduler.log        # Scheduler logs
│   └── health_check.json    # Health check results
├── Scripts/                  # Utility scripts
│   ├── exchange_user_to_page_token.py  # Token management
│   ├── context_builder.py   # Context generation
│   └── prompt_generator.py  # Prompt templates
├── Tests/                    # Test suite
│   ├── test_auto_post.py    # Posting tests
│   ├── test_auto_generate.py  # Generation tests
│   ├── validation_runner.py # Test runner
│   └── test_gui.py          # GUI tests
├── .env                      # Environment variables (create this!)
├── requirements.txt          # Python dependencies
└── selected_assets.json      # Selected assets for posting
```

---

**Last Updated**: October 26, 2025  
**Version**: 3.0  
**Status**: Phase 5 - Final Testing & Validation

For questions or support, please refer to the project documentation or check the logs for detailed error information.

