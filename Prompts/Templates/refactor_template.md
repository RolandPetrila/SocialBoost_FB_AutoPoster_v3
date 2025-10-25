# Refactoring Task - {project_name}

**Generated**: {timestamp}  
**Stage**: {current_stage}  
**Root Path**: {project_root}

## 🎯 Refactoring Goal
{refactoring_goal}

## 📋 Current Context
{context}

## 🔍 Current Implementation Issues
{current_issues}

## 💡 Proposed Changes
{proposed_changes}

## 📐 Refactoring Guidelines

### Core Principles
1. **Maintain Backward Compatibility** - Don't break existing functionality
2. **Improve Readability** - Make code self-documenting
3. **Reduce Complexity** - Simplify logic where possible
4. **Follow DRY** - Don't Repeat Yourself
5. **SOLID Principles** - Single responsibility, Open/closed, etc.

### Refactoring Patterns
- **Extract Method** - Break large functions into smaller ones
- **Extract Class** - Move related functionality to separate classes
- **Rename** - Use clear, descriptive names
- **Replace Magic Numbers** - Use named constants
- **Simplify Conditionals** - Reduce nested if statements
- **Remove Dead Code** - Delete unused code

### Code Quality Goals
- Functions under 50 lines
- Classes under 200 lines
- Cyclomatic complexity under 10
- Clear separation of concerns
- Proper abstraction levels

## 📁 Files to Refactor
{files_to_refactor}

## 🧪 Testing Strategy
{testing_strategy}

### Test Coverage Requirements
1. **Preserve Tests** - Keep all existing tests passing
2. **Add Tests** - Write tests for refactored code
3. **Performance Tests** - Ensure no performance regression
4. **Integration Tests** - Verify system still works end-to-end

## 📊 Success Metrics
{success_metrics}

### Measurable Improvements
- [ ] Code complexity reduced by X%
- [ ] Test coverage increased to Y%
- [ ] Performance maintained or improved
- [ ] Linting warnings reduced
- [ ] Documentation coverage improved

## 🔄 Refactoring Process

### Step-by-Step Approach
1. **Create Backup** - Run `python backup_manager.py`
2. **Identify Scope** - List all affected files and functions
3. **Write Tests First** - Ensure current behavior is tested
4. **Refactor Incrementally** - Small, testable changes
5. **Run Tests Often** - Verify each change
6. **Review Changes** - Check diff for unintended modifications
7. **Update Documentation** - Reflect new structure

### Safety Checks
- [ ] All tests pass before starting
- [ ] Create feature branch for changes
- [ ] Regular commits with clear messages
- [ ] Code review before merging

## 🎨 Code Style Guidelines

### Naming Conventions
- **Classes**: PascalCase (e.g., `UserManager`)
- **Functions**: snake_case (e.g., `get_user_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRIES`)
- **Private**: Leading underscore (e.g., `_internal_method`)

### Structure Guidelines
```python
# Good structure example
class WellStructuredClass:
    """Clear class documentation."""
    
    def __init__(self):
        """Initialize with clear purpose."""
        self._setup_internals()
    
    def public_method(self) -> str:
        """Public API with type hints."""
        return self._process_data()
    
    def _process_data(self) -> str:
        """Private helper method."""
        pass
```

## 🚫 Common Pitfalls to Avoid
- Over-engineering simple solutions
- Breaking existing APIs
- Ignoring edge cases
- Forgetting to update tests
- Not updating documentation
- Creating circular dependencies
- Premature optimization

## ✅ Refactoring Checklist
- [ ] Current functionality preserved
- [ ] All tests pass
- [ ] Code is more readable
- [ ] Complexity reduced
- [ ] Performance maintained/improved
- [ ] Documentation updated
- [ ] No new linting warnings
- [ ] Peer review completed

## 📝 Documentation Updates
- [ ] Update function/class docstrings
- [ ] Update README if API changed
- [ ] Update CHANGELOG.md
- [ ] Update architectural docs if structure changed
- [ ] Add migration guide if breaking changes

## 🔄 Post-Refactoring Actions
- [ ] Run full test suite
- [ ] Run performance benchmarks
- [ ] Update documentation
- [ ] Create pull request with detailed description
- [ ] Get code review
- [ ] Merge and tag version
- [ ] Copy refactoring report to Update_AI/

---
**Remember**: Refactoring is about improving code quality without changing functionality.
