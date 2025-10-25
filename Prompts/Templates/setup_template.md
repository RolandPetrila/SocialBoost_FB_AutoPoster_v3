# Setup Task - {project_name}

**Generated**: {timestamp}  
**Stage**: {current_stage}  
**Root Path**: {project_root}

## 🎯 Setup Objective
{setup_objective}

## 💻 Environment Requirements
{environment_requirements}

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **RAM**: Minimum 4GB, Recommended 8GB
- **Disk Space**: Minimum 500MB free
- **Internet**: Required for API calls and package installation

### Required Software
- Python 3.11+
- Git
- pip (Python package manager)
- Virtual environment tool (venv/virtualenv)

## 📦 Installation Steps
{installation_steps}

### 1. Clone Repository
```bash
git clone <repository-url>
cd SocialBoost_FB_AutoPoster_v3
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Windows: notepad .env
# macOS/Linux: nano .env
```

## ⚙️ Configuration
{configuration}

### Required API Keys
1. **Facebook API**
   - App ID: Get from https://developers.facebook.com
   - App Secret: From Facebook App Dashboard
   - Page Token: Generate using exchange script

2. **OpenAI API**
   - API Key: Get from https://platform.openai.com/api-keys

### Configuration Files
- `.env` - Environment variables and secrets
- `Config/config_keys.json` - Additional configuration
- `PROJECT_CONTEXT.json` - Project metadata

## ✅ Verification Steps
{verification_steps}

### 1. Verify Python Installation
```bash
python --version
# Should show Python 3.11.x or higher
```

### 2. Verify Dependencies
```bash
pip list
# Check all required packages are installed
```

### 3. Verify Project Structure
```bash
python Scripts/context_validator.py
# Should show all checks passed
```

### 4. Test Core Functionality
```bash
# Test orchestrator
python orchestrator.py health

# Test backup system
python backup_manager.py list

# Test context builder
python Scripts/context_builder.py --type general
```

### 5. Run Tests
```bash
# If tests exist
python -m pytest Tests/ -v
```

## 🔧 Troubleshooting
{troubleshooting}

### Common Issues and Solutions

#### Python Version Issues
**Problem**: Python version is too old
**Solution**: 
```bash
# Windows - Install via Microsoft Store or python.org
# macOS - Use Homebrew: brew install python@3.11
# Linux - Use package manager: sudo apt install python3.11
```

#### Permission Errors
**Problem**: Permission denied when installing packages
**Solution**: 
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use sudo (Linux/macOS) - not recommended
sudo pip install -r requirements.txt
```

#### Import Errors
**Problem**: Module not found errors
**Solution**: 
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### API Key Issues
**Problem**: Invalid API key errors
**Solution**: 
- Verify keys are correctly copied to .env
- Check for extra spaces or quotes
- Ensure keys are active and not expired

#### Network Issues
**Problem**: Connection errors during setup
**Solution**: 
- Check internet connection
- Verify firewall/proxy settings
- Try using different pip index: `pip install --index-url https://pypi.org/simple/`

## 🚀 Quick Start Guide

### First Run
1. Activate virtual environment
2. Set up .env file with credentials
3. Run health check: `python orchestrator.py health`
4. Create initial backup: `python backup_manager.py create`
5. Start GUI: `python GUI/main_gui.py` (if available)

### Daily Usage
```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run main application
python orchestrator.py full

# Or use GUI
python GUI/main_gui.py
```

## 📋 Setup Checklist
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] API keys added
- [ ] Health check passed
- [ ] Initial backup created
- [ ] Test run successful

## 🔒 Security Best Practices
1. **Never commit .env file** - Keep secrets out of version control
2. **Use strong API keys** - Rotate keys regularly
3. **Limit permissions** - Use minimum required scopes
4. **Secure storage** - Encrypt sensitive data
5. **Regular updates** - Keep dependencies updated

## 📚 Additional Resources
- [Project Documentation](Docs/README.md)
- [API Documentation](Docs/API.md)
- [Troubleshooting Guide](Docs/TROUBLESHOOTING.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## ✔️ Success Criteria
{success_criteria}

## 🔄 Post-Setup Actions
- [ ] Verify all components working
- [ ] Create initial project backup
- [ ] Generate context documentation
- [ ] Run validation suite
- [ ] Update PROJECT_CONTEXT.json
- [ ] Copy setup log to Update_AI/
- [ ] Ready for development/usage

---
**Remember**: Proper setup ensures smooth operation. Take time to verify each step.
