# Validation Task - {project_name}

**Generated**: {timestamp}  
**Stage**: {current_stage}  
**Root Path**: {project_root}

## 🎯 Validation Scope
{validation_scope}

## 📋 Current Context
{context}

## 🧪 Tests to Run
{tests_to_run}

## ✅ Validation Checklist

### Code Quality
- [ ] **Syntax Check** - All Python files have valid syntax
- [ ] **Import Check** - All imports resolve correctly
- [ ] **No Dead Code** - Remove unused imports/variables/functions

### Testing
- [ ] **Unit Tests** - All unit tests pass
- [ ] **Integration Tests** - System integration tests pass
- [ ] **Coverage** - Code coverage meets minimum threshold (80%)
- [ ] **Edge Cases** - Boundary conditions tested

### Code Standards
- [ ] **Linting (flake8)** - No linting errors
  ```bash
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  ```
- [ ] **Type Checking (mypy)** - No type errors
  ```bash
  mypy . --ignore-missing-imports
  ```
- [ ] **Security (bandit)** - No security vulnerabilities
  ```bash
  bandit -r . -f json -o bandit_report.json
  ```

### Documentation
- [ ] **Docstrings** - All public functions/classes documented
- [ ] **README.md** - Up to date with current features
- [ ] **CHANGELOG.md** - Recent changes documented
- [ ] **API Docs** - API documentation current (if applicable)

### Configuration
- [ ] **.env.example** - All required variables documented
- [ ] **requirements.txt** - All dependencies listed with versions
- [ ] **Config Files** - Valid JSON/YAML syntax

### Project Structure
- [ ] **File Organization** - Files in appropriate directories
- [ ] **Naming Convention** - Consistent naming throughout
- [ ] **No Sensitive Data** - No hardcoded secrets or credentials

### Performance
- [ ] **Response Times** - Operations complete in reasonable time
- [ ] **Memory Usage** - No memory leaks detected
- [ ] **Error Handling** - Graceful degradation on errors

## 📊 Expected Results
{expected_results}

## 📝 Validation Commands

### Quick Validation
```bash
python Scripts/context_validator.py
```

### Full Test Suite
```bash
python -m pytest Tests/ -v --cov=. --cov-report=html
```

### Individual Checks
```bash
# Syntax check
python -m py_compile **/*.py

# Linting
flake8 . --config=.flake8

# Type checking
mypy . --config-file=mypy.ini

# Security scan
bandit -r . --severity-level medium
```

## 📋 Report Format
{report_format}

### Report Sections
1. **Executive Summary** - Pass/Fail status with key metrics
2. **Detailed Results** - Component-by-component breakdown
3. **Issues Found** - List of all issues with severity
4. **Recommendations** - Suggested fixes and improvements
5. **Metrics** - Coverage, performance, quality scores

## 🚨 Critical Issues (Must Fix)
- Syntax errors in Python files
- Failing core functionality tests
- Security vulnerabilities (High/Critical)
- Missing critical dependencies
- Broken imports or modules

## ⚠️ Warnings (Should Fix)
- Low test coverage areas
- Minor linting issues
- Missing documentation
- Deprecated function usage
- Performance bottlenecks

## 💡 Improvements (Nice to Have)
- Code refactoring opportunities
- Additional test cases
- Enhanced error messages
- Performance optimizations
- Documentation enhancements

## 🔄 Post-Validation Actions
- [ ] Fix all critical issues
- [ ] Address high-priority warnings
- [ ] Update documentation
- [ ] Re-run validation after fixes
- [ ] Generate final validation report
- [ ] Copy report to Update_AI/
- [ ] Update PROJECT_CONTEXT.json with validation status

---
**Remember**: A thorough validation ensures system reliability and maintainability.
